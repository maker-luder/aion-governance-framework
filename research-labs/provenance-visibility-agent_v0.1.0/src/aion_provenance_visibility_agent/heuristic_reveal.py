from __future__ import annotations

import importlib
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from math import sqrt
from pathlib import Path
from typing import Any

RGBPixel = tuple[int, int, int]

DEFAULT_PERIODS: tuple[int, ...] = (4, 8, 16, 32, 64, 128)
PERIODICITY_CUE_THRESHOLD = 0.35


@dataclass(frozen=True, slots=True)
class RevealLayer:
    name: str
    width: int
    height: int
    pixels: tuple[int, ...]
    explanation_zh_tw: str


@dataclass(frozen=True, slots=True)
class PeriodicityCue:
    period: int
    score: float


@dataclass(frozen=True, slots=True)
class HeuristicRevealReport:
    width: int
    height: int
    method: str
    candidate_period: int | None
    periodicity_cue: float
    periodicity_scan: tuple[PeriodicityCue, ...]
    layers: tuple[RevealLayer, ...]
    visible_label_zh_tw: str
    watermark_verdict: str = "NOT_ESTABLISHED"
    heuristic_score_is_probability: bool = False
    local_only: bool = True
    network_required: bool = False
    removal_or_evasion: str = "OUT_OF_SCOPE"

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _validate_rgb_input(
    width: int,
    height: int,
    pixels: Sequence[RGBPixel],
) -> None:
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")
    if len(pixels) != width * height:
        raise ValueError("pixel count must equal width * height")
    for pixel in pixels:
        if len(pixel) != 3:
            raise ValueError("RGB pixels must contain exactly three channels")
        if any(channel < 0 or channel > 255 for channel in pixel):
            raise ValueError("RGB channels must be in the inclusive range 0..255")


def _luma(pixel: RGBPixel) -> int:
    red, green, blue = pixel
    return (77 * red + 150 * green + 29 * blue) >> 8


def _signed_local_residual(
    width: int,
    height: int,
    pixels: Sequence[RGBPixel],
) -> tuple[int, ...]:
    luma = tuple(_luma(pixel) for pixel in pixels)
    residual = [0] * (width * height)
    if width < 3 or height < 3:
        return tuple(residual)

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            index = y * width + x
            neighbour_sum = 0
            for yy in (y - 1, y, y + 1):
                row = yy * width
                for xx in (x - 1, x, x + 1):
                    if xx == x and yy == y:
                        continue
                    neighbour_sum += luma[row + xx]
            residual[index] = 8 * luma[index] - neighbour_sum
    return tuple(residual)


def _robust_abs_scale(values: Sequence[int]) -> int:
    magnitudes = sorted(abs(value) for value in values if value)
    if not magnitudes:
        return 1
    index = int(round(0.99 * (len(magnitudes) - 1)))
    return max(1, magnitudes[index])


def _normalize_signed(values: Sequence[int]) -> tuple[int, ...]:
    scale = _robust_abs_scale(values)
    output: list[int] = []
    for value in values:
        clipped = max(-scale, min(scale, value))
        normalized = int(round(128 + (127 * clipped / scale)))
        output.append(max(0, min(255, normalized)))
    return tuple(output)


def _lsb_map(pixels: Sequence[RGBPixel]) -> tuple[int, ...]:
    return tuple(
        ((red & 1) + (green & 1) + (blue & 1)) * 85
        for red, green, blue in pixels
    )


def _correlation_shift(
    values: Sequence[int],
    width: int,
    height: int,
    dx: int,
    dy: int,
) -> float:
    overlap_width = width - dx
    overlap_height = height - dy
    if overlap_width <= 1 or overlap_height <= 1:
        return 0.0

    count = 0
    sum_x = 0.0
    sum_y = 0.0
    sum_xx = 0.0
    sum_yy = 0.0
    sum_xy = 0.0

    for y in range(overlap_height):
        row_a = y * width
        row_b = (y + dy) * width
        for x in range(overlap_width):
            value_x = float(values[row_a + x])
            value_y = float(values[row_b + x + dx])
            count += 1
            sum_x += value_x
            sum_y += value_y
            sum_xx += value_x * value_x
            sum_yy += value_y * value_y
            sum_xy += value_x * value_y

    numerator = count * sum_xy - sum_x * sum_y
    denominator_x = count * sum_xx - sum_x * sum_x
    denominator_y = count * sum_yy - sum_y * sum_y
    if denominator_x <= 0.0 or denominator_y <= 0.0:
        return 0.0
    return numerator / sqrt(denominator_x * denominator_y)


