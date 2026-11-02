#!/usr/bin/env python3
"""AiGoodBro 重置消息一键出片：文案 + G4 配音 + 9:16 视频 + 封面。

用法（最常用，一条命令）：
  python3 make_reset.py --mode forecast --date 2026-11-02 --time 16:00
  python3 make_reset.py --mode card --date 2026-11-02            # 只说“重置卡已发放”
  python3 make_reset.py --mode done --date 2026-11-02 --time 16:10
可选：--out 目录  --voice-file 已有中文干声  --voice-file-en 已有英文干声  --no-voice  --no-en
"""
from pathlib import Path
from urllib.request import Request, urlopen
import argparse, hashlib, json, math, shutil, subprocess, sys, uuid, wave, datetime as dt

SK = Path(__file__).resolve().parent.parent
A = SK / 'assets'
VOICE = A / 'voice' if (A / 'voice/reference.wav').exists() else SK.parent / 'gbro-social-workflow/assets/voice/aigoodbro-g4'
TAGS = '#codex #aigoodbro #tibo #codex重置'
END_ZH = '关注 AiGoodBro，第一时间获取重置消息'
END_EN = 'Follow AiGoodBro for reset news first'
REMIND_ZH = '谨慎使用重置卡，合理安排使用额度'
TTS = 'http://127.0.0.1:7862'
CN = '零一二三四五六七八九'


def cnum(n):  # 0-59 → 中文读法
    if n < 10: return CN[n]
    t, o = divmod(n, 10)
    return ('' if t == 1 else CN[t]) + '十' + (CN[o] if o else '')


def ffmpeg():
    for p in ['/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg', shutil.which('ffmpeg')]:
        if p and Path(p).exists(): return p
    sys.exit('缺 ffmpeg')


def build_text(mode, d, hm):
    m, day = d.month, d.day
    if hm:
        h, mi = hm
        part = '凌晨' if h < 6 else '上午' if h < 12 else '中午' if h < 13 else '下午' if h < 18 else '晚上'
        h12 = h if h <= 12 else h - 12
        clock = f'{part}{h12}点' + (f'{mi:02d}分' if mi else '')
        clock_sp = f'{part}{cnum(h12)}点' + (f'{cnum(mi)}分' if mi else '')
        en_clock = (dt.time(h, mi).strftime('%-I:%M %p') if mi else dt.time(h, 0).strftime('%-I %p'))
    date = f'{m}月{day}日'; date_sp = f'{cnum(m)}月{cnum(day)}日'
    en_date = d.strftime('%b %-d')
    if mode == 'forecast':
        big, sub = '预计重置', f'北京时间 {date}<br>{clock}左右'
        line = f'Codex 重置消息：预计北京时间 {date} {clock}左右重置。'
        spoken = f'Codex 重置消息。预计北京时间，{date_sp}，{clock_sp}左右重置。'
        en = f'Codex reset alert: expected around {en_clock} Beijing time, {en_date}.'
        en_big, en_sub = 'Reset expected', f'{en_date} · Beijing time<br>~{en_clock}'
    elif mode == 'done':
        big, sub = '已经重置', f'北京时间 {date}<br>{clock}左右'
        line = f'Codex 已重置：北京时间 {date} {clock}左右完成重置。'
        spoken = f'Codex 已经重置。北京时间，{date_sp}，{clock_sp}左右完成重置。'
        en = f'Codex has reset: around {en_clock} Beijing time, {en_date}.'
        en_big, en_sub = 'Codex has reset', f'{en_date} · Beijing time<br>~{en_clock}'
    else:  # card
        big, sub = '重置卡已发放', f'北京时间 {date}' + (f'<br>{clock}左右' if hm else '')
        line = f'Codex 重置卡已发放：北京时间 {date}' + (f' {clock}左右' if hm else '') + '，去账号里查看。'
        spoken = f'Codex 重置卡已经发放。北京时间，{date_sp}' + (f'，{clock_sp}左右' if hm else '') + '，去账号里查看。'
        en = f'Codex reset cards are out ({en_date}' + (f', ~{en_clock} Beijing' if hm else '') + '). Check your account.'
        en_big, en_sub = 'Reset cards are out', f'{en_date} · Beijing time' + (f'<br>~{en_clock}' if hm else '')
    zh_copy = f'{line}{REMIND_ZH}。{END_ZH}。'
    zh_voice = f'{spoken}{REMIND_ZH}。关注 AiGoodBro，第一时间获取重置消息。'
    en_copy = f'{en} Use reset cards wisely. {END_EN}.'
    return dict(big=big, sub=sub, zh_copy=zh_copy, zh_voice=zh_voice, en_copy=en_copy,
                en_voice=en_copy, en_big=en_big, en_sub=en_sub,
                title=f'Codex {big}｜{sub.replace("北京时间 ", "").replace("<br>", " ")}')


