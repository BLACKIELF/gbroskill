#!/usr/bin/env python3
"""GBro 通用配音视频模板（非重置类用；重置类用 make_reset.py）。

口播稿 = 若干段，每段一张字幕卡；最后一段必须是落版主句（按 --kind 校验）。
默认：1080×1920、连续红蓝球面背景、直接文字字幕（无方框）、G4 配音、tech BGM、全画布落版卡。

  python3 make_narrated.py --script 稿.txt --kind tutorial --out ~/Movies/GBro/教程-1104v1
可选：--image-dir 图目录（01.png 起按卡序配图）  --voice-file 已有 G4 干声
      --bgm tech|lofi|pulse|ambient|bright  --timeline 精确时间轴.json  --no-voice
"""
from pathlib import Path
import argparse, json, math, re, shutil, subprocess, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gbro_video as G


def load_cards(path):
    text = Path(path).read_text(encoding='utf-8').strip()
    paras = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    if len(paras) < 2:
        sys.exit('口播稿至少要有 2 段：正文卡 + 落版主句（每段之间空一行）')
    cards, cta = paras[:-1], paras[-1]
    if len(cards) > 12:
        sys.exit(f'字幕卡 {len(cards)} 张，超过 12 张，请精简（GBro 视频要短）')
    for c in cards:
        G.wrap_lines(c, 19)
    return cards, cta


def weigh(text):
    return len(re.sub(r'[^\w一-鿿]', '', text)) or 1


def timeline_for(cards, cta, voice_seconds):
    total = sum(map(weigh, cards)) + weigh(cta)
    t, out = 0.0, []
    for c in cards:
        d = voice_seconds * weigh(c) / total
        out.append((c, t, t + d)); t += d
    return out, t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--script', required=True)
    ap.add_argument('--kind', choices=list(G.ENDCARDS), default='tutorial')
    ap.add_argument('--out', required=True)
    ap.add_argument('--image-dir'); ap.add_argument('--voice-file')
    ap.add_argument('--bgm', default='tech'); ap.add_argument('--timeline')
    ap.add_argument('--lang', default='zh', choices=['zh', 'en'])
    ap.add_argument('--no-voice', action='store_true'); ap.add_argument('--tag', default=None)
    a = ap.parse_args()
    out = Path(a.out).expanduser(); out.mkdir(parents=True, exist_ok=True)
    tag = a.tag or out.name
    work = out / '记录'; work.mkdir(exist_ok=True)
    cards, cta = load_cards(a.script)
    if cta not in G.ENDCARDS[a.kind][0 if a.lang == 'zh' else 1]:
        sys.exit(f'落版主句必须是「{G.ENDCARDS[a.kind][0 if a.lang == "zh" else 1]}」，当前是「{cta}」')
    full = '\n'.join(cards + [cta])
    voice = Path(a.voice_file) if a.voice_file else out / f'口播-G4-{tag}.wav'
    if a.no_voice:
        voice = None; secs = max(9.0, 1.6 * len(cards) + 3)
    else:
        if not voice.exists():
            print('生成 G4 配音…', flush=True)
            secs = G.tts(full, voice)
        else:
            secs = G.wav_seconds(voice)
    if a.timeline:
        tl = json.loads(Path(a.timeline).read_text())
        rows = [(c, float(r['start']), float(r['end'])) for c, r in zip(cards, tl)]
        cta_at = float(tl[-1].get('cta_at', rows[-1][2])) if isinstance(tl, list) else 0.0
    else:
        rows, cta_at = timeline_for(cards, cta, secs)
    cta_at = G.cta_start(secs, cta, full) if not a.timeline else cta_at
    rows = [(c, s, min(e, cta_at)) for c, s, e in rows]
    dur = round(secs + 0.7, 3)
    bg = G.bg_still(work)
    imgs = sorted(Path(a.image_dir).glob('*')) if a.image_dir else []
    shots = []
    for i, (c, s, e) in enumerate(rows, 1):
        img = imgs[i - 1].as_uri() if i - 1 < len(imgs) else None
        png = work / f'card-{i:02d}.png'
        G.shoot(G.card_html(c, bg.as_uri(), img, f'{i:02d} / {len(rows):02d}', a.kind), png, work, transparent=True)
        shots.append((png, s, e))
    end = work / 'endcard.png'
    G.shoot(G.endcard_html(a.kind, a.lang), end, work, transparent=True)
    music = G.music(work, dur, a.bgm, voice_gain=0.16 if voice else 1.0)
    mp4 = out / f'GBro-{a.kind}-竖版{"" if voice else "-待配音"}-{tag}.mp4'
    G.compose(shots, end, voice, music, mp4, dur, cta_at)
    for t, n in [(0.2, '首帧'), (max(0, cta_at + 0.4), '落版帧'), (dur - 0.25, '末帧')]:
        subprocess.run([G.ffmpeg(), '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', str(mp4),
                        '-frames:v', '1', str(work / f'{n}.png')], check=True)
    manifest = {'video': str(mp4), 'canonical': [G.W, G.H], 'kind': a.kind, 'bgm': a.bgm,
                'voice': str(voice) if voice else None, 'voice_seconds': secs, 'duration': dur,
                'cta_at': round(cta_at, 3), 'cards': [{'text': c, 'start': round(s, 3), 'end': round(e, 3)} for c, s, e in rows],
                'endcard_text': G.ENDCARDS[a.kind][0 if a.lang == 'zh' else 1],
                'sha256': G.sha256(mp4)}
    (work / '出片回执.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
