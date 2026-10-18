#!/usr/bin/env python3
"""Render practical-width optical proofs, preserving natural SVG proportions.
Requires Inkscape and Pillow; output remains internal DRAFT review evidence.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
import re
import sys

HERE=Path(__file__).resolve().parents[1]
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)

def render(file,out,width,reverse=False):
    out.parent.mkdir(parents=True,exist_ok=True)
    source=file.read_text()
    if reverse:
        source=source.replace('#000000','#ffffff')
    temp=out.with_suffix('.svg')
    temp.write_text(source)
    subprocess.run(['inkscape',str(temp),'--export-type=png',f'--export-filename={out}',f'--export-width={width}',f'--export-background={"#000000" if reverse else "#ffffff"}','--export-background-opacity=1'],check=True,capture_output=True)
    temp.unlink()

for pass_no in ([int(v) for v in sys.argv[1:]] or (1,2,3)):
    target=HERE/f'proofs/pass-{pass_no}'
    samples=[]
    for orientation in ('horizontal','stacked'):
        file=HERE/f'developed/open-counter-{orientation}-v{pass_no}.svg'
        render(file,target/f'{orientation}-large.png',1600)
        for width in (320,240):
            for reverse in (False,True):
                out=target/f'{orientation}-{width}{"-reverse" if reverse else ""}.png'
                render(file,out,width,reverse)
                samples.append((orientation,width,reverse,out))
    # Each wordmark below is displayed at its real pixel width: no enlargement.
    sheet=Image.new('RGB',(760,700),'#ededed')
    draw=ImageDraw.Draw(sheet)
    draw.text((20,16),f'D — OPEN COUNTER / OPTICAL PASS {pass_no} / DRAFT — NOT FOR PUBLICATION',font=font,fill='black')
    for index,(orientation,width,reverse,out) in enumerate(samples):
        col=index%2;row=index//2
        x=20+col*370;y=61+row*153
        draw.text((x,y),f'{orientation} · {width}px · {"reverse" if reverse else "black"}',font=font,fill='black')
        img=Image.open(out).convert('RGB')
        sheet.paste(img,(x,y+25))
    sheet.save(target/'practical-widths.png')
    # Large reverse proof verifies that the tiny-size result is not concealing
    # rough joins or unwanted contour overlap at display scale.
    render(HERE/f'developed/open-counter-stacked-v{pass_no}.svg',target/'stacked-large-reverse.png',1600,True)
print('Rendered selected optical passes at 320/240px, black/reverse, plus large proofs.')
