#!/usr/bin/env python3
"""Original open-contour TP development. No font, mask or white overlay geometry."""
from pathlib import Path
import json, subprocess
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'renders';V=ROOT/'versions'
R.mkdir(exist_ok=True);V.mkdir(exist_ok=True)
VERSIONS={
'v0-review-08':'M28 28H140C205 28 228 65 228 96C228 142 197 163 133 177V102H146C170 102 181 113 181 130V140C190 129 194 117 194 104V85C194 73 188 68 177 68H61C56 68 52 67 48 65C52 83 61 95 74 95H91V169C91 194 103 207 133 223H110C45 223 28 190 28 142Z',
'v1-counter-balance':'M28 28H140C205 28 228 65 228 96C228 142 197 163 133 177V101H147C167 101 179 111 179 126L184 126C191 116 194 107 194 99V85C194 73 188 68 177 68H62C57 68 53 67 49 66C53 83 62 95 75 95H90V169C90 193 102 207 133 223H110C45 223 28 190 28 142Z',
'v2-level-terminal':'M28 28H140C205 28 228 65 228 96C228 142 197 163 133 177V101H147C165 101 176 109 179 121H187C192 113 194 105 194 97V85C194 73 188 68 177 68H62C57 68 53 67 49 66C53 83 62 95 75 95H90V169C90 193 102 207 133 223H110C45 223 28 190 28 142Z',
'v3-compact-cut':'M28 28H140C205 28 228 65 228 96C228 142 197 163 134 177V103H146C165 103 175 110 180 121H188C192 114 194 107 194 98V86C194 74 188 69 177 69H62C57 69 53 68 49 67C54 84 63 95 76 95H88V168C88 193 101 207 133 223H110C45 223 28 190 28 142Z',
}
SELECTED='v1-counter-balance';COMPACT='v3-compact-cut'
def svg(path,title,reverse=False):
 ink='#ffffff' if reverse else '#000000'
 bg='<rect width="256" height="256" fill="#000000"/>' if reverse else ''
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">\n<title>Open Praise {title} — DRAFT — NOT FOR PUBLICATION</title>\n<desc>Original P-like outer contour holding an open negative T. One actual outline; letter recognition remains subject to review.</desc>\n{bg}<path fill="{ink}" d="{path}"/>\n</svg>\n'
for name,path in VERSIONS.items():
 (V/(name+'.svg')).write_text(svg(path,name))
(ROOT/'primary.svg').write_text(svg(VERSIONS[SELECTED],SELECTED))
(ROOT/'reverse.svg').write_text(svg(VERSIONS[SELECTED],SELECTED,True))
(ROOT/'compact.svg').write_text(svg(VERSIONS[COMPACT],COMPACT))
(ROOT/'compact-reverse.svg').write_text(svg(VERSIONS[COMPACT],COMPACT,True))
jobs=[]
for name in VERSIONS:
 for size in [16,20,24,32,64,512]:jobs.append((V/(name+'.svg'),R/f'{name}-{size}.png',size))
for name in ['primary','reverse','compact','compact-reverse']:
 for size in [16,20,24,32,64,512]:jobs.append((ROOT/(name+'.svg'),R/f'{name}-{size}.png',size))
def render(job):
 src,out,size=job
 subprocess.run(['inkscape',str(src),'--export-type=png',f'--export-filename={out}',f'--export-width={size}',f'--export-height={size}'],check=True,capture_output=True)
with ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(render,jobs))
FONT=ROOT.parents[1]/'creative-review-05/assets/noto-sans-regular.ttf'
f=ImageFont.truetype(str(FONT),20);small=ImageFont.truetype(str(FONT),15)
board=Image.new('RGB',(1600,1300),'white');d=ImageDraw.Draw(board)
d.text((40,24),'OPEN PRAISE — OUTLINE DEVELOPMENT 09',font=f,fill='black')
d.text((40,59),'DRAFT — NOT FOR PUBLICATION / changes remain inside the existing figure-ground TP premise',font=small,fill='black')
labels=['08 baseline','Balanced / proposed primary','Level terminal / rejected','Compact cut / small use']
for col,(name,label) in enumerate(zip(VERSIONS,labels)):
 im=Image.open(R/f'{name}-512.png').convert('RGBA');im.thumbnail((310,310),Image.Resampling.LANCZOS)
 board.paste(im,(45+col*395,108),im)
 d.text((45+col*395,439),label,font=small,fill='black')
 notes=[['Long tapered hook.','Bar and stem read, unequal P/T.'],['Blunt five-unit terminal.','Wider stem; lower exit unchanged.'],['Short level hook.','More mechanical and less open.'],['Terminal reduced for raster use.','Stem widened by three units.']][col]
 for j,line in enumerate(notes):d.text((45+col*395,470+j*24),line,font=small,fill='black')
