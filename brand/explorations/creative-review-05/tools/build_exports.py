#!/usr/bin/env python3
"""Render exact review artwork into visible draft PNG and PDF review documents.

Reads the current review-data.json; does not change direction masters or review data.
The browser review remains the source for native CSS-pixel tests and applications.
"""
from __future__ import annotations
import asyncio,base64,hashlib,json,re
from html import escape
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'exports'
DRAFT='DRAFT — NOT FOR PUBLICATION'

def art(mark,box,reverse=False):
    # Only ink is reversed. Every original path, counter, transform and proportion stays.
    if reverse:
        mark=re.sub(r'(?:#000000|#111111|#111\b|currentColor|\bblack\b)','#ffffff',mark,flags=re.I)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{box}" aria-hidden="true">{mark}</svg>'

def font_data(file):
    return base64.b64encode((ROOT/'assets'/file).read_bytes()).decode()

def overview(directions):
    cards=[]
    for d in directions:
        cards.append(f'''<article class="overview-card">
          <div class="card-label"><b>{d['id']}</b><span>{escape(d['title'])}</span></div>
          <h2>{escape(d['name'])}</h2>
          <div class="overview-art">{d['lockups']['stacked']}</div>
          <p>{escape(SHORT[d['id']])}</p>
        </article>''')
    return f'''<section class="overview sheet" id="overview">
      <header><div class="eyebrow">RCCG TABERNACLE OF PRAISE · CREATIVE REVIEW 05</div>
        <h1>Five directions. One shared name.</h1><p class="subhead">Equal conditions. Black and white. No logo, color or typography approval.</p></header>
      <div class="overview-grid">{''.join(cards)}</div>
      <footer><span>{DRAFT}</span><span>Meaning, construction and open questions follow.</span></footer>
    </section>'''

SHORT={
 'A':'A shared cross-shaped interior, held open by two folded boundaries.',
 'B':'The sheltering surfaces themselves turn outward in expression.',
 'C':'A crafted TP identifier held within an open enclosing roundel.',
 'D':'The complete name, with a repeatable grammar of custom counters.',
 'E':'A joined architectural face develops cadence through its openings.',
}
SCALE={
 'A':'Cross holds at 16 px; threshold is clearer at 24 px and above.',
 'B':'24 px better preserves the held interior; 16 px favors the wave reading.',
 'C':'32 px is the more credible TP test; tiny letters and reverse crowd.',
 'D':'Tested at 320/240 px wide. A very small avatar remains unresolved.',
 'E':'32 px best retains the measured cuts; the finer cut merges at 16 px.',
}
CONSTRUCTION={
 'A':'Two filled boundaries give the crossing its shape. The lower threshold remains open.',
 'B':'The return is integral to the shelter. A passing cut keeps the two surfaces visibly apart.',
 'C':'The roundel and the original T/P paths are separate, related contours.',
 'D':'Six original letter drawings: T, P, a, e, r and f. Other letters retain licensed Source Serif 4 outlines.',
 'E':'One compound face. Real removed material makes the openings; the lower threshold stays open.',
}

def detail(d):
    parts=''.join(f'<figure><div class="part-art">{art(p["mark"],p["viewBox"])}</div><figcaption>{escape(p["label"])}</figcaption></figure>' for p in d['parts'])
    sketches=[]
    for s in d['sketches']:
        sketches.append(f'''<figure class="sketch {'selected' if s.get('selected') else ''}">
         <div class="sketch-art">{art(s['mark'],s['viewBox'])}</div>
         <figcaption><b>{escape(s['id'])} · {escape(s['name'])}</b><span>{'DEVELOPED PREMISE' if s.get('selected') else 'ALTERNATIVE PREMISE'}</span></figcaption>
        </figure>''')
    return f'''<section class="direction sheet" id="direction-{d['id'].lower()}">
      <header class="direction-heading"><span class="direction-id">{d['id']}</span><div><div class="eyebrow">{escape(d['title'])}</div><h1>{escape(d['name'])}</h1></div><div class="review-state">CREATIVE REVIEW 05<br>DRAFT</div></header>
      <div class="primary-pair"><div class="primary white">{art(d['mark'],d['viewBox'])}<span>POSITIVE</span></div><div class="primary black">{art(d['mark'],d['viewBox'],True)}<span>REVERSE</span></div></div>
      <div class="name-lockup">{d['lockups']['horizontal']}</div>
      <div class="meaning-grid"><div><h3>The idea</h3><p>{escape(d['meaning'])}</p></div><div><h3>The open question</h3><p>{escape(d['risk'])}</p></div></div>
      <section class="construction"><div class="section-heading"><h3>Construction &amp; negative space</h3><p>{escape(CONSTRUCTION[d['id']])}</p></div><div class="parts">{parts}</div></section>
      <section class="sketches"><h3>Initial constructions · {len(d['sketches'])} distinct premises</h3><div class="sketch-grid count-{len(d['sketches'])}">{''.join(sketches)}</div></section>
      <div class="scale-note"><b>Scale limit</b><span>{escape(SCALE[d['id']])}</span><small>Native-size proofs and application studies are in the interactive review.</small></div>
      <footer><span>{DRAFT}</span><span>{d['id']} · Tabernacle of Praise · No approval</span></footer>
    </section>'''

