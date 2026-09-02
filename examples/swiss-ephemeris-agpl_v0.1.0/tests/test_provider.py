# SPDX-License-Identifier: AGPL-3.0-only
from pathlib import Path
import hashlib
import io
import json
from types import SimpleNamespace

import pytest

from aion_swiss_ephemeris import provider as p

FIXTURES = Path(__file__).parent / "fixtures"


def output():
    return (FIXTURES / "j2000-tt.txt").read_text(encoding="utf-8")


def test_captured_pinned_tt_output():
    result = p.parse_output(output(), "", 0, 2451545.0)
    assert len(result) == 10
    assert result[0]["longitude_degrees"] == 280.3681656
    assert result[1]["longitude_degrees"] == 223.3148705
    assert result[6]["speed_degrees_per_day"] < 0


@pytest.mark.parametrize("jd", [True, None, "2451545", float("nan"), float("inf"), 2399999, 2500001, 10**400])
def test_invalid_epoch_rejected(jd):
    with pytest.raises(ValueError):
        p.validate_jd(jd)


def test_exit_zero_moshier_fallback_is_rejected():
    text = (FIXTURES / "moshier-fallback.txt").read_text(encoding="utf-8")
    with pytest.raises(ValueError, match="fallback"):
        p.parse_output(text, "", 0, 2451545)


@pytest.mark.parametrize("change", [
    lambda s: s.replace("version 2.10.03", "version 2.10.02"),
    lambda s: s.replace("2451545.000000000", "2451546.000000000"),
    lambda s: s.replace("280.3681656", "nan"),
    lambda s: s.replace("1.0194341", "inf"),
    lambda s: s.replace("Sun            ,", "Moon           ,"),
    lambda s: s.replace("Pluto", "Unknown"),
    lambda s: s + "Sun, 1, 2\n",
    lambda s: s + "x" * 65537,
])
def test_invalid_output_rejected(change):
    with pytest.raises(ValueError):
        p.parse_output(change(output()), "", 0, 2451545)


@pytest.mark.parametrize("error,code", [("failure", 0), ("", 1)])
def test_process_failure_rejected(error, code):
    with pytest.raises(ValueError):
        p.parse_output(output(), error, code, 2451545)


def tiny_lock(monkeypatch):
    entry = {"path": "ephe/test.se1", "bytes": 3, "sha256": hashlib.sha256(b"abc").hexdigest()}
    monkeypatch.setattr(p, "manifest", lambda: {"files": [entry]})
    return entry


def test_cache_digest_and_missing_data_fail_before_execution(monkeypatch, tmp_path):
    tiny_lock(monkeypatch)
    with pytest.raises(FileNotFoundError):
        p.calculate(tmp_path, 2451545)
    path = tmp_path / "ephe/test.se1"
    path.parent.mkdir(); path.write_bytes(b"xyz")
    with pytest.raises(ValueError, match="mismatch"):
        p.calculate(tmp_path, 2451545)
    path.write_bytes(b"abc")
    assert len(p.verify_cache(tmp_path)) == 1


def test_existing_cache_verifies_without_network(monkeypatch, tmp_path):
    tiny_lock(monkeypatch)
    path = tmp_path / "ephe/test.se1"
    path.parent.mkdir(); path.write_bytes(b"abc")
    monkeypatch.setattr(p.urllib.request, "build_opener", lambda *a: SimpleNamespace(
        open=lambda *a, **kw: pytest.fail("network must not be used for valid existing cache")))
    assert p.fetch(tmp_path)["files"] == 1


def test_path_escape_rejected(tmp_path):
    with pytest.raises(ValueError):
        p.cache_path(tmp_path, "../external.se1")


def test_calculation_uses_explicit_argv_and_preserves_nonclaims(monkeypatch, tmp_path):
    monkeypatch.setattr(p, "verify_cache", lambda cache: [])
    monkeypatch.setattr(p.sys, "platform", "win32")
    captured = {}
    def run(argv, **kwargs):
        captured.update(argv=argv, kwargs=kwargs)
        return SimpleNamespace(stdout=output(), stderr="", returncode=0)
    monkeypatch.setattr(p.subprocess, "run", run)
    result = p.calculate(tmp_path, 2451545)
    assert "-bj2451545.000000000" in captured["argv"]
    assert captured["kwargs"]["timeout"] == 30
    assert "shell" not in captured["kwargs"]
    assert result["time_scale"] == "TT" and result["complete_chart"] is False
    assert result["canonical_effect"] == "NONE" and result["subjectivity"] == "NOT_ESTABLISHED"
    assert result["network_during_calculation"] is False
    json.dumps(result, allow_nan=False)


def test_packaged_lock_has_explicit_immutable_urls():
    lock = p.manifest()
    assert len(lock["files"]) == 7
    for entry in lock["files"]:
        assert entry["url"] == f"https://raw.githubusercontent.com/aloistr/swisseph/{p.UPSTREAM_COMMIT}/{entry['path']}"
        assert len(entry["sha256"]) == 64 and entry["bytes"] > 0


@pytest.mark.parametrize("payload,success", [(b"abc", True), (b"xyz", False)])
def test_acquisition_checks_before_persisting(monkeypatch, tmp_path, payload, success):
    tiny_lock(monkeypatch)
    def open_url(url, timeout):
        assert url == f"https://raw.githubusercontent.com/aloistr/swisseph/{p.UPSTREAM_COMMIT}/ephe/test.se1"
        assert timeout == 60
        return io.BytesIO(payload)
    monkeypatch.setattr(p.urllib.request, "build_opener", lambda *a: SimpleNamespace(open=open_url))
    if success:
        assert p.fetch(tmp_path)["status"] == "PASS"
        assert (tmp_path / "ephe/test.se1").read_bytes() == b"abc"
    else:
        with pytest.raises(ValueError, match="mismatch"):
            p.fetch(tmp_path)
        assert not (tmp_path / "ephe/test.se1").exists()


def test_redirects_are_not_followed():
    assert p.NoRedirect().redirect_request(None, None, 302, None, {}, "https://other.example") is None


def test_platform_and_path_list_are_explicit(monkeypatch, tmp_path):
    monkeypatch.setattr(p, "verify_cache", lambda cache: [])
    monkeypatch.setattr(p.sys, "platform", "linux")
    with pytest.raises(ValueError, match="Windows"):
        p.calculate(tmp_path, 2451545)
    monkeypatch.setattr(p.sys, "platform", "win32")
    with pytest.raises(ValueError, match="delimiter"):
        p.calculate(tmp_path / "one;two", 2451545)


@pytest.mark.parametrize("command", ["fetch", "verify", "calculate"])
def test_cli_routes_explicit_operation(monkeypatch, tmp_path, capsys, command):
    from aion_swiss_ephemeris import __main__ as cli
    monkeypatch.setattr(cli, "fetch", lambda cache: {"status": "PASS"})
    monkeypatch.setattr(cli, "verify_cache", lambda cache: [1] * 7)
    monkeypatch.setattr(cli, "calculate", lambda cache, jd: {"jd_tt": jd})
    argv = ["provider", command, "--cache", str(tmp_path)]
    if command == "calculate":
        argv += ["--jd-tt", "2451545"]
    monkeypatch.setattr(p.sys, "argv", argv)
    assert cli.main() == 0
    assert isinstance(json.loads(capsys.readouterr().out), dict)
