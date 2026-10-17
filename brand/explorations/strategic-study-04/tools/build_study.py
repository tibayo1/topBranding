#!/usr/bin/env python3
"""Build research data, outlined review lockups and neutral application studies.
All artwork is exploratory. No approved palette, type system or final lockup implied.
"""
from pathlib import Path
from html import escape
import json,re,xml.etree.ElementTree as ET
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from PIL import ImageFont
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'exports';OUT.mkdir(exist_ok=True)

def clean(s):
 return re.sub(r'\s(?:id|aria-labelledby)="[^"]*"','',s).replace('ns0:','').replace(':ns0','')
def read_art(file):
 text=(ROOT/file).read_text()
 box=re.search(r'viewBox="([^"]+)"',text)[1]
 inner=re.sub(r'<(?:title|desc)\b[^>]*>.*?</(?:title|desc)>','',text,flags=re.S)
 inner=re.sub(r'^.*?<svg\b[^>]*>|</svg>\s*$','',inner,flags=re.S)
 return clean(inner),box
def wrap(mark,box,title):
 return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="'+box+'" role="img" aria-label="'+escape(title,quote=True)+'"><title>'+escape(title)+' — DRAFT</title><desc>DRAFT — NOT FOR PUBLICATION. Unapproved strategic identity study for RCCG Tabernacle of Praise.</desc>'+mark+'</svg>'
def fit(mark,box,x,y,w,h):
 a,b,bw,bh=map(float,box.split());s=min(w/bw,h/bh)
 tx=x+(w-bw*s)/2-a*s;ty=y+(h-bh*s)/2-b*s
 return f'<g transform="translate({tx:.3f} {ty:.3f}) scale({s:.6f})">{mark}</g>'
class Face:
 def __init__(self,file,axes):
  f=TTFont(file);self.gs=f.getGlyphSet(location=axes);self.cmap=f.getBestCmap();self.upm=f['head'].unitsPerEm
  self.pil=ImageFont.truetype(str(file),1000);self.pil.set_variation_by_axes([axes.get(a.axisTag,a.defaultValue) for a in f['fvar'].axes])
 def width(self,text,size):return self.pil.getlength(text)*size/1000
 def text(self,text,x,baseline,size):
  paths=[]
  for i,c in enumerate(text):
   if c==' ':continue
   advance=(self.pil.getlength(text[:i+1])-self.pil.getlength(c))*size/1000
   pen=SVGPathPen(self.gs,ntos=lambda n:format(n,'.2f').rstrip('0').rstrip('.') if n else '0')
   self.gs[self.cmap[ord(c)]].draw(TransformPen(pen,(size/self.upm,0,0,-size/self.upm,x+advance,baseline)))
   paths.append('<path data-letter="'+escape(c,quote=True)+'" d="'+pen.getCommands()+'"/>')
  return '<g fill="#000000">'+''.join(paths)+'</g>'
serif=Face(ROOT/'assets/fonts/sourceserif4/SourceSerif4[opsz,wght].ttf',{'wght':550,'opsz':24})
sans=Face(ROOT/'assets/fonts/instrumentsans/InstrumentSans[wdth,wght].ttf',{'wght':550,'wdth':100})
def lockups(mark,box,face):
 horizontal=fit(mark,box,24,26,200,200)+face.text('Tabernacle',264,114,75)+face.text('of Praise',264,202,75)
 w1=face.width('Tabernacle',88);w2=face.width('of Praise',88)
 stacked=fit(mark,box,130,20,280,245)+face.text('Tabernacle',(540-w1)/2,390,88)+face.text('of Praise',(540-w2)/2,486,88)
 return {'horizontal':wrap(horizontal,'0 0 760 256','Tabernacle of Praise — horizontal lockup'), 'stacked':wrap(stacked,'0 0 540 540','Tabernacle of Praise — stacked lockup')}
