# Source snapshots

Run `python scripts/fetch_ziwei_sources.py` from the repository root.

Redistributable Wikisource and MIT repository documents are retained under
`reviewed-snapshots/`. Package tarballs and official calendar PDFs are fetched,
hashed and discarded; their exact URLs, sizes and hashes remain in
`SOURCE_FETCH_MANIFEST.json`. None of these sources are fetched at runtime.
