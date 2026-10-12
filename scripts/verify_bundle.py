#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Verify the release manifest, private-data exclusions and Skill entrypoints offline."""
import hashlib,json,re,sys,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from package import files
errors=[]
manifest=json.loads((ROOT/'files.sha256.json').read_text())['files']
actual={str(p.relative_to(ROOT)):p for p in files()}
if set(actual)!=set(x['path']for x in manifest):errors.append('Manifest file set differs')
for x in manifest:
    f=ROOT/x['path']
    if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=x['sha256']:errors.append('Hash mismatch: '+x['path'])
lock=json.loads((ROOT/'dependencies.lock.json').read_text())
ids=[x['id']for x in lock['components']]
if len(ids)!=len(set(ids)):errors.append('Duplicate dependency IDs')
for c in lock['components']:
    if c['status']=='bundled' and (not c.get('path') or not (ROOT/c['path']).exists()):errors.append('Missing component: '+c['id'])
    if c['status']=='bundled' and c['license']=='NOASSERTION':errors.append('Unlicensed bundled component: '+c['id'])
private=re.compile(r'/Users/[A-Za-z0-9_.-]+/|/var/folders/')
secrets=re.compile(r'gh[pousr]_[A-Za-z0-9]{24,}|sk-[A-Za-z0-9]{32,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----\n[A-Za-z0-9+/=]{20,}')
for rel,f in actual.items():
    if rel== 'scripts/verify_bundle.py':continue
    if f.stat().st_size>8_000_000:errors.append('Oversized unchecked file: '+rel);continue
    try:t=f.read_text()
    except UnicodeError:continue
    approved=json.loads((ROOT/'config/scanner-fixtures.json').read_text())
    excepted=approved.get(rel,{}).get('sha256')==hashlib.sha256(f.read_bytes()).hexdigest()
    if private.search(t) and not excepted:errors.append('Private source marker: '+rel)
    if secrets.search(t):
        # Upstream test fixture exceptions are file-hash pinned and individually reviewed.
        approved=json.loads((ROOT/'config/scanner-fixtures.json').read_text())
        if not excepted:errors.append('Credential-like content: '+rel)
for f in sorted((ROOT/'skills').glob('*/SKILL.md')):
    t=f.read_text();m=re.match(r'^---\n(.*?)\n---',t,re.S)
    if not m or not re.search(r'''^name:\s*["']?[a-z0-9-]+["']?\s*$''',m[1],re.M) or not re.search(r'^description:\s*\S',m[1],re.M):errors.append('Invalid Skill frontmatter: '+str(f.relative_to(ROOT)))
    if not any(x.name.lower().startswith('license')for x in f.parent.iterdir()):errors.append('Missing Skill license: '+f.parent.name)
# Installer's no-overwrite behavior matters: test using a temporary destination only.
with tempfile.TemporaryDirectory(prefix='gbro-bundle-check-')as d:
    dest=Path(d)/'skills';base=[sys.executable,str(ROOT/'scripts/install_skills.py'),'--destination',str(dest)]
    preview=subprocess.run(base,capture_output=True)
    if preview.returncode or dest.exists():errors.append('Preview wrote files or failed')
    applied=subprocess.run(base+['--apply'],capture_output=True)
    target=dest/'gbro-social-workflow/SKILL.md'
    if applied.returncode or not target.is_file():errors.append('Install failed')
    if target.exists():
        target.write_text('user modification\n')
        conflict=subprocess.run(base+['--apply','--skill','gbro-social-workflow','--skill','human-writing'],capture_output=True)
        if conflict.returncode!=2 or target.read_text()!='user modification\n' or (dest/'human-writing').exists():errors.append('Conflict handling overwrote or partly installed')
print(json.dumps({'ok':not errors,'files':len(actual),'skills':len(list((ROOT/'skills').glob('*/SKILL.md'))),'components':len(ids),'errors':errors},ensure_ascii=False,indent=2))
raise SystemExit(1 if errors else 0)