def app_svg(concept,kind):
 lock=concept['lockups']['horizontal'];box=re.search(r'viewBox="([^"]+)"',lock)[1]
 inner=re.sub(r'<(?:title|desc)\b[^>]*>.*?</(?:title|desc)>','',lock,flags=re.S)
 inner=re.sub(r'^.*?<svg\b[^>]*>|</svg>\s*$','',inner,flags=re.S)
 if kind=='signage':
  art='<rect width="1200" height="800" fill="#e8e8e5"/><path d="M0 150H1200V720H0Z" fill="#d8d8d4"/><path d="M0 150H1200V174H0Z" fill="#bcbcb6"/><path d="M0 720H1200V800H0Z" fill="#c4c4bd"/><rect x="70" y="548" width="250" height="172" fill="#777773"/><rect x="346" y="548" width="250" height="172" fill="#777773"/><path d="M720 548H1100V720H720Z" fill="#a1a19a"/><path d="M910 548V720" stroke="#e6e6df" stroke-width="4"/><rect x="72" y="232" width="1060" height="244" rx="2" fill="#aaa9a3"/><rect x="72" y="220" width="1060" height="244" rx="2" fill="#ffffff"/>'+fit(inner,box,240,238,840,195)+'<rect x="105" y="279" width="110" height="110" fill="#f0f0ec" stroke="#888880"/>'+label('RCCG ASSET',160,322,13,'middle')+label('RESERVED',160,343,13,'middle')+label('RCCG · ISTANBUL, TÜRKİYE',240,445,15)+label('ILLUSTRATIVE ELEVATION — NOT THE ACTUAL PREMISES',40,60,17)+label('DRAFT — NOT FOR PUBLICATION',40,770,15)
 else:
  art='<rect width="1200" height="800" fill="#dfdfd9"/><path d="M142 67H817V754H142Z" fill="#bfbfb8"/><rect x="126" y="52" width="675" height="687" fill="#ffffff"/>'+fit(inner,box,180,94,566,165)+label('RCCG TABERNACLE OF PRAISE',186,313,16)+label('ISTANBUL, TÜRKİYE',186,340,15)+'<path d="M186 368H741" stroke="#222222" stroke-width="2"/>'+label('[CORRESPONDENCE TEXT]',186,415,17)+'<path d="M186 455H712M186 483H724M186 511H678M186 539H700" stroke="#d5d5cd" stroke-width="7"/><path d="M668 558H1141V751H668Z" fill="#b7b7b0"/><rect x="650" y="543" width="473" height="193" fill="#ffffff"/>'+fit(inner,box,680,567,413,139)+label('PRINT PROPORTION STUDY / NO CONTACT DETAILS INVENTED',34,33,15)+label('DRAFT — NOT FOR PUBLICATION',34,780,15)
 return wrap(art,'0 0 1200 800',concept['name']+' — '+kind+' application')
def label(text,x,y,size,anchor='start'):
 return f'<text x="{x}" y="{y}" font-family="Noto Sans, Arial, sans-serif" font-size="{size}" text-anchor="{anchor}" fill="#222222">{escape(text)}</text>'
