from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import subprocess
P=Path(__file__).resolve().parent
DRAFT='DRAFT — NOT FOR PUBLICATION'
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
shapes={
'new-B8-lifted-lintel':('Lifted Lintel','M 35 207 V 83 H 116 C 149 83 177 62 207 31 L 233 58 C 204 94 170 120 128 120 H 74 V 207 Z'),
'new-B9-responsive-corner':('Responsive Corner','M 30 211 V 88 H 109 L 208 31 L 228 66 L 124 126 H 69 V 172 H 149 L 184 152 L 204 187 L 160 212 Z'),
'new-B10-unfolding-place':('Unfolding Place','M 29 203 V 67 H 112 L 161 35 L 181 65 L 124 103 H 67 V 166 H 146 L 185 136 V 91 L 222 66 V 154 L 158 203 Z'),
}
def svg(name,d):
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" role="img" aria-labelledby="title"><title id="title">B / {name} — {DRAFT}</title><desc>Direction B: one sheltering structure opens in expression. Original exploratory construction.</desc><path fill="#000000" d="{d}"/></svg>\n'
board=Image.new('RGB',(1500,680),'white');draw=ImageDraw.Draw(board)
font=ImageFont.truetype(F,20);small=ImageFont.truetype(F,14)
draw.text((24,20),DRAFT,font=small,fill='black')
for i,(stem,(name,d)) in enumerate(shapes.items()):
 (P/(stem+'.svg')).write_text(svg(name,d))
 subprocess.run(['inkscape',str(P/(stem+'.svg')),'--export-type=png',f'--export-filename={P/(stem+".png")}','--export-width=440'],check=True,capture_output=True)
 im=Image.open(P/(stem+'.png')).convert('RGBA');board.paste(im,(i*500+30,90),im)
 draw.text((i*500+35,580),name,font=font,fill='black')
board.save(P/'new-structural-review.png')
