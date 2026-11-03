#!/usr/bin/env python3
"""GBro 视频公共版式库：卡片、字幕断行、落版卡、连续背景、配音、BGM。
被 make_narrated.py（通用模板）和 make_test_video.py（验收示例）共用。

硬规则（见 references/GBro视频强制规范.md）：
- 画布永远 1080×1920（9:16）。
- 字幕是直接文字，不加方框、圆角底板或半透明卡片；文案变动由调用方决定。
- 断行按语义，闭合标点 ，。！？；：、）》】」』”’ 不能出现在行首；断了就报错，不靠缩字号硬塞。
- 落版卡全画布，不加窗口框、不重复品牌标题；主句=口播末句，非重置类加次行，主句只出现一次。
"""
from pathlib import Path
import hashlib, json, re, shutil, subprocess, sys, wave

SK = Path(__file__).resolve().parent.parent
A = SK / 'assets'
VOICE = A / 'voice' if (A / 'voice/reference.wav').exists() else SK.parent / 'gbro-social-workflow/assets/voice/aigoodbro-g4'
TTS = 'http://127.0.0.1:7862'
W, H = 1080, 1920
NO_LINE_START = '，。！？；：、）》】」』”’,.!?;:%'
BRAND = '<span style="color:#9BD9F8">Ai</span><span style="color:#fff">Good</span><span style="color:#FF6B62">Bro</span>'
ENDCARDS = {
    'skill':    ('关注 AiGoodBro，获取更多免费 Skill！', 'Follow AiGoodBro for more free Skills!'),
    'tutorial': ('关注 AiGoodBro，获取更多教程！', 'Follow AiGoodBro for more tutorials!'),
    'reset':    ('关注 AiGoodBro，第一时间获取重置消息！', 'Follow AiGoodBro for reset news first!'),
    'news':     ('关注 AiGoodBro，第一时间获取Ai资讯消息！', 'Follow AiGoodBro for the latest AI news!'),
}
SECOND = ('第一时间获取重置消息！', 'Get reset news first!')
KIND_KICKER = {'skill': 'GBro · SKILL', 'tutorial': 'GBro · 教程', 'news': 'GBro · 资讯', 'reset': 'CODEX 重置消息'}


def ffmpeg():
    for p in ['/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg', shutil.which('ffmpeg')]:
        if p and Path(p).exists(): return p
    sys.exit('缺 ffmpeg')


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ---------- 字体与断行 ----------
def font_family():
    return '"PingFang SC","Noto Sans CJK SC","Source Han Sans SC",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif'


def _w(tok):
    """宽度（em）：中文字≈1，西文字符≈0.55。"""
    return sum(1.0 if ord(c) > 0x2E80 else 0.55 for c in tok)


def wrap_lines(text, max_units, brand_token='\u0001'):
    """语义断行：先按标点切成小句，整句尽量不拆；长句才在词边界拆分。
    闭合标点永不行首；断行后文字（含品牌占位符）逐字不变。"""
    sentinel = '\x00'
    body = text.replace(brand_token, sentinel)
    clauses, cur = [], ''
    for ch in body:
        cur += ch
        if ch in '，。！？；：、!?;:,':
            clauses.append(cur); cur = ''
    if cur.strip(): clauses.append(cur)

    def toks(cl):
        return re.findall(r'\x00|[A-Za-z0-9]+(?:[.\-/][A-Za-z0-9]+)*|\s+|.', cl)

    def split_long(cl):
        parts, line, size = [], '', 0.0
        for t in toks(cl):
            wt = 0.0 if t == sentinel else _w(t)
            if line and size + wt > max_units:
                parts.append(line); line, size = '', 0.0
            if not line and t in NO_LINE_START and parts:
                parts[-1] += t; continue
            line += t; size += wt
        if line: parts.append(line)
        return parts

    lines, line, size = [], '', 0.0
    for cl in clauses:
        for t in toks(cl):
            wt = 0.0 if t == sentinel else _w(t)
            if line and size + wt > max_units:
                lines.append(line); line, size = '', 0.0
            if not line and t in NO_LINE_START and lines:
                lines[-1] += t; continue
            line += t; size += wt
    if line: lines.append(line)
    lines = [l.rstrip() for l in lines if l.strip()]
    assert lines, '空字幕'
    bad = [l for l in lines if l[0] in NO_LINE_START]
    assert not bad, f'闭合标点落到行首：{bad}'
    restored = [l.replace(sentinel, brand_token) for l in lines]
    assert ''.join(''.join(restored).split()) == ''.join(text.split()), '断行改变了文字'
    return restored