base=json.loads((ROOT/'sketches/foundation-sketches.json').read_text())
collective=json.loads((ROOT/'source/collective-sketches.json').read_text())
typography=json.loads((ROOT/'sketches/typography-sketches.json').read_text())
sketches=base+collective+typography
selected={'01','07','09','11'}
files={'01':'concepts/01-responsive-cover-v4.svg','07':'concepts/07-common-ground-v2.svg','09':'concepts/09-cadenced-wall-v2.svg','11':'concepts/11-shared-line-v2.svg'}
reasons={
'01':'Advances because the covering and its upward response are the same draped construction. It offers the most direct dwelling association without a separate worship icon.',
'02':'Set aside: the coupled lengths look like an industrial/technology monogram; the meaningful textile premise is better expressed by 01.',
'03':'Set aside: its literal plan becomes a rigid venue/maze-like sign and the internal panels can look like a face. It is less welcoming than the brief requires.',
'04':'Set aside: the return reads as a P/e or wayfinding sign before it communicates thanksgiving. The explanation would carry too much of the idea.',
'05':'Set aside: the apparent flame or seed overwhelms the intended held interior. A white aperture must not be labeled as a depiction of God.',
'06':'Set aside: the hard portal and inner fragment feel like an architectural software icon. Its internal detail adds complexity without clearer meaning.',
'07':'Advances because interdependent surfaces visibly make one shared room; the generous opening gives belonging a spatial form rather than a ring of people.',
'08':'Set aside: the organic center reads too much like a generic community flower. Softness alone does not establish a parish identity.',
'09':'Advances as a genuinely different, architectural way to test praise through cadence. Broad folded faces carry rhythm without instrument strings.',
'10':'Set aside: the lifted covering overlaps the stronger dwelling premise in 01; the enclosing fold also risks a page/app icon.',
'11':'Advances as the strongest full-name alternative. The actual initial T provides the shared structure, making typography carry the identity.',
'12':'Set aside: the rising baseline risks campaign/event typography. The quieter, shared structural line in 11 offers a clearer long-term premise.'}
for s in sketches:
 file=files.get(s['id']) or s.get('file') or ('sketches/11-living-line-v1.svg' if s['id']=='11' else 'sketches/12-lifted-praise-v1.svg')
 mark,box=read_art(file)
 s.update(mark=mark,symbolViewBox=box,sourceFile=file,decision='shortlisted' if s['id'] in selected else 'setaside',reason=reasons[s['id']])
 s.pop('markinnerSVG',None)
 if s['id']=='01':s['idea']='Joined textile folds make a dwelling whose own lifted edges express response and praise.';s['approach']='Pictorial material fusion / generous negative interior'
