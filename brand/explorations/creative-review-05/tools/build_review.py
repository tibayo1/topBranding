#!/usr/bin/env python3
"""Build a monochrome review from the direction masters; no approved standards."""
from pathlib import Path
from html import escape
import json,re
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from PIL import ImageFont
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'exports';OUT.mkdir(exist_ok=True)
DRAFT='DRAFT — NOT FOR PUBLICATION'
FOLDERS=['a-sacred-space','b-dwelling-expression','c-ecclesial-emblem','d-custom-typography','e-cadenced-reimagined']

def clean(text):
 return re.sub(r'\s(?:id|aria-labelledby)="[^"]*"','',text).replace('currentColor','#000000')
def read_art(file):
 text=(ROOT/file).read_text();box=re.search(r'viewBox="([^"]+)"',text)[1]
 inner=re.sub(r'<(?:title|desc)\b[^>]*>.*?</(?:title|desc)>','',text,flags=re.S)
 inner=re.sub(r'^.*?<svg\b[^>]*>|</svg>\s*$','',inner,flags=re.S)
 return clean(inner),box

def svg(mark,box,title):
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{box}" role="img" aria-label="{escape(title,quote=True)}"><title>{escape(title)} — DRAFT</title><desc>{DRAFT}. Unapproved identity exploration for RCCG Tabernacle of Praise.</desc>{mark}</svg>'
def fit(mark,box,x,y,w,h):
 a,b,bw,bh=map(float,box.split());s=min(w/bw,h/bh)
 return f'<g transform="translate({x+(w-bw*s)/2-a*s:.3f} {y+(h-bh*s)/2-b*s:.3f}) scale({s:.6f})">{mark}</g>'

class Face:
 def __init__(self,family,file,axes):
  f=ROOT/'assets/fonts'/family/file;self.font=TTFont(f);self.gs=self.font.getGlyphSet(location=axes);self.cmap=self.font.getBestCmap();self.upm=self.font['head'].unitsPerEm
  self.pil=ImageFont.truetype(str(f),1000);self.pil.set_variation_by_axes([axes.get(a.axisTag,a.defaultValue) for a in self.font['fvar'].axes])
 def width(self,text,size):return self.pil.getlength(text)*size/1000
 def text(self,text,x,y,size):
  parts=[]
  for i,c in enumerate(text):
   if c==' ':continue
   advance=(self.pil.getlength(text[:i+1])-self.pil.getlength(c))*size/1000
   pen=SVGPathPen(self.gs,ntos=lambda v:format(v,'.2f').rstrip('0').rstrip('.') if v else '0')
   self.gs[self.cmap[ord(c)]].draw(TransformPen(pen,(size/self.upm,0,0,-size/self.upm,x+advance,y)))
   parts.append(f'<path data-letter="{escape(c,quote=True)}" d="{pen.getCommands()}"/>')
  return '<g fill="#000000">'+''.join(parts)+'</g>'
serif=Face('sourceserif4','SourceSerif4[opsz,wght].ttf',{'wght':550,'opsz':24})
sans=Face('instrumentsans','InstrumentSans[wdth,wght].ttf',{'wght':550,'wdth':100})

def make_lockups(d,face):
 h=fit(d['mark'],d['viewBox'],20,24,204,208)+face.text('Tabernacle',266,114,76)+face.text('of Praise',266,202,76)
 size=82;w1=face.width('Tabernacle',size);w2=face.width('of Praise',size)
 s=fit(d['mark'],d['viewBox'],145,20,270,245)+face.text('Tabernacle',(560-w1)/2,377,size)+face.text('of Praise',(560-w2)/2,469,size)
 return {'horizontal':svg(h,'0 0 760 256',d['name']+' / full parish name / horizontal'),'stacked':svg(s,'0 0 560 530',d['name']+' / full parish name / stacked')}
def label(text,x,y,size=16,anchor='start',color='#222222'):
 return f'<text x="{x}" y="{y}" font-family="Noto Sans,Arial,sans-serif" font-size="{size}" text-anchor="{anchor}" fill="{color}">{escape(text)}</text>'
