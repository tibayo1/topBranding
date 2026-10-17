#!/usr/bin/env python3
"""Two original typographic compositions; licensed base letter outlines, not a new font.
DRAFT — NOT FOR PUBLICATION. Original unmodified source fonts/OFL accompany the study.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from PIL import ImageFont
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'sketches'
FONTS = ROOT / 'assets' / 'fonts'

class OutlinedFace:
    def __init__(self, file, axes):
        self.file = file
        self.font = TTFont(file)
        self.axes = axes
        self.gs = self.font.getGlyphSet(location=axes)
        self.cmap = self.font.getBestCmap()
        self.upm = self.font['head'].unitsPerEm
        self.pil = ImageFont.truetype(str(file), 1000)
        self.pil.set_variation_by_axes([axes.get(a.axisTag, a.defaultValue) for a in self.font['fvar'].axes])

    def width(self, text, size):
        return self.pil.getlength(text) * size / 1000

    def text(self, text, x, baseline, size, per_letter_lift=None):
        """Latin text: shaped prefix - current advance retains actual pair kerning.
        No ligature-bearing pairs occur in these two wordmark strings. Letter lifts are
        intentional composition edits; original glyph shapes are otherwise unchanged.
        """
        paths = []
        for i, c in enumerate(text):
            if c == ' ':
                continue
            glyph = self.gs[self.cmap[ord(c)]]
            pen = SVGPathPen(self.gs)
            glyph.draw(pen)
            d = pen.getCommands()
            advance = (self.pil.getlength(text[:i + 1]) - self.pil.getlength(c)) * size / 1000
            lift = per_letter_lift(i, c) if per_letter_lift else 0
            paths.append(f'<path data-letter="{escape(c)}" d="{d}" transform="translate({x + advance:.4f} {baseline - lift:.4f}) scale({size / self.upm:.6f} {-size / self.upm:.6f})"/>')
        return ''.join(paths)

serif = OutlinedFace(FONTS / 'sourceserif4' / 'SourceSerif4[opsz,wght].ttf', {'wght': 550, 'opsz': 24})
sans = OutlinedFace(FONTS / 'bricolagegrotesque' / 'BricolageGrotesque[opsz,wdth,wght].ttf', {'wght': 550, 'wdth': 100, 'opsz': 24})

# 11: the actual initial T becomes a common overhead line and a single anchor.
# The T is purpose-drawn from the serif's stem/terminal vocabulary; all other
# letters remain licensed Source Serif 4 outlines with their actual shaping.
custom_t = '''<g id="custom-initial-T"><path d="M30 40H876L880 91H861L850 61H62L50 91H27Z"/><path d="M127 51H179C176 142 176 235 179 340H127C130 235 130 142 127 51Z"/><path d="M88 340V322L127 316H179L218 322V340Z"/></g>'''
mark11 = custom_t + serif.text('abernacle', 210, 183, 148) + serif.text('of Praise', 210, 319, 148)

# 12: a stable first line and a continuous, measured upward response in the
# second; the letter outlines are not slanted or stretched. A common amount
# of rise per advancing letter avoids random bouncing or decorative notes.
# The first line is anchored; Praise begins on the same level as "of" and rises
# gently across its six readable letters. No additional symbol is attached.
mark12 = sans.text('Tabernacle', 42, 149, 148)
mark12 += sans.text('of', 42, 296, 104)
mark12 += sans.text('Praise', 196, 296, 148, lambda i, c: i * 4.5)

records = [
 dict(id='11', name='Shared Line', territory='F', idea='The first T becomes the common structure holding the full name together.', approach='Custom structural initial plus full-name serif wordmark', viewBox='0 0 920 390', markinnerSVG=mark11, construction='Purpose-drawn initial T: 21-unit overhead beam, one stem, serif base; remaining Source Serif 4 outlines at weight 550 / optical size 24. The two lines read T + abernacle / of Praise. Every visible letter belongs to the name.', risk='The long T can suggest a signboard or an overbearing roof; the oversized initial changes reading order. A wide wordmark has no automatically successful compact avatar.'),
 dict(id='12', name='Lifted Praise', territory='F', idea='A steady dwelling-name is answered by a gently rising word of praise.', approach='Full-name expressive sans wordmark with measured baseline movement', viewBox='0 0 870 365', markinnerSVG=mark12, construction='Bricolage Grotesque outlines at weight 550 / width 100 / optical size 24; the Tabernacle line remains stable. The six Praise letters rise 4.5 canvas units per letter without rotating or distorting their shapes; of remains readable.', risk='Baseline movement can feel playful or like event typography rather than an enduring church identifier; the name is expressive but not inherently a compact symbol.')
]

for record in records:
    desc = 'DRAFT — NOT FOR PUBLICATION. ' + record['idea'] + ' ' + record['construction'] + ' Risk: ' + record['risk']
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{record['viewBox']}" role="img" aria-labelledby="title desc"><title id="title">{record['id']} — {escape(record['name'])} — Tabernacle of Praise — DRAFT</title><desc id="desc">{escape(desc)}</desc><g fill="#000000">{record['markinnerSVG']}</g></svg>'''
    file = OUT / ('11-living-line-v1.svg' if record['id'] == '11' else '12-lifted-praise-v1.svg')
    file.write_text(svg + '\n')

(OUT / 'typography-sketches.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
print('Built two outlined typographic explorations; no font binary was modified.')
