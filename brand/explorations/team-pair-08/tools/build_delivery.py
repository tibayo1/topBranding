#!/usr/bin/env python3
"""Render a three-page draft comparison from frozen SVG artwork, without redrawing it."""
from pathlib import Path
from html import escape
import base64
import hashlib
import json
import re
from playwright.sync_api import sync_playwright
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'exports'
DATA = json.loads((OUT / 'review-artwork.json').read_text())
DRAFT = 'DRAFT — NOT FOR PUBLICATION'

NOTES = {
    'shared-rhythm': {
        'role': 'User-favoured direction · refinement',
        'meaning': 'Four folded faces hold a shared open space. Their uneven rise and fall suggests a gathered community responding in praise.',
        'risk': 'May resemble architecture, a cultural venue or a property identity. Praise remains abstract.',
        'sizes': 'At 16 px, two adjacent faces touch through antialiasing. Four separate faces survive at 24 px and above; spatial depth is clearest at 32 px and above.',
        'prompt': 'Does the open gathering space and cadence communicate the right feeling?',
    },
    'second-direction': {
        'role': 'New contrasting proposal · for review',
        'meaning': 'A P-like outer contour holds an open negative T. Tabernacle and Praise meet through one counterform, with the opening suggesting welcome.',
        'risk': 'The two letters may not be equally obvious at first glance. The monogram may suggest a publisher, creative studio or luxury identity.',
        'sizes': 'The broad opening survives these samples. At 16 px, the tapered hook softens; 24–32 px gives clearer letter reading. The T remains a reading to test.',
        'prompt': 'Can you discover the T without the explanation, and does the mark feel suitable for the church?',
    },
}


def uri(path):
    path = ROOT / path
    mime = 'image/svg+xml' if path.suffix == '.svg' else 'image/png'
    return 'data:' + mime + ';base64,' + base64.b64encode(path.read_bytes()).decode()


def artwork(path, klass='', label=''):
    return f'<img class="{klass}" src="{uri(path)}" alt="{escape(label or str(path), quote=True)}">'


def page_header(title, label, page):
    return (f'<header><div class="eyebrow"><span>RCCG TABERNACLE OF PRAISE · ISTANBUL</span><span>DEVELOPMENT 08 / {page}</span></div>'
            f'<h1>{escape(title)}</h1><p class="subtitle">{escape(label)}</p></header>')


def footer(page):
    return (f'<footer><span>{DRAFT}</span><span>Symbol, companion typography and lockups remain provisional.</span><span>{page} / 3</span></footer>')


def reverse_file(row):
    return row['folder'] + '/reverse.svg'


def overview():
    cards = []
    for number, row in enumerate(DATA['directions'], 1):
        note = NOTES[row['folder']]
        cards.append(f'''<article class="overview-card">
<div class="concept-head"><h2>{number:02d} / {escape(row['name'])}</h2><p>{escape(note['role'])}</p></div>
<div class="stacked-field">{artwork(row['lockups']['stacked'], 'stacked', row['name'] + ' with Tabernacle of Praise')}</div>
<div class="overview-bottom"><div class="reverse-mini">{artwork(reverse_file(row), 'mini', row['name'] + ' in reverse')}</div><div><p>{escape(note['meaning'])}</p><p class="risk"><b>Watch:</b> {escape(note['risk'])}</p></div></div>
</article>''')
    return (f'<section class="sheet overview" id="overview">' + page_header('Two directions for discussion', 'Monochrome comparison · complete name · equal artwork conditions', 1)
            + '<main class="overview-grid">' + ''.join(cards) + '</main>'
            + '<p class="overview-note">Discuss the form first: which feels more distinctive, welcoming and appropriate for Tabernacle of Praise? No identity decision is final.</p>'
            + footer(1) + '</section>')


def native_path(row, size, reverse=False):
    if row['folder'] == 'shared-rhythm':
        return f"shared-rhythm/renders/primary-{'reverse' if reverse else 'black'}-{size}.png"
    return f"second-direction/renders/{'reverse' if reverse else 'primary'}-{size}.png"


def native_row(row, reverse=False):
    samples = []
    for size in [64, 32, 24, 16]:
        samples.append(f'<div class="sample"><div class="sample-art">{artwork(native_path(row, size, reverse), "native", f"Native-source {size} px sample") .replace("class=\"native\"", f"class=\"native\" width=\"{size}\" height=\"{size}\"")}</div><span>{size} px</span></div>')
    return '<div class="native-row' + (' reversed' if reverse else '') + '">' + ''.join(samples) + '</div>'