CSS='''
*{box-sizing:border-box}html,body{margin:0;background:#d9d9d7;color:#111}body{font-family:ReviewSans,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}svg{display:block;width:100%;height:100%;overflow:visible}h1,h2,h3,p,figure{margin:0}h1,h2{font-weight:500;letter-spacing:-.04em}h3{font-size:11px;letter-spacing:.055em;text-transform:uppercase;font-weight:600}.sheet{position:relative;background:#fff;break-after:page;overflow:hidden}.sheet:last-child{break-after:auto}.eyebrow{font-size:10px;letter-spacing:.12em;font-weight:600;text-transform:uppercase}.overview{width:1122px;height:794px;padding:36px 42px;page:overview}.overview h1{font-size:40px;line-height:1.15;margin-top:9px}.subhead{font-size:13px;color:#555;margin-top:9px}.overview-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:13px;margin-top:25px}.overview-card{grid-column:span 2;height:276px;background:#fafafa;border:1px solid #e4e4e4;padding:16px 18px 12px}.overview-card:nth-child(4){grid-column:2/span 2}.overview-card:nth-child(5){grid-column:4/span 2}.card-label{display:flex;gap:10px;align-items:baseline;font-size:9px;text-transform:uppercase;letter-spacing:.07em;color:#555}.card-label b{font-size:16px;color:#111}.overview-card h2{font-size:21px;line-height:1.2;margin-top:3px}.overview-art{height:168px;padding:10px 5px 5px}.overview-card p{font-size:10px;line-height:1.35;color:#555;margin-top:3px}.sheet footer{position:absolute;bottom:17px;left:42px;right:42px;display:flex;justify-content:space-between;font-size:9px;line-height:1.35;letter-spacing:.02em;color:#555}.sheet footer span:first-child{font-weight:600;letter-spacing:.07em}.direction{width:794px;height:1122px;padding:35px 42px;page:direction}.direction-heading{height:69px;display:flex;align-items:flex-start;gap:15px}.direction-id{font-size:46px;line-height:1;font-weight:500;letter-spacing:-.05em;margin-top:0}.direction-heading .eyebrow{font-size:9px;margin-top:2px;letter-spacing:.08em}.direction-heading h1{font-size:29px;line-height:1.2;margin-top:4px}.review-state{font-size:8px;letter-spacing:.08em;line-height:1.6;margin-left:auto;text-align:right;color:#555}.primary-pair{display:grid;grid-template-columns:1fr 1fr;gap:12px;height:239px}.primary{position:relative;display:flex;align-items:center;justify-content:center;border:1px solid #ddd}.primary svg{height:196px;width:calc(100% - 52px)}.primary span{position:absolute;bottom:10px;left:13px;font-size:8px;letter-spacing:.12em;color:#666}.black{background:#111;border-color:#111}.black span{color:#ddd}.white{background:#fff}.name-lockup{height:105px;margin-top:9px;padding:4px 44px 7px;border-bottom:1px solid #ddd}.meaning-grid{display:grid;grid-template-columns:1fr 1fr;gap:25px;margin-top:15px;min-height:102px}.meaning-grid h3{margin-bottom:6px}.meaning-grid p{font-size:12px;line-height:1.45;color:#333}.construction{margin-top:7px}.section-heading{display:flex;gap:20px;align-items:baseline}.section-heading h3{flex:0 0 208px}.section-heading p{font-size:10px;line-height:1.4;color:#555}.parts{display:grid;grid-template-columns:repeat(3,1fr);gap:11px;margin-top:9px}.parts figure{height:130px;border:1px solid #e6e6e6;padding:9px}.part-art{height:89px}.part-art svg{width:100%;height:100%}.parts figcaption{font-size:9px;line-height:1.3;color:#555;text-align:center;margin-top:8px}.sketches{margin-top:16px}.sketches h3{margin-bottom:9px}.sketch-grid{display:grid;gap:9px;grid-template-columns:repeat(3,1fr)}.sketch-grid.count-4{grid-template-columns:repeat(4,1fr)}.sketch{height:106px;border-top:1px solid #ddd;padding-top:7px}.sketch-art{height:66px;padding:0 8px}.sketch figcaption{margin-top:5px;font-size:9px;line-height:1.25;text-align:center}.sketch figcaption b{font-weight:500;display:block}.sketch figcaption span{display:block;font-size:7px;letter-spacing:.065em;color:#777;margin-top:3px}.sketch.selected{border-top:2px solid #111;padding-top:6px}.sketch.selected figcaption b{font-weight:700}.sketch.selected figcaption span{color:#111}.scale-note{position:absolute;left:42px;right:42px;bottom:42px;display:grid;grid-template-columns:68px 1fr;font-size:10px;line-height:1.4;gap:1px 8px;padding-top:9px;border-top:1px solid #ddd}.scale-note b{font-weight:600}.scale-note small{font-size:9px;color:#666;grid-column:2}.direction footer{font-size:8px}.direction .name-lockup svg{overflow:visible}.direction .primary svg{overflow:visible}
@page overview{size:297mm 210mm;margin:0}@page direction{size:210mm 297mm;margin:0}@media print{html,body{background:white}.sheet{margin:0}.overview{width:297mm;height:210mm}.direction{width:210mm;height:297mm}}
'''