for row,stem in enumerate(['primary','reverse','compact','compact-reverse']):
 y=560+row*155;rev='reverse' in stem
 if rev:d.rectangle((40,y-15,1560,y+125),fill='black')
 ink='white' if rev else 'black'
 d.text((55,y+7),stem+' / native pixels',font=f,fill=ink)
 for j,size in enumerate([64,32,24,20,16]):
  x=520+j*190;im=Image.open(R/f'{stem}-{size}.png').convert('RGBA')
  board.paste(im,(x+(64-size)//2,y),im)
  d.text((x,y+83),f'{size} px',font=small,fill=ink)
d.text((40,1213),'Primary retains the open P/T idea. Compact is a raster compensation, not a new logo.',font=small,fill='black')
d.text((40,1240),'16–20 px: silhouette first; full letter reading is more dependable at 24–32 px. No worship pictogram is claimed.',font=small,fill='black')
board.save(R/'outline-comparison.png')

metadata={
 'id':'B','name':'Open Praise','status':'DRAFT — NOT FOR PUBLICATION',
 'primary':'primary.svg','reverse':'reverse.svg','compact':'compact.svg','compactReverse':'compact-reverse.svg',
 'viewBox':'0 0 256 256','primaryType':'symbol','source':'source/build.py',
 'selectedVersion':SELECTED,'compactVersion':COMPACT,
 'baseline':'../../team-pair-08/second-direction/primary.svg',
 'idea':'A P-like outer gesture holds an open T-shaped interior.',
 'visible':'One broad, compact contour with a negative crossbar, descending stem and open lower exit.',
 'meaning':'T and P refer to Tabernacle and Praise. An interior held open can suggest welcome and response. This is a name-based figure-ground proposal; it is not a literal worshipper, sanctuary or musical instrument.',
 'construction':'One closed path traces the open indentation. Negative space stays connected to the surrounding background. No white overlay, clipping path, mask, font glyph or stock icon is used.',
 'changes':{
  'baseline':'Review08 geometry preserved as v0-review-08.svg for direct comparison.',
  'primary':'Outer silhouette unchanged. The long tapered counter hook ends fourteen units earlier with a five-unit blunt terminal. The negative stem increases from 42 to 43 units. Crossbar and lower turn remain fluid.',
  'rejected':'The level-terminal trial replaces the hook with an eight-unit shelf. It is preserved but not chosen because it feels more mechanical and makes the P dominate.',
  'compact':'A separate provisional raster cut widens the negative stem from 43 to 46 units and replaces the curved tip with a shorter, eight-unit terminal. Outer silhouette remains identical. This improves the held vertical interval but makes the counter less expressive.'
 },
 'risk':'The negative T remains inferential and the P may dominate. The compact monogram can suggest a creative studio, publisher or luxury identity. The blunt counter reduces the former beak-like hook but does not guarantee a particular reading. No originality or trademark clearance is claimed.',
 'smallSize':'Actual native 16/20/24/32/64 px black and reverse renders were inspected, alongside 512 px curves. At 16–20 px, silhouette recognition is stronger than full letter reading. At 24–32 px, the internal T is more dependable. Compact is a provisional raster compensation, not a final minimum-size rule or a proven readability advantage for every placement.',
 'reverseNote':'Reverse is an explicit white path on a black proof background. Transparent white geometry may be obtained by removing only the background rect. No separate reversed outline is prescribed yet.',
 'referencePrinciples':'Original Review08 figure-ground premise. User-supplied logos contribute compact confidence and purposeful negative space only. Their shields, figures, books, stars, NV geometry and typographic letterforms are not reused.',
 'proofs':['renders/outline-comparison.png','renders/pixel-detail.png'],
 'versions':[{'name':name,'source':'versions/'+name+'.svg','selected':name==SELECTED,'smallUse':name==COMPACT} for name in VERSIONS],
 'checks':{'actualRendersInspected':True,'audit':'20 anchors, one closed filled path, one color; no SVG audit issues. The heuristic score is not a design endorsement or approval.'},
 'approval':False
}
(ROOT/'metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
# Enlarged raster detail supplements, but never replaces, native-size samples.
b=Image.new('RGB',(1140,900),'white');d=ImageDraw.Draw(b)
d.text((25,15),'Raster compensation detail — x5 nearest-neighbour enlargement',fill='black',font=f)
d.text((25,44),'Use the native samples on the main proof to judge actual size.',fill='black',font=small)
for row,name in enumerate(['primary','compact','reverse','compact-reverse']):
 y=100+row*190;rev='reverse' in name
 if rev:d.rectangle((20,y-10,1120,y+170),fill='black')
 ink='white' if rev else 'black';d.text((30,y+5),name,fill=ink,font=f)
 for col,size in enumerate([16,20,24]):
  im=Image.open(R/f'{name}-{size}.png').convert('RGBA').resize((size*5,size*5),Image.Resampling.NEAREST)
  x=300+col*260;b.paste(im,(x,y),im);d.text((x,y+132),f'{size}px x5',fill=ink,font=small)
b.save(R/'pixel-detail.png')
