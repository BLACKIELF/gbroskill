#!/usr/bin/env python3
"""GBro 视频自动验收：逐条检查强制规范，输出通过/失败清单。
  python3 check_video.py 视频.mp4 [--voice 干声.wav] [--kind news] [--spec-only]
任一硬项失败返回 1。ASR、哈希、解码成功只能证明对应层面，主观听感仍需用户试听。
"""
from pathlib import Path
import argparse, hashlib, json, re, subprocess, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gbro_video as G


def probe(p):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(p)]))


def frames(p, ss=None, n=1, scale='320:-1'):
    cmd = [G.ffmpeg(), '-v', 'error', '-y', '-i', str(p)]
    if ss is not None: cmd[4:4] = ['-ss', f'{ss:.3f}']
    cmd += ['-frames:v', str(n), '-vf', f'scale={scale}', '-f', 'rawvideo', '-pix_fmt', 'gray', '-']
    return subprocess.check_output(cmd)


def audio_pcm(p, ss=None, t=None):
    cmd = [G.ffmpeg(), '-v', 'error', '-i', str(p)]
    if ss is not None: cmd += ['-ss', f'{ss:.3f}']
    if t is not None: cmd += ['-t', f'{t:.3f}']
    cmd += ['-ac', '1', '-ar', '48000', '-f', 's16le', '-']
    return subprocess.check_output(cmd)


def rms(buf):
    import array, math
    a = array.array('h'); a.frombytes(buf[:len(buf) // 2 * 2])
    if not a: return 0.0
    return math.sqrt(sum(x * x for x in a) / len(a)) / 32768


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('video'); ap.add_argument('--voice'); ap.add_argument('--kind', default='news')
    ap.add_argument('--spec-only', action='store_true'); ap.add_argument('--manifest')
    ap.add_argument('--frame-review', help='最终视频红绿多色呼吸包框的实际目视回执 JSON')
    a = ap.parse_args()
    checks, hard_fail = [], False

    def add(name, ok, detail, hard=True):
        nonlocal hard_fail
        checks.append({'check': name, 'pass': bool(ok), 'hard': hard, 'detail': detail})
        if hard and not ok: hard_fail = True

    v = Path(a.video).expanduser()
    add('文件存在', v.is_file(), str(v))
    if not v.is_file():
        print(json.dumps({'pass': False, 'checks': checks}, ensure_ascii=False, indent=2)); sys.exit(1)
    review = {}
    try:
        if a.frame_review:
            review = json.loads(Path(a.frame_review).expanduser().read_text())
    except (OSError, ValueError):
        pass
    if not isinstance(review, dict):
        review = {}
    digest = hashlib.sha256()
    with v.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            digest.update(block)
    expected_hash = digest.hexdigest()
    evidence = review.get('evidence_frames', [])
    review_ok = (review.get('video_sha256') == expected_hash
                 and all(review.get(k) is True for k in ('red_green_visible', 'motion_visible', 'seams_checked'))
                 and isinstance(evidence, list) and len(evidence) >= 4
                 and all(isinstance(x, str) and Path(x).is_absolute() and Path(x).is_file() for x in evidence))
    add('红绿多色呼吸包框的最终成片目视回执', review_ok,
        '已绑定本次视频及实际对比图；视觉结论须由检查者负责' if review_ok else '缺有效回执；背景运动和解码成功不能代替包框验收')
    info = probe(v); vs = [s for s in info['streams'] if s['codec_type'] == 'video'][0]
    aus = [s for s in info['streams'] if s['codec_type'] == 'audio']
    dur = float(info['format']['duration'])
    add('画幅 9:16 且 1080×1920', (vs['width'], vs['height']) == (1080, 1920) and abs(vs['width'] / vs['height'] - 9 / 16) < 1e-6,
        f"{vs['width']}×{vs['height']}")
    add('有音轨', bool(aus), aus[0]['codec_name'] if aus else '无')
    # 背景整片连续：抽 5 个时间点，画面必须有变化（不是静止幻灯片/纯黑）
    samples = [frames(v, ss=t, scale='160:-1') for t in (0.3, dur * .25, dur * .5, dur * .75, max(0, dur - .4))]
    diffs = [sum(abs(x - y) for x, y in zip(samples[i], samples[i + 1])) / max(1, len(samples[i])) for i in range(len(samples) - 1)]
    add('背景整片有动态（非黑底静止）', all(d > 0.4 for d in diffs), [round(d, 2) for d in diffs])
    add('画面非纯黑', any(sum(s) / len(s) > 4 for s in samples), [round(sum(s) / len(s), 1) for s in samples])
    if aus:
        head = rms(audio_pcm(v, t=min(1.0, dur / 4)))
        tail = rms(audio_pcm(v, ss=max(0, dur - 0.5)))
        add('开头有声音', head > 0.002, round(head, 4))
        add('结尾没有硬截断（末 0.5s 仍有声或自然淡出）', tail > 0.0008, round(tail, 4))
        # BGM 存在：整片中间某段（若无人声段）应有持续能量
        mid = rms(audio_pcm(v, ss=dur * 0.6, t=0.5))
        add('中段有混音能量（口播或 BGM）', mid > 0.002, round(mid, 4), hard=False)
    if a.voice:
        vp = Path(a.voice).expanduser()
        vs_ = G.wav_seconds(vp)
        add('成片时长 ≥ 配音时长 + 0.5s（留足尾音）', dur >= vs_ + 0.5, f'视频 {dur:.2f}s / 配音 {vs_:.2f}s')
        j = vp.with_suffix('.json')
        if j.exists():
            meta = json.loads(j.read_text())
            if meta.get('expected_samples'):
                add('配音未被解码截断', meta['samples'] == meta['expected_samples'],
                    f"{meta['samples']} vs {meta['expected_samples']}（帧×1920＋分段间隔）")
            elif meta.get('samples') and meta.get('token_counts'):
                gaps = max(0, int(meta.get('chunk_count') or 1) - 1) * round(24000 * 0.18)
                add('配音未被解码截断', meta['samples'] == sum(meta['token_counts']) * 1920 + gaps,
                    f"{meta['samples']} vs {sum(meta['token_counts'])*1920+gaps}")
            else:
                add('配音解码长度可核', True, '该干声未带帧数记录，需人工听末字', hard=False)
    # 落版卡：末尾画面应与中段不同，且落版期间有画面（非全黑）
    end = frames(v, ss=max(0, dur - 0.25), scale='160:-1')
    add('落版卡可见', sum(end) / len(end) > 4, round(sum(end) / len(end), 1))
    mf = Path(a.manifest) if a.manifest else None
    if mf and mf.is_file():
        m = json.loads(mf.read_text())
        add('分镜卡 ≤12 张', len(m.get('cards', [])) <= 12, len(m.get('cards', [])))
        add('BGM 已入混音', bool(m.get('bgm')), str(m.get('bgm')))
    result = {'video': str(v), 'duration': round(dur, 3), 'pass': not hard_fail,
              'note': '技术层面通过 ≠ 用户已接受；音色、版式与手机可读性仍要目视与试听', 'checks': checks}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if not hard_fail else 1)


if __name__ == '__main__':
    main()
