#!/usr/bin/env python3
"""Shared Rhythm optical cut studies; all art remains DRAFT, not approved identity."""
from pathlib import Path
import json
import re
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=[
 'M16 132 69 103 65 217 16 207Z',
 'M67 95 122 65 118 167 85 176 81 97Z',
 'M133 45 173 18 169 176 137 167Z',
 'M184 105 240 138 240 217 188 199Z'
]
VERSIONS={
 'v1-primary-preserved':{'label':'Primary / unchanged from 08','paths':PRIMARY,'note':'Keeps the liked four-plane silhouette and projecting second apex.'},
 'v2-compact-open-fold':{'label':'Small-use A / open fold','paths':[
 'M16 136 62 111 58 217 16 207Z',
 'M78 90 120 66 116 165 86 173 82 94Z',
 'M136 45 173 18 169 176 140 167Z',
 'M188 108 240 138 240 217 192 199Z'
 ],'note':'Shortens the projecting apex and opens all three intervals; preserves unequal lower edges.'},
 'v3-compact-facets':{'label':'Small-use B / simplified facets','paths':[
 'M16 132 66 105 62 217 16 207Z',
 'M85 85 121 65 117 163 89 171Z',
 'M139 43 174 19 170 172 141 164Z',
 'M190 108 240 138 240 217 194 199Z'
 ],'note':'Removes the small projecting apex; four quieter quadrilaterals preserve the forecourt.'}
}
OPEN_COMPACT=[
 'M16 140 62 114 58 217 16 207Z',
 'M84 89 115 71 111 164 89 171 87 92Z',
 'M144 44 174 22 170 172 148 164Z',
 'M201 115 240 138 240 217 205 201Z'
]

def svg(paths,reverse=False,background=False,label='Shared Rhythm'):
 ink='#FFFFFF' if reverse else '#000000'
 bg='<rect width="256" height="256" fill="#000000"/>' if background else ''
 drawings=''.join(f'<path id="plane-{i+1}" fill="{ink}" d="{p}"/>' for i,p in enumerate(paths))
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" role="img" aria-labelledby="title"><title id="title">{label} — DRAFT — NOT FOR PUBLICATION</title><desc>Four unequal folded faces hold an open forecourt. Rising and falling surfaces suggest collective rhythm.</desc>{bg}{drawings}</svg>\n'

def component_count(im,threshold=128):
 im=im.convert('RGBA'); w,h=im.size
 ink={(x,y) for y in range(h) for x in range(w) if im.getpixel((x,y))[3]>=threshold}
 groups=[]
 while ink:
  seed=ink.pop(); stack=[seed]; group=[seed]
  while stack:
   x,y=stack.pop()
   for dx in (-1,0,1):
    for dy in (-1,0,1):
     q=(x+dx,y+dy)
     if q in ink:ink.remove(q);stack.append(q);group.append(q)
  groups.append(len(group))
 return groups

def main():
 (ROOT/'renders').mkdir(parents=True,exist_ok=True)
 fontpath=ROOT.parents[1]/'creative-review-05/assets/noto-sans-regular.ttf'
 font=ImageFont.truetype(str(fontpath),24)
 small=ImageFont.truetype(str(fontpath),18)
 counts={}
 board=Image.new('RGB',(1800,1450),'#F3F3F1');draw=ImageDraw.Draw(board)
 draw.text((40,28),'SHARED RHYTHM / SMALL-USE OPTICAL STUDIES',font=font,fill='black')
 draw.text((40,66),'DRAFT — NOT FOR PUBLICATION  /  Native 16–32 px below; enlarged pixels are diagnostic only.',font=small,fill='black')
 for col,(key,v) in enumerate(VERSIONS.items()):
  (ROOT/f'{key}.svg').write_text(svg(v['paths'],label=v['label']))
  x=col*590+25
  draw.text((x+8,112),v['label'],font=font,fill='black')
  counts[key]={}
  for rev in (False,True):
   mode='reverse' if rev else 'black';y=165+(610 if rev else 0)
   board.paste('black' if rev else 'white',(x,y,x+570,y+580))
   source=svg(v['paths'],reverse=rev,background=False,label=v['label'])
   for size in (16,20,24,32,64,512):
    out=ROOT/'renders'/f'{key}-{mode}-{size}.png'
    with tempfile.NamedTemporaryFile(mode='w',suffix='.svg',dir=ROOT/'renders') as tmp:
     tmp.write(source); tmp.flush()
     subprocess.run(['inkscape',tmp.name,f'--export-filename={out}',f'--export-width={size}',f'--export-height={size}'],check=True,capture_output=True)
    image=Image.open(out).convert('RGBA')
    if not rev:counts[key][str(size)]=component_count(image)
   large=Image.open(ROOT/'renders'/f'{key}-{mode}-512.png').convert('RGBA').resize((356,356),Image.Resampling.LANCZOS)
   board.paste(large,(x+107,y+8),large)
   for idx,size in enumerate((16,20,24,32)):
    tx=x+28+idx*139
    image=Image.open(ROOT/'renders'/f'{key}-{mode}-{size}.png').convert('RGBA')
    draw.text((tx,y+362),f'{size} px',font=small,fill='white' if rev else 'black')
    board.paste(image,(tx,y+396),image)
    enlarged=image.resize((size*4,size*4),Image.Resampling.NEAREST)
    board.paste(enlarged,(tx,y+440),enlarged)
   draw.text((x+18,y+553),'4× nearest-neighbor pixel enlargement',font=small,fill='white' if rev else 'black')
 board.save(ROOT/'renders'/'optical-development.png')
 (ROOT/'source'/'pixel-components.json').write_text(json.dumps(counts,indent=2)+'\n')
 print(json.dumps(counts,indent=2))
