# Western astrology source snapshots

- `public-domain/ptolemy-tetrabiblos-pg70850.txt` is Project Gutenberg ebook
  70850, identified by Project Gutenberg as public domain in the United States.
- `public-domain/sepharial-astrology-pg46963.txt` is Project Gutenberg ebook
  46963, identified by Project Gutenberg as public domain in the United States.
- `public-domain/wikisource-christian-astrology.txt` is the pinned revision
  `15666418` of William Lilly's public-domain work with Wikisource's CC BY-SA
  transcription layer. Its known OCR errors are explicit; it is a table and
  terminology cross-check rather than a sole authority.
- `SOURCE_FETCH_MANIFEST.json` contains the exact URLs, byte counts, SHA-256
  hashes, acquisition transport, license/terms labels, and retention policy.

Dorotheus and Valens bibliographic/translation-link registers, Swiss Ephemeris
documentation, JPL Horizons documentation, and Astrodienst reference pages are
link-and-hash records only. No copyrighted Dorotheus/Valens translation and no
Swiss Ephemeris code/data dependency was introduced.

The three Alan Leo 1910 scan parts are identified by the source library with a
Public Domain Mark 1.0. Each is downloaded and hashed, then discarded so that
roughly 87 MB of scans are not added to the repository.

Refresh deterministically from the repository root:

```powershell
& 'C:\A15\venv\Scripts\python.exe' scripts\fetch_astrology_bazi_sources.py
```