def content(art):
 return re.sub(r'^.*?<svg\b[^>]*>|</svg>\s*$','',re.sub(r'<(?:title|desc)\b[^>]*>.*?</(?:title|desc)>','',art,flags=re.S),flags=re.S)
def make_app(d,kind):
 lock=d['lockups']['horizontal'];box=re.search(r'viewBox="([^"]+)"',lock)[1];mark=content(lock)
 if kind=='signage':
  art='<rect width="1200" height="800" fill="#dcdcdc"/><path d="M0 85H1200V720H0Z" fill="#ececec"/><path d="M0 85H1200V101H0Z" fill="#a8a8a8"/><path d="M0 720H1200V800H0Z" fill="#bbbbbb"/><rect x="90" y="238" width="1020" height="247" rx="2" fill="#bfbfbf"/><rect x="90" y="227" width="1020" height="247" rx="2" fill="#ffffff"/>'+fit(mark,box,272,241,780,201)+'<rect x="121" y="286" width="116" height="116" fill="#f2f2f2" stroke="#969696"/>'+label('RCCG EMBLEM',179,334,12,'middle')+label('ASSET NEEDED',179,354,12,'middle')+label('RCCG · ISTANBUL, TÜRKİYE',272,455,13)+'<path d="M110 561H443V720H110Z M470 561H678V720H470Z M753 561H1088V720H753Z" fill="#8e8e8e"/><path d="M913 561V720" stroke="#d8d8d8" stroke-width="5"/>'+label('ILLUSTRATIVE WALL SIGN — NOT THE ACTUAL PREMISES',40,44,17)+label(DRAFT,40,773,15)
 else:
  art='<rect width="1200" height="800" fill="#e0e0e0"/><path d="M150 67H817V751H150Z" fill="#bababa"/><rect x="135" y="52" width="667" height="682" fill="#ffffff"/>'+fit(mark,box,187,91,565,174)+label('RCCG TABERNACLE OF PRAISE',190,318,16)+label('ISTANBUL, TÜRKİYE',190,345,14)+'<path d="M190 374H745" stroke="#333333" stroke-width="1.5"/>'+label('[CORRESPONDENCE TEXT]',190,425,16)+'<path d="M190 467H714M190 494H727M190 521H679M190 548H703" stroke="#d1d1d1" stroke-width="7"/><path d="M666 554H1144V747H666Z" fill="#b2b2b2"/><rect x="653" y="541" width="478" height="193" fill="#ffffff"/>'+fit(mark,box,681,567,421,139)+label('PAPER PROPORTION STUDY — NO CONTACT DETAILS INVENTED',35,33,15)+label(DRAFT,35,779,15)
 return svg(art,'0 0 1200 800',d['name']+' / '+kind+' identity study')
