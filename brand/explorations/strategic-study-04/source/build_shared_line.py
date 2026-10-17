#!/usr/bin/env python3
"""Rebuild Shared Line v2 draft wordmark and provisional compact letter.
DRAFT — NOT FOR PUBLICATION. Original Source Serif 4 outlines + drawn initial T;
this does not modify, rename, or redistribute a derived font binary.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.roundingPen import RoundingPen
from PIL import ImageFont
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'concepts'
FONT = ROOT / 'assets/fonts/sourceserif4/SourceSerif4[opsz,wght].ttf'

class OutlinedFace:
    def __init__(self, file=FONT, axes=None):
        self.axes = axes or {'wght': 550, 'opsz': 24}
        self.font = TTFont(file)
        self.gs = self.font.getGlyphSet(location=self.axes)
        self.cmap = self.font.getBestCmap()
        self.upm = self.font['head'].unitsPerEm
        self.pil = ImageFont.truetype(str(file), 1000)
        self.pil.set_variation_by_axes([self.axes.get(a.axisTag, a.defaultValue) for a in self.font['fvar'].axes])

    def width(self, text, size):
        return self.pil.getlength(text) * size / 1000

    def text(self, text, x, baseline, size):
        paths=[]
        for i,c in enumerate(text):
            if c == ' ': continue
            pen=SVGPathPen(self.gs, ntos=lambda v: format(v, ".2f").rstrip("0").rstrip(".") if v else "0")
            # Round only after the complete font-to-canvas transform; canvas
            # precision is 0.01 units, while preserving the source contours.
            rpen=RoundingPen(pen, roundFunc=lambda v: round(v,2))
            advance=(self.pil.getlength(text[:i+1])-self.pil.getlength(c))*size/1000
            tpen=TransformPen(rpen,(size/self.upm,0,0,-size/self.upm,x+advance,baseline))
            self.gs[self.cmap[ord(c)]].draw(tpen)
            paths.append('<path data-letter="'+escape(c)+'" d="'+pen.getCommands()+'"/>')
        return ''.join(paths)


def document(title, viewbox, mark, desc):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)} — Tabernacle of Praise — DRAFT</title><desc id="desc">DRAFT — NOT FOR PUBLICATION. {escape(desc)}</desc><g fill="#000000">{mark}</g></svg>\n'''


def build():
    OUT.mkdir(parents=True,exist_ok=True)
    face=OutlinedFace()

    # A 16-unit beam rather than v1's 21; tapered end serifs retain the
    # drawn T vocabulary. Slightly lighter stem and open inset text.
    t_primary='''<g data-custom="initial-T"><path d="M28 40H876L880 87H864L850 56H62L49 87H28Z"/><path d="M132 50H174C171 142 171 235 174 340H132C135 235 135 142 132 50Z"/><path d="M96 340V323L132 317H174L210 323V340Z"/></g>'''
    primary=t_primary+face.text('abernacle',210,183,148)+face.text('of Praise',210,319,148)

    # Same custom T grammar at a scale appropriate for one text baseline.
    # The final name is never stretched to fit a preselected rectangle.
    t_horizontal='''<g data-custom="initial-T"><path d="M30 64H1428L1432 105H1416L1402 80H62L48 105H28Z"/><path d="M86 74H114C112 115 112 158 114 205H86C88 158 88 115 86 74Z"/><path d="M61 205V192L86 187H114L139 192V205Z"/></g>'''
    horizontal=t_horizontal+face.text('abernacle of Praise',154,205,148)

    # A separate, provisional letter cut is acknowledged as generic without
    # the full name. No claim that this already establishes recognition.
    compact='''<g data-custom="compact-initial-T"><path d="M28 24H228L232 70H216L202 40H54L40 70H24Z"/><path d="M108 35H148C145 92 145 151 148 220H108C111 151 111 92 108 35Z"/><path d="M73 236V219L108 212H148L183 219V236Z"/></g>'''

    variants={
        'primary':dict(file='11-shared-line-v2.svg',viewBox='0 0 920 390',markinnerSVG=primary,description='Two-line full-name wordmark. The initial T is a drawn common overhead line and one anchor; the remaining name uses Source Serif 4 outlines at weight 550 / optical size 24. The shared line is an artistic dwelling association, not a reconstruction of the biblical tabernacle.'),
        'horizontal':dict(file='11-shared-line-horizontal-v2.svg',viewBox='0 0 1470 260',markinnerSVG=horizontal,description='Single-line full name with the same structural initial T grammar. Source Serif 4 outlines at weight 550 / optical size 24. The name remains uncompressed; this very wide arrangement needs enough display width.'),
        'compact':dict(file='11-shared-line-compact-v2.svg',viewBox='0 0 256 256',markinnerSVG=compact,description='Provisional compact T derived from the structural initial. Less distinctive without the full name; recognition and minimum reproduction size are unapproved. This is a Latin initial, not a claimed biblical depiction.')
    }
    for name,v in variants.items():
        (OUT/v['file']).write_text(document('11 — Shared Line '+name,v['viewBox'],v['markinnerSVG'],v['description']))

    data=dict(id='11',name='Shared Line',territory='F',status='DRAFT — NOT FOR PUBLICATION',idea='The first T becomes a shared structure holding the full name together.',approach='A structural initial drawn into a full-name serif wordmark',
      connection={'tabernacle':'The shared overhead line and one anchoring stem suggest dwelling through the name’s own initial.','praise':'The words “of Praise” visibly sit within the same structure, making the complete spoken name the identifier. No instrument or additional icon is attached.'},
      construction='A purpose-drawn initial T uses a 16-unit common beam, tapered ends, and a flared stem; Source Serif 4 weight 550 / optical size 24 provides the other letter outlines. Native kerning is retained. The horizontal arrangement uses the same grammar with a shorter stem; it does not stretch the text.',
      license='Original Source Serif 4 under SIL OFL 1.1; license, original variable font, and metadata stored in assets/fonts/sourceserif4/. Only logo outlines and a drawn T are modified; no font binary is modified.',
      risk='The long overhead line may read as a signboard or roof. The compact T has weaker distinctiveness without the full name. The single-line arrangement is very wide; minimum sizes and final clear space are not established.',
      variants=variants)
    (ROOT/'source/concept11-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print('Built Shared Line v2 primary, horizontal, and provisional compact SVGs.')

if __name__=='__main__':
    build()
