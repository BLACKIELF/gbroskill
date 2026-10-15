#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Create a source ZIP from an explicit per-file manifest. No Git history or local state."""
import argparse,hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKIP={'.git','.venv','node_modules','__pycache__','.pytest_cache','.data','dist','private','profiles','cookies','accounts'}
META={'files.sha256.json','SHA256SUMS.txt'}
def files():
    for p in sorted(ROOT.rglob('*')):
        rel=p.relative_to(ROOT)
        if p.is_symlink():raise SystemExit('Refuse symlink: '+str(rel))
        if not p.is_file() or any(x in SKIP for x in rel.parts) or str(rel) in META or p.name=='.DS_Store' or p.suffix in ['.pyc','.log']:continue
        if p.name=='.env' or (p.name.startswith('.env.') and p.name not in ['.env.example','.env.template']):continue
        if p.name.endswith('.local.json'):continue
        yield p

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--refresh',action='store_true');p.add_argument('--output',type=Path);a=p.parse_args()
    if not a.refresh and not a.output:p.error('Choose --refresh and/or --output')
    rows=[{'path':str(f.relative_to(ROOT)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size}for f in files()]
    if a.refresh:
        (ROOT/'files.sha256.json').write_text(json.dumps({'algorithm':'sha256','files':rows},ensure_ascii=False,indent=2)+'\n')
        (ROOT/'SHA256SUMS.txt').write_text(''.join(f'{x["sha256"]}  {x["path"]}\n'for x in rows))
    else:
        expected=json.loads((ROOT/'files.sha256.json').read_text())['files']
        if expected!=rows:raise SystemExit('Source changed; verify it, then --refresh the manifest')
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(a.output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9)as z:
            for rel in [x['path']for x in rows]+sorted(META):
                f=ROOT/rel;info=zipfile.ZipInfo('gbroskill-'+(ROOT/'VERSION').read_text().strip()+'/'+rel,date_time=(2026,10,12,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=(f.stat().st_mode&0o777)<<16
                z.writestr(info,f.read_bytes())
        with zipfile.ZipFile(a.output)as z:
            if z.testzip():raise SystemExit('ZIP CRC failed')
        checksum=hashlib.sha256(a.output.read_bytes()).hexdigest()
        a.output.with_name(a.output.name+'.sha256').write_text(checksum+'  '+a.output.name+'\n')
        print(json.dumps({'files':len(rows)+2,'bytes':a.output.stat().st_size,'sha256':checksum}))
    else:print(json.dumps({'files':len(rows),'manifest':'refreshed'}))
if __name__=='__main__':main()