def write_copy(out, t, tag):
    zh = t['zh_copy']; en = t['en_copy']
    files = {
        '微博': f'{zh} {TAGS}', '快手': f'{zh} {TAGS}',
        '抖音': f'{t["title"]}\n\n{zh}\n\n{TAGS} #AI编程',
        '视频号': f'{t["title"]}\n\n{zh}\n\n{TAGS}',
        '小红书': f'{t["title"]}\n\n{zh}\n\n{TAGS} #AI工具 #AI编程',
        'B站': f'标题：{t["title"]}\n\n{zh}\n\n{TAGS}',
        '公众号': f'标题：{t["title"]}\n\n{zh}',
        'X': f'{en} {TAGS}', 'TikTok': f'{en} {TAGS} #ai',
        'YouTube': f'Title: {t["en_big"]} | {t["en_sub"].replace("<br>", " ")}\n\n{en} {TAGS}',
    }
    lines = [f'# 全平台文案 {tag}\n']
    for k, v in files.items():
        lines.append(f'## {k}\n\n{v}\n')
    (out / f'全平台文案-{tag}.md').write_text('\n'.join(lines))
    (out / f'全平台文案-{tag}.json').write_text(json.dumps(files, ensure_ascii=False, indent=2))


def tts(text, dest):
    prof = json.loads((VOICE / 'profile.json').read_text()); ref = VOICE / 'reference.wav'
    assert hashlib.sha256(ref.read_bytes()).hexdigest() == prof['reference_sha256'], 'G4 参考音被改动，停止'
    with urlopen(TTS + '/health', timeout=8) as f: h = json.load(f)
    assert h.get('service') == 'breeze-workbench' and not h.get('busy'), f'配音服务未就绪或在忙：{h}'
    fields = {'text': text, 'instruction': '', 'ref_text': prof['reference_text'], 'seed': '1447',
              'cfg_scale': '4', 'pronunciation': 'off', 'voice_id': ''}
    b = 'gbro' + uuid.uuid4().hex; body = b''
    for k, v in fields.items():
        body += f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    body += (f'--{b}\r\nContent-Disposition: form-data; name="ref_audio"; filename="reference.wav"\r\n'
             'Content-Type: audio/wav\r\n\r\n').encode() + ref.read_bytes() + f'\r\n--{b}--\r\n'.encode()
    req = Request(TTS + '/v1/audio/speech', data=body, headers={'Content-Type': f'multipart/form-data; boundary={b}'})
    with urlopen(req, timeout=300) as f:
        oid = f.headers.get('X-Output-Id'); data = f.read()
    if data[:4] == b'RIFF':
        dest.write_bytes(data)
    else:
        src = Path('/Volumes/4t/BreezeTTS2/workbench/outputs') / f'{oid}.wav'
        assert oid and src.exists(), f'配音返回异常：{data[:200]!r}'
        meta = json.loads(src.with_suffix('.json').read_text())
        assert meta.get('chunk_count') == 1 and meta.get('instruction') == '' and meta.get('seed') == 1447, meta
        shutil.copy2(src, dest)
    dest.with_suffix('.json').write_text(json.dumps({'text': text, 'instruction': '', 'seed': 1447,
        'reference_sha256': prof['reference_sha256'], 'route': 'G4 pure clone, one-shot'}, ensure_ascii=False, indent=2))