def _periodicity_score(
    residual: Sequence[int],
    width: int,
    height: int,
    period: int,
) -> float:
    directional: list[float] = []
    if period < width:
        directional.append(
            max(0.0, _correlation_shift(residual, width, height, period, 0))
        )
    if period < height:
        directional.append(
            max(0.0, _correlation_shift(residual, width, height, 0, period))
        )
    if not directional:
        return 0.0
    return sum(directional) / len(directional)


def _scan_periodicity(
    residual: Sequence[int],
    width: int,
    height: int,
    periods: Sequence[int],
) -> tuple[PeriodicityCue, ...]:
    cues: list[PeriodicityCue] = []
    for period in periods:
        if period <= 1:
            raise ValueError("period candidates must be greater than 1")
        if period >= width and period >= height:
            continue
        score = _periodicity_score(residual, width, height, period)
        cues.append(PeriodicityCue(period=period, score=score))
    return tuple(cues)


def _choose_period(cues: Sequence[PeriodicityCue]) -> tuple[int | None, float]:
    if not cues:
        return None, 0.0
    best_score = max(cue.score for cue in cues)
    if best_score < PERIODICITY_CUE_THRESHOLD:
        return None, best_score

    near_best = tuple(
        cue
        for cue in cues
        if cue.score >= best_score - 0.05
        and cue.score >= PERIODICITY_CUE_THRESHOLD
    )
    chosen = min(near_best, key=lambda cue: cue.period)
    return chosen.period, chosen.score


def _fold_periodic_template(
    residual: Sequence[int],
    width: int,
    height: int,
    period: int,
) -> tuple[int, ...]:
    sums = [0] * (period * period)
    counts = [0] * (period * period)

    for y in range(height):
        for x in range(width):
            template_index = (y % period) * period + (x % period)
            sums[template_index] += residual[y * width + x]
            counts[template_index] += 1

    template = tuple(
        int(round(total / count)) if count else 0
        for total, count in zip(sums, counts, strict=True)
    )
    normalized_template = _normalize_signed(template)
    return tuple(
        normalized_template[(y % period) * period + (x % period)]
        for y in range(height)
        for x in range(width)
    )


def _neutral_layer(width: int, height: int) -> tuple[int, ...]:
    return (128,) * (width * height)


def _composite_layer(
    residual: Sequence[int],
    lsb: Sequence[int],
    periodic: Sequence[int],
) -> tuple[int, ...]:
    output: list[int] = []
    for residual_value, lsb_value, periodic_value in zip(
        residual,
        lsb,
        periodic,
        strict=True,
    ):
        combined = (
            128
            + 0.50 * (residual_value - 128)
            + 0.20 * (lsb_value - 128)
            + 0.30 * (periodic_value - 128)
        )
        output.append(max(0, min(255, int(round(combined)))))
    return tuple(output)


def reveal_hidden_signal_from_rgb(
    width: int,
    height: int,
    pixels: Sequence[RGBPixel],
    *,
    periods: Sequence[int] = DEFAULT_PERIODS,
) -> HeuristicRevealReport:
    """Surface hidden-signal cues without claiming a watermark verdict."""

    _validate_rgb_input(width, height, pixels)
    signed_residual = _signed_local_residual(width, height, pixels)
    residual_layer = _normalize_signed(signed_residual)
    lsb_layer = _lsb_map(pixels)

    periodicity_scan = _scan_periodicity(
        signed_residual,
        width,
        height,
        periods,
    )
    candidate_period, periodicity_cue = _choose_period(periodicity_scan)
    periodic_layer = (
        _fold_periodic_template(
            signed_residual,
            width,
            height,
            candidate_period,
        )
        if candidate_period is not None
        else _neutral_layer(width, height)
    )
    composite_layer = _composite_layer(
        residual_layer,
        lsb_layer,
        periodic_layer,
    )

    if candidate_period is None:
        label = (
            "本機啟發式分析沒有找到達到門檻的週期性線索；"
            "這不等於證明沒有隱藏浮水印。"
        )
    else:
        label = (
            f"本機啟發式分析在約 {candidate_period}px 週期找到可視化線索；"
            "這只是反向推理的候選結構，不是浮水印驗證結果。"
        )

    layers = (
        RevealLayer(
            name="local_residual",
            width=width,
            height=height,
            pixels=residual_layer,
            explanation_zh_tw="放大局部亮度殘差，讓低能量高頻擾動較容易被看見。",
        ),
        RevealLayer(
            name="lsb_balance",
            width=width,
            height=height,
            pixels=lsb_layer,
            explanation_zh_tw="把 RGB 最低有效位元的組合直接映射成灰階，供位元平面檢視。",
        ),
        RevealLayer(
            name="periodic_fold",
            width=width,
            height=height,
            pixels=periodic_layer,
            explanation_zh_tw=(
                "以候選週期折疊並平均局部殘差，放大可能重複出現的弱結構；"
                "未達門檻時保持中性灰。"
            ),
        ),
        RevealLayer(
            name="aion_reverse_reveal_composite",
            width=width,
            height=height,
            pixels=composite_layer,
            explanation_zh_tw=(
                "AION 自創工程啟發式：50% 局部殘差 + 20% LSB + "
                "30% 週期折疊。只供顯影與人工複核，不是 detector。"
            ),
        ),
    )

    return HeuristicRevealReport(
        width=width,
        height=height,
        method="AION_REVERSE_REVEAL_V0_1",
        candidate_period=candidate_period,
        periodicity_cue=periodicity_cue,
        periodicity_scan=periodicity_scan,
        layers=layers,
        visible_label_zh_tw=label,
    )


