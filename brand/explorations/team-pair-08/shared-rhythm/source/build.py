#!/usr/bin/env python3
"""Rebuild three intentionally close, editable Shared Rhythm symbol studies.
The favored raster is retained separately in praise-study-07; these are new path drawings.
"""
from pathlib import Path
import json
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
VERSIONS = {
 'v1-faithful-reconstruction': {
  'label': '01 / Faithful reconstruction',
  'note': 'Four folded planes; preserves the favored sketch silhouette.',
  'paths': [
   'M16 132 71 102 67 217 16 207Z',
   'M67 95 122 65 118 167 85 176 81 97Z',
   'M133 45 173 18 169 176 137 167Z',
   'M184 105 240 138 240 217 188 199Z'
  ]
 },
 'v2-open-intervals': {
  'label': '02 / More even open intervals',
  'note': 'Opens the first interval by two units; the four-plane idea is unchanged.',
  'paths': [
   'M16 132 69 103 65 217 16 207Z',
   'M67 95 122 65 118 167 85 176 81 97Z',
   'M133 45 173 18 169 176 137 167Z',
   'M184 105 240 138 240 217 188 199Z'
  ]
 },
 'v3-courtyard-and-apex': {
  'label': '03 / Quieter apex, deeper court',
  'note': 'Shortens the projecting second apex and raises the two inner lower edges.',
  'paths': [
   'M16 132 69 103 65 217 16 207Z',
   'M70 94 122 65 118 164 85 173 81 97Z',
   'M133 45 173 18 169 173 137 164Z',
   'M184 105 240 138 240 217 188 199Z'
  ]
 }
}

def svg(paths, reverse=False, background=False, label='Shared Rhythm'):
 ink = '#FFFFFF' if reverse else '#000000'
 bg = '<rect width="256" height="256" fill="#000000"/>' if background else ''
 drawings = ''.join(f'<path id="plane-{i+1}" fill="{ink}" d="{d}"/>' for i,d in enumerate(paths))
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" role="img" aria-labelledby="title"><title id="title">{label} — DRAFT — NOT FOR PUBLICATION</title><desc>Four unequal folded planes open around a shared white forecourt. An abstract spatial rhythm, with no added harp, cross or human figure.</desc>{bg}{drawings}</svg>\n'

def render(source, size, out):
 with tempfile.NamedTemporaryFile(suffix='.svg', mode='w', dir=ROOT/'renders') as temp:
  temp.write(source); temp.flush()
  subprocess.run(['inkscape', temp.name, f'--export-filename={out}', f'--export-width={size}', f'--export-height={size}'], check=True, capture_output=True)

ROOT.mkdir(parents=True,exist_ok=True)
(ROOT/'renders').mkdir(exist_ok=True)
font_path = ROOT.parents[1]/'creative-review-05/assets/noto-sans-regular.ttf'
font = ImageFont.truetype(str(font_path),24)
small = ImageFont.truetype(str(font_path),18)
board = Image.new('RGB',(1680,1310),'#F5F5F3')
draw = ImageDraw.Draw(board)
draw.text((42,26),'SHARED RHYTHM / LIMITED OPTICAL DEVELOPMENT',font=font,fill='black')
for col,(key,version) in enumerate(VERSIONS.items()):
 x=col*550+25
 (ROOT/f'{key}.svg').write_text(svg(version['paths'],label=version['label']))
 for rev in (False,True):
  mode='reverse' if rev else 'black'
  source=svg(version['paths'],reverse=rev,background=rev,label=version['label'])
  render(source,512,ROOT/'renders'/f'{key}-{mode}-512.png')
  for size in (16,24,32,64):render(source,size,ROOT/'renders'/f'{key}-{mode}-{size}.png')
 draw.text((x+15,84),version['label'],font=small,fill='black')
 for row,mode in enumerate(('black','reverse')):
  y=128+row*553
  board.paste('#000000' if row else '#FFFFFF',(x,y,x+520,y+520))
  pic=Image.open(ROOT/'renders'/f'{key}-{mode}-512.png').convert('RGBA')
  proof = pic.resize((448,448), Image.Resampling.LANCZOS)
  board.paste(proof,(x+36,y+10),proof)
  px=x+19
  for size in (16,24,32,64):
   image=Image.open(ROOT/'renders'/f'{key}-{mode}-{size}.png').convert('RGBA')
   board.paste(image,(px,y+453),image)
   draw.text((px,y+427),str(size),font=small,fill='white' if row else 'black')
   px+=113
board.save(ROOT/'renders'/'optical-development.png')
# Candidate 02 is the deliberately conservative primary. Its geometry is identical in reverse.
selected=VERSIONS['v2-open-intervals']['paths']
(ROOT/'primary.svg').write_text(svg(selected))
(ROOT/'reverse.svg').write_text(svg(selected,reverse=True))
(ROOT/'reverse-on-black.svg').write_text(svg(selected,reverse=True,background=True))
for size in (16,24,32,64,512):
 render(svg(selected),size,ROOT/'renders'/f'primary-black-{size}.png')
 render(svg(selected,reverse=True,background=True),size,ROOT/'renders'/f'primary-reverse-{size}.png')
