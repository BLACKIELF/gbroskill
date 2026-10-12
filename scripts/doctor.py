#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Local inventory only. Does not access accounts, log in or upload."""
import json,os,shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1]
runtime=Path(os.environ.get('GBRO_RUNTIME_ROOT',str(root/'vendor')))
print(json.dumps({'mode':'local-only','credentials_read':False,'network_requests':False,
 'commands':{n:bool(shutil.which(n)) for n in ['python3','node','bun','ffmpeg','lark-cli']},
 'source_components':{n:(runtime/n).is_dir() for n in ['social-auto-upload','autotok','stylewx','agent-reach','biliup','lark-cli']},
 'python_environments':{n:(runtime/n/'.venv/bin/python').exists() for n in ['social-auto-upload','autotok']},
 'login_status':'not_checked','publication_status':'not_checked'},indent=2))