MEANINGS={
'A':'Two folded boundaries hold an open cross-shaped interior. Christian gathering is visible; praise is a quieter association with opening and response.',
'B':'Passing surfaces make a sheltered interval and release upward through the same construction. Gathering and expression belong to the same fold.',
'C':'An open roundel holds crafted T and P initials. Enclosure and a returning letter contour connect dwelling with the name’s response of praise.',
'D':'Enclosed bowls and rising counter floors repeat across the actual letters. The complete name carries the identity through one consistent letter grammar.',
'E':'One joined architectural face enlarges its openings as it turns. Cadence comes from changing openness within the dwelling, rather than separate rising buildings.'}
RISKS={
'A':'The dense faceted form can feel institutional; the lower opening may read as a chevron. Praise is less immediate than the Christian sacred-space reading.',
'B':'Wave, bird, or folded fabric can lead before dwelling. The held interval needs enough scale to be understood as a shared place.',
'C':'The roundel and initials may suggest a university, heritage institution, or luxury identity. Its ring can feel decorative rather than essential.',
'D':'The familiar serif base can feel editorial or bookish. Custom details are restrained and do not make the Christian association explicit without the name.',
'E':'A sculptural property or product emblem remains possible. The large interior can still suggest a flame; finer cadence weakens at tiny sizes.'}
TYPES={
'A':{'family':'Source Serif 4 / 550 / optical size 24','edits':'Outlined humanist letterforms and shaped kerning soften the dense faceted symbol. The phrase keeps natural line lengths; no enlarged initial or roof bar.','license':'Original Source Serif 4 under SIL OFL 1.1, retained in assets/fonts/sourceserif4/. No font binary modified. Companion lettering is a review specimen, not a final type system.'},
'B':{'family':'Instrument Sans / 550 / width 100','edits':'Calm open sans letterforms give the passing gesture room. Shaped spacing and equal-size name lines preserve a clear, welcoming reading.','license':'Original Instrument Sans under SIL OFL 1.1, retained in assets/fonts/instrumentsans/. No font binary modified.'},
'C':{'family':'Instrument Sans / 550 / width 100','edits':'A restrained open sans companion balances the more inscribed TP emblem. It reduces the double heritage emphasis of an ornate symbol plus a serif name.','license':'Original Instrument Sans under SIL OFL 1.1, retained in assets/fonts/instrumentsans/. The TP symbol is separately drawn original artwork; no font binary modified.'},
'E':{'family':'Source Serif 4 / 550 / optical size 24','edits':'Humanist counters add warmth beside the angular architecture. The complete name anchors a mark that would otherwise resemble a cultural or property emblem.','license':'Original Source Serif 4 under SIL OFL 1.1, retained in assets/fonts/sourceserif4/. No font binary modified.'}}
EVAL={
'A': ['Distinct counterform; familiar cross aids recall.','Dwelling appears through held space, rather than a literal building.','Christian space is clear; praise is the weaker half.','Most immediate Christian cue among the symbolic directions.','Clean thresholds and related facets; dark mass remains heavy.','Conventional Christian association can endure; distinctive enclosure must earn recognition.','Cross holds at16; diagonal threshold clearer at24+.','Strong broad silhouette; no effect-dependent detail.','Institutional badge or chevron.','An open Christian gathering space; do not claim it depicts God.'],
'B': ['Most gestural silhouette; broad crossing is distinct within this set.','The sheltered interval connects the fold to dwelling.','The same surfaces hold and release; meaning stays abstract.','Warm and expressive, with weaker independent church recognition.','Integrated return improves the earlier detached ribbon; cut junctions need proofing.','Avoids trend effects, but wave/bird associations need a reader test.','Silhouette holds tiny;24+ better for the held interval.','Expressive without color; central space does real work.','Surf, bird, fabric, or hospitality.','Gathering makes a shelter and turns outward in response.'],
'C': ['Crafted initials give a memorable formal identifier; roundels are familiar.','T and P directly identify Tabernacle and Praise.','Enclosure and return relate, but ring and letters remain separate contours.','Dignified ecclesial character, with a strong heritage tone.','Resolved letter junctions and open counters; fine T/P separation needs care.','Traditional inscription language is relatively durable, though not uniquely church-like.','TP reads best at32+; tiny initials and reverse crowd.','Works as a flat emblem; color is not carrying it.','University, heritage institution, or luxury monogram.','The parish initials held in a shared enclosing form.'],
'D': ['Distinctive repeated counter grammar; overall voice remains familiar serif.','The complete name gives the clearest verbal identification.','Dwelling/response are expressed inside real letterforms, subtly.','Appropriate dignified name; faith association relies on words and RCCG context.','Six originally drawn letters and optical pair spacing; no oversize T.','Familiar letter structures support enduring reading; editorial tone is a decision.','Full name tested320/240 wide; no 16px avatar claim.','The wordmark stands without a badge, color, or mockup.','Book imprint, editorial identity, or cultural organization.','The name itself shares a held-and-opening letter grammar.'],
'E': ['Strong joined diagonal mass; different from the earlier skyline.','A wall becomes a shared interior, rather than separate buildings.','Changing openings supply cadence inside the architecture.','Church meaning is indirect; full name remains essential.','Real bridges and open lower threshold repair earlier fragile joins.','Structural silhouette can endure; property association remains unresolved.','Full cadence best32+; finer cut merges at16.','One mass and its cuts work in pure black and reverse.','Sculptural property, product, or cultural identity.','One dwelling opens progressively into collective response.']}
KEYS=['distinctiveness','nameConnection','integration','churchSuitability','craft','endurance','smallScale','monochrome','industryRisk','explainability']

