# Western astrology source snapshots

- `public-domain/ptolemy-tetrabiblos-pg70850.txt` is Project Gutenberg ebook
  70850, identified by Project Gutenberg as public domain in the United States.
- `public-domain/sepharial-astrology-pg46963.txt` is Project Gutenberg ebook
  46963, identified by Project Gutenberg as public domain in the United States.
- `SOURCE_FETCH_MANIFEST.json` contains the exact URLs, byte counts, SHA-256
  hashes, acquisition transport, license/terms labels, and retention policy.

Swiss Ephemeris documentation, JPL Horizons documentation, and Astrodienst
reference pages are link-and-hash records only. Their payloads are deliberately
not retained in this repository. No Swiss Ephemeris code/data dependency was
introduced.

Refresh deterministically from the repository root:

```powershell
& 'C:\A15\venv\Scripts\python.exe' scripts\fetch_astrology_bazi_sources.py
```