def detail(row, page):
    note = NOTES[row['folder']]
    anchor = 'shared-rhythm' if row['folder'] == 'shared-rhythm' else 'open-praise'
    return f'''<section class="sheet detail" id="{anchor}">
{page_header(row['name'], note['role'], page)}
<main>
<div class="hero-pair"><div class="hero light">{artwork(row['primary'], 'hero-mark', row['name'] + ' black symbol')}<span>BLACK / WHITE</span></div><div class="hero dark">{artwork(reverse_file(row), 'hero-mark', row['name'] + ' reversed symbol')}<span>WHITE / BLACK</span></div></div>
<div class="horizontal-field">{artwork(row['lockups']['horizontal'], 'horizontal', row['name'] + ' full-name horizontal lockup')}</div>
<div class="notes"><div><h3>Meaning to test</h3><p>{escape(note['meaning'])}</p></div><div><h3>Main risk</h3><p>{escape(note['risk'])}</p></div></div>
<div class="native-section"><h3>Small-size evidence</h3><div class="native-pair">{native_row(row)}{native_row(row, True)}</div><p class="size-observation">{escape(note['sizes'])}</p><p class="technical-note">Native-source PNG samples at labelled CSS widths. This board is exported at 2×; use the editable SVG or browser proof for a 1:1 pixel check.</p></div>
<p class="discussion"><b>Team question:</b> {escape(note['prompt'])}</p>
<p class="asset-note">Official RCCG emblem is separate. Its source PNG is absent; actual emblem pairing has not been verified. Instrument Sans is temporary common companion lettering.</p>
</main>{footer(page)}</section>'''


