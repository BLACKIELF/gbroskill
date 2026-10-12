#!/usr/bin/env python3
"""Install chosen source Skills without overwriting existing installations."""
# SPDX-License-Identifier: MIT
import argparse, hashlib, json, shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def inventory(path):
    return {str(p.relative_to(path)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in path.rglob('*') if p.is_file()}
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--destination',type=Path,required=True)
    p.add_argument('--skill',action='append',default=[])
    p.add_argument('--all',action='store_true',help='Select all bundled top-level Skills')
    p.add_argument('--apply',action='store_true',help='Actually copy; otherwise preview only')
    args=p.parse_args()
    available={x.name:x for x in (ROOT/'skills').iterdir() if (x/'SKILL.md').is_file()}
    if args.all and args.skill:p.error('Choose --all or --skill, not both')
    names=sorted(available) if args.all else (args.skill or ['gbro-social-workflow'])
    unknown=set(names)-set(available)
    if unknown:p.error('Unknown Skill: '+', '.join(sorted(unknown)))
    plan=[]
    for name in names:
        src=available[name];dst=args.destination.expanduser()/name
        if any(x.is_symlink() for x in src.rglob('*')):p.error('Source contains a symlink: '+name)
        if dst.is_symlink():state='conflict'
        elif dst.exists():state='unchanged' if dst.is_dir() and inventory(src)==inventory(dst) else 'conflict'
        else:state='new'
        plan.append({'skill':name,'state':state})
    print(json.dumps({'apply':args.apply,'destination':str(args.destination.expanduser()),'plan':plan},ensure_ascii=False,indent=2))
    if any(x['state']=='conflict' for x in plan):
        print('Conflicts found. Nothing changed. Compare and back up existing Skills manually.')
        return 2
    if args.apply:
        args.destination.expanduser().mkdir(parents=True,exist_ok=True)
        for row in plan:
            if row['state']=='new':shutil.copytree(available[row['skill']],args.destination.expanduser()/row['skill'])
    return 0
if __name__=='__main__':raise SystemExit(main())
