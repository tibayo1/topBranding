#!/usr/bin/env python3
"""Actual-size monochrome review evidence. All output remains DRAFT.

Requires Inkscape and Pillow. Sources are rendered at their natural aspect
ratio; the pixel-size ladder is pasted into the sheet without enlargement.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'proofs/pass-2'
OUT.mkdir(parents=True, exist_ok=True)
FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)


def render(source, target, width, reverse=False):
    subprocess.run([
        'inkscape', str(source), '--export-type=png',
        f'--export-filename={target}', f'--export-width={width}',
        f'--export-background={"#000000" if reverse else "#ffffff"}',
        '--export-background-opacity=1',
    ], check=True, capture_output=True)


sheet = Image.new('RGB', (800, 750), '#ededed')
draw = ImageDraw.Draw(sheet)
draw.text((20, 14), 'C — JOINED ROUNDEL / OPTICAL PASS 2 / DRAFT — NOT FOR PUBLICATION', font=FONT, fill='black')
for reverse, x in ((False, 20), (True, 410)):
    source = HERE / 'developed' / ('c-developed-reverse.svg' if reverse else 'c-developed-v3.svg')
    suffix = '-reverse' if reverse else ''
    render(source, OUT / f'symbol-large{suffix}.png', 768, reverse)
    draw.text((x, 52), f'Symbol / {"reverse" if reverse else "black"} / actual pixel sizes', font=FONT, fill='black')
    for index, width in enumerate((16, 24, 32, 48)):
        target = OUT / f'symbol-{width}{suffix}.png'
        render(source, target, width, reverse)
        xx = x + index * 84
        draw.text((xx, 83), f'{width}px', font=FONT, fill='black')
        sheet.paste(Image.open(target).convert('RGB'), (xx, 108))
    lockup = HERE / 'developed' / ('c-lockup-horizontal-reverse.svg' if reverse else 'c-lockup-horizontal.svg')
    for index, width in enumerate((320, 240)):
        yy = 202 + index * 205
        target = OUT / f'lockup-{width}{suffix}.png'
        render(lockup, target, width, reverse)
        draw.text((x, yy), f'Complete lockup / {width}px / {"reverse" if reverse else "black"}', font=FONT, fill='black')
        sheet.paste(Image.open(target).convert('RGB'), (x, yy + 25))
draw.text((20, 666), 'At 16px the silhouette persists; TP reading and lower gaps are unreliable.', font=FONT, fill='black')
draw.text((20, 690), '32px is the more credible symbol test. The complete name needs its own width.', font=FONT, fill='black')
sheet.save(OUT / 'practical-widths.png')
print('Rendered symbol 16/24/32/48px and complete lockup 320/240px in black/reverse.')
