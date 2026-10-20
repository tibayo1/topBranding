#!/usr/bin/env python3
"""Build both refined draft identities in their selected working teal palette."""
from pathlib import Path
from copy import deepcopy
from html import escape
import json
import hashlib
import re
import xml.etree.ElementTree as ET
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform
from fontTools.svgLib.path import parse_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'exports'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
DRAFT = 'DRAFT — NOT FOR PUBLICATION'


def read_art(path):
    root = ET.parse(path).getroot()
    for child in list(root):
        if child.tag.rsplit('}', 1)[-1] in ('title', 'desc'):
            root.remove(child)
    return root


def bounds(root):
    # SVGPath.draw ignores ancestor group transforms. Walk the generated
    # translate/scale/matrix hierarchy explicitly when measuring contours.
    pen = BoundsPen(None)
    def walk(node, parent):
        local = Transform()
        for command, values in re.findall(r'(\w+)\(([^)]+)\)', node.get('transform', '')):
            args = [float(v) for v in re.split(r'[ ,]+', values.strip())]
            if command == 'translate':
                local = local.translate(args[0], args[1] if len(args)>1 else 0)
            elif command == 'scale':
                local = local.scale(args[0], args[1] if len(args)>1 else args[0])
            elif command == 'matrix':
                local = local.transform(Transform(*args))
            else:
                raise ValueError(f'Unsupported generated transform: {command}')
        combined = parent.transform(local)
        if node.tag.rsplit('}', 1)[-1] == 'path':
            parse_path(node.get('d', ''), TransformPen(pen, combined))
        for child in node:
            walk(child, combined)
    walk(root, Transform())
    return pen.bounds


def inner(root, ink='#000000'):
    root = deepcopy(root)
    for node in root.iter():
        for key in ('id', 'aria-labelledby'):
            node.attrib.pop(key, None)
        for key in ('fill', 'stroke'):
            if node.get(key) in ('#000000', '#000', 'black', 'currentColor'):
                node.set(key, ink)
    return f'<g fill="{ink}">' + ''.join(ET.tostring(child, encoding='unicode') for child in root) + '</g>'


def fit(root, field, ink='#000000'):
    x, y, w, h = field
    a, b, c, d = bounds(root)
    s = min(w / (c-a), h / (d-b))
    tx, ty = x+(w-(c-a)*s)/2-a*s, y+(h-(d-b)*s)/2-b*s
    return f'<g transform="translate({tx:.7f} {ty:.7f}) scale({s:.9f})">{inner(root, ink)}</g>'


def at_height(root, height, cx, cy, ink):
    a, b, c, d = bounds(root)
    s = height/(d-b)
    tx, ty = cx-(a+c)*s/2, cy-(b+d)*s/2
    return f'<g data-part="symbol" transform="translate({tx:.7f} {ty:.7f}) scale({s:.9f})">{inner(root, ink)}</g>'


def document(body, box, label):
    return (f'<svg xmlns="{NS}" viewBox="{box}" role="img" aria-label="{escape(label)}">'
            f'<title>{escape(label)} — DRAFT</title><desc>{DRAFT}. '
            'Teal and sand selected for working development. Instrument Sans title-case companion, weight 470, '
            'original glyph outlines with refined spacing. Final identity and production approval remain open.</desc>'+body+'</svg>\n')


