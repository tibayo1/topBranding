#!/usr/bin/env python3
"""Editable Direction E development. DRAFT — NOT FOR PUBLICATION.
Rebuild only this direction. Original SVG geometry; no external mark traced.
Material ideation is an explicitly generated exploratory source, not a church photo.
"""
from pathlib import Path
from html import escape
import json, subprocess
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
STUDY=ROOT.parents[1]
DRAFT='DRAFT — NOT FOR PUBLICATION'

SKETCHES=[
('E1','Returning Court','A folded perimeter turns around a common court; its increasing depth becomes the expression.','Plan-like enclosing fold with open entrance',
'''<path fill-rule="evenodd" d="M28 126 55 77 101 43 162 29 214 68 232 129 202 182 166 198 149 171 179 150 194 116 176 87 145 76 110 85 83 109 76 139 98 163 123 174 132 205 88 200 47 172Z M56 77 77 139 59 112Z M101 43 111 85 99 68Z M162 29 145 76 154 49Z"/>''',
'Gathered interior is visible. A cog, wreath or enclosing fortress remains possible; the tapering seams are too complex for a lead mark.'),
('E2','One Fold','One strip folds around an interior and then rises beyond its own enclosure.','Continuous folded ribbon',
'''<path d="M35 168V92L98 49 169 64 191 28 222 108 198 176 135 220 57 200 35 168Z M68 153 82 174 130 186 165 161 186 112 158 98 114 83 69 112Z" fill-rule="evenodd"/><path d="M45 103 63 123 68 153 51 130Z" fill="#fff"/><path d="M143 188 171 169 198 176 162 192Z" fill="#fff"/>''',
'One continuous object carries dwelling and movement. The interlocking corners can read as packaging, recycling or a technology loop.'),
('E3','Answering Surfaces','Two folded surfaces answer across one shared interior; each helps make the room.','Interdependent solid and counterform',
'''<path d="M30 135Q27 94 69 69L159 29 138 83Q79 103 77 144L132 221 66 198Z"/><path d="M171 61 225 106 225 163Q204 203 157 222L143 180Q180 155 180 117Z"/>''',
'Large counter and directional weight are clear. At first glance it may be an abstract leaf pair, split flame or rotational industry mark.'),
('E4','Opening Measure','A stable architectural mass progressively opens, so its own structure becomes generous.','Carved mass with opening intervals',
'''<path d="M29 184 34 100 184 32 226 111 218 217 151 217 170 180 191 154 190 107 163 84 118 107 99 145 112 185 147 217 91 213Z"/><path d="M53 111 99 83 76 144 86 186 65 171Z" fill="#fff"/><path d="M120 71 157 54 133 95 107 113Z" fill="#fff"/>''',
'The carved mass has a strong edge but the wedge/roof silhouette still suggests contemporary property or a sculptural building.'),
('E5','Processional Fold','A horizontal gathering becomes one broad rising return, expressing praise through movement.','Low pleated procession and rising sweep',
'''<path d="M25 169 51 143 81 147 107 115 139 124 165 79 207 35 231 92 206 170 152 215 99 204 47 205Z"/><path d="M51 143 64 180 47 205 49 169Z M107 115 119 166 99 204 99 155Z M165 79 170 144 152 215 148 141Z" fill="#fff"/>''',
'The sweep is kinetic and changes the axis of the original. Jagged peaks can suggest mountains, a sports brand or an upward chart.'),
('E6','Common Vault','Unequal folded shells join around one interior rather than stand as individual pillars.','Sculptural enclosing shell',
'''<path d="M28 143Q34 82 122 31L172 71Q212 78 229 135L211 192 158 224 106 209 53 206Z M82 149Q82 116 129 86L163 106Q186 129 164 168L132 192Z" fill-rule="evenodd"/><path d="M122 31 129 86 113 69Z M229 135 164 168 190 147Z M53 206 82 149 74 184Z" fill="#fff"/>''',
'The most unified shell construction, with cadence around a room. Could read as a folded rosette, aperture or abstract flame; avoid overclaiming immediate church recognition.')]