def main():
    font = base64.b64encode((ROOT / 'assets/fonts/instrumentsans/InstrumentSans[wdth,wght].ttf').read_bytes()).decode()
    css = '''
@font-face{font-family:Review;src:url(data:font/ttf;base64,FONTDATA);font-weight:100 900;font-stretch:75% 100%;font-display:block}
*{box-sizing:border-box}html,body{margin:0;padding:0;background:#e7e7e7;color:#000;font-family:Review,Arial,sans-serif;font-weight:450}img{display:block;object-fit:contain}p,h1,h2,h3{margin:0}b{font-weight:650}
.sheet{position:relative;overflow:hidden;background:#fff;break-after:page;page-break-after:always;margin:0 auto 24px;padding:33px 42px 44px}.sheet:last-child{break-after:auto;page-break-after:auto}.overview{width:1122px;height:794px;page:overview}.detail{width:794px;height:1122px;page:detail}
.eyebrow{display:flex;justify-content:space-between;gap:14px;font-size:10px;letter-spacing:1.2px;font-weight:600}.eyebrow span:last-child{white-space:nowrap}h1{font-size:34px;line-height:1.08;font-weight:550;letter-spacing:-.8px;margin-top:20px}.subtitle{font-size:13px;line-height:1.4;color:#444;margin-top:8px}footer{position:absolute;left:42px;right:42px;bottom:20px;padding-top:12px;border-top:1px solid #ccc;display:flex;align-items:center;justify-content:space-between;gap:12px;font-size:9px;line-height:1.4;color:#444}footer span:first-child{font-weight:650;letter-spacing:.45px;color:#000;white-space:nowrap}footer span:last-child{white-space:nowrap}
.overview-grid{display:grid;grid-template-columns:1fr 1fr;gap:42px;margin-top:28px}.overview-card{min-width:0}.concept-head{border-top:1px solid #bcbcbc;padding-top:13px}.concept-head h2{font-size:20px;line-height:1.15;font-weight:550}.concept-head p{font-size:11px;color:#555;line-height:1.3;margin-top:5px}.stacked-field{height:368px;display:flex;justify-content:center;align-items:center}.stacked{width:380px;height:361px}.overview-bottom{display:grid;grid-template-columns:88px 1fr;gap:16px;align-items:start}.reverse-mini{height:88px;background:#000;display:flex;align-items:center;justify-content:center}.mini{width:74px;height:74px}.overview-bottom p{font-size:12px;line-height:1.45}.overview-bottom .risk{font-size:11px;line-height:1.45;color:#444;margin-top:7px}.overview-note{position:absolute;left:42px;right:42px;bottom:69px;font-size:11px;color:#444;line-height:1.4}
.detail h1{font-size:36px}.detail .subtitle{font-size:12px}.hero-pair{margin-top:23px;display:grid;grid-template-columns:1fr 1fr;gap:16px}.hero{height:256px;display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative}.hero.light{border:1px solid #dedede}.hero.dark{background:#000;color:#fff}.hero-mark{width:240px;height:224px}.hero span{position:absolute;bottom:10px;font-size:8px;letter-spacing:1px;opacity:.68}.horizontal-field{height:213px;display:flex;align-items:center;justify-content:center}.horizontal{width:600px;height:213px}.notes{display:grid;grid-template-columns:1fr 1fr;gap:28px;border-top:1px solid #d3d3d3;padding-top:17px}.notes h3,.native-section h3{font-size:10px;text-transform:uppercase;letter-spacing:1px;font-weight:600;line-height:1.3}.notes p{font-size:13px;line-height:1.5;margin-top:7px}.native-section{margin-top:21px}.native-pair{margin-top:10px;display:grid;grid-template-columns:1fr 1fr;gap:16px}.native-row{height:106px;border:1px solid #dedede;display:flex;justify-content:space-around;padding:9px 7px 7px}.native-row.reversed{border-color:#000;background:#000;color:#fff}.sample{width:73px;display:flex;flex-direction:column;align-items:center;justify-content:space-between}.sample-art{height:66px;display:flex;align-items:center;justify-content:center}.native{image-rendering:auto;flex:none;max-width:none}.sample span{font-size:9px;opacity:.7}.size-observation{font-size:11px;line-height:1.45;margin-top:10px}.technical-note{font-size:9px;line-height:1.4;color:#555;margin-top:5px}.discussion{font-size:12px;line-height:1.45;margin-top:16px}.asset-note{font-size:9px;line-height:1.45;color:#555;margin-top:10px;max-width:680px}
@page overview{size:A4 landscape;margin:0}@page detail{size:A4 portrait;margin:0}@media print{html,body{background:#fff;print-color-adjust:exact;-webkit-print-color-adjust:exact}.sheet{margin:0}.overview{width:297mm;height:210mm}.detail{width:210mm;height:297mm}}
'''.replace('FONTDATA', font)
    body = overview() + ''.join(detail(row, index + 2) for index, row in enumerate(DATA['directions']))
    source = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Tabernacle of Praise · Team review 08 · DRAFT</title><style>' + css + '</style><body>' + body + '</body></html>'
    (OUT / 'review-source.html').write_text(source)
    reports = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox', '--disable-dev-shm-usage'])
        page = browser.new_page(viewport={'width':1200,'height':1200}, device_scale_factor=2)
        page.set_content(source, wait_until='load')
        page.evaluate('document.fonts.ready')
        for anchor, filename in [('overview','two-directions.png'),('shared-rhythm','shared-rhythm-review.png'),('open-praise','open-praise-review.png')]:
            element = page.locator('#' + anchor)
            element.screenshot(path=str(OUT / filename), animations='disabled')
            reports.append(page.evaluate('''id => {const s=document.getElementById(id),b=s.getBoundingClientRect();return {page:id,width:b.width,height:b.height,brokenImages:[...s.querySelectorAll('img')].filter(x=>!x.complete||x.naturalWidth===0).length,bodyBottom:Math.max(...[...s.querySelectorAll('main,p.asset-note,p.overview-note')].map(x=>x.getBoundingClientRect().bottom-b.top)),footerTop:s.querySelector('footer').getBoundingClientRect().top-b.top}}''',anchor))
        page.pdf(path=str(OUT / 'team-review-08.pdf'), prefer_css_page_size=True, print_background=True, display_header_footer=False)
        browser.close()
    reader = PdfReader(OUT / 'team-review-08.pdf')
    assert len(reader.pages) == 3, f'Unexpected page count: {len(reader.pages)}'
    for row in reports:
        assert row['brokenImages'] == 0, row
        assert row['bodyBottom'] < row['footerTop'] - 4, row
    print(json.dumps({'layout':reports,'pdfPages':[list(map(float,page.mediabox)) for page in reader.pages]}, indent=2))
    for name in ['two-directions.png','shared-rhythm-review.png','open-praise-review.png','team-review-08.pdf','review-source.html']:
        content = (OUT / name).read_bytes()
        print(hashlib.sha256(content).hexdigest(), name, len(content))


if __name__ == '__main__':
    main()
