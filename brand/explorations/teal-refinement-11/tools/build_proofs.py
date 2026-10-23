#!/usr/bin/env python3
"""Build a true-scale vector A4 sheet and a native-pixel screen proof.

The sheet is for a subsequent physical print check; generating this PDF is not
proof that ink, stock, small text or vinyl will reproduce adequately.
"""
from __future__ import annotations

from copy import deepcopy
from html import escape
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

import fitz
from PIL import Image, ImageDraw, ImageFont
from fontTools.misc.transform import Transform
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / 'proofs'
PREVIOUS = ROOT.parent / 'identity-development-09'
FONT = PREVIOUS / 'type-study/fonts/instrumentsans/InstrumentSans[wdth,wght].ttf'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
TEAL, IVORY = '#10494C', '#F6F3EC'


def artwork(path):
    root = ET.parse(path).getroot()
    for child in list(root):
        if child.tag.rsplit('}', 1)[-1] in ('title', 'desc', 'rect'):
            root.remove(child)
    for node in root.iter():
        node.attrib.pop('id', None)
        node.attrib.pop('aria-labelledby', None)
    return root


def bounds(root):
    pen = BoundsPen(None)
    def walk(node, parent):
        local = Transform()
        for command, raw in re.findall(r'(\w+)\(([^)]+)\)', node.get('transform', '')):
            args = [float(v) for v in re.split(r'[ ,]+', raw.strip())]
            if command == 'translate':
                local = local.translate(args[0], args[1] if len(args) > 1 else 0)
            elif command == 'scale':
                local = local.scale(args[0], args[1] if len(args) > 1 else args[0])
            elif command == 'matrix':
                local = local.transform(Transform(*args))
            else:
                raise ValueError(f'Unsupported source transform {command}')
        combined = parent.transform(local)
        if node.tag.rsplit('}', 1)[-1] == 'path':
            parse_path(node.get('d', ''), TransformPen(pen, combined))
        for child in node:
            walk(child, combined)
    walk(root, Transform())
    if not pen.bounds:
        raise ValueError('Artwork has no path contours')
    return pen.bounds


def ink(root, color):
    copy = deepcopy(root)
    for node in copy.iter():
        if node.tag.rsplit('}', 1)[-1] == 'path':
            node.set('fill', color)
            node.attrib.pop('style', None)
        elif 'fill' in node.attrib:
            node.set('fill', color)
    return ''.join(ET.tostring(child, encoding='unicode') for child in copy)


def fit_ink(root, x, y, *, width=None, height=None, color=TEAL):
    a, b, c, d = bounds(root)
    scale = width / (c-a) if width is not None else height / (d-b)
    return (f'<g transform="translate({x-a*scale:.8f} {y-b*scale:.8f}) scale({scale:.10f})">'
            + ink(root, color) + '</g>')


class Labels:
    def __init__(self):
        face = TTFont(FONT)
        self.glyphs = face.getGlyphSet(location={'wdth': 100, 'wght': 450})
        self.cmap = face.getBestCmap()
        self.units = face['head'].unitsPerEm
        self.shaper = ImageFont.truetype(str(FONT), 1000)
        self.shaper.set_variation_by_axes([100 if a.axisTag == 'wdth' else 450 for a in face['fvar'].axes])

    def draw(self, text, x, y, size=2.7, color='#30383B'):
        paths = []
        for index, character in enumerate(text):
            if character == ' ':
                continue
            advance = self.shaper.getlength(text[:index+1]) - self.shaper.getlength(character)
            pen = SVGPathPen(self.glyphs)
            self.glyphs[self.cmap[ord(character)]].draw(TransformPen(pen, (size/self.units, 0, 0, -size/self.units, x+advance*size/1000, y)))
            paths.append(f'<path d="{pen.getCommands()}"/>')
        return f'<g fill="{color}">'+''.join(paths)+'</g>'