if __name__=='__main__':main()

# The last one-unit adjustment prevents diagonal fringe contact at16px; not a new concept.
def finalize():
 v4=OPEN_COMPACT.copy();v4[2]='M143 43 174 22 170 172 147 164Z'
 for name,paths in (('v4-compact-generous-intervals',v4),('v5-compact-pixel-intervals',OPEN_COMPACT)):
  (ROOT/f'{name}.svg').write_text(svg(paths,label='Shared Rhythm small-use study'))
 counts={}
 for name,paths in (('primary',PRIMARY),('compact',OPEN_COMPACT)):
  counts[name]={}
  (ROOT/f'{name}.svg').write_text(svg(paths,label=f'Shared Rhythm {name}'))
  reverse_file='reverse.svg' if name=='primary' else 'compact-reverse.svg'
  (ROOT/reverse_file).write_text(svg(paths,reverse=True,label=f'Shared Rhythm {name} reversed'))
  (ROOT/f'{name}-reverse-on-black.svg').write_text(svg(paths,reverse=True,background=True,label=f'Shared Rhythm {name} reversed'))
  for reverse in (False,True):
   mode='reverse' if reverse else 'black';counts[name][mode]={}
   for size in (16,20,24,32,64,512):
    out=ROOT/'renders'/f'{name}-{mode}-{size}.png'
    with tempfile.NamedTemporaryFile(mode='w',suffix='.svg',dir=ROOT/'renders') as tmp:
     tmp.write(svg(paths,reverse=reverse));tmp.flush()
     subprocess.run(['inkscape',tmp.name,f'--export-filename={out}',f'--export-width={size}',f'--export-height={size}'],check=True,capture_output=True)
    image=Image.open(out)
    counts[name][mode][str(size)]={str(t):len(component_count(image,t)) for t in (1,32,64,128,192,224)}
 (ROOT/'source'/'inkscape-pixel-components.json').write_text(json.dumps(counts,indent=2)+'\n')
 fontpath=ROOT.parents[1]/'creative-review-05/assets/noto-sans-regular.ttf'
 font=ImageFont.truetype(str(fontpath),24);small=ImageFont.truetype(str(fontpath),18)
 board=Image.new('RGB',(1440,1260),'#F3F3F1');draw=ImageDraw.Draw(board)
 draw.text((30,24),'SHARED RHYTHM / PRIMARY + SMALL-USE OPTICAL CUT',font=font,fill='black')
 draw.text((30,61),'DRAFT — NOT FOR PUBLICATION / same identity, two drawings for different sizes.',font=small,fill='black')
 for col,name in enumerate(('primary','compact')):
  x=24+col*710
  draw.text((x,105),'Primary / unchanged 08 silhouette' if name=='primary' else 'Compact / provisional 16–20 px only',font=font,fill='black')
  for row,mode in enumerate(('black','reverse')):
   y=150+row*535;bg='black' if row else 'white';ink='white' if row else 'black'
   board.paste(bg,(x,y,x+680,y+505))
   image=Image.open(ROOT/'renders'/f'{name}-{mode}-512.png').convert('RGBA').resize((340,340),Image.Resampling.LANCZOS)
   board.paste(image,(x+170,y+5),image)
   for idx,size in enumerate((16,20,24,32)):
    tx=x+30+idx*163
    draw.text((tx,y+355),f'{size}px',font=small,fill=ink)
    image=Image.open(ROOT/'renders'/f'{name}-{mode}-{size}.png').convert('RGBA')
    board.paste(image,(tx,y+385),image)
    enlarged=image.resize((size*2,size*2),Image.Resampling.NEAREST)
    board.paste(enlarged,(tx+66,y+380),enlarged)
   draw.text((x+23,y+463),'Native pixels at left; 2× diagnostic enlargement at right.',font=small,fill=ink)
 draw.text((30,1224),'Compact separates the four faces. Folded planes and shared interior are clearest in the primary at 32 px+.',font=small,fill='black')
 board.save(ROOT/'renders'/'primary-and-compact.png')
 print('Final SVGs and Inkscape native-size proofs rebuilt.')

if __name__=='__main__':finalize()
