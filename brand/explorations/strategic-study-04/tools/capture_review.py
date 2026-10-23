#!/usr/bin/env python3
"""Readable review boards and PDF from the exact browser/vector data."""
from pathlib import Path
from html import escape
import base64,json,re,textwrap
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'exports'
s=(ROOT/'data.js').read_text();data=json.loads(s.split('window.TOPStudy = ',1)[1].rsplit(';',1)[0])
def fit(mark,box,x,y,w,h):
 a,b,bw,bh=map(float,box.split());z=min(w/bw,h/bh)
 return f'<g transform="translate({x+(w-bw*z)/2-a*z:.3f} {y+(h-bh*z)/2-b*z:.3f}) scale({z:.6f})">{mark}</g>'
def art(svg):
 box=re.search(r'viewBox="([^"]+)"',svg)[1]
 inner=re.sub(r'<(?:title|desc)\b[^>]*>.*?</(?:title|desc)>','',svg,flags=re.S)
 inner=re.sub(r'^.*?<svg\b[^>]*>|</svg>\s*$','',inner,flags=re.S)
 return inner,box
def text(x,y,content,size=20,color='#111111',width=None):
 lines=textwrap.wrap(content,width=width) if width else [content]
 return ''.join(f'<text x="{x}" y="{y+i*size*1.45:.1f}" font-family="Noto Sans,Arial,sans-serif" font-size="{size}" fill="{color}">{escape(line)}</text>' for i,line in enumerate(lines))
