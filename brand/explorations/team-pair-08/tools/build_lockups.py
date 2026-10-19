#!/usr/bin/env python3
"""Outline temporary companion lettering around the selected draft symbols."""
from pathlib import Path
from html import escape
import json
import re
from PIL import ImageFont
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.svgLib.path import parse_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'exports'
FONT = ROOT / 'assets/fonts/instrumentsans/InstrumentSans[wdth,wght].ttf'
DRAFT = 'DRAFT — NOT FOR PUBLICATION'


class Lettering:
    def __init__(self):
        self.font = TTFont(FONT)
        axes = {'wdth': 100, 'wght': 450}
        self.glyphs = self.font.getGlyphSet(location=axes)
        self.cmap = self.font.getBestCmap()
        self.units = self.font['head'].unitsPerEm
        self.shaper = ImageFont.truetype(str(FONT), 1000)
        self.shaper.set_variation_by_axes([axes[axis.axisTag] for axis in self.font['fvar'].axes])

    def width(self, text, size, spacing):
        return self.shaper.getlength(text) * size / 1000 + max(0, len(text) - 1) * spacing

    def draw(self, text, x, baseline, size, spacing=0.8):
        pieces = []
        for index, character in enumerate(text):
            if character == ' ':
                continue
            advance = (self.shaper.getlength(text[:index + 1]) - self.shaper.getlength(character)) * size / 1000
            pen = SVGPathPen(self.glyphs)
            transform = (size / self.units, 0, 0, -size / self.units,
                         x + advance + index * spacing, baseline)
            self.glyphs[self.cmap[ord(character)]].draw(TransformPen(pen, transform))
            pieces.append(f'<path data-letter="{escape(character, quote=True)}" d="{pen.getCommands()}"/>')
        return '<g fill="#000000">' + ''.join(pieces) + '</g>'


def artwork(path):
    raw = path.read_text()
    view_box = re.search(r'viewBox="([^"]+)"', raw)[1]
    inner = re.sub(r'<(?:title|desc)\b[^>]*>.*?</(?:title|desc)>', '', raw, flags=re.S)
    inner = re.sub(r'^.*?<svg\b[^>]*>|</svg>\s*$', '', inner, flags=re.S)
    inner = re.sub(r'\s(?:id|aria-labelledby)="[^"]*"', '', inner)
    return inner.replace('currentColor', '#000000'), view_box


def fit(mark, box, x, y, width, height):
    a, b, w, h = map(float, box.split())
    scale = min(width / w, height / h)
    return f'<g transform="translate({x + (width-w*scale)/2-a*scale:.4f} {y + (height-h*scale)/2-b*scale:.4f}) scale({scale:.7f})">{mark}</g>'


def ink_box(mark):
    # Both draft masters contain explicit filled paths in their own coordinates.
    # Fit their actual contours to a common presentation field, not empty canvas.
    assert not re.search(r'\btransform=', mark), 'Resolve source transforms before fitting ink bounds.'
    pen = BoundsPen(None)
    for path in re.findall(r'<path\b[^>]*\bd="([^"]+)"', mark):
        parse_path(path, pen)
    assert pen.bounds, 'No filled path bounds found.'
    x0, y0, x1, y1 = pen.bounds
    return f'{x0} {y0} {x1-x0} {y1-y0}'


def svg(inner, box, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{box}" role="img" '
            f'aria-label="{escape(label, quote=True)}"><title>{escape(label)} — DRAFT</title>'
            f'<desc>{DRAFT}. Full parish name in temporary Instrument Sans companion lettering. '
            'No logo or typography system approved.</desc>' + inner + '</svg>\n')


def main():
    OUT.mkdir(exist_ok=True)
    face = Lettering()
    candidates = [('shared-rhythm', 'Shared Rhythm')]
    second = ROOT / 'second-direction/metadata.json'
    if second.exists():
        meta = json.loads(second.read_text())
        if meta.get('includeInReview', meta.get('inReview')) is True:
            candidates.append(('second-direction', meta['name']))
    records = []
    for folder, name in candidates:
        mark, box = artwork(ROOT / folder / 'primary.svg')
        bounds = ink_box(mark)
        horizontal = fit(mark, bounds, 20, 30, 204, 196)
        horizontal += face.draw('Tabernacle', 270, 109, 72)
        horizontal += face.draw('of Praise', 270, 194, 72)
        stacked = fit(mark, bounds, 70, 28, 260, 225)
        for text, baseline in [('Tabernacle', 294), ('of Praise', 338)]:
            stacked += face.draw(text, (400 - face.width(text, 40, 0.8)) / 2, baseline, 40)
        wordmark = ''
        for text, baseline in [('Tabernacle', 63), ('of Praise', 135)]:
            wordmark += face.draw(text, (420 - face.width(text, 64, 0.8)) / 2, baseline, 64)
        variants = {'horizontal': (horizontal, '0 0 680 256'),
                    'stacked': (stacked, '0 0 400 380'),
                    'wordmark': (wordmark, '0 0 420 160')}
        prefix = folder if folder != 'second-direction' else 'second-option'
        files = {}
        for kind, (inner, view_box) in variants.items():
            file = OUT / f'{prefix}-{kind}-DRAFT.svg'
            file.write_text(svg(inner, view_box, f'{name} / Tabernacle of Praise / {kind}'))
            files[kind] = file.relative_to(ROOT).as_posix()
            if kind != 'wordmark':
                _, _, w, h = view_box.split()
                reverse = f'<rect width="{w}" height="{h}" fill="#111111"/>' + inner.replace('#000000', '#ffffff')
                rev = OUT / f'{prefix}-{kind}-reverse-DRAFT.svg'
                rev.write_text(svg(reverse, view_box, f'{name} / full parish name / {kind} reversed'))
                files[kind + 'Reverse'] = rev.relative_to(ROOT).as_posix()
        records.append({'folder': folder, 'name': name, 'primary': f'{folder}/primary.svg',
                        'viewBox': box, 'inkBox': bounds, 'lockups': files})
    data = {'status': DRAFT, 'lettering': {'family': 'Instrument Sans', 'weight': 450,
            'width': 100, 'tracking': '0.8 SVG units in both companion name lines',
            'note': 'Temporary common lettering for fair comparison. Shaped and outlined; no font binary modified.',
            'license': 'assets/fonts/instrumentsans/OFL.txt'}, 'directions': records}
    (OUT / 'review-artwork.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(f'Built full-name outlined lockups for {len(records)} draft direction(s).')


if __name__ == '__main__':
    main()