def wav_seconds(p):
    out = subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)])
    return float(out)


def bgm(path, dur):
    import numpy as np
    sr = 48000; n = int(dur * sr); t = np.arange(n) / sr; x = np.zeros(n)
    for i, f0 in enumerate([110, 130.81, 98, 123.47]):
        sel = (np.floor(t / 4).astype(int) % 4) == i
        for r, a in [(1, .006), (1.5, .004), (2, .002)]: x += sel * a * np.sin(2 * np.pi * f0 * r * t)
    for beat in np.arange(0, dur, .5):
        k = int(beat * sr); ln = min(int(.36 * sr), n - k); y = np.arange(ln) / sr
        f = [440, 554.37, 659.26, 554.37][int(beat * 2) % 4]
        x[k:k + ln] += .018 * np.sin(2 * np.pi * f * y) * np.exp(-y * 14) * np.minimum(1, y / .01)
    x *= np.minimum(1, t / .15) * np.clip((dur - t) / .6, 0, 1)
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((x * 32767).astype('<i2').tobytes())


BRAND = '<span style="color:#9BD9F8">Ai</span><span style="color:#fff">Good</span><span style="color:#FF6B62">Bro</span>'
CSS = '''html,body{margin:0;width:%(w)dpx;height:%(h)dpx;overflow:hidden;color:#fff;text-align:center;
font-family:"PingFang SC","Noto Sans CJK SC","Source Han Sans SC",sans-serif;font-synthesis:none;background:%(bg)s}
*{box-sizing:border-box}.wrap{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:%(gap)dpx;padding:0 72px}
.brand{display:flex;align-items:center;gap:18px;font-size:%(bs)dpx;font-weight:600}.brand img{width:%(av)dpx;height:%(av)dpx;border-radius:50%%}
.kicker{font-size:%(ks)dpx;font-weight:600;letter-spacing:.04em;color:#C9CFE8}
.big{font-size:%(gs)dpx;line-height:1.08;font-weight:700;letter-spacing:-.02em;background:linear-gradient(120deg,#DFE4FF,#fff 45%%,#CFD7FF);-webkit-background-clip:text;background-clip:text;color:transparent}
.sub{font-size:%(ss)dpx;font-weight:600;color:#9BD9F8;line-height:1.2}
.remind{font-size:%(rs)dpx;color:#E6E8F0;padding:18px 36px;border-radius:999px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18)}
.end{font-size:%(es)dpx;color:#fff;font-weight:600}.end b{font-weight:600}
.endcard .big.endmsg{background:none;-webkit-background-clip:border-box;background-clip:border-box;color:#fff}.endcard .big{font-size:%(ecs)dpx;line-height:1.35;white-space:nowrap}
.sub span{font-size:.62em;color:#C9CFE8;font-weight:500}'''


