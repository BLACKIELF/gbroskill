#!/usr/bin/env python3
"""生成 AiGoodBro 原创 BGM 库（纯代码合成，无第三方录音）。
python3 make_bgm.py [--seconds 60] [--out ../assets/bgm]
每条为 60 秒立体声 m4a，首尾淡入淡出，可任意截取。"""
from pathlib import Path
import argparse, shutil, subprocess, wave
import numpy as np

SR = 44100


def note(m):  # MIDI → Hz
    return 440 * 2 ** ((m - 69) / 12)


def env(n, a=.01, d=6.0):
    x = np.arange(n) / SR
    return np.minimum(1, x / a) * np.exp(-x * d)


def tone(f, n, kind='sine'):
    t = np.arange(n) / SR; p = 2 * np.pi * f * t
    if kind == 'saw':
        return sum(np.sin(p * k) / k for k in range(1, 7)) * .6
    if kind == 'tri':
        return sum(((-1) ** i) * np.sin(p * (2 * i + 1)) / (2 * i + 1) ** 2 for i in range(4)) * .8
    if kind == 'pluck':
        return (np.sin(p) + .5 * np.sin(2 * p) + .25 * np.sin(3 * p))
    return np.sin(p)


def place(buf, sig, t0, pan=0.0):
    k = int(t0 * SR)
    if k >= len(buf): return
    sig = sig[:len(buf) - k]
    buf[k:k + len(sig), 0] += sig * (1 - pan) / 2 * 2 ** .5
    buf[k:k + len(sig), 1] += sig * (1 + pan) / 2 * 2 ** .5


def kick(n=int(.35 * SR)):
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * (45 + 90 * np.exp(-t * 30)) * t) * np.exp(-t * 9)


def hat(rng, n=int(.05 * SR)):
    return rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 80) * .25


def snare(rng, n=int(.2 * SR)):
    t = np.arange(n) / SR
    return (rng.standard_normal(n) * .6 + np.sin(2 * np.pi * 190 * t)) * np.exp(-t * 18)


PROG = {  # 四和弦循环（MIDI 根音 + 和弦音）
    'minor': [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]],   # Am F C G
    'major': [[48, 52, 55], [55, 59, 62], [57, 60, 64], [53, 57, 60]],   # C G Am F
    'dream': [[50, 53, 57, 60], [55, 58, 62, 65], [48, 52, 55, 59], [53, 57, 60, 64]],
}


def track(style, secs, seed=7):
    rng = np.random.default_rng(seed)
    n = int(secs * SR); buf = np.zeros((n, 2))
    cfg = {
        'pulse':  dict(bpm=120, prog='minor', pad=.05, arp='tri', arpv=.08, drums='light'),
        'lofi':   dict(bpm=84,  prog='dream', pad=.07, arp='pluck', arpv=.05, drums='lofi'),
        'tech':   dict(bpm=128, prog='minor', pad=.04, arp='saw', arpv=.05, drums='four'),
        'ambient':dict(bpm=70,  prog='dream', pad=.10, arp='sine', arpv=.04, drums=None),
        'bright': dict(bpm=110, prog='major', pad=.05, arp='pluck', arpv=.07, drums='four'),
    }[style]
    beat = 60 / cfg['bpm']; bar = beat * 4; chords = PROG[cfg['prog']]
    for b in range(int(secs / bar) + 1):
        ch = chords[b % 4]; t0 = b * bar
        # pad：整小节长音，慢起慢收
        ln = int(bar * SR * 1.05)
        e = np.minimum(1, np.arange(ln) / SR / .4) * np.clip((bar * 1.05 - np.arange(ln) / SR) / .5, 0, 1)
        for i, m in enumerate(ch):
            place(buf, tone(note(m), ln, 'tri') * e * cfg['pad'], t0, pan=(i - 1) * .4)
        # bass
        bl = int(beat * 2 * SR)
        for k in (0, 2):
            place(buf, tone(note(ch[0] - 12), bl, 'sine') * env(bl, .01, 2.5) * .22, t0 + k * beat)
        # arp：十六分或八分
        step = beat / (4 if style in ('tech', 'pulse') else 2)
        seq = (ch + [ch[0] + 12]) * 4
        for j in range(int(bar / step)):
            m = seq[j % len(seq)] + 12; al = int(step * SR * 1.6)
            place(buf, tone(note(m), al, cfg['arp']) * env(al, .005, 9) * cfg['arpv'], t0 + j * step, pan=.5 * np.sin(j))
        # drums
        dr = cfg['drums']
        for q in range(4):
            tq = t0 + q * beat
            if dr == 'four':
                place(buf, kick() * .35, tq)
                place(buf, hat(rng), tq + beat / 2, pan=.3)
                if q in (1, 3): place(buf, snare(rng) * .12, tq)
            elif dr == 'light':
                if q in (0, 2): place(buf, kick() * .25, tq)
                place(buf, hat(rng) * .6, tq + beat / 2, pan=-.3)
            elif dr == 'lofi':
                if q in (0, 2): place(buf, kick() * .3, tq + (.03 if q == 2 else 0))
                if q in (1, 3): place(buf, snare(rng) * .09, tq)
                place(buf, hat(rng) * .4, tq + beat * .55, pan=.2)
    if style == 'lofi':  # 黑胶底噪
        buf += rng.standard_normal((n, 2)) * .004
    # 简单混响：多抽头延迟
    out = buf.copy()
    for d, g in [(.031, .25), (.047, .2), (.071, .15), (.113, .1)]:
        k = int(d * SR); out[k:, 0] += buf[:-k, 1] * g; out[k:, 1] += buf[:-k, 0] * g
    t = np.arange(n) / SR
    out *= (np.minimum(1, t / 1.5) * np.clip((secs - t) / 3, 0, 1))[:, None]
    out /= max(1e-9, np.abs(out).max()) / .7
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--seconds', type=float, default=60)
    ap.add_argument('--out', default=str(Path(__file__).resolve().parent.parent / 'assets/bgm'))
    a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    ff = '/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg' if Path('/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg').exists() else shutil.which('ffmpeg')
    for i, s in enumerate(['pulse', 'lofi', 'tech', 'ambient', 'bright']):
        x = track(s, a.seconds, seed=11 + i); tmp = out / f'{s}.wav'
        with wave.open(str(tmp), 'wb') as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype('<i2').tobytes())
        subprocess.run([ff, '-v', 'error', '-y', '-i', str(tmp), '-c:a', 'aac', '-b:a', '128k', str(out / f'{s}.m4a')], check=True)
        tmp.unlink(); print('BGM', out / f'{s}.m4a')


if __name__ == '__main__':
    main()
