#!/usr/bin/env python3
"""Enlarge the intact RCCG reference in existing editable paired layouts."""
from pathlib import Path
from io import BytesIO
import base64
import hashlib
import json
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
REPO = HERE.parents[3]
LAYOUT = json.loads((HERE / 'layout.json').read_text())
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)


def main():
    exports = STUDY / 'exports'
    exports.mkdir(parents=True, exist_ok=True)
    reference = (REPO / LAYOUT['reference']).read_bytes()
    assert hashlib.sha256(reference).hexdigest() == LAYOUT['referenceSHA256']
    image = Image.open(BytesIO(reference))
    bounds = image.getbbox()
    side = LAYOUT['emblemImageSizeAfter']
    ratio = side / image.width
    cx, cy = LAYOUT['emblemVisibleCenter']
    x = cx - (bounds[0] + bounds[2]) / 2 * ratio
    y = cy - (bounds[1] + bounds[3]) / 2 * ratio
    panel_side = LAYOUT['whitePanelSize']
    records = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox', '--disable-dev-shm-usage'])
        page = browser.new_page()
        page.set_content('<canvas id="stage"></canvas>')
        for direction in LAYOUT['directions']:
            for shape, size in LAYOUT['formats'].items():
                source = REPO / LAYOUT['sourceStudy'] / 'exports' / f"{direction['id']}-RCCG-motion-{shape}-end-DRAFT.svg"
                original = ET.parse(source).getroot()
                tree = ET.parse(source).getroot()
                seal = next(tree.iter(f'{{{NS}}}image'))
                for key, value in {'x': x, 'y': y, 'width': side, 'height': side}.items():
                    seal.set(key, str(value))
                panel = next(node for node in tree.iter(f'{{{NS}}}rect') if node.get('fill', '').upper() == '#FFFFFF')
                for key, value in {'x': cx-panel_side/2, 'y': cy-panel_side/2, 'width': panel_side, 'height': panel_side}.items():
                    panel.set(key, str(value))
                next(tree.iter(f'{{{NS}}}title')).text = direction['name'] + ' — larger separate RCCG seal — DRAFT'
                next(tree.iter(f'{{{NS}}}desc')).text = 'DRAFT — NOT FOR PUBLICATION. RCCG reference enlarged to nearly the complete parish logo height, with its original PNG payload unchanged. Parish artwork and full name below preserved; entire pairing recentered. Static size exploration, not final approval or a high-resolution emblem master.'
                pairing = next(node for node in tree.iter(f'{{{NS}}}g') if node.get('data-part') == 'pairing')
                pairing.set('transform', f"translate({size['sceneX']} {size['sceneY']}) scale({size['sceneScale']})")
                original_paths = [node.attrib for node in original.iter(f'{{{NS}}}path')]
                assert [node.attrib for node in tree.iter(f'{{{NS}}}path')] == original_paths
                assert [node.attrib for node in original.iter(f'{{{NS}}}g') if node.get('data-part') != 'pairing'] == [node.attrib for node in tree.iter(f'{{{NS}}}g') if node.get('data-part') != 'pairing']
                assert ''.join(node.get('data-letter', '') for node in tree.iter(f'{{{NS}}}path')) == 'TabernacleofPraise'
                href = seal.get('href') or seal.get('{http://www.w3.org/1999/xlink}href')
                assert base64.b64decode(href.split(',')[1]) == reference
                assert not list(tree.iter(f'{{{NS}}}clipPath')) and not list(tree.iter(f'{{{NS}}}mask'))
                stem = f"{direction['id']}-RCCG-larger-{shape}-DRAFT"
                svg = exports / (stem + '.svg')
                svg.write_text(ET.tostring(tree, encoding='unicode'))
                raw = base64.b64encode(svg.read_bytes()).decode()
                encoded = page.evaluate('''async([raw,w,h])=>{const c=document.getElementById('stage');c.width=w;c.height=h;const im=new Image();await new Promise((r,j)=>{im.onload=r;im.onerror=j;im.src='data:image/svg+xml;base64,'+raw});c.getContext('2d').drawImage(im,0,0);return c.toDataURL('image/png').split(',')[1]}''', [raw, size['width'], size['height']])
                png = svg.with_suffix('.png')
                png.write_bytes(base64.b64decode(encoded))
                assert Image.open(png).size == (size['width'], size['height'])
                records.append({'concept': direction['id'], 'format': shape, 'source': str(source.relative_to(REPO)), 'sourceSHA256': hashlib.sha256(source.read_bytes()).hexdigest(), 'svg': str(svg.relative_to(STUDY)), 'png': str(png.relative_to(STUDY)), 'pngSHA256': hashlib.sha256(png.read_bytes()).hexdigest(), 'visibleEmblemHeight': round((bounds[3]-bounds[1])*ratio*size['sceneScale'], 3), 'completeParishLogoHeight': round(direction['completeLogoHeight']*size['sceneScale'], 3), 'parishSymbolHeight': round(direction['symbolInkHeight']*size['sceneScale'], 3), 'emblemImageDisplaySize': side*size['sceneScale']})
        browser.close()
    board = Image.new('RGB', (1200, 710), '#F6F3EC')
    draw = ImageDraw.Draw(board)
    font_path = REPO / 'brand/explorations/identity-development-09/type-study/fonts/instrumentsans/InstrumentSans[wdth,wght].ttf'
    def label(text, xy, size):
        draw.text(xy, text, font=ImageFont.truetype(str(font_path), size), fill='#10494C')
    label('RCCG enlarged to balance the complete parish logo', (40, 24), 30)
    label('Shared Rhythm', (40, 76), 23)
    label('Open Praise', (620, 76), 23)
    for direction, x_pos in zip(LAYOUT['directions'], (40, 620)):
        png = exports / f"{direction['id']}-RCCG-larger-square-DRAFT.png"
        im = Image.open(png).convert('RGB').resize((540, 540), Image.Resampling.LANCZOS)
        board.paste(im, (x_pos, 116))
    label('DRAFT — NOT FOR PUBLICATION', (40, 675), 18)
    board.save(exports / 'larger-RCCG-comparison-DRAFT.png')
    (exports / 'manifest.json').write_text(json.dumps({'status': LAYOUT['status'], 'finalApproval': False, 'referenceSHA256': LAYOUT['referenceSHA256'], 'referenceBytesPreserved': True, 'allParishPathsInternalTransformsAndNamePreserved': True, 'increasePercent': LAYOUT['increasePercent'], 'records': records, 'note': 'Existing 236px reference is displayed larger for proportion review; no additional source detail or production-master status is claimed. Motion 14 files retain their preceding proportions.'}, ensure_ascii=False, indent=2)+'\n')
    print('Rendered 4 updated PNG/SVG pairs and comparison; original RCCG bytes and all parish artwork preserved.')


if __name__ == '__main__':
    main()