def page_html(t, lang, w, h, bg_uri, end=False):
    v = w / 1080 if h >= w else h / 1080
    tall = h / w > 1.5
    s = dict(w=w, h=h, gap=int((64 if tall else 40) * v), bs=int(56 * v), av=int(88 * v), ks=int(60 * v), gs=int((200 if tall else 176) * v),
             ss=int((96 if tall else 84) * v), rs=int(46 * v), es=int(46 * v), ecs=int(84 * v),
             bg=(f'linear-gradient(#0003,#0003),url("{bg_uri}") center/cover' if bg_uri else 'transparent'))
    av = (A / 'avatar.png').as_uri()
    brand = f'<div class="brand"><img src="{av}"><div>{BRAND}</div></div>'
    if end:
        msg = (f'关注 {BRAND}<br>第一时间获取重置消息' if lang == 'zh' else f'Follow {BRAND}<br>for reset news first')
        body = f'<div class="wrap endcard"><img src="{av}" style="width:{int(220*v)}px;height:{int(220*v)}px;border-radius:50%"><div class="big endmsg">{msg}</div></div>'
    else:
        big, sub = (t['big'], t['sub']) if lang == 'zh' else (t['en_big'], t['en_sub'])
        remind = REMIND_ZH if lang == 'zh' else 'Use reset cards wisely'
        endl = f'关注 {BRAND}，第一时间获取重置消息' if lang == 'zh' else f'Follow {BRAND} for reset news first'
        body = (f'<div class="wrap">{brand}<div class="kicker">CODEX 重置消息</div>' if lang == 'zh' else f'<div class="wrap">{brand}<div class="kicker">CODEX RESET</div>')
        sub_h = '<span>' + sub.replace('<br>', '</span><br>', 1) if '<br>' in sub else sub
        n = len(big) if lang == 'zh' else 0
        fs = f' style="font-size:{int(min(200, 900 / n) * (w / 1080 if h >= w else h / 1080))}px"' if n > 4 else (f' style="font-size:{int(132 * (w / 1080 if h >= w else h / 1080))}px"' if lang == 'en' else '')
        body += f'<div class="big"{fs}>{big}</div><div class="sub">{sub_h}</div><div class="remind">{remind}</div><div class="end">{endl}</div></div>'
    return '<!doctype html><meta charset="utf-8"><style>' + CSS % s + '</style>' + body


def shoot(html_text, path, w, h, transparent, browser, work):
    src = work / (path.stem + '.html'); src.write_text(html_text)
    pg = browser.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
    pg.goto(src.as_uri()); pg.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth>0)')
    pg.screenshot(path=str(path), omit_background=transparent); pg.close()


