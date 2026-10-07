"""Rebuild pinned tables from explicit offline inputs / 從明示的離線官方原檔重建固定版本資料。"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from typing import Iterator

SOURCES = {
    'DerivedCoreProperties.txt': 'https://www.unicode.org/Public/15.0.0/ucd/DerivedCoreProperties.txt',
    'Scripts.txt': 'https://www.unicode.org/Public/15.0.0/ucd/Scripts.txt',
    'confusables.txt': 'https://www.unicode.org/Public/security/15.0.0/confusables.txt',
}


def rows(path: Path) -> Iterator[list[str]]:
    for line in path.read_text(encoding='utf-8').splitlines():
        body = line.split('#')[0].strip()
        if body:
            yield [part.strip() for part in body.split(';')]


def bounds(value: str) -> list[int]:
    start, *end = value.split('..')
    return [int(start,16),int(end[0] if end else start,16)]


def build(source: Path, manifest: Path) -> bytes:
    """Digest-check raw inputs before derivation / 衍生前核對官方原檔 bytes 摘要。"""
    expected = json.loads(manifest.read_text(encoding='utf-8'))['sources']
    for name in SOURCES:
        if hashlib.sha256((source/name).read_bytes()).hexdigest() != expected[name]['sha256']:
            raise ValueError(f'SOURCE_DIGEST_MISMATCH: {name}')
    data = {
        'version':'15.0.0',
        'default_ignorable':[bounds(r[0]) for r in rows(source/'DerivedCoreProperties.txt') if r[1]=='Default_Ignorable_Code_Point'],
        'scripts':sorted([bounds(r[0])+[r[1]] for r in rows(source/'Scripts.txt')]),
        'confusables':{str(int(r[0],16)):[int(x,16) for x in r[1].split()] for r in rows(source/'confusables.txt')},
        'sources':{name:{'url':url,'sha256':expected[name]['sha256']} for name,url in SOURCES.items()},
    }
    return (json.dumps(data,ensure_ascii=True,sort_keys=True,separators=(',',':'))+'\n').encode()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-directory',type=Path,required=True)
    parser.add_argument('--manifest',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    payload=build(args.source_directory,args.manifest)
    # Exclusive creation: never overwrite source or manifest / 排他建立，避免覆寫来源或既有檔案。
    with args.output.open('xb') as handle:
        handle.write(payload)