def make_parts(d,meta):
 mark=d['mark'];paths=re.findall(r'<path\b[^>]*?/?>',mark)
 def group(items,rule='nonzero'):return '<g fill="#000000" fill-rule="'+rule+'">'+''.join(items)+'</g>'
 if d['id']=='A':
  original=re.search(r'd="([^"]+)"',paths[0])[1];sub=re.split(r'(?<=[Zz])\s*(?=[Mm])',original)
  return [{'label':'First folded boundary','mark':group([f'<path d="{sub[0]}"/>']),'viewBox':d['viewBox']},{'label':'Answering boundary','mark':group([f'<path d="{sub[1]}"/>']),'viewBox':d['viewBox']},{'label':'Shared crossing and thresholds','mark':mark,'viewBox':d['viewBox']}]
 if d['id']=='E':
  original=re.search(r'd="([^"]+)"',paths[0])[1];sub=re.split(r'(?<=[Zz])\s*(?=[Mm])',original)
  return [{'label':'Architectural mass before cuts','mark':group([f'<path d="{sub[0]}"/>']),'viewBox':d['viewBox']},{'label':'Measured cuts — removed material','mark':group([f'<path d="{x}"/>' for x in sub[1:]]),'viewBox':d['viewBox']},{'label':'Joined face and shared interior','mark':mark,'viewBox':d['viewBox']}]
 if d['id']=='C':return [{'label':'Open enclosing contour','mark':group(paths[:1]),'viewBox':d['viewBox']},{'label':'Crafted T and P','mark':group(paths[1:]),'viewBox':d['viewBox']},{'label':'Complete roundel','mark':mark,'viewBox':d['viewBox']}]
 if d['id']=='D':
  cm,cb=read_art(meta['constructionFile']);cp=re.findall(r'<path\b[^>]*?/?>',cm)
  return [{'label':'Originally drawn P counter','mark':group([p for p in cp if 'data-letter="P"' in p],'evenodd'),'viewBox':'760 0 700 840'},{'label':'Related a and e openings','mark':group([p for p in cp if 'data-letter="a"' in p or 'data-letter="e"' in p],'evenodd'),'viewBox':'1500 0 1250 840'},{'label':'Six originally drawn letters','mark':cm,'viewBox':cb}]
 if d['id']=='B' and paths:
  original=re.search(r'd="([^"]+)"',paths[0])[1];sub=re.split(r'(?<=[Zz])\s*(?=[Mm])',original)
  return [{'label':'Sheltering surface and integral return','mark':group([f'<path d="{sub[0]}"/>']),'viewBox':d['viewBox']},{'label':'Rising continuation at the passing cut','mark':group([f'<path d="{x}"/>' for x in sub[1:]]),'viewBox':d['viewBox']},{'label':'Integrated held interval','mark':mark,'viewBox':d['viewBox']}]
 return [{'label':'Complete passing construction','mark':mark,'viewBox':d['viewBox']}]