# ---------- 页面 ----------
def base_css(bg_uri=None, extra=''):
    bg = f'linear-gradient(#0003,#0003),url("{bg_uri}") center/cover' if bg_uri else 'transparent'
    return f'''html,body{{margin:0;width:{W}px;height:{H}px;overflow:hidden;background:{bg};color:#fff;
text-align:center;font-family:{",".join(font_family())};font-synthesis:none}}*{{box-sizing:border-box}}
.brand{{display:flex;align-items:center;justify-content:center;gap:18px;font-size:54px;font-weight:600}}
.brand img{{width:84px;height:84px;border-radius:50%}}
.kicker{{font-size:48px;font-weight:600;letter-spacing:.06em;color:#C9CFE8}}
.caption{{position:absolute;left:76px;width:928px;bottom:150px;font-size:46px;line-height:1.34;font-weight:500;
color:#fff;text-align:left;text-shadow:0 2px 18px rgba(0,0,0,.55)}}
.caption .hi{{color:#9BD9F8;font-weight:600}}
.pic{{position:absolute;left:86px;top:250px;width:908px;display:flex;align-items:center;justify-content:center}}
.pic img{{max-width:908px;max-height:1000px;object-fit:contain;border-radius:28px;
box-shadow:0 24px 60px rgba(0,0,0,.55)}}
.page{{position:absolute;right:84px;bottom:84px;font-size:28px;color:#B2C6E0}}
.endcard{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:42px;padding:0 72px}}
.endcard .main{{font-size:84px;line-height:1.35;font-weight:600;white-space:nowrap}}
.endcard .second{{font-size:56px;font-weight:600;color:#E6E8F0;white-space:nowrap}}
.endcard img.av{{width:220px;height:220px;border-radius:50%}}{extra}'''


def card_html(caption, bg_uri, image_uri=None, page=None, kind='news', hi=None):
    cap = caption.replace('AiGoodBro', '\u0001')

    pic = f'<div class="pic"><img src="{image_uri}"></div>' if image_uri else ''
    pg = f'<div class="page">{page}</div>' if page else ''
    return ('<!doctype html><meta charset="utf-8"><style>' + base_css(bg_uri) + '</style>'
            f'<div class="brand"><img src="{(A/"avatar.png").as_uri()}"><div>{BRAND}</div></div>'
            f'<div class="kicker">{KIND_KICKER.get(kind, "GBro")}</div>{pic}'
            f'<div class="caption">{"<br>".join(wrap_lines(cap, 19)).replace(chr(1), BRAND)}</div>{pg}')


def endcard_main(kind='news', lang='zh'):
    main = ENDCARDS[kind][0 if lang == 'zh' else 1].replace('AiGoodBro', BRAND)
    return main.replace('，', '<br>', 1) if lang == 'zh' else main.replace(f'{BRAND} ', f'{BRAND}<br>', 1)


def endcard_html(kind='news', lang='zh', bg_uri=None):
    second = '' if kind == 'reset' else f'<div class="second">{SECOND[0 if lang == "zh" else 1]}</div>'
    return ('<!doctype html><meta charset="utf-8"><style>' + base_css(bg_uri) + '</style>'
            f'<div class="endcard"><img class="av" src="{(A/"avatar.png").as_uri()}">'
            f'<div class="main">{endcard_main(kind, lang)}</div>{second}</div>')


