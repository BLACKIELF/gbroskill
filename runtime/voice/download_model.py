#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Download the pinned upstream model only after explicit license acceptance."""
import argparse,hashlib,json,os,sys,urllib.request
from pathlib import Path
BASE=Path(__file__).resolve().parent

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
    return h.hexdigest()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--destination',type=Path,required=True)
    p.add_argument('--accept-license',action='store_true',help='You have read and independently accept the bundled model LICENSE for research/non-commercial use.')
    p.add_argument('--check-only',action='store_true',help='Verify an existing local model without networking or changing it.')
    a=p.parse_args();m=json.loads((BASE/'model.json').read_text())
    if not a.check_only and not a.accept_license:
        print((BASE/'LICENSE').read_text());print('\nNo download started. Read the full license, then explicitly pass --accept-license if you agree.',file=sys.stderr)
        return 2
    rows=[]
    for entry in m['files']:
        relative=Path(entry['path'])
        if relative.is_absolute() or '..' in relative.parts:raise ValueError('Invalid manifest path')
        f=a.destination/relative
        if f.is_file():
            if f.stat().st_size!=entry['bytes'] or digest(f)!=entry['sha256']:raise SystemExit('Existing file differs; not overwritten: '+str(f))
            rows.append({'path':entry['path'],'status':'verified'});continue
        if a.check_only:raise SystemExit('Missing: '+str(f))
        f.parent.mkdir(parents=True,exist_ok=True);part=f.with_name(f.name+'.part')
        if part.exists():raise SystemExit('Partial file exists; inspect it before retrying: '+str(part))
        url=f"https://huggingface.co/{m['repo']}/resolve/{m['revision']}/{entry['path']}"
        request=urllib.request.Request(url,headers={'User-Agent':'gbroskill-model-fetcher'})
        with urllib.request.urlopen(request,timeout=90) as response, part.open('xb') as dest:
            while True:
                block=response.read(4*1024*1024)
                if not block:break
                dest.write(block)
        if part.stat().st_size!=entry['bytes'] or digest(part)!=entry['sha256']:raise SystemExit('Download hash mismatch; kept partial file: '+str(part))
        part.rename(f);rows.append({'path':entry['path'],'status':'downloaded-and-verified'})
        print(json.dumps(rows[-1]),flush=True)
    print(json.dumps({'ok':True,'revision':m['revision'],'files':len(rows),'network_used':not a.check_only and any(r['status'].startswith('downloaded') for r in rows)}))
    return 0
if __name__=='__main__':raise SystemExit(main())
