"""Explain the actual drawing, separating visible meaning from intended associations.

DRAFT — NOT FOR PUBLICATION. No theological number claims or approval implied.
"""
from pathlib import Path
from html import escape
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parents[2]
ROOT.mkdir(parents=True, exist_ok=True)


def contents(path):
    return [element for element in ET.parse(path).getroot().iter() if element.tag.endswith('path')]


def path_svg(element):
    attrs = ' '.join(f'{key}="{escape(value, quote=True)}"' for key, value in element.attrib.items())
    return '<path ' + attrs + '/>'


old = REPO / 'brand/concepts/exploration-01'
b = contents(old / 'b-sanctuary-strings-v3.svg')[0]
bparts = re.split(r'(?<=Z)\s+(?=M)', b.attrib['d'])
c = contents(old / 'c-praise-ligature-v3.svg')
studies = [
    {'name': 'B / Sanctuary Strings', 'operation': '-', 'pieces': [f'<path d="{bparts[0]}"/>', ''.join(f'<path d="{part}"/>' for part in bparts[1:]), path_svg(b)],
     'labels': ['01 / HARP-LIKE OUTLINE', '02 / THREE NEGATIVE OPENINGS', '03 / THE COMBINED MARK'],
     'reading': 'What reads clearly: a harp and musical praise.',
     'intention': 'The enclosing curve was intended as shelter. A tabernacle is not yet clear in the drawing.',
     'limit': 'The number of openings is a compositional choice, not an approved theological statement.'},
    {'name': 'C / Praise Ligature', 'operation': '+', 'pieces': [path_svg(c[0]), path_svg(c[1]), ''.join(path_svg(item) for item in c)],
     'labels': ['01 / T — TABERNACLE', '02 / P — PRAISE', '03 / NESTED T + P'],
     'reading': 'What reads clearly: the initials of Tabernacle and Praise.',
     'intention': 'The broad T and open P were intended to feel spacious. Sanctuary and worship are indirect associations.',
     'limit': 'The narrow white channel separates the letters; it is a functional detail, not a hidden religious symbol.'},
]

new = ROOT / 'd-resonant-sanctuary-v1.svg'
if new.exists():
    d = contents(new)
    studies.append({'name': 'D / Resonant Sanctuary — new proposal', 'operation': '+',
                    'pieces': ['<g transform="translate(-7 0)">' + ''.join(path_svg(item) for item in group) + '</g>' for group in (d[:3], d[3:], d)],
                    'labels': ['01 / ENCLOSING FOLDS', '02 / RISING RHYTHM', '03 / SPACE + PRAISE'],
                    'reading': 'A protected shared space, with enclosing contours that open into an outward rhythm.',
                    'intention': 'The same structure explores dwelling and collective praise, without an instrument or a monogram.',
                    'limit': 'The bands may suggest leaves or growth. The abstract sanctuary reading and fine seams need testing.'})

parts = ['<rect width="1500" height="' + str(170 + 480 * len(studies)) + '" fill="#f7f6f1"/>',
         '<text x="60" y="65" font-family="Noto Sans" font-size="34">Tabernacle of Praise / Reading the marks</text>',
         '<text x="60" y="105" font-family="Noto Sans" font-size="17" fill="#555">DRAFT — NOT FOR PUBLICATION / Visible meaning versus intended association</text>']
for row, study in enumerate(studies):
    y = 150 + row * 480
    parts.append(f'<rect x="45" y="{y}" width="1410" height="450" rx="6" fill="#fff" stroke="#ddd"/>')
    parts.append(f'<text x="75" y="{y+45}" font-family="Noto Sans" font-size="24">{escape(study["name"])}</text>')
    for column, piece in enumerate(study['pieces']):
        x = 120 + column * 460
        parts.append(f'<svg x="{x}" y="{y+65}" width="200" height="200" viewBox="0 0 256 256"><g fill="#111">{piece}</g></svg>')
        parts.append(f'<text x="{x+100}" y="{y+290}" text-anchor="middle" font-family="Noto Sans" font-size="13" fill="#555">{escape(study["labels"][column])}</text>')
        if column < 2:
            parts.append(f'<text x="{x+300}" y="{y+170}" text-anchor="middle" font-family="Noto Sans" font-size="26" fill="#777">{ study["operation"] if column == 0 else "=" }</text>')
    for line, text in enumerate((study['reading'], study['intention'], study['limit'])):
        parts.append(f'<text x="75" y="{y+340+line*32}" font-family="Noto Sans" font-size="17" fill="{ "#111" if line == 0 else "#555" }">{escape(text)}</text>')
height = 170 + len(studies) * 480
(ROOT / 'logo-meaning-breakdown.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="{height}" viewBox="0 0 1500 {height}">' + ''.join(parts) + '</svg>\n')
print('Built meaning breakdown for', len(studies), 'concepts')