def doc(name,body,vb='0 0 256 256',desc='',color='#000000'):
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-labelledby="title desc"><title id="title">{escape(name)} — {DRAFT}</title><desc id="desc">{escape(desc)} {DRAFT}.</desc><g id="symbol" fill="{color}">{body}</g></svg>\n'
def write(name,body,**kw):
 (ROOT/name).write_text(doc(name.replace('.svg',''),body,**kw))
def render(svg,size=640):
 subprocess.run(['inkscape',str(ROOT/svg),'--export-type=png',f'--export-filename={ROOT/svg.replace(".svg",".png")}',f'--export-width={size}'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

def initial():
 for id,name,idea,approach,path,reason in SKETCHES:
  file=f'{id.lower()}-{name.lower().replace(" ","-")}-v1.svg'
  write(file,path,desc=idea)
  render(file)
 W,H=1500,1130
 board=Image.new('RGB',(W,H),'white');d=ImageDraw.Draw(board)
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',21)
 small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
 d.text((44,28),'E  /  CADENCED WALL REIMAGINED',fill='black',font=font)
 d.text((44,64),DRAFT+'  ·  Six constructions, one shared premise: the structure itself responds.',fill='#555',font=small)
 for i,(id,name,idea,approach,path,reason) in enumerate(SKETCHES):
  x=(i%3)*500;y=110+(i//3)*480
  p=ROOT/f'{id.lower()}-{name.lower().replace(" ","-")}-v1.png'
  art=Image.open(p).convert('RGBA'); art.thumbnail((350,350))
  board.paste(art,(x+75,y),art)
  d.text((x+44,y+363),id+' / '+name,fill='black',font=font)
  import textwrap
  for k,line in enumerate(textwrap.wrap(approach,45)):
   d.text((x+44,y+399+k*22),line,fill='#555',font=small)
 board.save(ROOT/'initial-board.png')



# The developed study is drawn from the carved mass premise, not the generated
# black rings. The two material boards remain for review, including failures.
DEV = {
 'v1': '<path d="M29 184 34 100 184 32 226 111 218 217 151 217 170 180 191 154 190 107 163 84 118 107 99 145 112 185 147 217 91 213Z"/><path d="M53 111 99 83 76 144 86 186 65 171Z M120 71 157 54 133 95 107 113Z" fill="#fff"/>',
 'v2': '<path d="M29 172 51 110 180 36Q199 73 209 112Q225 174 170 214L139 222 156 185Q184 160 179 124L154 90 119 111 102 148 116 185 139 222 77 211Z"/><path d="M51 110 79 94 67 149 78 188 53 167Z M109 77 145 56 129 103 98 124Z" fill="#fff"/>',
 'v3': '<path fill-rule="evenodd" d="M30 172 51 112 177 39Q196 73 207 111Q224 172 170 213L139 221 155 185Q182 160 177 124L153 92 121 111 105 147 118 184 139 221 78 210Z M53 115 79 100 68 149 79 184 56 164Z M110 81 143 62 129 102 101 124Z"/>',
 'v4': '<path fill-rule="evenodd" d="M30 172 51 112 177 39Q196 73 207 111Q224 172 170 213L151 219 160 185Q182 160 177 124L153 92 121 111 105 147 119 181 129 211 78 204Z M57 121 78 109 69 149 79 177 60 160Z M111 91 137 76 125 101 107 112Z"/>',
}

def developed():
 for version,path in DEV.items():
  write('developed-'+version+'.svg',path,desc='Opening Measure: a joined architectural mass carved by two small measured intervals and one generous interior. Cadence is a change in openness within the same enclosing surface.')
  render('developed-'+version+'.svg')
  # v3 and v4 use genuine counters. Preserve both reverse sources.
  if version in ['v3','v4']:
   write(f'developed-{version}-reverse.svg',path,color='#ffffff',desc=f'White reverse of developed {version}; true negative counters.')
   render(f'developed-{version}-reverse.svg')
 # Stable selected sources for the assembled review. Iterations remain separate.
 write('developed.svg',DEV['v4'],desc='Opening Measure: the selected v4 study, with substantial top bridges and an open lower threshold. A single folded wall opens into a shared interior.')
 write('developed-reverse.svg',DEV['v4'],color='#ffffff',desc='White reverse of selected developed v4; genuine negative cuts and open threshold.')
 render('developed.svg')
 render('developed-reverse.svg')
 # Exact pixel renders, independently saved for native-size checking.
 for version in DEV:
  for size in [16,24,32,64,256]:
   subprocess.run(['inkscape',str(ROOT/('developed-'+version+'.svg')),'--export-type=png',f'--export-filename={ROOT}/developed-{version}-{size}.png',f'--export-width={size}'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 for version in ['v3','v4']:
  for size in [16,24,32,64]:
   subprocess.run(['inkscape',str(ROOT/f'developed-{version}-reverse.svg'),'--export-type=png',f'--export-filename={ROOT}/developed-{version}-reverse-{size}.png',f'--export-width={size}'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 for size in [16,24,32,64]:
  subprocess.run(['inkscape',str(ROOT/'developed-reverse.svg'),'--export-type=png',f'--export-filename={ROOT}/developed-reverse-{size}.png',f'--export-width={size}'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 board=Image.new('RGB',(1500,1060),'white'); d=ImageDraw.Draw(board)
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',23)
 small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
 d.text((45,28),'E4 / OPENING MEASURE — REFINEMENT',fill='black',font=font)
 d.text((45,67),DRAFT+' · Genuine counters; no rendering effects.',fill='#555',font=small)
 for i,version in enumerate(['v1','v2','v3']):
  x=i*500
  art=Image.open(ROOT/('developed-'+version+'.png')).convert('RGBA');art.thumbnail((420,420))
  board.paste(art,(x+40,135),art)
  d.text((x+45,572),version.upper(),fill='black',font=font)
  labels={'v1':'Angular carved mass; too close to a roof.', 'v2':'Turned outer face; smoother lifted motion.', 'v3':'Counter spacing and silhouette balanced.'}
  d.text((x+45,612),labels[version],fill='#555',font=small)
  for j,size in enumerate([16,24,32,64]):
   icon=Image.open(ROOT/f'developed-{version}-{size}.png').convert('RGBA')
   bx=x+45+j*90;by=687
   board.paste(icon,(bx,by),icon)
   d.text((bx,770),str(size)+' px',fill='#555',font=small)
 # Reverse native-size sizes on black.
 d.rectangle((0,835,1500,1060),fill='black')
 d.text((45,860),'V3 / TRUE REVERSE',fill='white',font=small)
 for j,size in enumerate([16,24,32,64]):
  icon=Image.open(ROOT/f'developed-v3-reverse-{size}.png').convert('RGBA')
  bx=430+j*130;board.paste(icon,(bx,890),icon)
  d.text((bx,985),str(size)+' px',fill='white',font=small)
 board.save(ROOT/'refinement-board.png')

 # A separate proof preserves the first board and shows the limited structural
 # correction at actual sizes, with nearest-neighbour pixel enlargements below.
 board=Image.new('RGB',(1400,1120),'white'); d=ImageDraw.Draw(board)
 d.text((40,25),'E4 / OPENING MEASURE — STRUCTURAL REFINEMENT',fill='black',font=font)
 d.text((40,65),DRAFT+' · V4 thickens upper ties and opens the lower threshold.',fill='#555',font=small)
 for i,version in enumerate(['v3','v4']):
  x=40+i*700
  art=Image.open(ROOT/f'developed-{version}.png').convert('RGBA'); art.thumbnail((410,410))
  board.paste(art,(x+100,100),art)
  d.text((x,500),version.upper()+' / '+('point contact, slender top ties' if version=='v3' else 'open threshold, substantial top ties'),fill='black',font=font)
  for j,size in enumerate([16,24,32,64]):
   icon=Image.open(ROOT/f'developed-{version}-{size}.png').convert('RGBA')
   px=x+j*145
   board.paste(icon,(px,565),icon)
   d.text((px,645),f'{size} px',fill='#555',font=small)
   if size<64:
    zoom=icon.resize((size*4,size*4),Image.Resampling.NEAREST)
    board.paste(zoom,(px,700),zoom)
  d.text((x,845),'4× pixel enlargement above; native-size row remains at 1×.',fill='#555',font=small)
 d.rectangle((0,900,1400,1120),fill='black')
 d.text((40,925),'V4 / TRUE REVERSE — native sizes',fill='white',font=small)
 for j,size in enumerate([16,24,32,64]):
  icon=Image.open(ROOT/f'developed-reverse-{size}.png').convert('RGBA')
  px=460+j*190;board.paste(icon,(px,955),icon)
  d.text((px,1050),f'{size} px',fill='white',font=small)
 board.save(ROOT/'structural-refinement-board.png')

def metadata():
 prefix='directions/e-cadenced-reimagined/'
 data={
  'direction':'E',
  'title':'Cadenced Wall Reimagined',
  'status':DRAFT,
  'sketches':[
   {'id':id,'name':name,'idea':idea,'approach':approach,
    'sourceFile':prefix+f'{id.lower()}-{name.lower().replace(" ","-")}-v1.svg',
    'reason':reason}
   for id,name,idea,approach,path,reason in SKETCHES
  ],
  'developed':{
   'name':'Opening Measure',
   'sourceFile':prefix+'developed-v4.svg',
   'chosenSketchId':'E4',
   'idea':'A single folded wall enlarges its openings as it turns around a shared interior; the dwelling itself supplies the cadence.',
   'visible':'A joined sloping surface, two measured cuts and one generous interior open through the lower edge. Angular left faces answer a curved outer return.',
   'meaning':'The same structural gesture makes room and expresses movement. Joined construction suggests a shared dwelling; changing intervals and an expansive return suggest collective response. These are contemporary design associations, not a historical reconstruction or an image of divine presence.',
   'construction':[
    'One upper diagonal joins every zone. The two cuts sit below it with substantial material bridges instead of dividing the mark into separate pillars.',
    'Small intervals lead toward a larger shared interior. The lower threshold is genuinely open, replacing v3’s pinched point contact.',
    'Angular folded faces on the left contrast with a broad curved return on the right. All cuts are real negative space in one filled compound path.'
   ],
   'risk':'The primary association can still be a sculptural building or product emblem. A residual flame-like reading is possible in the large interior. Christian parish meaning needs the complete name and context; the artwork alone does not make it explicit.',
   'smallSize':'Native 16 px retains the sloping silhouette and open interior, while the finer upper interval largely merges. At 24 px the folded structure is identifiable; at 32 px the measured cuts are clearer. White reverse retains the threshold but looks slightly heavier at tiny sizes. Use 32 px or larger when the full cadence matters.',
   'longevity':'The identity rests on a structural silhouette and the relationship of solid to space, without a transient effect. Long-term usefulness is plausible, but church warmth and the sculptural/property association need congregation review.',
   'selectionReason':'E4 gives the strongest connection between architectural rhythm and a shared interior. E1/E2 read as loops or packaging; E3 reads as a split flame or rotation; E5 retains peaks and chart associations; E6 approaches an aperture. V4 repairs v3’s fragile upper ties and common bottom point without restarting the concept. Extra investigation does not make E the strongest of the five directions.',
   'iterations':[prefix+f'developed-v{n}.svg' for n in range(1,5)]
  }
 }
 (ROOT/'metadata.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')

if __name__=='__main__':
 initial()
 developed()
 metadata()
