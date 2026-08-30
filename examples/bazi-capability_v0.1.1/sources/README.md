# Bazi source snapshots and attribution

The exact URL, version/commit, byte count, SHA-256, transport, and retention
policy for every item are in `SOURCE_FETCH_MANIFEST.json`.

- `lunar-python-1.4.8-LICENSE.txt` and `README_EN.md` are pinned to commit
  `000c8a3d74eed098d6256a28fdd51b869324c559`; the software is MIT licensed.
- The lunar-python 1.4.8 sdist is downloaded and verified against PyPI SHA-256
  `3aa11cc73c25e70ddf0ba5bdac7398c03acc9491a3aa512a91c9642973b669d6`,
  then discarded because the runtime dependency is already declared normally.
- Wikisource snapshots contain public-domain source texts with Wikisource's
  CC BY-SA site/transcription layer. Attribution and source URLs are preserved
  here and in the manifest. `淵海子平` is comparison evidence only because the
  source page flags completeness/provenance concerns. The `三命通會` item is an
  index/provenance snapshot, not a claim of one definitive edition.
- Hong Kong Observatory and Taiwan Central Weather Administration references
  are link-and-hash only and are not retained.

No network access is needed at runtime.