concepts=[]
for i,sketch_id in enumerate(('01','07','09','11')):
 s=next(s for s in sketches if s['id']==sketch_id)
 c={k:s[k] for k in ('name','territory','idea','mark','symbolViewBox','sourceFile')}
 c.update(id=f'S{i+1}',sketchId=sketch_id,primaryType='wordmark' if sketch_id=='11' else 'symbol')
 paths=re.findall(r'<path\b[^>]*?/?>',c['mark'])
 if sketch_id=='01':
  c.update(meaning='Tabernacle is the joined, sheltering textile. Praise is the lift and opening made by that same material. The form is a contemporary interpretation, not a reconstruction of the Exodus tent.',construction=['Four curved textile faces define one generous interior; the middle is a real open counter.','Diagonal breaks make folding and coupling visible; nothing is added inside as a second religious icon.','The silhouette is low and broad. No meaning is assigned to the number of pieces.'],risk='The white opening may suggest a robed figure or flame; the draped silhouette can suggest a tent venue or sails. Fine fold tips soften at micro sizes, and praise is less explicit than dwelling.',longevity='A recognizable draped silhouette could become an enduring identifier if its alternate venue/sail reading is acceptable. It needs name recognition and material proofing.',smallSize='The main interior survives 24–32px. At 16px the finest tapered folds lose distinction; a separately reviewed micro cut would be required for critical tiny use.')
  face=serif;family='Source Serif 4 / 550 / optical size 24';rationale='The humanist serif supplies dignity and warmth beside the broad draped mass. Equal-sized name lines preserve the phrase; shaped kerning and deliberate spacing are retained. These are review outlines, not a final wordmark.'
  c['parts']=[{'label':'Coupled upper material','mark':'<g fill="#000000">'+paths[0]+paths[2]+'</g>'},{'label':'Lower folds hold the room','mark':'<g fill="#000000">'+paths[1]+paths[3]+'</g>'}]
 elif sketch_id=='07':
  c.update(meaning='Distinct surfaces depend on each other to make one shared room. The gathering creates the dwelling; varied contours suggest collective participation rather than a single performer.',construction=['Four unequal broad surfaces surround one shared interior and a substantial front opening.','The surfaces rise and turn around the center; their relationship is the symbol rather than separate people or heads.','A fine overlap crease is secondary. The room and opening must remain recognizable when that crease closes small.'],risk='May read as an architectural/cultural institution rather than a church. The fine left crease closes small; do not assign doctrinal meaning to the number of surfaces.',longevity='The stable shared-room silhouette is promising for recognition across sign, screen, and paper. An independent reader test should establish whether it feels warm and ecclesial.',smallSize='The shared interior and broad front opening remain visible at 16–32px. The secondary left crease closes at the smallest sizes, so it must not carry the core meaning.')
  face=sans;family='Instrument Sans / 550 / width 100';rationale='Open sans letterforms keep the full name welcoming and legible beside the more expressive spatial form. The calmer type lets the room carry the character; line lengths are accepted instead of stretching lowercase.'
  c['parts']=[{'label':'Shared enclosing surfaces','mark':'<g fill="#000000">'+paths[0]+paths[1]+'</g>'},{'label':'The open common ground','mark':'<g fill="#000000">'+paths[2]+paths[3]+'</g>'}]
 elif sketch_id=='09':
  c.update(meaning='A folded architectural wall gathers around an implied forecourt. Its changing heights and intervals make the dwelling itself expressive: praise as cadence, with no musical instrument.',construction=['Five broad filled faces turn through a measured sequence, keeping a visible relationship to folded construction.','Major seams are at least 12 units on the 256-unit canvas. There are no hairline strings or white overlays.','The lower edges hold an implied forecourt; changing height creates the cadence. Piece count is compositional.'],risk='Could suggest a cultural venue, performance hall, or skyline. Rhythm is a creative association with praise; architecture alone cannot establish worship.',longevity='Its distinctive broad sequence could become recognizable at sign and header scale. A successful compact cut is still needed before it could cover every digital use.',smallSize='At 24–64px the fold sequence is visible. At 16px the articulation weakens into a segmented skyline; this is an unresolved limitation, not a passed favicon.')
  face=serif;family='Source Serif 4 / 550 / optical size 24';rationale='The serif counters the harder architectural edges with a human voice. The full name remains at the same type size and spacing logic as the other symbol tests, so the folded wall is judged on its own merits.'
  c['parts']=[{'label':'Lower repeated folds','mark':'<g fill="#000000">'+''.join(paths[:3])+'</g>'},{'label':'The rising return','mark':'<g fill="#000000">'+''.join(paths[3:])+'</g>'}]
 else:
  spec=json.loads((ROOT/'source/concept11-data.json').read_text())
  c.update(meaning='The initial T becomes a common overhead structure and anchor for the complete name. “of Praise” inhabits that same typographic structure: the words carry the meaning without a separate icon.',construction=[spec['construction'],'The two-line and true single-line compositions share a drawn initial and licensed Source Serif 4 outlines. The font binary is not modified.','The compact T is only a provisional derived initial; the full wordmark carries more recognition.'],risk=spec['risk'],longevity='The complete name offers immediate verbal identification and a typographic route to long-term recognition. Its oversized T and roof-like beam need reader testing; the compact initial is less distinctive.',smallSize='The compact T is tested separately at 64–16px. The complete wordmark is tested at 320/240px width; it is not claimed to be readable at 16px.')
  variants=spec['variants'];pm,pb=read_art('concepts/'+variants['primary']['file']);hm,hb=read_art('concepts/'+variants['horizontal']['file']);cm,cb=read_art('concepts/'+variants['compact']['file'])
  c.update(mark=pm,symbolViewBox=pb,lockups={'horizontal':wrap(hm,hb,'Tabernacle of Praise — Shared Line horizontal'),'stacked':wrap(pm,pb,'Tabernacle of Praise — Shared Line two-line')},compact={'mark':cm,'viewBox':cb,'label':'Provisional derived T / compact test','caution':'The compact T is less distinctive without the full name. It is a companion hypothesis, not an approved standalone emblem.'})
  c['parts']=[{'label':'Purpose-drawn structural T','mark':cm,'symbolViewBox':cb},{'label':'The complete inhabited name','mark':pm,'symbolViewBox':pb}]
  family='Source Serif 4 outlines + purpose-drawn initial T';rationale='The initial is constructed to hold the two readable name lines; other letters retain their licensed humanist shapes and actual kerning. The lighter developed beam gives the ascenders room. A single-line horizontal version uses the same grammar.'
 c['type']={'family':family,'rationale':rationale,'license':'SIL Open Font License 1.1. Original fonts, copyright and exact OFLs retained under assets/fonts/. No font binary is modified; no typography system is approved.'}
 if 'lockups' not in c:c['lockups']=lockups(c['mark'],c['symbolViewBox'],face)
 c['applications']={k:app_svg(c,k) for k in ('signage','paper')}
 c['parts'].append({'label':'Complete concept','mark':c['mark'],'symbolViewBox':c['symbolViewBox']})
 for kind,svg in c['lockups'].items():(OUT/f'{c["id"]}-{c["name"].lower().replace(" ","-")}-{kind}-DRAFT.svg').write_text(svg+'\n')
 for kind,svg in c['applications'].items():(OUT/f'{c["id"]}-{c["name"].lower().replace(" ","-")}-{kind}-DRAFT.svg').write_text(svg+'\n')
 (OUT/f'{c["id"]}-{c["name"].lower().replace(" ","-")}-primary-DRAFT.svg').write_text(wrap(c['mark'],c['symbolViewBox'],c['name'])+'\n')
 if c.get('compact'):(OUT/'S4-shared-line-compact-DRAFT.svg').write_text(wrap(c['compact']['mark'],c['compact']['viewBox'],'Shared Line — provisional compact T')+'\n')
 concepts.append(c)