def render_video(ff, layer, endlayer, voice, music, out, dur):
    bg = A / 'bg-loop-1080x1920.mp4'; es = max(0.0, dur - 2.8)
    vf = (f'[0:v]setsar=1,drawbox=0:0:iw:ih:color=black@0.15:t=fill[b];[b][1:v]overlay=0:0[m];'
          f'[2:v]format=rgba,fade=t=in:st={es:.2f}:d=0.35:alpha=1[e];[m][e]overlay=0:0,format=yuv420p[v];')
    vf = vf.replace('[b][1:v]overlay=0:0[m]', f'[1:v]format=rgba,fade=t=out:st={es:.2f}:d=0.3:alpha=1[l];[b][l]overlay=0:0[m]')
    if voice:
        vf += '[3:a]aresample=48000,adelay=150|150,apad[a];[a][4:a]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=7[aout]'
        ins = ['-i', str(voice), '-i', str(music)]
    else:
        vf += '[3:a]aresample=48000,volume=4,loudnorm=I=-20:TP=-1.5[aout]'; ins = ['-i', str(music)]
    cmd = [ff, '-v', 'error', '-y', '-stream_loop', '-1', '-i', str(bg), '-loop', '1', '-framerate', '30', '-i', str(layer),
           '-loop', '1', '-framerate', '30', '-i', str(endlayer), *ins, '-filter_complex', vf, '-map', '[v]', '-map', '[aout]',
           '-t', f'{dur:.3f}', '-r', '30', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p',
           '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(out)]
    subprocess.run(cmd, check=True)
    subprocess.run([ff, '-v', 'error', '-i', str(out), '-f', 'null', '-'], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', choices=['forecast', 'done', 'card'], required=True)
    ap.add_argument('--date', required=True, help='北京时间日期 YYYY-MM-DD')
    ap.add_argument('--time', help='北京时间 HH:MM（card 模式可省略）')
    ap.add_argument('--out'); ap.add_argument('--voice-file'); ap.add_argument('--voice-file-en')
    ap.add_argument('--no-voice', action='store_true'); ap.add_argument('--no-en', action='store_true')
    a = ap.parse_args()
    d = dt.date.fromisoformat(a.date)
    hm = tuple(map(int, a.time.split(':'))) if a.time else None
    if a.mode != 'card' and not hm: sys.exit('forecast/done 需要 --time')
    tag = d.strftime('%m%d') + 'v1'
    out = Path(a.out or f'/Volumes/4t/AiGoodBro-GBro/{d:%Y%m%d}-Codex重置消息')
    out.mkdir(parents=True, exist_ok=True)
    while (out / f'Codex重置-中文竖版-{tag}.mp4').exists():  # 不覆盖旧版
        tag = tag[:-1] + str(int(tag[-1]) + 1) if tag[-1].isdigit() and tag[-2] == 'v' else tag + '2'
    work = out / '记录'; work.mkdir(exist_ok=True)
    t = build_text(a.mode, d, hm); write_copy(out, t, tag)
    (work / f'口播稿-{tag}.json').write_text(json.dumps(t, ensure_ascii=False, indent=2))
    ff = ffmpeg(); bgstill = work / 'bg.png'
    subprocess.run([ff, '-v', 'error', '-y', '-i', str(A / 'bg-loop-1080x1920.mp4'), '-frames:v', '1', str(bgstill)], check=True)
    langs = ['zh'] + ([] if a.no_en else ['en'])
    voices = {}
    for lang in langs:
        given = a.voice_file if lang == 'zh' else a.voice_file_en
        if given: voices[lang] = Path(given); continue
        if a.no_voice: voices[lang] = None; continue
        dest = out / f'{"中文" if lang == "zh" else "英文"}口播-G4-{tag}.wav'
        try:
            tts(t['zh_voice'] if lang == 'zh' else t['en_voice'], dest); voices[lang] = dest
        except Exception as e:
            print(f'⚠ {lang} 配音失败：{e}；该语言改出 BGM 版并标记待配音', flush=True); voices[lang] = None
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        br = p.chromium.launch(headless=True, args=['--allow-file-access-from-files'],
                               **({'executable_path': chrome} if Path(chrome).exists() else {}))
        bg_uri = bgstill.as_uri()
        for lang in langs:
            L = '中文' if lang == 'zh' else '英文'
            shoot(page_html(t, lang, 1080, 1920, None), work / f'layer-{lang}.png', 1080, 1920, True, br, work)
            shoot(page_html(t, lang, 1080, 1920, None, end=True), work / f'end-{lang}.png', 1080, 1920, True, br, work)
            shoot(page_html(t, lang, 1080, 1920, bg_uri), out / f'封面-{L}-9比16-{tag}.png', 1080, 1920, False, br, work)
            shoot(page_html(t, lang, 1080, 1440, bg_uri), out / f'封面-{L}-3比4-{tag}.png', 1080, 1440, False, br, work)
            shoot(page_html(t, lang, 1920, 1080, bg_uri), out / f'封面-{L}-16比9-{tag}.png', 1920, 1080, False, br, work)
        br.close()
    report = {'tag': tag, 'mode': a.mode, 'beijing': f'{a.date} {a.time or ""}'.strip(), 'outputs': []}
    for lang in langs:
        v = voices[lang]; dur = (wav_seconds(v) + 0.9) if v else 9.0; dur = max(dur, 7.0)
        music = work / f'bgm-{lang}.wav'; bgm(music, dur)
        L = '中文' if lang == 'zh' else '英文'
        mp4 = out / f'Codex重置-{L}竖版-{tag}.mp4'
        render_video(ff, work / f'layer-{lang}.png', work / f'end-{lang}.png', v, music, mp4, dur)
        for tm, nm in [(0.1, '首帧'), (dur - 0.3, '末帧')]:
            subprocess.run([ff, '-v', 'error', '-y', '-ss', f'{tm:.2f}', '-i', str(mp4), '-frames:v', '1', str(work / f'{nm}-{lang}.png')], check=True)
        report['outputs'].append({'video': str(mp4), 'seconds': round(dur, 2), 'voice': str(v) if v else 'NONE-待配音',
                                  'sha256': hashlib.sha256(mp4.read_bytes()).hexdigest()})
    (work / f'出片回执-{tag}.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print('DONE', out)


if __name__ == '__main__':
    main()