def main():
    OUT.mkdir(exist_ok=True)
    palette = json.loads((ROOT/'source/working-palette.json').read_text())
    type_root = ROOT / 'lettering'
    name = read_art(type_root/'wordmark.svg')
    centered = read_art(type_root/'wordmark-centered.svg')
    single = read_art(type_root/'wordmark-single-line.svg')
    for art in (name, centered, single):
        assert ''.join(p.get('data-letter', '') for p in art.iter(f'{{{NS}}}path')) == 'TabernacleofPraise'
    records = []
    for slug, title, factor in [('shared-rhythm', 'Shared Rhythm', 1), ('open-praise', 'Open Praise', .93)]:
        mark = read_art(ROOT/slug/'primary.svg')
        compact = read_art(ROOT/slug/'compact.svg')
        lockups = {}
        symbols = {}
        for reverse in (False, True):
            ink = palette['neutral'] if reverse else palette['primary']
            background = palette['primary'] if reverse else palette['neutral']
            # Scale by actual contour height, not a maximum width/height field.
            # This makes the 7% optical reduction exact in each arrangement.
            horizontal = at_height(mark, 184*factor, 126, 128, ink)
            horizontal += '<g data-part="name">'+fit(name, (270, 53, 385, 150), ink)+'</g>'
            stacked = at_height(mark, 210*factor, 200, 127, ink)
            stacked += '<g data-part="name">'+fit(centered, (61, 269, 278, 105), ink)+'</g>'
            single_line = at_height(mark, 124*factor, 90, 80, ink)
            single_line += '<g data-part="name">'+fit(single, (190, 49, 780, 62), ink)+'</g>'
            for kind, body, box in [('horizontal', horizontal, '0 0 680 256'), ('stacked', stacked, '0 0 400 410'), ('singleLine', single_line, '0 0 1000 160')]:
                suffix = '-reverse' if reverse else ''
                key = kind+'Reverse' if reverse else kind
                file = f'{slug}-{kind}{suffix}-DRAFT.svg'
                _, _, w, h = box.split()
                body = f'<rect width="{w}" height="{h}" fill="{background}"/>'+body
                (OUT/file).write_text(document(body, box, f'{title} / Tabernacle of Praise / {kind}{suffix}'))
                lockups[key] = 'exports/'+file
            for kind, art in [('primary', mark), ('compact', compact)]:
                suffix = '-reverse' if reverse else ''
                file = f'{slug}-{kind}{suffix}-DRAFT.svg'
                (OUT/file).write_text(document(f'<rect width="256" height="256" fill="{background}"/>'+inner(art, ink), '0 0 256 256', f'{title} / {kind}{suffix}'))
                symbols[kind+('Reverse' if reverse else '')] = 'exports/'+file
        records.append({'id': slug, 'name': title, 'primaryFile': f'{slug}/primary.svg', 'compactFile': f'{slug}/compact.svg',
                        'viewBox': '0 0 256 256', 'inkBounds': bounds(mark), 'lockups': lockups, 'symbols': symbols,
                        'practicalSymbolScale': factor, 'symbolInkHeights': {'horizontal': 184*factor, 'stacked': 210*factor, 'singleLine': 124*factor}})
    source_files = [ROOT/d[k] for d in records for k in ('primaryFile','compactFile')]
    source_files += [type_root/f for f in ('wordmark.svg','wordmark-centered.svg','wordmark-single-line.svg')]
    result = {'status': DRAFT, 'finalApproval': False, 'workingPalette': palette,
        'lettering': {'family': 'Instrument Sans', 'axes': {'wdth':100,'wght':470}, 'source':'lettering/metadata.json',
                     'classification':'Original font glyphs with optical spacing; no custom-drawn font claim.'},
        'comparison':'Same lettering scale and spacing for both options. Open Praise has exactly 93% of Shared Rhythm actual symbol ink height in each practical arrangement; no nonuniform scaling.',
        'darkTreatment':'Ivory/porcelain symbol and name on teal. Soft gold is a restrained layout accent.',
        'compact':'16–20 px candidate only. Primary geometry remains in normal avatars and larger applications.',
        'rccg':{'assetPresent':False,'actualPairingVerified':False,'manifest':'../../assets/rccg-emblem/README.md'},
        'sources':[{'file':f.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in source_files],
        'directions':records}
    (OUT/'artwork.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print('Built 12 outlined name lockups and 8 symbol color proofs for both working directions.')


if __name__ == '__main__':
    main()
