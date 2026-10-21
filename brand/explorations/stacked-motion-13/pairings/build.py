#!/usr/bin/env python3
"""Pair the unchanged RCCG reference beside each name-below parish layout."""
from pathlib import Path
from html import escape
import base64
import hashlib
import json
import xml.etree.ElementTree as ET

import fitz
from playwright.sync_api import sync_playwright


HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
REPO = STUDY.parents[2]
PREVIOUS = STUDY.parent / 'teal-refinement-11'
ASSET = REPO / 'brand/assets/rccg-emblem/references/rccg-wayforward-reference.png'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
DRAFT = 'DRAFT — NOT FOR PUBLICATION'


def uri(path):
    mime = 'image/svg+xml' if path.suffix == '.svg' else 'image/png'
    return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode()


def make_pair(direction, mode):
    key = 'stackedReverse' if mode == 'dark' else 'stacked'
    source = PREVIOUS / direction['lockups'][key]
    tree = ET.parse(source).getroot()
    for child in list(tree):
        if child.tag.rsplit('}', 1)[-1] in ('title', 'desc', 'rect'):
            tree.remove(child)
    parish = ''.join(ET.tostring(child, encoding='unicode') for child in tree)
    bg = '#10494C' if mode == 'dark' else '#FFFFFF'
    panel = '<rect x="139" y="66" width="212" height="212" fill="#FFFFFF"/>' if mode == 'dark' else ''
    image = f'<image x="155" y="82" width="180" height="180" preserveAspectRatio="xMidYMid meet" href="{uri(ASSET)}"/>'
    body = f'<rect width="960" height="500" fill="{bg}"/>' + panel + image
    body += f'<g transform="translate(465 45)">{parish}</g>'
    title = f'{direction["name"]}: full name below parish symbol, separate RCCG reference / {mode}'
    svg = (f'<svg xmlns="{NS}" viewBox="0 0 960 500" role="img" aria-label="{escape(title)}">'
           f'<title>{escape(title)} — DRAFT</title><desc>{DRAFT}. '
           'Full parish name remains beneath the symbol. Original refinement 11 paths and internal transforms preserved. '
           'The RCCG PNG is the existing parish-source reference, embedded byte-for-byte in full color, '
           'with no cropping, recoloring, masking, background removal or regeneration. '
           'Final lockup, original-upload integrity and production approval remain open.</desc>' + body + '</svg>\n')
    return svg, source


