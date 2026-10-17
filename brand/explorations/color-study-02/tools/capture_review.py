#!/usr/bin/env python3
"""Capture verified browser previews and a printable review of all applications.

Start the study's local HTTP server first. Optional argv[1] is its loopback URL.
"""
from pathlib import Path
import base64
from html import escape
import json
import sys

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'exports'
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8765'
OUT.mkdir(exist_ok=True)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path='/usr/bin/chromium', headless=True,
                                         args=['--no-sandbox', '--disable-dev-shm-usage'])
    page = browser.new_page(viewport={'width': 1440, 'height': 1100}, reduced_motion='reduce', device_scale_factor=1)
    page.goto(URL, wait_until='networkidle')
    page.evaluate('document.fonts.ready')
    page.evaluate('document.activeElement.blur()')
    page.mouse.move(0, 0)
    page.screenshot(path=str(OUT / 'explorer-overview.png'), full_page=True)
    page.locator('#meanings').screenshot(path=str(OUT / 'meaning-cards-desktop.png'), animations='disabled')
    page.locator('#matrix').screenshot(path=str(OUT / 'comparison-matrix.png'), animations='disabled')
    page.locator('#checks').screenshot(path=str(OUT / 'form-and-contrast.png'), animations='disabled')
    for palette in ('teal', 'navy'):
        page.locator(f'.palette-choice[data-value={palette}]').click()
        for mode in ('light', 'dark'):
            page.locator(f'[data-action=mode][data-value={mode}]').click()
            page.evaluate('document.activeElement.blur()')
            page.mouse.move(0, 0)
            page.locator('#workbench').screenshot(path=str(OUT / f'{palette}-{mode}-preview.png'), animations='disabled')
    page.locator('.palette-choice[data-value=teal]').click()
    page.locator('[data-action=mode][data-value=light]').click()
    for application in ('flyer', 'instagram', 'avatar', 'signage'):
        page.locator(f'[data-action=application][data-value={application}]').click()
        page.evaluate('document.activeElement.blur()')
        page.mouse.move(0, 0)
        page.locator('#applications').screenshot(path=str(OUT / f'application-{application}.png'), animations='disabled')
    page.set_viewport_size({'width': 390, 'height': 844})
    page.locator('#workbench').screenshot(path=str(OUT / 'mobile-workbench.png'), animations='disabled')
    page.locator('#meanings').screenshot(path=str(OUT / 'meaning-cards-mobile.png'), animations='disabled')
    page.set_viewport_size({'width': 1440, 'height': 1100})
    page.locator('[data-action=application][data-value=flyer]').click()
    data = page.evaluate('window.TOPData')
    matrix = page.locator('#matrix-rows').inner_html()

    # The printable book uses exactly the same vector generator as the app.
    # Fonts are embedded once into the review source, not duplicated in 78 SVGs.
    sans = base64.b64encode((ROOT / 'assets/noto-sans-regular.ttf').read_bytes()).decode()
    serif = base64.b64encode((ROOT / 'assets/noto-serif-regular.ttf').read_bytes()).decode()
    css = f"@font-face{{font-family:'Study Sans';src:url(data:font/ttf;base64,{sans})}}@font-face{{font-family:'Study Serif';src:url(data:font/ttf;base64,{serif})}}"
    css += """
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}body{margin:0;color:#202a2b;font-family:'Study Sans',Arial,sans-serif;background:white}.sheet{width:297mm;height:210mm;padding:11mm 13mm;page-break-after:always;overflow:hidden;position:relative}.sheet:last-child{page-break-after:auto}h1{font:32px 'Study Serif',Georgia,serif;letter-spacing:-1px;margin:5px 0 9px}p{margin:0;font-size:11px;line-height:1.7}.kicker{font-size:8px;letter-spacing:1.5px;color:#52615c;text-transform:uppercase}.note{font-size:9px;color:#52615c}.footer{position:absolute;bottom:7mm;left:13mm;right:13mm;display:flex;justify-content:space-between;border-top:1px solid #d5dcd2;padding-top:9px;font-size:8px;color:#52615c}.matrix-head,.matrix-row{display:grid;grid-template-columns:170px 1fr 1fr;gap:13px}.matrix-head{font-size:8px;margin:14px 0 5px}.matrix-row{padding:8px 0;border-top:1px solid #d8dcd5;align-items:center}.matrix-palette .eyebrow{font-size:7px;margin:0 0 4px}.matrix-palette h3{font-size:12px;margin:0}.matrix-palette>p{font-size:7px}.matrix-values{display:grid;grid-template-columns:1fr 1fr;gap:4px;margin:5px 0}.matrix-values button{font:8px 'Study Sans';border:0;padding:0;text-align:left;background:none;display:flex;gap:3px}.matrix-values i{width:6px;height:18px;display:block}.matrix-values small{display:block;font-size:5px;text-transform:uppercase}.matrix-values code{font:7px 'Study Sans'}.ratio-label{font-size:7px}.matrix-cell{display:grid;grid-template-columns:1fr 1fr;gap:6px}.matrix-sample{min-height:88px;position:relative;padding:12px 7px 10px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;border:1px solid #ddd;background:none;font-family:'Study Sans'}.matrix-sample .brand-mark{width:30px;height:30px}.brand-wordmark{font-family:'Study Sans';line-height:1.15;font-size:9px}.sample-mode{position:absolute;top:3px;left:5px;font-size:5px;text-transform:uppercase}.sample-accent{position:absolute;height:2px;bottom:0;left:0;right:0}.studies{display:grid;grid-template-columns:1fr 1fr;gap:17px;margin-top:15px}.study{min-width:0}.study h2{font:12px 'Study Sans';margin:0 0 9px}.study svg{display:block;margin:auto;max-width:100%;width:auto;max-height:535px}.application-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:20px}.application-grid h2{font:11px 'Study Sans';margin:0 0 8px}.application-grid p{font-size:8px;margin-top:8px}.application-grid svg{max-width:100%;height:auto;max-height:470px;display:block}.application-grid.avatar svg{border-radius:50%;margin-top:65px}.application-grid.signage{grid-template-columns:1fr 1fr}.application-grid.signage svg{max-height:235px}.application-grid.signage .study h2{margin-top:5px}.review-copy{display:grid;grid-template-columns:1fr 1fr;gap:35px;margin-top:35px}.review-copy h2{font:24px 'Study Serif';margin:0 0 12px}.review-copy p{font-size:14px;line-height:1.9}.review-copy li{font-size:12px;line-height:1.9;margin:8px 0}svg text{font-synthesis:none}button{color:inherit}*{-webkit-print-color-adjust:exact;print-color-adjust:exact}
"""
    css += """
.matrix-row{height:96px;padding:6px 0}.matrix-palette{font-size:8px;line-height:1.1}.matrix-palette .eyebrow{display:block;font-size:6px;line-height:1.2;margin-bottom:2px}.matrix-palette h3{font-size:11px;line-height:1.2}.matrix-palette>p{display:none}.matrix-values{margin:5px 0;gap:3px}.matrix-sample{height:82px;min-height:0;padding:10px 5px}.ratio-label{font-size:6px}
.matrix-head,.matrix-row{grid-template-columns:150px repeat(3,minmax(0,1fr));gap:10px}.application-grid{grid-template-columns:repeat(6,minmax(0,1fr));gap:12px}.application-grid h2{font-size:9px;line-height:1.4;min-height:28px}.application-grid p{font-size:7px;line-height:1.5}.application-grid.avatar svg{margin-top:45px}.application-grid.signage{grid-template-columns:repeat(3,minmax(0,1fr));column-gap:16px;row-gap:12px}.application-grid.signage svg{max-height:175px;width:100%;height:auto}.application-grid.signage .study h2{margin-top:0}.review-copy{margin-top:23px;gap:30px}.review-copy h2{font-size:21px}.review-copy p{font-size:12px;line-height:1.8}.review-copy li{font-size:11px;line-height:1.7;margin:7px 0}
"""
    footer = '<div class="footer"><span>DRAFT — NOT FOR PUBLICATION · No logo, palette, or typography is approved.</span><span>Tabernacle of Praise / Color study 02</span></div>'
    sheets = ['<section class="sheet"><p class="kicker">RCCG TABERNACLE OF PRAISE · ISTANBUL, TÜRKİYE</p><h1>Three concepts. Five color directions.</h1><p>B/C retain their existing geometry; D introduces a new original shared-space direction. Equal presentation conditions. Light and dark for every palette. Proposed HEX values.</p><div class="matrix-head"><span>PALETTE / ROLE VALUES</span><span>B / SANCTUARY STRINGS</span><span>C / PRAISE LIGATURE</span><span>D / RESONANT SANCTUARY</span></div>' + matrix + footer + '</section>']
    render_page = browser.new_page(viewport={'width': 1500, 'height': 1500}, reduced_motion='reduce')
    render_page.goto(URL, wait_until='networkidle')
    render_page.evaluate('document.fonts.ready')
    for application, title in [('flyer', 'Sunday service flyer'), ('instagram', 'Instagram post'), ('avatar', 'Social media avatar'), ('signage', 'Church signage study')]:
        for mode in ('light', 'dark'):
            cards = []
            for palette_id in ('teal', 'navy'):
                palette = next(item for item in data['palettes'] if item['id'] == palette_id)
                for concept in data['concepts']:
                    svg = page.evaluate('(options) => window.TOPApplications.render(options)', {'type': application, 'palette': palette, 'concept': concept, 'mode': mode})
                    cards.append(f'<article class="study"><h2>{concept["id"]} / {escape(concept["name"])}</h2>{svg}<p>{escape(palette["name"])} / {mode}</p></article>')
            sheets.append(f'<section class="sheet"><p class="kicker">SHORTLISTED PALETTES / {mode.upper()} TREATMENT</p><h1>{title}</h1><p class="note">Editable vector layout study. Bracketed event information is a placeholder; typography is a shared provisional specimen.</p><div class="application-grid {application}">{"".join(cards)}</div>{footer}</section>')
    sheets.append('<section class="sheet"><p class="kicker">RECOMMENDATIONS FOR DISCUSSION</p><h1>Two palettes. Three concepts to weigh.</h1><div class="review-copy"><div><h2>1 / Teal & sand</h2><p>The strongest contemporary distinction with tactile warmth. Keep sand as a surface and gold as a measured accent.</p><h2 style="margin-top:24px">2 / Navy & gold</h2><p>A dignified, dependable alternative with a strong dark-on-light foundation. Familiar territory; the mark must supply distinction.</p><h2 style="margin-top:24px">What the marks visibly communicate</h2><p>B is a harp-led musical direction; its shelter association is weaker. C identifies the name through a T/P monogram. D encloses shared space and opens into three rising bands, suggesting praise through rhythm. These are design intentions, not established church doctrine.</p></div><div><h2>C / Current durability benchmark</h2><p>C remains the current benchmark for a durable identifier, with its T/P channel and editorial character still open to refinement. B needs a small-size string solution.</p><h2 style="margin-top:24px">D / New shared-space challenger</h2><p>D gives the sacred-dwelling association more visual weight. Its enclosing surround and rising bands connect shared space with praise, although the bands can also suggest leaves or growth. No replacement is approved.</p><ul><li>The official RCCG emblem remains separate; an authorized source asset is pending.</li><li>Screen HEX values require real print and material proofing.</li><li>Final geometry, typography, palette, and approval remain open.</li></ul></div></div>' + footer + '</section>')
    review = '<!doctype html><html><head><meta charset="utf-8"><title>Tabernacle of Praise — Draft color review</title><style>' + css + '</style></head><body>' + ''.join(sheets) + '</body></html>'
    (OUT / 'printable-review.html').write_text(review)
    render_page.set_content(review, wait_until='networkidle')
    render_page.evaluate('document.fonts.ready')
    overlaps = render_page.evaluate('''() => [...document.querySelectorAll('.sheet')].map((sheet,index) => {
      const footer = sheet.querySelector('.footer').getBoundingClientRect();
      const children = [...sheet.children].filter(child => !child.classList.contains('footer'));
      const bottom = Math.max(...children.map(child => child.getBoundingClientRect().bottom));
      return {page:index+1, overlap:bottom > footer.top-2};
    }).filter(result => result.overlap)''')
    assert not overlaps, f'Review content overlaps footer: {overlaps}'
    assert render_page.locator('.sheet').count() == 10
    assert render_page.locator('.application-grid').count() == 8
    for gallery in render_page.locator('.application-grid').all():
        assert gallery.locator('.study').count() == 6
        sizes = gallery.locator('svg').evaluate_all('(elements) => elements.map(element => [element.getBoundingClientRect().width,element.getBoundingClientRect().height])')
        assert all(all(abs(value - reference) < .1 for value, reference in zip(size, sizes[0])) for size in sizes), f'Unequal application sizes: {sizes}'
    render_page.pdf(path=str(OUT / 'color-study-review.pdf'), print_background=True, prefer_css_page_size=True)
    browser.close()
print('Captured matrix, workbench light/dark, application galleries, mobile preview, and printable review PDF.')