def save_board(name,parts,w,h):
 (OUT/(name+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>Tabernacle of Praise — {name} — DRAFT</title><desc>DRAFT — NOT FOR PUBLICATION. All logo, palette, and typography decisions are open.</desc>'+''.join(parts)+'</svg>\n')
parts=['<rect width="1800" height="2480" fill="#f7f6f2"/>',text(60,67,'Tabernacle of Praise / 12 investigated ideas',38),text(60,108,'DRAFT — NOT FOR PUBLICATION / Six territories / Monochrome / Four advance for review',18,'#555555')]
for i,item in enumerate(data['sketches']):
 x=50+(i%3)*570;y=150+(i//3)*570
 parts+= [f'<rect x="{x}" y="{y}" width="550" height="548" fill="#ffffff" stroke="#dddddd"/>',text(x+25,y+37,item['id']+' / TERRITORY '+item['territory'],14,'#555555'),fit(item['mark'],item['symbolViewBox'],x+55,y+58,440,246),text(x+25,y+354,item['name'],24),text(x+25,y+394,item['idea'],17,'#444444',width=47),text(x+25,y+515,'DEVELOP FURTHER' if item['decision']=='shortlisted' else 'SET ASIDE / SEE REVIEW NOTES',13,'#555555')]
save_board('initial-explorations',parts,1800,2480)
parts=['<rect width="1800" height="1660" fill="#f7f6f2"/>',text(60,65,'Tabernacle of Praise / Four developed directions',38),text(60,110,'DRAFT — NOT FOR PUBLICATION / No logo, typeface, or palette selected',18,'#555555')]
for i,c in enumerate(data['concepts']):
 x=50+(i%2)*860;y=155+(i//2)*735
 shape,box=art(c['lockups']['stacked'])
 parts += [f'<rect x="{x}" y="{y}" width="840" height="710" fill="#ffffff" stroke="#dddddd"/>',text(x+35,y+46,c['id']+' / '+c['name'],25),fit(shape,box,x+70,y+74,700,423),text(x+35,y+545,c['idea'],18,'#333333',width=75),text(x+35,y+635,'OPEN QUESTION: '+c['risk'],14,'#555555',width=94)]
save_board('four-developed-concepts',parts,1800,1660)
# Print review: research; twelve ideas over two pages; four developed studies;
# paper/signage comparisons; review/limits. Ten explicit A4 landscape pages.
font=base64.b64encode((ROOT/'assets/noto-sans-regular.ttf').read_bytes()).decode()
css="@font-face{font-family:Review;src:url(data:font/ttf;base64,"+font+")}"
css+='''@page{size:A4 landscape;margin:0}*{box-sizing:border-box}body{margin:0;color:#111;font-family:Review,Arial,sans-serif}h1{font-size:28px;font-weight:400;margin:8px 0 15px}h2{font-size:18px;font-weight:400;margin:0 0 10px}p,li{font-size:11px;line-height:1.7;margin:0 0 10px}.sheet{width:297mm;height:210mm;padding:11mm 13mm;position:relative;break-after:page}.sheet:last-child{break-after:auto}.kicker{font-size:8px;letter-spacing:1px;text-transform:uppercase;color:#555}.footer{position:absolute;bottom:7mm;left:13mm;right:13mm;border-top:1px solid #ddd;padding-top:7px;font-size:8px;display:flex;justify-content:space-between}.cols{display:grid;grid-template-columns:1fr 1fr;gap:30px}.research{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:23px}.research h2{font-size:14px}.research p{font-size:10px}.initials{display:grid;grid-template-columns:repeat(3,1fr);gap:13px;margin-top:18px}.initial{border:1px solid #ddd;padding:14px;height:274px}.initial>svg{width:100%;height:120px}.initial h2{font-size:14px}.initial p{font-size:9px;line-height:1.5}.concept-art{height:260px;border:1px solid #ddd;display:flex;align-items:center;justify-content:center}.concept-art svg{width:75%;height:220px}.nameproof{height:150px;display:flex;align-items:center;justify-content:center}.nameproof svg{max-width:100%;max-height:145px}.small{font-size:9px;color:#555}.apps{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:20px}.apps figure{margin:0}.apps svg{width:100%;height:220px}.apps figcaption{font-size:10px;margin-top:5px}.sizes{display:flex;align-items:end;gap:25px;margin-top:18px}.sizes svg{display:block}.sizes span{font-size:8px;display:block;text-align:center;margin-top:6px}a{color:#111}*{-webkit-print-color-adjust:exact;print-color-adjust:exact}'''
footer='<div class="footer"><span>DRAFT — NOT FOR PUBLICATION / No identity decision approved.</span><span>RCCG Tabernacle of Praise / Strategic study 04</span></div>'
sheets=[]
def page(title,body,kicker='RESEARCH-LED IDENTITY EXPLORATION'):
 sheets.append('<section class="sheet"><p class="kicker">'+kicker+'</p><h1>'+escape(title)+'</h1>'+body+footer+'</section>')
page('A dwelling. A response. One identity.','<p>'+escape(data['strategy']['lead'])+'</p><p>'+escape(data['strategy']['principle'])+'</p><div class="research">'+''.join('<article><h2>'+escape(f['title'])+'</h2><p>'+escape(f['text'])+'</p><p class="small">Sources '+', '.join(f['sourceIds'])+'</p></article>' for f in data['strategy']['findings'])+'</div><p class="small" style="margin-top:22px">Exact public-domain WEB excerpts, mirror URLs, retrieval hashes, architectural limits, and typography licenses are retained in the browser study and research folder. Contemporary visual interpretations are not parish doctrine or archaeological reconstructions.</p>')
for start in (0,6):
 page('Twelve investigated ideas / '+('01–06' if start==0 else '07–12'),'<div class="initials">'+''.join('<article class="initial"><h2>'+s['id']+' / '+escape(s['name'])+'</h2><svg viewBox="'+s['symbolViewBox']+'">'+s['mark']+'</svg><p>'+escape(s['idea'])+'</p><p class="small">'+escape(s['reason'])+'</p></article>' for s in data['sketches'][start:start+6])+'</div>','SIX TERRITORIES / MONOCHROME HYPOTHESES')
for c in data['concepts']:
 display=c['compact'] if c.get('compact') else {'mark':c['mark'],'viewBox':c['symbolViewBox']}
 sizes=''.join('<div><svg width="'+str(z)+'" height="'+str(z)+'" viewBox="'+display['viewBox']+'">'+display['mark']+'</svg><span>'+str(z)+'px</span></div>' for z in(64,32,24,16))
 page(c['id']+' / '+c['name'],'<div class="cols"><div><div class="concept-art"><svg viewBox="'+c['symbolViewBox']+'">'+c['mark']+'</svg></div><div class="nameproof">'+c['lockups']['horizontal']+'</div><div class="sizes">'+sizes+'</div><p class="small">'+escape(c['smallSize'])+'</p></div><div><h2>The name, made visible</h2><p>'+escape(c['meaning'])+'</p><h2>Construction</h2><ul>'+''.join('<li>'+escape(t)+'</li>' for t in c['construction'])+'</ul><h2>Typography</h2><p>'+escape(c['type']['family'])+'</p><p class="small">'+escape(c['type']['rationale'])+'</p><h2>Open question</h2><p>'+escape(c['risk'])+'</p></div></div>','FOUR DEVELOPED DIRECTIONS / NOT AN APPROVAL')
for kind,title in (('signage','Illustrative building signage'),('paper','Printed identity proportions')):
 page(title,'<div class="apps">'+''.join('<figure>'+c['applications'][kind]+'<figcaption>'+c['id']+' / '+escape(c['name'])+'</figcaption></figure>' for c in data['concepts'])+'</div>','LIMITED IDENTITY APPLICATIONS / SAME PRESENTATION CONDITIONS')
page('Four hypotheses for your review.','<div class="cols"><div><h2>What advances</h2><p>'+escape(data['selectionNotes'])+'</p><h2>Questions to answer</h2><ul><li>Which form feels like a whole parish rather than a building, choir, or venue?</li><li>Does the name-to-form connection deepen recognition without a long explanation?</li><li>Which alternative reading is acceptable, and which would undermine the identity?</li><li>Can the small-scale limitation be resolved without losing the central idea?</li></ul></div><div><h2>Decisions still open</h2><p>Logo direction, final geometry, typography, palette, minimum sizes, material reproduction, and official RCCG pairing.</p><h2>Evidence and limits</h2><p>Primary scriptural wording was checked using identified public-domain WEB mirrors. Several scholarly sites were blocked; historical dating and archaeology are not independently verified. Research is a creative foundation, not an official parish theological statement.</p><p>The RCCG emblem remains a separate labeled reservation; authorized artwork has not been supplied. Typeface licenses are retained. Screen rendering does not establish physical reproduction or legal exclusivity.</p><p>No weekly flyer generator, final brand guide, or publication template has been created.</p></div></div>')
review='<!doctype html><html><head><meta charset="utf-8"><title>Tabernacle of Praise — Draft strategic review</title><style>'+css+'</style></head><body>'+''.join(sheets)+'</body></html>'
(OUT/'printable-review.html').write_text(review)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 pg=browser.new_page(viewport={'width':1440,'height':1100},reduced_motion='reduce')
 pg.goto('http://127.0.0.1:8766',wait_until='networkidle');pg.evaluate('document.fonts.ready')
 pg.add_style_tag(content='.side-nav{visibility:hidden!important}#shortlist-overview::before{content:"DRAFT — NOT FOR PUBLICATION / FOUR REVIEW DIRECTIONS";grid-column:1/-1;font:10px Arial,sans-serif;letter-spacing:1px;padding-bottom:12px}#strategy::before,#sketches::before{content:"DRAFT — NOT FOR PUBLICATION";display:block;font:10px Arial,sans-serif;letter-spacing:1px;margin-bottom:20px}')
 for selector,name in(('#strategy','research-browser.png'),('#sketches','twelve-ideas-browser.png'),('#shortlist-overview','shortlist-browser.png')):pg.locator(selector).screenshot(path=str(OUT/name),animations='disabled')
 for c in data['concepts']:
  pg.locator('.concept[data-concept='+c['id']+']').screenshot(path=str(OUT/(c['id']+'-browser.png')),animations='disabled')
 pg.set_viewport_size({'width':390,'height':844});pg.locator('#shortlist-overview').screenshot(path=str(OUT/'shortlist-mobile.png'),animations='disabled')
 pg.set_content(review,wait_until='networkidle');pg.evaluate('document.fonts.ready')
 overlaps=pg.evaluate('''() => [...document.querySelectorAll('.sheet')].map((s,i)=>{const f=s.querySelector('.footer').getBoundingClientRect();const b=Math.max(...[...s.children].filter(c=>!c.classList.contains('footer')).map(c=>c.getBoundingClientRect().bottom));return {page:i+1,bottom:b,footer:f.top}}).filter(x=>x.bottom>x.footer-2)''')
 assert not overlaps,overlaps
 assert pg.locator('.sheet').count()==10
 pg.pdf(path=str(OUT/'strategic-review.pdf'),print_background=True,prefer_css_page_size=True)
 browser.close()
print('Built review boards, browser captures, and ten-page PDF with footer-clearance checks.')
