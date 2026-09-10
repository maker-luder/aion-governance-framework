"""Verify archives; optionally restore baseline into a NEW delivery-local directory.

No deletion, overwrite, Git mutation, network access, or incident-history rewrite.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import zipfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", help="Nonexistent child directory of this delivery folder")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    manifest = json.loads((here / "archive-hashes.json").read_text(encoding="utf-8"))
    for name, digest in manifest.items():
        if Path(name).name != name:
            raise ValueError("manifest names must be local filenames")
        if hashlib.sha256((here / name).read_bytes()).hexdigest() != digest:
            raise ValueError("artifact hash mismatch: " + name)
    print("ARTIFACT_HASHES=PASS")
    with zipfile.ZipFile(here / "baseline.zip") as archive:
        if archive.testzip() is not None:
            raise ValueError("baseline ZIP corruption")
        members = archive.infolist()
        for info in members:
            path = PurePosixPath(info.filename)
            if path.is_absolute() or ".." in path.parts or "\\" in info.filename or ":" in info.filename:
                raise ValueError("unsafe archive member")
            if stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError("symlink restoration requires explicit separate review")
        if not args.output:
            print("ROLLBACK_VERIFY=PASS; MODE=READ_ONLY")
            return
        output = Path(args.output).resolve()
        if here not in output.parents or output.exists():
            raise ValueError("output must be a NEW child of the delivery folder")
        output.mkdir(parents=True, exist_ok=False)
        for info in members:
            path = output.joinpath(*PurePosixPath(info.filename).parts)
            if info.is_dir():
                path.mkdir(parents=True, exist_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open("xb") as stream:
                    stream.write(archive.read(info))
        expected = {info.filename for info in members if not info.is_dir()}
        actual = {p.relative_to(output).as_posix() for p in output.rglob("*") if p.is_file()}
        if actual != expected:
            raise ValueError("restored member set mismatch")
        for name in expected:
            if output.joinpath(*PurePosixPath(name).parts).read_bytes() != archive.read(name):
                raise ValueError("restored bytes mismatch: " + name)
        print("RESTORED_BASELINE=PASS; FILES=" + str(len(expected)))
        print("EXISTING_CANDIDATE_MODIFIED=FALSE; INCIDENT_HISTORY_MODIFIED=FALSE")


if __name__ == "__main__":
    main()