def shoot(html_text, path, work, transparent=False, w=W, h=H, browser=None):
    from playwright.sync_api import sync_playwright
    own = browser is None
    if own:
        chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        pw = sync_playwright().start()
        browser = pw.chromium.launch(headless=True, args=['--allow-file-access-from-files'],
                                     **({'executable_path': chrome} if Path(chrome).exists() else {}))
    try:
        src = work / (Path(path).stem + '.html'); src.write_text(html_text)
        pg = browser.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        pg.goto(src.as_uri()); pg.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth>0)')
        pg.evaluate('''() => {
          for (const s of ['.endcard .main', '.endcard .second', '.caption']) {
            const el = document.querySelector(s); if (!el) continue;
            const limit = el.clientWidth || (document.documentElement.clientWidth - 144);
            let guard = 0;
            while (el.scrollWidth > limit + 1 && parseFloat(getComputedStyle(el).fontSize) > 44 && guard++ < 40)
              el.style.fontSize = (parseFloat(getComputedStyle(el).fontSize) - 2) + 'px';
            el.dataset.overflow = el.scrollWidth > limit + 1 ? '1' : '0';
          }
          document.querySelectorAll('.caption').forEach(el => {
            if (el.getBoundingClientRect().bottom > innerHeight - 40) throw new Error('字幕超出安全区');
          });
        }''')
        pg.screenshot(path=str(path), omit_background=transparent); pg.close()
    finally:
        if own:
            browser.close()


def bg_still(work):
    p = work / 'bg.png'
    subprocess.run([ffmpeg(), '-v', 'error', '-y', '-i', str(A / 'bg-loop-1080x1920.mp4'), '-frames:v', '1', str(p)], check=True)
    return p


# ---------- 配音 ----------
def tts(text, dest, require_free_gib=20):
    from urllib.request import Request, urlopen
    v4 = Path('/Volumes/4t')
    if not v4.is_mount() or shutil.disk_usage(v4).free < require_free_gib * 1024**3:
        raise RuntimeError('4T 未挂载或剩余不足，配音工作台会写 4T，跳过自动配音')
    prof = json.loads((VOICE / 'profile.json').read_text()); ref = VOICE / 'reference.wav'
    assert sha256(ref) == prof['reference_sha256'], 'G4 参考音被改动，停止'
    with urlopen(TTS + '/health', timeout=8) as f: h = json.load(f)
    assert h.get('service') == 'breeze-workbench' and not h.get('busy'), f'配音服务未就绪：{h}'
    import uuid
    fields = {'text': text, 'instruction': '', 'ref_text': prof['reference_text'], 'seed': '1447',
              'cfg_scale': '4', 'pronunciation': 'off', 'voice_id': ''}
    b = 'gbro' + uuid.uuid4().hex; body = b''
    for k, v in fields.items():
        body += f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    body += (f'--{b}\r\nContent-Disposition: form-data; name="ref_audio"; filename="reference.wav"\r\n'
             'Content-Type: audio/wav\r\n\r\n').encode() + ref.read_bytes() + f'\r\n--{b}--\r\n'.encode()
    req = Request(TTS + '/v1/audio/speech', data=body, headers={'Content-Type': f'multipart/form-data; boundary={b}'})
    with urlopen(req, timeout=600) as f:
        oid = f.headers.get('X-Output-Id'); data = f.read()
    if data[:4] == b'RIFF':
        Path(dest).write_bytes(data); meta = {}
    else:
        src = v4 / 'BreezeTTS2/workbench/outputs' / f'{oid}.wav'
        assert oid and src.exists(), f'配音返回异常：{data[:200]!r}'
        meta = json.loads(src.with_suffix('.json').read_text())
        shutil.copy2(src, dest)
    n = wave.open(str(dest)).getnframes()
    frames = sum(meta.get('token_counts') or [])
    chunks = int(meta.get('chunk_count') or 0)
    expected = frames * 1920 + max(0, chunks - 1) * round(24000 * 0.18)  # 工作台分段间隔
    if frames and n != expected:
        raise RuntimeError(f'配音长度异常：{n} 样本，应为 {expected}（帧 {frames}×1920 + 段间隔）；疑似断尾，停止')
    Path(dest).with_suffix('.json').write_text(json.dumps(
        {'text': text, 'seconds': n / 24000, 'samples': n, 'token_counts': meta.get('token_counts'),
         'instruction': '', 'seed': 1447, 'reference_sha256': prof['reference_sha256'],
         'route': 'G4 pure clone', 'chunk_count': chunks, 'expected_samples': expected if frames else None,
         'decode_check': 'samples == frames*1920 + gaps' if frames else 'not available'},
        ensure_ascii=False, indent=2))
    return n / 24000


