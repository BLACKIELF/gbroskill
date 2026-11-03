#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Lay out reviewed source-time SRT below a GBro video; write editable ASS + JSON."""
import argparse
import json
import re
import subprocess
from pathlib import Path
from PIL import ImageFont

CLOSE = '，。！？；：、）》】」』”’,.!?;:)]}'
OPEN = '（《【「『“‘([{'
WORD = re.compile(r'[A-Za-z0-9_@./:+-]+')


def seconds(value):
    h, m, s = value.replace(',', '.').split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)


def read_srt(path):
    cues = []
    for block in re.split(r'\n\s*\n', path.read_text(encoding='utf-8-sig').strip()):
        lines = block.splitlines()
        timing = next((i for i, line in enumerate(lines) if '-->' in line), None)
        if timing is None:
            raise ValueError('SRT block has no timing')
        a, b = lines[timing].split('-->')
        text = '\n'.join(line.strip() for line in lines[timing + 1:])
        text = re.sub(r'([A-Za-z0-9])\n(?=[A-Za-z0-9])', r'\1 ', text).replace('\n', '')
        if not text or any(c in text for c in '{}\\'):
            raise ValueError('Empty text or ASS control characters: review the source SRT')
        a, b = seconds(a.strip()), seconds(b.strip())
        if a < 0 or b <= a or (cues and a < cues[-1][1]):
            raise ValueError('Invalid or overlapping SRT timing')
        cues.append((a, b, text))
    return cues


def wrap(text, font, width):
    if any(font.getlength(m.group()) > width for m in WORD.finditer(text)):
        raise ValueError('An English token exceeds the safe width; revise the cue, do not shrink it')
    original, lines = text, []
    while text:
        if font.getlength(text) <= width:
            lines.append(text)
            break
        cut = 1
        while cut < len(text) and font.getlength(text[:cut + 1]) <= width:
            cut += 1
        boundaries = [i + 1 for i, c in enumerate(text[:cut])
                      if c in '，。！？；：、,!?;: ' and i + 1 >= max(1, int(cut * .52))]
        if boundaries:
            cut = boundaries[-1]
        for match in WORD.finditer(text):
            if match.start() < cut < match.end():
                cut = match.start()
                break
        while cut > 0 and (text[cut] in CLOSE or text[cut - 1] in OPEN):
            cut -= 1
        if not cut:
            raise ValueError('No safe semantic line break: ' + text)
        lines.append(text[:cut])
        text = text[cut:]
    if ''.join(lines) != original or any(line.lstrip()[0] in CLOSE for line in lines):
        raise ValueError('Punctuation or text preservation check failed')
    return lines


def stamp(t):
    cs = round(t * 100)
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f'{h}:{m:02d}:{s:02d}.{cs:02d}'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('srt', type=Path)
    parser.add_argument('--output', type=Path, required=True, help='ASS path; a layout JSON is written beside it')
    parser.add_argument('--source-start', type=float, default=0)
    parser.add_argument('--source-end', type=float, default=float('inf'))
    parser.add_argument('--intro-offset', type=float, default=0)
    parser.add_argument('--source-bottom', type=float, default=1215)
    args = parser.parse_args()
    if min(args.source_start, args.intro_offset, args.source_bottom) < 0 or args.source_end <= args.source_start:
        parser.error('Invalid source interval or intro offset')
    match = subprocess.check_output(['fc-match', '-f', '%{postscriptname}\n%{file}\n%{index}',
                                     'PingFang SC:style=Semibold'], text=True).splitlines()
    if len(match) != 3 or match[0] != 'PingFangSC-Semibold':
        raise SystemExit('Required PingFangSC-Semibold is unavailable; no automatic fallback')
    font = ImageFont.truetype(match[1], 72, index=int(match[2]))
    y = args.source_bottom + 65
    if not 72 <= y or y + 3 * 94 > 1848:
        parser.error('Source window leaves insufficient safe space for three subtitle lines')
    rendered, audit = [], []
    for a, b, text in read_srt(args.srt):
        a, b = max(a, args.source_start), min(b, args.source_end)
        if b <= a:
            continue
        lines = wrap(text, font, 936)
        groups = [lines[i:i + 3] for i in range(0, len(lines), 3)]
        weights = [sum(len(line) for line in group) for group in groups]
        pos = a
        for group, weight in zip(groups, weights):
            end = pos + (b - a) * weight / sum(weights)
            start_out = pos - args.source_start + args.intro_offset
            end_out = end - args.source_start + args.intro_offset
            if round(end_out * 100) - round(start_out * 100) < 75:
                raise ValueError('Subtitle would flash for less than 0.75s; merge/re-time the reviewed source cue')
            rendered.append({'start':start_out, 'end':end_out, 'lines':group})
            pos = end
        audit.append({'source_start':a,'source_end':b,'text':text,'lines':lines,
                      'max_width':max(font.getlength(line) for line in lines),'groups':len(groups)})
    if not rendered:
        raise ValueError('No cues in selected source interval')
    header = '''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,PingFangSC-Semibold,72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,8,72,72,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    events = []
    for cue in rendered:
        text = r'\N'.join(cue['lines'])
        events.append(f"Dialogue: 0,{stamp(cue['start'])},{stamp(cue['end'])},Default,,0,0,0,,{{\\an8\\q2\\pos(540,{y:g})}}" + text)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(header + '\n'.join(events) + '\n')
    result = {'source_start':args.source_start,'intro_offset':args.intro_offset,
              'time_mapping':'rendered = source - source_start + intro_offset',
              'font':'PingFangSC-Semibold','font_size_px':72,'position':[540,y],
              'max_width_px':936,'max_lines':3,'rendered_cues':rendered,'cues':audit}
    args.output.with_suffix('.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'source_cues':len(audit),'rendered_cues':len(rendered),'ass':str(args.output)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
