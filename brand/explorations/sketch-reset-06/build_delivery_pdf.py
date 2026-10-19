#!/usr/bin/env python3
"""Place existing rough PNGs unchanged on three printable review pages."""
from pathlib import Path
import base64
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
BOARDS = [('01-cadenced-roughs.png', '01 / Cadenced Wall roughs A–D'),
          ('02-new-construction-roughs.png', '02 / New construction roughs 1–6'),
          ('03-lettering-roughs.png', '03 / Lettering and alternative starts A–F')]


def main():
    sections = []
    for file, title in BOARDS:
        data = base64.b64encode((ROOT / 'exports' / file).read_bytes()).decode('ascii')
        sections.append(f'<section><header><span>Tabernacle of Praise / Sketch reset 06</span><span>{title}</span></header><img src="data:image/png;base64,{data}" alt="{title}"><footer><strong>DRAFT — NOT FOR PUBLICATION</strong><span>Raw ideation, including rejected sketches. No direction selected.</span></footer></section>')
    html = '''<!doctype html><html lang="en"><meta charset="utf-8"><title>Tabernacle of Praise — rough sketch boards</title><style>
    @page{size:A4 landscape;margin:0}*{box-sizing:border-box}body{margin:0;font:11px Arial,sans-serif;color:#111;background:white}section{width:297mm;height:210mm;padding:9mm 12mm;display:flex;flex-direction:column;break-after:page}section:last-child{break-after:auto}header,footer{display:flex;align-items:center;justify-content:space-between;gap:20px;height:10mm;flex-shrink:0}footer{font-size:10px}img{display:block;width:273mm;height:172mm;object-fit:contain;flex-shrink:0}
    </style>''' + ''.join(sections) + '</html>'
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox', '--disable-dev-shm-usage'])
        page = browser.new_page()
        page.set_content(html, wait_until='load')
        assert page.locator('img').evaluate_all('(els)=>els.every(e=>e.complete&&e.naturalWidth>1000)')
        page.pdf(path=str(ROOT / 'exports/sketch-boards-06.pdf'), print_background=True, prefer_css_page_size=True)
        browser.close()
    print('Created three-page PDF from the unchanged PNGs.')


if __name__ == '__main__':
    main()