def make_html(records):
    columns = []
    for slug, name in [('shared-rhythm', 'Shared Rhythm'), ('open-praise', 'Open Praise')]:
        panels = []
        for mode in ('light', 'dark'):
            row = next(r for r in records if r['id'] == slug and r['mode'] == mode)
            panels.append(f'<div class="label">{mode.title()} background</div><img class="pair" src="{uri(HERE / row["file"])}" alt="{name}, name below symbol, {mode} pairing">')
        columns.append(f'<article><h2>{name}</h2>' + ''.join(panels) + '</article>')
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Tabernacle of Praise / name below / RCCG pairing draft</title><style>
*{box-sizing:border-box}body{margin:0;background:#eee;color:#10494C;font-family:Arial,Helvetica,sans-serif}h1,h2,p{margin:0}.sheet{width:1122px;height:930px;background:#F6F3EC;padding:31px 42px 50px;position:relative;overflow:hidden}.eyebrow{display:flex;justify-content:space-between;font-size:10px;letter-spacing:1px;color:#5f6d65}h1{font-size:32px;font-weight:500;letter-spacing:-.5px;line-height:1.08;margin-top:20px}.sub{font-size:13px;line-height:1.5;color:#627169;margin-top:10px}.columns{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:25px}h2{font-weight:500;font-size:21px;border-top:1px solid #bdc7be;padding-top:12px;margin-bottom:15px}.label{font-size:10px;color:#65736a;margin-top:11px;margin-bottom:7px}.pair{display:block;width:100%;height:auto;border:1px solid #d8ded8}.note{font-size:11px;line-height:1.55;color:#5f6f65;margin-top:20px;max-width:990px}footer{position:absolute;left:42px;right:42px;bottom:20px;border-top:1px solid #bac7bd;padding-top:10px;display:flex;justify-content:space-between;gap:18px;font-size:9px;line-height:1.4;color:#66746b}footer strong{color:#10494C}@page{size:297mm 246mm;margin:0}@media print{body{background:#F6F3EC;print-color-adjust:exact;-webkit-print-color-adjust:exact}.sheet{width:297mm;height:246mm}}
</style></head><body><section class="sheet" id="comparison"><header><div class="eyebrow"><span>RCCG TABERNACLE OF PRAISE · ISTANBUL</span><span>NAME-BELOW UPDATE / 13</span></div><h1>The full name sits below each parish symbol</h1><p class="sub">Shared Rhythm and Open Praise · separate RCCG reference · light and dark</p></header><div class="columns">''' + ''.join(columns) + '''</div><p class="note">Both parish names keep the same centered two-line arrangement. The complete RCCG reference remains independent, in its original colors. A padded white panel protects the full image on teal; the parish symbol and name reverse to ivory.</p><footer><strong>DRAFT — NOT FOR PUBLICATION</strong><span>Unchanged 236×236 parish-source emblem reference. Final source authorization and production lockup approval remain open.</span></footer></section></body></html>'''


def main():
    data = json.loads((PREVIOUS / 'exports/artwork.json').read_text())
    records = []
    for direction in data['directions']:
        for mode in ('light', 'dark'):
            raw, source = make_pair(direction, mode)
            name = f'{direction["id"]}-stacked-{mode}-pairing-DRAFT.svg'
            path = HERE / name
            path.write_text(raw)
            records.append({'id': direction['id'], 'name': direction['name'], 'mode': mode, 'file': name,
                            'parishSource': source.relative_to(REPO).as_posix(),
                            'parishSHA256': hashlib.sha256(source.read_bytes()).hexdigest()})
    source = make_html(records)
    (HERE / 'comparison-source.html').write_text(source)
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox', '--disable-dev-shm-usage'])
        page = browser.new_page(viewport={'width': 1200, 'height': 1000}, device_scale_factor=2)
        page.set_content(source, wait_until='load')
        layout = page.evaluate('''()=>({broken:[...document.images].filter(i=>!i.complete||!i.naturalWidth).length,noteBottom:document.querySelector('.note').getBoundingClientRect().bottom,footerTop:document.querySelector('footer').getBoundingClientRect().top})''')
        assert layout['broken'] == 0, layout
        assert layout['noteBottom'] < layout['footerTop'] - 5, layout
        page.locator('#comparison').screenshot(path=str(HERE / 'stacked-pairing-comparison.png'))
        page.pdf(path=str(HERE / 'stacked-pairing-review.pdf'), prefer_css_page_size=True, print_background=True)
        browser.close()
    with fitz.open(HERE / 'stacked-pairing-review.pdf') as pdf:
        assert len(pdf) == 1
    asset_bytes = ASSET.read_bytes()
    for row in records:
        root = ET.parse(HERE / row['file']).getroot()
        embedded = list(root.iter(f'{{{NS}}}image'))
        assert len(embedded) == 1
        assert base64.b64decode(embedded[0].get('href').split(',', 1)[1]) == asset_bytes
        assert not list(root.iter(f'{{{NS}}}clipPath')) and not list(root.iter(f'{{{NS}}}mask'))
        original = ET.parse(REPO / row['parishSource']).getroot()
        assert [p.get('d') for p in root.iter(f'{{{NS}}}path')] == [p.get('d') for p in original.iter(f'{{{NS}}}path')]
        assert ''.join(p.get('data-letter', '') for p in root.iter(f'{{{NS}}}path')) == 'TabernacleofPraise'
    result = {'status': DRAFT, 'finalApproval': False, 'namePlacement': 'Centered below each parish symbol; complete Tabernacle of Praise name.',
              'emblem': {'file': ASSET.relative_to(REPO).as_posix(), 'sha256': hashlib.sha256(asset_bytes).hexdigest(), 'sourceDimensions': [236, 236], 'displayDimensions': [180, 180], 'originalChatUploadVerified': False},
              'layout': {'viewBox': [0, 0, 960, 500], 'emblemXY': [155, 82], 'parishTranslation': [465, 45], 'emblemAlignment': 'Centered on the parish symbol, with parish name below.'},
              'entries': records, 'checks': {'allParishPathsPreserved': True, 'allFullNamesComplete': True, 'allEmblemBytesPreserved': True, 'noEmblemClipOrMask': True, 'pdfPages': 1, 'renderLayout': layout}}
    (HERE / 'manifest.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print('Built four stacked parish/RCCG pairings, comparison PNG, one-page PDF and source manifest.')


if __name__ == '__main__':
    main()
