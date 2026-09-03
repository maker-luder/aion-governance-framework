from pathlib import Path
import hashlib
import json


def test_all_twelve_main_volumes_are_exact_revision_bound():
    root = Path(__file__).parents[1]
    manifest = json.loads((root/"sources/SOURCE_FETCH_MANIFEST.json").read_text(encoding="utf-8"))
    rows = [s for s in manifest["sources"] if s["source_id"].startswith("WIKISOURCE_SAN_MING_TONG_HUI_VOLUME_")]
    assert len(rows) == 12
    assert {s["source_id"][-2:] for s in rows} == {f"{i:02}" for i in range(1, 13)}
    for s in rows:
        assert f"oldid={s['revision_id']}" in s["url"]
        path = root/"sources/reviewed-snapshots"/s["repository_path"].split("/")[-1]
        payload = path.read_bytes()
        assert len(payload) == s["repository_bytes"]
        assert hashlib.sha256(payload).hexdigest() == s["repository_sha256"]
        assert s["download_status"] == "PASS"
        assert s["license_or_terms"] == "PUBLIC_DOMAIN_TEXT_CC_BY_SA_SITE_LAYER"


def test_rule_map_points_to_actual_retained_sections():
    root = Path(__file__).parents[1]/"sources/reviewed-snapshots"
    for volume, terms in [(1, ("論十干名字之義", "論十二支名字之義")),
                          (2, ("論人元司事", "論四時節氣", "論十干合", "論十干化氣")),
                          (5, ("論正官", "論印綬")), (10, ("日干為主", "提綱", "月令"))]:
        text = (root/f"wikisource-san-ming-tong-hui-volume-{volume:02}.txt").read_text(encoding="utf-8")
        assert all(term in text for term in terms)
