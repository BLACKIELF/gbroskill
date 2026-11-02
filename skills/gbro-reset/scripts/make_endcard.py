#!/usr/bin/env python3
"""GBro 视频落版卡（四类固定文案），与重置模板同一视觉。
python3 make_endcard.py --kind skill|tutorial|reset|news [--lang zh|en] [--out 目录]
输出：落版透明层 PNG（叠到成片最后 2.8 秒）+ 带背景静帧 PNG；并打印口播末句。
口播末句要写进完整口播稿、整段一次生成 G4 配音，不能单独生成后拼接。"""
from pathlib import Path
import argparse, subprocess, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_reset as R


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--kind', choices=list(R.ENDCARDS), required=True)
    ap.add_argument('--lang', choices=['zh', 'en'], default='zh')
    ap.add_argument('--out', default=str(Path.home() / 'Movies/AiGoodBro-GBro/落版卡'))
    a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    ff = R.ffmpeg(); bg = out / '.bg.png'
    subprocess.run([ff, '-v', 'error', '-y', '-i', str(R.A / 'bg-loop-1080x1920.mp4'), '-frames:v', '1', str(bg)], check=True)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        br = p.chromium.launch(headless=True, args=['--allow-file-access-from-files'],
                               **({'executable_path': chrome} if Path(chrome).exists() else {}))
        for name, bg_uri, transparent in [(f'落版层-{a.kind}-{a.lang}.png', None, True), (f'落版静帧-{a.kind}-{a.lang}.png', bg.as_uri(), False)]:
            R.shoot(R.page_html({}, a.lang, 1080, 1920, bg_uri, end=True, kind=a.kind), out / name, 1080, 1920, transparent, br, out)
        br.close()
    for f in out.glob('*.html'): f.unlink()
    bg.unlink()
    print('口播末句：', R.ENDCARDS[a.kind][0 if a.lang == 'zh' else 1])
    print('画面次行：', '（重置类不加）' if a.kind == 'reset' else R.SECOND[0 if a.lang == 'zh' else 1] + '（只显示，不念）')
    print('OUT', out)


if __name__ == '__main__':
    main()
