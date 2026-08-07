from __future__ import annotations
import hashlib,json,re,sys
from pathlib import Path
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
manifest_path=root/'PUBLIC_RELEASE_MANIFEST.json'
data=json.loads(manifest_path.read_text(encoding='utf-8'))
errors=[]
for row in data['files']:
 p=root/row['path']
 if not p.is_file(): errors.append('missing:'+row['path']); continue
 h=hashlib.sha256(p.read_bytes()).hexdigest()
 if h!=row['sha256']: errors.append('hash:'+row['path'])
for p in root.rglob('*'):
 if p.is_file() and p.suffix.lower() in {'.pyc','.whl','.zip','.exe','.dll'}: errors.append('forbidden:'+p.relative_to(root).as_posix())
print(json.dumps({'status':'PASS' if not errors else 'FAIL','errors':errors},indent=2))
raise SystemExit(0 if not errors else 1)
