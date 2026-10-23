"""Actual-size monochrome and reverse tests, not an approved asset system."""
from pathlib import Path
import sys

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parents[2] / '.agents/skills/logo-design/scripts'))
from concept_sheet import embed

names = [('a-folded-sanctuary', 'A / Folded Sanctuary'),
         ('b-sanctuary-strings', 'B / Sanctuary Strings'),
         ('c-praise-ligature', 'C / Praise Ligature')]
parts = ['<rect width="1200" height="610" fill="#fff"/>',
         '<text x="40" y="48" font-family="Noto Sans" font-size="26">DRAFT — NOT FOR PUBLICATION / Size tests</text>',
         '<text x="40" y="78" font-family="Noto Sans" font-size="15">Symbols at 64 / 32 / 24 / 16 CSS pixels. View this image at native size.</text>']
for row, (name, label) in enumerate(names):
    y = 112 + row * 158
    parts.append(f'<text x="40" y="{y+57}" font-family="Noto Sans" font-size="20">{label}</text>')
    parts.append(f'<rect x="740" y="{y}" width="414" height="110" rx="4" fill="#000"/>')
    for col, size in enumerate((64, 32, 24, 16)):
        x = 352 + col * 96
        parts.append(embed(str(ROOT / f'{name}-v3.svg'), f'light-{row}-{size}', x, y + 22 + (64-size)/2, size, size))
        dark = embed(str(ROOT / f'{name}-v3.svg'), f'dark-{row}-{size}', x+410, y+22+(64-size)/2, size, size)
        parts.append(dark.replace('#000000', '#ffffff'))
        parts.append(f'<text x="{x+size/2}" y="{y+138}" text-anchor="middle" font-family="Noto Sans" font-size="13">{size}px</text>')
        parts.append(f'<text x="{x+410+size/2}" y="{y+138}" text-anchor="middle" font-family="Noto Sans" font-size="13">{size}px</text>')
(ROOT / 'small-size-tests.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="610" viewBox="0 0 1200 610">' + ''.join(parts) + '</svg>')