def write_reveal_layers_pgm(
    report: HeuristicRevealReport,
    output_dir: str | Path,
) -> tuple[Path, ...]:
    """Write reveal layers as dependency-free binary PGM files."""

    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for layer in report.layers:
        destination = directory / f"{layer.name}.pgm"
        header = f"P5\n{layer.width} {layer.height}\n255\n".encode("ascii")
        destination.write_bytes(header + bytes(layer.pixels))
        written.append(destination)

    return tuple(written)


def reveal_hidden_image_file(
    path: str | Path,
    *,
    output_dir: str | Path | None = None,
    periods: Sequence[int] = DEFAULT_PERIODS,
) -> HeuristicRevealReport:
    """Decode a common image locally with optional Pillow and run heuristic reveal."""

    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(file_path)

    try:
        pillow_image = importlib.import_module("PIL.Image")
    except ImportError as exc:
        raise RuntimeError(
            "Install the optional forensics dependency: "
            'pip install -e "research-labs/provenance-visibility-agent_v0.1.0[forensics]"'
        ) from exc

    with pillow_image.open(str(file_path)) as image:
        rgb_image = image.convert("RGB")
        width, height = (int(rgb_image.size[0]), int(rgb_image.size[1]))
        raw_pixels: Any = tuple(rgb_image.getdata())

    pixels: list[RGBPixel] = []
    for item in raw_pixels:
        if not isinstance(item, tuple) or len(item) < 3:
            raise ValueError("Pillow RGB conversion returned an unexpected pixel")
        pixels.append((int(item[0]), int(item[1]), int(item[2])))

    report = reveal_hidden_signal_from_rgb(
        width,
        height,
        pixels,
        periods=periods,
    )
    if output_dir is not None:
        write_reveal_layers_pgm(report, output_dir)
    return report


def render_heuristic_reveal_markdown(report: HeuristicRevealReport) -> str:
    lines = [
        "# 隱藏訊號啟發式顯影報告",
        "",
        f"- 方法：{report.method}",
        f"- 尺寸：{report.width}×{report.height}",
        (
            "- 候選週期："
            f"{report.candidate_period if report.candidate_period is not None else '未建立'}"
        ),
        f"- 週期線索值：{report.periodicity_cue:.4f}（不是機率）",
        f"- 浮水印判定：{report.watermark_verdict}",
        f"- 明示標籤：{report.visible_label_zh_tw}",
        "",
        "## 顯影層",
    ]
    for layer in report.layers:
        lines.append(f"- {layer.name}：{layer.explanation_zh_tw}")
    lines.extend(
        [
            "",
            "## 解讀邊界",
            "- HEURISTIC_CUE != WATERMARK_DETECTION",
            "- HEURISTIC_SCORE != PROBABILITY",
            "- 顯影出的規律可能來自壓縮、去馬賽克、抖動、縮放、銳化或其他處理。",
            "- 不以此結果推論作者、帳號、模型身分或 prompt。",
            "- 本功能不提供浮水印移除、破壞或規避。",
        ]
    )
    return "\n".join(lines) + "\n"