territories=[
{'id':'A','title':'The Dwelling of Praise','intent':'Can the covering itself become an act of uplift? Joined textile and an expressive interior form one gesture.','risk':'A roof with another worship icon placed underneath.'},
{'id':'B','title':'Enter His Courts','intent':'Can access and thanksgiving become one generous spatial movement? Investigate threshold and response.','risk':'Generic gates, a maze, an exclusive fortress, or a false historical-access claim.'},
{'id':'C','title':'The Presence Within','intent':'Can the interior matter more than the container? Explore attention, an opening, and meaningful negative space.','risk':'Claiming a white void, flame, or ray is a literal depiction of God.'},
{'id':'D','title':'One House, Many Voices','intent':'Can distinct contributions make one shared dwelling? Make the parts interdependent, with a generous common center.','risk':'People around a circle, a flower, stick figures, or a networking icon.'},
{'id':'E','title':'A Dwelling that Sings','intent':'Can architectural or textile rhythm carry praise without an instrument? The structure supplies the cadence.','risk':'Harp strings under a new name, an equalizer, or an arbitrary skyline.'},
{'id':'F','title':'The Living Wordmark','intent':'Can the complete name carry the identity through letter relationships, shared structure, and readable expression?','risk':'Illegible ligatures, decorative bounce, or an oversized initial that overpowers the name.'}]
sources=[
{'id':'1','title':'Exodus 25:8–9 — sanctuary and dwelling among the people','url':'https://raw.githubusercontent.com/TehShrike/world-english-bible/master/json/exodus.json','note':'WEB public-domain text, identified third-party mirror. Exact selected verses and response hash retained locally; no claim of publisher-hosted retrieval.'},
{'id':'2','title':'Exodus 40:34–38 — cloud, glory, and the journey','url':'https://raw.githubusercontent.com/TehShrike/world-english-bible/master/json/exodus.json','note':'Text describes presence and journey. It supplies no prescribed logo for God.'},
{'id':'3','title':'Psalm 100:1–5 — entering, thanksgiving, and praise','url':'https://raw.githubusercontent.com/TehShrike/world-english-bible/master/json/psalms.json','note':'Read in its own worship setting. Its courts are not treated as an Exodus architectural diagram.'},
{'id':'4','title':'Psalm 150 — many expressions, all breath','url':'https://raw.githubusercontent.com/TehShrike/world-english-bible/master/json/psalms.json','note':'Multiple instruments and bodily expression prevent a compulsory harp-only interpretation of praise.'},
{'id':'5','title':'Hebrews 9 — earthly sanctuary and Christological argument','url':'https://raw.githubusercontent.com/TehShrike/world-english-bible/master/json/hebrews.json','note':'Restricted ancient access and the argument of the chapter are retained; a floorplan is not a complete Christian identity statement.'},
{'id':'6','title':'Exodus 26–27 / Numbers 4 — joined construction and portability','url':'research/architecture-and-symbolism.md','note':'Primary textual description: coupled textiles, coverings, frames, screens, and court. Archaeological dating or a precise historical reconstruction was not independently verified; scholarly site retrieval was blocked.'},
{'id':'7','title':'Scriptural evidence and retrieval provenance','url':'research/sources/scriptural-excerpts.json','note':'80 selected public-domain WEB verses with retrieval timestamp, exact URLs, text normalization notes, and source-file hashes. Research date: 17 October 2026.'},
{'id':'8','title':'Typography study and exact font licenses','url':'research/typography-study.md','note':'Source Serif 4, Instrument Sans, and Bricolage Grotesque were inspected in the complete name. Original variable fonts, OFLs, metadata, and checksums are retained.'}]
data={'status':'DRAFT — NOT FOR PUBLICATION','strategy':{'lead':'A shared dwelling, made expressive through the response of praise. The containing space and the gesture of opening, gathering, or lifting should belong to the same form.','principle':'The name should be recognized before the explanation is known. The explanation should deepen a strong form, rather than rescue an arbitrary one.','findings':[
{'title':'Dwelling among a people','text':'Exodus 25:8 links sanctuary with dwelling “among them.” Design for a relationship between sacred dwelling and people, rather than real estate alone.','sourceIds':['1']},
{'title':'Presence is more than an icon','text':'Exodus 40 describes the cloud covering the Tent of Meeting and glory filling the tabernacle. Light, an opening, or a held interior would be contemporary artistic interpretations, not a graphic depiction of God.','sourceIds':['2']},
{'title':'Entering with thanksgiving','text':'Psalm 100 connects gladness, singing, entering, thanksgiving, praise, and belonging. A threshold can explore invitation without pretending to reconstruct the wilderness sanctuary.','sourceIds':['3']},
{'title':'Praise extends beyond music','text':'Psalm 150 names several instruments, dancing, and everything that has breath. The parish identity need not be led by any one instrument.','sourceIds':['4']},
{'title':'Context matters','text':'Hebrews 9 describes earthly sanctuary arrangements and restricted priestly access, then develops its Christological argument. It is not a logo blueprint or a mandate for literal furniture.','sourceIds':['5']},
{'title':'Joined material, one dwelling','text':'Exodus 26–27 and Numbers 4 describe joined textiles, covering, frames, screens, court, and transport. Coupling and a shared interior offer a fresh construction language. Historical reconstruction and archaeological claims remain outside the verified evidence.','sourceIds':['6','7']}]},'territories':territories,'sketches':sketches,'concepts':concepts,'sources':sources,'selectionNotes':'The four develop different kinds of identifier: a draped covering, a shared spatial enclosure, a broad architectural cadence, and a full-name wordmark. Selection favors a visible relationship to the name, silhouette distinction, and credible reproduction. The other eight remain visible with specific reasons. This is a development shortlist for your review, not a selection of the church’s identity.'}
(ROOT/'data.js').write_text('/* DRAFT — NOT FOR PUBLICATION. Generated from editable SVG sources and research. */\nwindow.TOPStudy = '+json.dumps(data,ensure_ascii=False,indent=2)+';\n')
(OUT/'study-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('Built 12 explored ideas, four developed review concepts, 21 SVG exports, and reusable browser data.')
