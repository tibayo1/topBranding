#!/usr/bin/env python3
"""Render exact pixel tests with Inkscape and place them at 1:1 on a board."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'renders';R.mkdir(exist_ok=True)
F=ROOT.parents[1]/'creative-review-05/assets/noto-sans-regular.ttf'
font=ImageFont.truetype(str(F),18)
small=ImageFont.truetype(str(F),13)
for stem in ['primary','reverse']:
    for size in [16,24,32,64,512]:
        out=R/f'{stem}-{size}.png'
        subprocess.run(['inkscape',str(ROOT/f'{stem}.svg'),'--export-type=png',f'--export-filename={out}',f'--export-width={size}',f'--export-height={size}'],check=True,capture_output=True)
board=Image.new('RGB',(1200,900),'#ffffff');d=ImageDraw.Draw(board)
d.text((36,25),'OPEN PRAISE  /  DRAFT — NOT FOR PUBLICATION',font=font,fill='#111111')
d.text((36,61),'One open contour: P-like outer mass, negative T exiting through the lower edge.',font=small,fill='#333333')
for col,version in enumerate(['v1-counterform','v2-open-counter']):
    im=Image.open(R/f'{version}.png').convert('RGBA');im.thumbnail((256,256),Image.Resampling.LANCZOS)
    x=95+col*380;board.paste(im,(x,118),im)
    d.text((x,390),version,font=font,fill='#111111')
d.text((870,130),'Primary change:',font=font,fill='#111111')
for idx,line in enumerate(['Wider usable crossbar.','Shorter pointed hook.','Open lower T retained.','One silhouette, no seams.']):d.text((870,166+idx*31),line,font=small,fill='#333333')
d.line((36,438,1164,438),fill='#cccccc',width=1)
for row,stem in enumerate(['primary','reverse']):
    y=487+row*163
    if stem=='reverse':d.rectangle((36,y-18,1164,y+125),fill='#000000')
    ink='#111111' if stem=='primary' else '#ffffff'
    d.text((55,y),('BLACK / native pixels' if stem=='primary' else 'REVERSE / native pixels'),font=font,fill=ink)
    for j,size in enumerate([64,32,24,16]):
        x=380+j*178
        im=Image.open(R/f'{stem}-{size}.png').convert('RGBA')
        board.paste(im,(x+(64-size)//2,y),im)
        d.text((x,y+84),str(size)+' px',font=small,fill=ink)
d.text((36,842),'At 16 px the tapered hook softens; judge the T as a broad opening, not a fragile terminal.',font=small,fill='#333333')
board.save(R/'optical-development.png')