def main():
 directions=[]
 for folder in FOLDERS:
  meta=json.loads((ROOT/'directions'/folder/'metadata.json').read_text());m=meta['developed'];id=meta['direction']
  mark,box=read_art(m['sourceFile'])
  d=dict(id=id,title=meta['title'],name=m['name'],primaryType='wordmark' if id=='D' else 'symbol',mark=mark,viewBox=box,sourceFile=m['sourceFile'],idea=m['idea'],visible=m['visible'],meaning=MEANINGS[id],construction=m['construction'],risk=RISKS[id],smallSize=m['smallSize'],longevity=m['longevity'],type=m.get('type',TYPES.get(id)),evaluation=dict(zip(KEYS,EVAL[id])),sketches=[])
  # Keep the screen concise; original metadata contains the complete craft record.
  d['construction']=[str(x) for x in d['construction'][:3]]
  if id!='D':
   d['type']=TYPES[id];d['lockups']=make_lockups(d,sans if id in ('B','C') else serif)
  else:
   hm,hb=read_art(m['horizontalFile']);sm,sb=read_art(m['stackedFile'])
   d['lockups']={'horizontal':svg(hm,hb,d['name']+' / full parish name / horizontal'),'stacked':svg(sm,sb,d['name']+' / full parish name / stacked')}
   d['lockupSources']={'horizontal':m['horizontalFile'],'stacked':m['stackedFile']}
  d['parts']=make_parts(d,m)
  for s in meta['sketches']:
   sm,sb=read_art(s['sourceFile']);d['sketches'].append(dict(s,mark=sm,viewBox=sb,selected=s['id']==m['chosenSketchId']))
  d['applications']={kind:make_app(d,kind) for kind in ('signage','paper')}
  prefix=id+'-'+re.sub(r'[^a-z0-9]+','-',d['name'].lower()).strip('-')
  (OUT/(prefix+'-primary-DRAFT.svg')).write_text(svg(mark,box,d['name'])+'\n')
  a,b,w,h=box.split();rev=f'<rect x="{a}" y="{b}" width="{w}" height="{h}" fill="#111111"/>'+mark.replace('#000000','#ffffff')
  (OUT/(prefix+'-reverse-DRAFT.svg')).write_text(svg(rev,box,d['name']+' / reverse')+'\n')
  for kind,art in {**d['lockups'],**d['applications']}.items():(OUT/(prefix+'-'+kind+'-DRAFT.svg')).write_text(art+'\n')
  directions.append(d)
 data={'title':'Tabernacle of Praise — Creative Review 05','status':DRAFT,'lead':'Five ways to connect sacred dwelling and praise. Each is tested in monochrome, with its strengths and unresolved readings visible.','directions':directions,'rccg':{'available':False,'note':'The repository records a user-supplied RCCG PNG and its checksum, but the actual image file is still absent. This is a labeled reservation only; no emblem is reconstructed. Actual emblem balance and publication authorization remain unverified.'},'sources':[{'title':'RCCG emblem provenance and missing-file status','url':'source/rccg-emblem-manifest.md','note':'Retained from the newer user-authored repository manifest. Its original PNG is still to be transferred.'},{'title':'Cadenced Wall context','url':'source/cadenced-wall-context.md','note':'Retained context for the deeper investigation; the current user brief requests five distinct A–E directions.'},{'title':'Creative Review 05 brief','url':'source/user-brief.md','note':'The current scope and feedback; all concepts remain draft.'},{'title':'Art direction and evaluation conditions','url':'source/art-direction.md','note':'Five distinct responsibilities and the same presentation conditions.'},{'title':'Retained biblical and architectural foundation','url':'source/research/identity-strategy.md','note':'Study04 research retained as context. Contemporary forms are interpretations; no parish doctrine is invented.'},{'title':'Scriptural sources and interpretation limits','url':'source/research/scriptural-foundations.md','note':'Exact passages distinguish sacred dwelling, praise, and current design interpretations.'}],'assessment':['C is the most resolved emblematic construction, and D provides the clearest name recognition. Neither is automatically the best parish identity: C risks heritage/luxury associations, while D remains editorial and its custom character is restrained.','A has the most immediate Christian association, but its dark mass still needs a warmth test. B has the most expressive gesture, with the least secure church reading. E is the most substantial architectural rethinking: keep it active, while testing its sculptural/property association and tiny cuts.','E received more exploration because the brief requested it. The developed comparison uses the same area, backgrounds, full names, size proofs, and applications for all five. No direction, palette, type system, or publishing template is approved.']}
 (ROOT/'data.js').write_text('/* DRAFT — NOT FOR PUBLICATION. Built from editable direction masters. */\nwindow.TOPReview05 = '+json.dumps(data,ensure_ascii=False,indent=2)+';\n')
 (OUT/'review-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print(f'Built {len(directions)} directions, {sum(len(d["sketches"]) for d in directions)} explorations and 30 editable review SVGs.')
if __name__=='__main__':main()