async def main():
    data_file=OUT/'review-data.json'
    if not data_file.exists():raise SystemExit('Run tools/build_review.py first.')
    data=json.loads(data_file.read_text())
    fonts=f"@font-face{{font-family:ReviewSans;src:url(data:font/ttf;base64,{font_data('noto-sans-regular.ttf')}) format('truetype');font-weight:100 900;font-display:block}}"
    body=overview(data['directions'])+''.join(detail(d) for d in data['directions'])
    html='<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Tabernacle of Praise — Creative Review 05 — Draft</title><style>'+fonts+CSS+'</style></head><body>'+body+'</body></html>'
    async with async_playwright() as p:
      browser=await p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
      page=await browser.new_page(viewport={'width':1200,'height':1200},device_scale_factor=2)
      await page.set_content(html,wait_until='load');await page.evaluate('document.fonts.ready')
      overflow=await page.evaluate('''() => [...document.querySelectorAll('.sheet')].map(s=>({id:s.id,w:s.clientWidth,h:s.clientHeight,scrollW:s.scrollWidth,scrollH:s.scrollHeight,footerTop:s.querySelector('footer').getBoundingClientRect().top-s.getBoundingClientRect().top,scaleBottom:s.querySelector('.scale-note') ? s.querySelector('.scale-note').getBoundingClientRect().bottom-s.getBoundingClientRect().top : null,sketchBottom:s.querySelector('.sketches') ? s.querySelector('.sketches').getBoundingClientRect().bottom-s.getBoundingClientRect().top : null}))''')
      for x in overflow:
        if x['scrollW']>x['w'] or x['scrollH']>x['h']:raise RuntimeError('Sheet overflows: '+str(x))
        if x.get('sketchBottom') is not None and x['sketchBottom']>x['h']-94:raise RuntimeError('Sketch section collides with scale/footer: '+str(x))
      await page.locator('#overview').screenshot(path=str(OUT/'creative-review-05-overview.png'))
      for d in data['directions']:
        await page.locator('#direction-'+d['id'].lower()).screenshot(path=str(OUT/f'direction-{d["id"].lower()}.png'))
      await page.pdf(path=str(OUT/'tabernacle-creative-review-05.pdf'),print_background=True,prefer_css_page_size=True,display_header_footer=False)
      await browser.close()
    names=['creative-review-05-overview.png',*[f'direction-{d["id"].lower()}.png' for d in data['directions']],'tabernacle-creative-review-05.pdf']
    print(json.dumps({'source_sha256':hashlib.sha256(data_file.read_bytes()).hexdigest(),'files':{n:hashlib.sha256((OUT/n).read_bytes()).hexdigest() for n in names},'layout':overflow},indent=2))
if __name__=='__main__':asyncio.run(main())
