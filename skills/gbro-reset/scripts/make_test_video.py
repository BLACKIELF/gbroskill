#!/usr/bin/env python3
"""GBro 验收测试片：任何人拿到本包，一条命令确认版式、背景、字幕、配音、BGM、落版是否符合强制规范。
  python3 make_test_video.py [--out 目录] [--kind tutorial|news|skill|reset] [--no-voice]
产出：GBro-验收测试片-*.mp4、记录/首帧|中段帧|落版帧|末帧.png、记录/出片回执.json
"""
from pathlib import Path
import argparse, json, subprocess, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gbro_video as G

BODY = [
    '这条测试片用来核对 GBro 的固定版式：连续红蓝球面呼吸光底、直接文字字幕，不加任何方框。',
    '字幕按语义断行，句号不会跑到下一行开头。',
    '配音是固定的 AiGoodBro 品牌声音，末句必须完整，不能吞字。',
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(Path.home() / 'Movies/AiGoodBro-GBro/验收测试片'))
    ap.add_argument('--kind', default='tutorial', choices=list(G.ENDCARDS))
    ap.add_argument('--lang', default='zh', choices=['zh', 'en'])
    ap.add_argument('--bgm', default='tech'); ap.add_argument('--no-voice', action='store_true')
    ap.add_argument('--voice-file')
    a = ap.parse_args()
    out = Path(a.out).expanduser() / f'{G.ENDCARDS[a.kind][0 if a.lang == "zh" else 1][:0]}测试片-{a.kind}'
    out.mkdir(parents=True, exist_ok=True); work = out / '记录'; work.mkdir(exist_ok=True)
    cards, cta = BODY, G.ENDCARDS[a.kind][0 if a.lang == 'zh' else 1]
    if len(G.wrap_lines(cards[0], 19)) > 4:
        cards[0] = '这条测试片核对 GBro 固定版式：连续呼吸光底、直接文字字幕、不加方框。'
    full = '\n'.join(cards + [cta])
    voice = Path(a.voice_file) if a.voice_file else out / '口播-G4-测试片.wav'
    if a.no_voice:
        voice = None; secs = 11.0
    elif voice.exists():
        secs = G.wav_seconds(voice)
    else:
        print('生成 G4 测试配音…', flush=True); secs = G.tts(full, voice)
    cta_at = G.cta_start(secs, cta, full); dur = round(secs + 0.7, 3)
    total = sum(len(c) for c in cards)
    t, rows = 0.0, []
    for c in cards:
        d = cta_at * len(c) / total; rows.append((c, t, t + d)); t += d
    bg = G.bg_still(work)
    from playwright.sync_api import sync_playwright
    shots = []
    with sync_playwright() as p:
        chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        br = p.chromium.launch(headless=True, args=['--allow-file-access-from-files'],
                               **({'executable_path': chrome} if Path(chrome).exists() else {}))
        for i, (c, s, e) in enumerate(rows, 1):
            png = work / f'card-{i:02d}.png'
            G.shoot(G.card_html(c, bg.as_uri(), None, f'{i:02d} / {len(rows):02d}', a.kind), png, work, transparent=True, browser=br)
            shots.append((png, s, e))
        end = work / 'endcard.png'
        G.shoot(G.endcard_html(a.kind, a.lang), end, work, transparent=True, browser=br)
        br.close()
    music = G.music(work, dur, a.bgm, voice_gain=0.16 if voice else 1.0)
    mp4 = out / f'GBro-验收测试片-{a.kind}{"" if voice else "-待配音"}.mp4'
    G.compose(shots, end, voice, music, mp4, dur, cta_at)
    for tm, n in [(0.2, '首帧'), (cta_at * .5, '中段帧'), (cta_at + 0.4, '落版帧'), (dur - .25, '末帧')]:
        subprocess.run([G.ffmpeg(), '-v', 'error', '-y', '-ss', f'{max(0,tm):.2f}', '-i', str(mp4),
                        '-frames:v', '1', str(work / f'{n}.png')], check=True)
    m = work / '出片回执.json'
    m.write_text(json.dumps({'video': str(mp4), 'kind': a.kind, 'voice': str(voice) if voice else None,
                             'voice_seconds': secs, 'duration': dur, 'cta_at': round(cta_at, 3), 'bgm': a.bgm,
                             'cards': [{'text': c, 'start': round(s, 3), 'end': round(e, 3)} for c, s, e in rows],
                             'endcard_text': cta, 'sha256': G.sha256(mp4)}, ensure_ascii=False, indent=2))
    print(json.dumps({'video': str(mp4), 'duration': dur, 'cta_at': round(cta_at, 3), 'manifest': str(m)}, ensure_ascii=False, indent=2))
    print(f'\n自动验收：python3 {Path(__file__).parent/"check_video.py"} "{mp4}"'
          + (f' --voice "{voice}"' if voice else '') + f' --manifest "{m}"')


if __name__ == '__main__':
    main()
