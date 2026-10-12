# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 AiGoodBro contributors
# Modified 2026-10-12: portable data and browser paths; original guard retained.
"""Fixed local TikTok runtime; stdout belongs to the requested CLI/MCP command."""
import os
from pathlib import Path
import sys
import functools

ROOT = Path(os.environ.get('GBRO_DATA_DIR', str(Path.home() / '.local/share/gbroskill')))
DATA = ROOT / 'private-tiktok'
CHROME = os.environ.get('GBRO_CHROME', '')


def validate_caption(caption: str) -> None:
    from autotok.captions import build_caption
    from autotok.errors import ValidationError
    if not isinstance(caption, str):
        raise ValidationError('caption is required')
    _, extras = build_caption(caption)
    tags = [item['hashtag_name'] for item in extras if item['type'] == 1]
    if 'AiGoodBro' not in tags:
        raise ValidationError('GBro captions must contain the exact #AiGoodBro hashtag.')
    if len(tags) > 5:
        raise ValidationError('GBro currently allows at most 5 hashtags including #AiGoodBro. This is a local operating limit.')


def install_caption_guard() -> None:
    from autotok.uploader import Client
    original = Client.upload
    @functools.wraps(original)
    def guarded_upload(self, video, caption, **kwargs):
        validate_caption(caption)
        return original(self, video, caption, **kwargs)
    Client.upload = guarded_upload


def main() -> int:
    argv = sys.argv[1:]
    if argv and argv[0] == '--mcp':
        argv = ['mcp', *argv[1:]]
    for index, item in enumerate(argv):
        if item.startswith('--browser=') and item != '--browser=local':
            raise SystemExit('This GBro installation uses the local browser only.')
        if item == '--browser' and (index + 1 >= len(argv) or argv[index + 1] != 'local'):
            raise SystemExit('This GBro installation uses the local browser only.')
        if item.startswith('--host=') and item.split('=', 1)[1] not in ('127.0.0.1', 'localhost', '::1'):
            raise SystemExit('The unauthenticated TikTok MCP HTTP server must stay on loopback.')
        if item == '--host' and (index + 1 >= len(argv) or argv[index + 1] not in ('127.0.0.1', 'localhost', '::1')):
            raise SystemExit('The unauthenticated TikTok MCP HTTP server must stay on loopback.')

    os.umask(0o077)
    DATA.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.environ.update({
        'AUTOTOK_HOME': str(DATA),
        'AUTOTOK_BROWSER': 'local',
        'AUTOTOK_BROWSER_CHANNEL': 'chrome',
    })
    if CHROME:
        os.environ['AUTOTOK_BROWSER_PATH'] = CHROME
    # Avoid another project's .env, legacy cookies or videos being picked up.
    os.chdir(DATA)
    install_caption_guard()
    from autotok.cli import main as autotok_main
    return autotok_main(argv)


if __name__ == '__main__':
    raise SystemExit(main())