def wav_seconds(p):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                          '-of', 'csv=p=0', str(p)]))


# ---------- 时间 ----------
def cta_start(voice_seconds, cta, full_text):
    """按末句字数占比估 CTA 起点，留足显示时间；返回秒。"""
    total = len(re.sub(r'[^\w一-鿿]', '', full_text)) or 1
    share = len(re.sub(r'[^\w一-鿿]', '', cta)) / total
    est = voice_seconds * (1 - share)
    return max(0.0, min(est, voice_seconds - 1.2))


def music(work, dur, name='tech', voice_gain=0.16):
    lib = sorted((A / 'bgm').glob('*.m4a'))
    pick = A / 'bgm' / f'{name}.m4a'
    assert pick.exists(), f'没有这首 BGM：{name}；可选 {[p.stem for p in lib]}'
    out = work / f'bgm-{name}.wav'
    subprocess.run([ffmpeg(), '-v', 'error', '-y', '-stream_loop', '-1', '-i', str(pick), '-t', f'{dur:.3f}',
                    '-af', f'volume={voice_gain},afade=t=in:d=1.2,afade=t=out:st={max(0, dur-1.0):.2f}:d=1.0',
                    '-ar', '48000', '-ac', '2', str(out)], check=True)
    return out


# ---------- 合成 ----------
def compose(cards, endcard, voice, musicfile, out, dur, cta_at, fps=30):
    """cards: [(png, start_s, end_s)]；落版卡从 cta_at 起，整片背景连续。"""
    ff = ffmpeg(); bg = A / 'bg-loop-1080x1920.mp4'
    segs = [(png, max(b - a, 1 / fps)) for png, a, b in cards] + [(endcard, max(dur - cta_at, 1 / fps))]
    ins, parts, labels = ['-stream_loop', '-1', '-i', str(bg)], [], []
    for i, (png, secs) in enumerate(segs, 1):
        ins += ['-loop', '1', '-framerate', str(fps), '-i', str(png)]
        parts.append(f'[{i}:v]fps={fps},setsar=1,trim=duration={secs:.3f},setpts=PTS-STARTPTS[c{i}]')
        labels.append(f'[c{i}]')
    parts.append(''.join(labels) + f'concat=n={len(labels)}:v=1:a=0[fg]')
    parts.append(f'[fg]format=rgba,fade=t=in:st=0:d=0.25:alpha=1[fgf]')
    parts.append(f'[0:v]fps={fps},setsar=1,drawbox=0:0:iw:ih:color=black@0.12:t=fill[bgd]')
    parts.append('[bgd][fgf]overlay=0:0:format=auto,format=yuv420p[v]')
    vi = len(segs) + 1  # 背景 0，卡片 1..n，配音/音乐从这里开始
    if voice:
        parts.append(f'[{vi}:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={dur:.3f},'
                     'alimiter=limit=0.95:latency=1[vc]')
        parts.append(f'[vc][{vi+1}:a]amix=inputs=2:duration=first:normalize=0[a]')
        ains = ['-i', str(voice), '-i', str(musicfile)]
    else:
        parts.append(f'[{vi}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=duration={dur:.3f},'
                     'loudnorm=I=-18:TP=-1.5[a]')
        ains = ['-i', str(musicfile)]
    cmd = [ff, '-v', 'error', '-y', *ins, *ains, '-filter_complex', ';'.join(parts),
           '-map', '[v]', '-map', '[a]', '-t', f'{dur:.3f}', '-r', str(fps),
           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
           '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(out)]
    subprocess.run(cmd, check=True)
    subprocess.run([ff, '-v', 'error', '-i', str(out), '-f', 'null', '-'], check=True)
    return out
