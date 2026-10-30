#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read-only local readiness check; never installs, downloads or generates audio."""
import argparse
import hashlib
import importlib.metadata
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
VOICE = BASE.parents[1] / 'skills/gbro-social-workflow/assets/voice/aigoodbro-g4'


def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b''):
            value.update(chunk)
    return value.hexdigest()


def verify_model(directory, manifest=None):
    manifest = manifest or json.loads((BASE / 'model.json').read_text())
    result = {'checked': directory is not None, 'ok': False, 'files_verified': 0, 'errors': []}
    if directory is None:
        result['errors'].append('model_directory_not_supplied')
        return result
    for entry in manifest['files']:
        relative = Path(entry['path'])
        if relative.is_absolute() or '..' in relative.parts:
            result['errors'].append('unsafe_manifest_path')
            continue
        path = directory / relative
        if not path.is_file():
            result['errors'].append('missing:' + entry['path'])
        elif path.stat().st_size != entry['bytes'] or digest(path) != entry['sha256']:
            result['errors'].append('hash_or_size_mismatch:' + entry['path'])
        else:
            result['files_verified'] += 1
    result['ok'] = not result['errors']
    return result


def runtime_environment():
    expected = dict(line.strip().split('==', 1) for line in (BASE / 'requirements.txt').read_text().splitlines() if '==' in line)
    installed = {}
    for name in expected:
        try:
            installed[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            installed[name] = None
    system, machine = platform.system(), platform.machine()
    platform_ok = system == 'Darwin' and machine.lower() in ('arm64', 'aarch64')
    python_ok = sys.version_info[:2] == (3, 12)
    versions_ok = installed == expected
    metal = False
    if platform_ok and python_ok and versions_ok:
        try:
            import mlx.core as mx
            metal = bool(mx.metal.is_available())
        except (ImportError, OSError, RuntimeError, AttributeError):
            pass
    return {'system': system, 'architecture': machine, 'python': platform.python_version(),
            'verified_platform_match': platform_ok, 'python_3_12': python_ok,
            'expected_packages': expected, 'installed_packages': installed,
            'package_versions_match': versions_ok, 'metal_available': metal,
            'ready': platform_ok and python_ok and versions_ok and metal}


def font_available():
    if platform.system() == 'Darwin' and Path('/System/Library/Fonts/PingFang.ttc').is_file():
        return True
    if shutil.which('fc-match'):
        try:
            result = subprocess.run(['fc-match', '-f', '%{family}\n', 'PingFang SC'], capture_output=True, text=True, timeout=5)
            return result.returncode == 0 and any(name.strip() == 'PingFang SC' for name in result.stdout.strip().split(','))
        except (OSError, subprocess.TimeoutExpired):
            pass
    return False


def inspect_environment(model=None):
    from generate import validate_voice_profile
    asset_errors = []
    try:
        profile = json.loads((VOICE / 'profile.json').read_text())
        validate_voice_profile(profile)
        for file_key, hash_key in [('reference_audio', 'reference_sha256'), ('sample_file', 'sample_sha256'), ('accepted_sample_file', 'accepted_sample_sha256')]:
            path = VOICE / profile[file_key]
            if not path.is_file() or digest(path) != profile[hash_key]:
                asset_errors.append('voice_asset_mismatch:' + profile[file_key])
    except (OSError, ValueError, KeyError, SystemExit) as error:
        asset_errors.append(type(error).__name__ + ': invalid_voice_profile_or_assets')
    runtime = runtime_environment()
    model_check = verify_model(model)
    can_generate = not asset_errors and runtime['ready'] and model_check['ok']
    return {'mode': 'local_read_only', 'network_requests': False, 'files_written': False,
            'audio_generated': False, 'voice': {'can_generate': can_generate,
            'asset_errors': asset_errors, 'runtime': runtime, 'model': model_check},
            'media': {'ffmpeg_available': bool(shutil.which('ffmpeg')),
                      'ffprobe_available': bool(shutil.which('ffprobe')),
                      'required_font_available': font_available(),
                      'browser_webgl2': 'not_checked', 'render_acceptance': 'not_checked'},
            'next_action': 'generate_complete_narration_then_listen' if can_generate else
            'continue_text_and_layout; reuse_approved_audio_or_handoff_complete_script_to_verified_Apple_Silicon_worker; do_not_substitute_TTS'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', type=Path, help='Verify every file of an existing model; no download.')
    args = parser.parse_args()
    result = inspect_environment(args.model)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['voice']['can_generate'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
