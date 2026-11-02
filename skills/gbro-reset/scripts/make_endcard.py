#!/usr/bin/env python3
"""GBro 视频落版卡（四类固定文案），与重置模板同一视觉。
python3 make_endcard.py --kind skill|tutorial|reset|news [--lang zh|en] [--out 目录]
输出：落版透明层 PNG（叠到成片最后 2.8 秒）+ 带背景静帧 PNG；并打印口播末句。
口播末句要写进完整口播稿、整段一次生成 G4 配音，不能单独生成后拼接。"""
from pathlib import Path
from tempfile import TemporaryDirectory
import argparse, shutil, subprocess, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_reset as R


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--kind', choices=list(R.ENDCARDS), required=True)
    ap.add_argument('--lang', choices=['zh', 'en'], default='zh')
    ap.add_argument('--out', default=str(Path.home() / 'Movies/AiGoodBro-GBro/落版卡'))
    a = ap.parse_args(); out = Path(a.out)
    volume = Path('/Volumes/4t')
    if out.resolve().is_relative_to(volume.resolve()):
        if not volume.is_mount() or shutil.disk_usage(volume).free < 20 * 1024**3:
            sys.exit('4T 未挂载或可用空间不足 20 GiB，不能向指定的 4T 目录写入')
    out.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix='.endcard-', dir=out) as temporary:
        work = Path(temporary); bg = work / 'bg.png'
        ff = R.ffmpeg()
        subprocess.run([ff, '-v', 'error', '-y', '-i', str(R.A / 'bg-loop-1080x1920.mp4'), '-frames:v', '1', str(bg)], check=True)
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
            br = p.chromium.launch(headless=True, args=['--allow-file-access-from-files'],
                                   **({'executable_path': chrome} if Path(chrome).exists() else {}))
            for name, bg_uri, transparent in [(f'落版层-{a.kind}-{a.lang}.png', None, True), (f'落版静帧-{a.kind}-{a.lang}.png', bg.as_uri(), False)]:
                R.shoot(R.page_html({}, a.lang, 1080, 1920, bg_uri, end=True, kind=a.kind), out / name, 1080, 1920, transparent, br, work)
            br.close()
    print('口播末句：', R.ENDCARDS[a.kind][0 if a.lang == 'zh' else 1])
    print('画面次行：', '（重置类不加）' if a.kind == 'reset' else R.SECOND[0 if a.lang == 'zh' else 1] + '（只显示，不念）')
    print('OUT', out)


if __name__ == '__main__':
    main()