def print_sheet(data, base):
    labels = Labels()
    parts = ['<rect width="210" height="297" fill="#FFFFFF"/>']
    parts.append(labels.draw('TABERNACLE OF PRAISE / SIZE PROOF 11', 14, 15, 4.2))
    parts.append(labels.draw('DRAFT — NOT FOR PUBLICATION', 14, 21, 2.7))
    parts.append(labels.draw('Print at actual size (100%). Turn OFF Fit / Shrink. Measure the ruler before judging.', 14, 27, 2.65))
    parts.append(labels.draw('Screen HEX is a reference only. Physical reproduction and minimum sizes remain unverified.', 14, 32, 2.4))
    parts.append('<path d="M14 39H64" stroke="#000000" stroke-width=".3" fill="none"/>')
    for x in range(14, 65, 10):
        parts.append(f'<path d="M{x} 37V41" stroke="#000000" stroke-width=".25"/>')
    parts.append(labels.draw('0', 13.3, 45, 2.3))
    parts.append(labels.draw('50 mm', 58.7, 45, 2.3))
    parts.append(labels.draw('Actual filled ink heights. Teal on proposed ivory at left; black on paper at right.', 14, 51, 2.55))
    records = []
    for direction, x in zip(data['directions'], [14, 110]):
        mark = artwork(base / direction['primaryFile'])
        horizontal = artwork(base / direction['lockups']['horizontal'])
        parts.append(labels.draw(direction['name'], x, 57, 3.3))
        a, b, c, d = bounds(mark)
        for index, mm in enumerate([8, 12, 18, 24]):
            top = 62+index*29
            yy = top+(24-mm)/2
            parts.append(labels.draw(f'{mm} mm', x, top+13, 2.5))
            parts.append(f'<rect x="{x+14}" y="{top-.5}" width="31" height="25" fill="{IVORY}"/>')
            for offset, color in [(16, TEAL), (53, '#000000')]:
                parts.append(fit_ink(mark, x+offset, yy, height=mm, color=color))
            records.append({'direction': direction['id'], 'kind': 'symbol', 'inkHeightMm': mm, 'scaleMmPerSourceUnit': mm/(d-b)})
        parts.append(labels.draw('Full-name lockups / actual ink width in mm', x, 184, 2.65))
        for mm, top in [(35, 190), (50, 205), (70, 225)]:
            a, b, c, d = bounds(horizontal)
            ink_height = mm*(d-b)/(c-a)
            parts.append(f'<rect x="{x+12}" y="{top-.75}" width="73" height="{ink_height+1.5:.8f}" fill="{IVORY}"/>')
            parts.append(labels.draw(f'{mm}', x, top+4, 2.5))
            parts.append(fit_ink(horizontal, x+13, top, width=mm))
            records.append({'direction': direction['id'], 'kind': 'horizontal', 'inkWidthMm': mm})
        parts.append(f'<rect x="{x}" y="256" width="86" height="25" fill="{TEAL}"/>')
        parts.append(fit_ink(horizontal, x+14, 259, width=58, color=IVORY))
        parts.append(labels.draw('Ivory reverse / same primary geometry', x, 286, 2.4))
    parts.append(labels.draw('Inspect word shapes, open intervals and counter clarity. This sheet sets no production minimum.', 14, 293, 2.35))
    return (f'<svg xmlns="{NS}" width="210mm" height="297mm" viewBox="0 0 210 297">'
            '<title>Tabernacle of Praise / true-scale A4 print proof / DRAFT</title>'
            '<desc>DRAFT — NOT FOR PUBLICATION. A physical print remains to be made and assessed. '
            'No actual RCCG emblem pairing is included.</desc>'+''.join(parts)+'</svg>\n'), records


def raster(root, width, foreground, background, directory, stem):
    source = directory / (stem+'.svg')
    target = directory / (stem+'.png')
    box = root.get('viewBox')
    source.write_text(f'<svg xmlns="{NS}" viewBox="{box}">'+ink(root, foreground)+'</svg>')
    env = os.environ.copy()
    env['XDG_CONFIG_HOME'] = str(directory/'config')
    env['XDG_CACHE_HOME'] = str(directory/'cache')
    subprocess.run(['inkscape', str(source), '--export-type=png', f'--export-filename={target}',
                    f'--export-width={width}', f'--export-background={background}', '--export-background-opacity=1'],
                   check=True, capture_output=True, env=env)
    return Image.open(target).convert('RGB')


