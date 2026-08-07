
from __future__ import annotations
import argparse, json
from .pipeline import run_pipeline

def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate one structured governance request")
    parser.add_argument("request_json")
    parser.add_argument("--db", default=":memory:")
    args = parser.parse_args()
    payload = json.loads(args.request_json)
    print(json.dumps(run_pipeline(payload, args.db), ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
