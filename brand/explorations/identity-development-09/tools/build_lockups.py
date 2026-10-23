#!/usr/bin/env python3
"""Assemble provisional lockups from editable symbol and outlined type studies."""
from pathlib import Path
from copy import deepcopy
from html import escape
import json
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


def inner(root, white=False):
    root = deepcopy(root)
    for node in root.iter():
        for key in ('id', 'aria-labelledby'):
            node.attrib.pop(key, None)
        if white:
            for key in ('fill', 'stroke'):
                if node.get(key) in ('#000000', '#000', 'black', 'currentColor'):
                    node.set(key, '#ffffff')
    return ''.join(ET.tostring(child, encoding='unicode') for child in root)


def fit(root, field, white=False):
    x, y, w, h = field
    a, b, c, d = bounds(root)
    s = min(w / (c-a), h / (d-b))
    tx, ty = x+(w-(c-a)*s)/2-a*s, y+(h-(d-b)*s)/2-b*s
    return f'<g transform="translate({tx:.7f} {ty:.7f}) scale({s:.9f})">{inner(root, white)}</g>'


def document(body, box, label):
    return (f'<svg xmlns="{NS}" viewBox="{box}" role="img" aria-label="{escape(label)}">'
            f'<title>{escape(label)} — DRAFT</title><desc>{DRAFT}. '
            'Working Instrument Sans title-case companion, weight 470, optically spaced original glyph outlines. '
            'No logo, palette, typography or production specification is approved.</desc>'+body+'</svg>\n')


def main():
    OUT.mkdir(exist_ok=True)
    type_root = ROOT / 'type-study'
    data = json.loads((type_root/'metadata.json').read_text())
    style = data['specimens'][0]
    name = read_art(type_root/style['twoLineFile'])
    # Centre each complete line independently for the vertical arrangement.
    letters = list(name.iter(f'{{{NS}}}path'))
    assert ''.join(p.get('data-letter', '') for p in letters) == 'TabernacleofPraise'
    centered = ET.Element(f'{{{NS}}}svg', {'viewBox': '0 0 531.0375 243'})
    for line in (letters[:10], letters[10:]):
        test = ET.Element(f'{{{NS}}}svg')
        for path in line:
            test.append(deepcopy(path))
        a, b, c, d = bounds(test)
        group = ET.SubElement(centered, f'{{{NS}}}g', {'fill': '#000000', 'transform': f'translate({265.51875-(a+c)/2:.7f} 0)'})
        for path in line:
            group.append(deepcopy(path))
    records = []
    for slug, title, factor in [('shared-rhythm', 'Shared Rhythm', 1), ('open-praise', 'Open Praise', .93)]:
        mark = read_art(ROOT/slug/'primary.svg')
        lockups = {}
        for reverse in (False, True):
            horizontal = fit(mark, (20, 128-98*factor, 204, 196*factor), reverse)
            horizontal += fit(name, (270, 53, 385, 150), reverse)
            stacked = fit(mark, (80, 127-105*factor, 240, 210*factor), reverse)
            stacked += fit(centered, (61, 269, 278, 100), reverse)
            for kind, body, box in [('horizontal', horizontal, '0 0 680 256'), ('stacked', stacked, '0 0 400 410')]:
                suffix = '-reverse' if reverse else ''
                key = kind+'Reverse' if reverse else kind
                file = f'{slug}-{kind}{suffix}-DRAFT.svg'
                if reverse:
                    _, _, w, h = box.split()
                    body = f'<rect width="{w}" height="{h}" fill="#000000"/>'+body
                (OUT/file).write_text(document(body, box, f'{title} / Tabernacle of Praise / {kind}{suffix}'))
                lockups[key] = 'exports/'+file
        wordmark = f'{slug}-wordmark-DRAFT.svg'
        (OUT/wordmark).write_text(document(fit(centered, (18, 18, 384, 126)), '0 0 420 162', f'{title} / full parish name'))
        lockups['wordmark'] = 'exports/'+wordmark
        records.append({'id': slug, 'name': title, 'primaryFile': f'{slug}/primary.svg', 'compactFile': f'{slug}/compact.svg',
                        'reverseFile': f'{slug}/reverse.svg', 'compactReverseFile': f'{slug}/compact-reverse.svg',
                        'viewBox': '0 0 256 256', 'inkBounds': bounds(mark), 'lockups': lockups,
                        'practicalSymbolScale': factor})
    result = {'status': DRAFT, 'approval': False, 'lettering': {
        'classification': 'Font-based, shaped and optically spaced; original glyph contours, not custom-drawn type.',
        'family': 'Instrument Sans', 'axes': style['axes'], 'study': 'type-study/metadata.json',
        'source': 'type-study/'+style['twoLineFile'], 'license': 'type-study/'+style['licenseFile'],
        'reason': 'Working title case retains readable word shapes and warmth. All three alternatives remain open.'},
        'comparison': 'Overview symbols have equal actual ink height. Practical lockups reduce the denser Open Praise symbol 7% at equal name scale; no nonuniform scaling.',
        'spacing': 'Stacked symbol and name have at least 37 SVG units of separation in a 400×410 study. These are draft arrangements, not production standards.',
        'compact': 'Tiny-use 16–20 px candidates only. Primary masters remain in avatars, signage, documents and normal social applications.',
        'rccg': 'Authorized original PNG absent; no actual RCCG pairing or reconstructed emblem.', 'directions': records}
    (OUT/'development-artwork.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print('Built 10 outlined lockups and development-artwork.json for both directions.')


if __name__ == '__main__':
    main()