def screen_sheet(data, base, directory, destination):
    image = Image.new('RGB', (1420, 1215), '#F6F3EC')
    draw = ImageDraw.Draw(image)
    def text(s, x, y, size=18, fill='#30383B'):
        draw.text((x, y), s, font=ImageFont.truetype(str(FONT), size), fill=fill)
    text('SCREEN SIZE PROOF / TEAL REFINEMENT 11', 36, 24, 28)
    text('DRAFT — NOT FOR PUBLICATION · Native raster samples; inspect at 100% zoom.', 36, 69, 17)
    for index, direction in enumerate(data['directions']):
        x = 36+index*704
        primary = artwork(base/direction['primaryFile'])
        compact = artwork(base/direction['compactFile'])
        horizontal = artwork(base/direction['lockups']['horizontal'])
        single = artwork(base/direction['lockups']['singleLine'])
        text(direction['name'], x, 116, 25)
        text('Primary canvas sizes', x, 159, 16)
        text('Compact canvas sizes', x+330, 159, 16)
        for offset, px, mark in [(18,24,primary),(113,32,primary),(214,40,primary),(352,16,compact),(451,20,compact)]:
            im = raster(mark, px, TEAL, IVORY, directory, f'{index}-symbol-{px}')
            image.paste(im, (x+offset, 201-(im.height//2)))
            text(f'{px} px', x+offset-2, 237, 15)
        for px, y in [(180,300),(240,401),(320,523)]:
            text(f'Horizontal / {px} px viewport width', x, y-25, 16)
            im = raster(horizontal, px, TEAL, IVORY, directory, f'{index}-horizontal-{px}')
            image.paste(im, (x, y))
        for px, y in [(320,693),(480,782)]:
            text(f'Single line / {px} px viewport width', x, y-25, 16)
            im = raster(single, px, TEAL, IVORY, directory, f'{index}-single-{px}')
            image.paste(im, (x, y))
        draw.rectangle((x, 902, x+642, 1138), fill=TEAL)
        text('Ivory reverse / 240 px horizontal + 480 px single line', x+12, 914, 15, IVORY)
        im = raster(horizontal, 240, IVORY, TEAL, directory, f'{index}-reverse-h')
        image.paste(im, (x+12, 940))
        im = raster(single, 480, IVORY, TEAL, directory, f'{index}-reverse-s')
        image.paste(im, (x+12, 1060))
    text('Small-name readability and symbolic recognition need viewer feedback; these samples establish no minimum-size rule.', 36, 1170, 17)
    image.save(destination)


def main():
    global TEAL, IVORY
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--provisional', action='store_true', help='Scratch layout only; never final deliverables')
    args = parser.parse_args()
    if args.provisional:
        data = json.loads((PREVIOUS/'exports/development-artwork.json').read_text())
        base = PREVIOUS
        for row in data['directions']:
            row['lockups']['singleLine'] = row['lockups']['horizontal']
        destination = Path('/tmp/refinement-11-proof-layout')
    else:
        path = ROOT/'exports/artwork.json'
        if not path.exists():
            raise SystemExit('Final11 artwork metadata is not ready. --provisional makes scratch layout only.')
        data = json.loads(path.read_text())
        base = ROOT
        destination = HERE
    palette = data.get('workingPalette', {})
    TEAL = palette.get('primary', TEAL)
    IVORY = palette.get('neutral', IVORY)
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='refinement11-proof-') as scratch:
        directory = Path(scratch)
        sheet, records = print_sheet(data, base)
        svg = destination/'a4-print-proof.svg'
        pdf = destination/'a4-print-proof.pdf'
        svg.write_text(sheet)
        env = os.environ.copy()
        env['XDG_CONFIG_HOME'] = str(directory/'config')
        env['XDG_CACHE_HOME'] = str(directory/'cache')
        subprocess.run(['inkscape', str(svg), '--export-type=pdf', f'--export-filename={pdf}'], check=True, capture_output=True, env=env)
        document = fitz.open(pdf)
        assert len(document) == 1
        assert abs(document[0].rect.width-210*72/25.4) < .03
        assert abs(document[0].rect.height-297*72/25.4) < .03
        assert not document[0].get_images(), 'Print artwork unexpectedly rasterized'
        document[0].get_pixmap(matrix=fitz.Matrix(2,2)).save(destination/'print-proof-preview.png')
        screen_sheet(data, base, directory, destination/'screen-size-proof.png')
        result = {'status': 'DRAFT — NOT FOR PUBLICATION', 'provisional': args.provisional,
                  'pdfPageMm': [210,297], 'pdfPages': 1, 'embeddedRasterImagesInPdf': 0,
                  'symbolInkHeightsMm': [8,12,18,24], 'horizontalInkWidthsMm': [35,50,70],
                  'rulerMm': 50, 'screenViewportWidthsPx': {'horizontal':[180,240,320],'singleLine':[320,480]},
                  'proofMeasures': records, 'physicalPrint': 'NOT PRINTED OR VERIFIED; print at100%, measure ruler and assess actual material.'}
        if not args.provisional:
            result['metadataSHA256'] = hashlib.sha256((ROOT/'exports/artwork.json').read_bytes()).hexdigest()
            inputs = []
            for row in data['directions']:
                for relative in [row['primaryFile'], row['compactFile'], row['lockups']['horizontal'], row['lockups']['singleLine']]:
                    inputs.append({'file': relative, 'sha256': hashlib.sha256((base/relative).read_bytes()).hexdigest()})
            result['inputs'] = inputs
            result['outputs'] = [{'file': 'proofs/'+name, 'sha256': hashlib.sha256((destination/name).read_bytes()).hexdigest()}
                                 for name in ['a4-print-proof.svg', 'a4-print-proof.pdf', 'print-proof-preview.png', 'screen-size-proof.png']]
            (destination/'checks.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
