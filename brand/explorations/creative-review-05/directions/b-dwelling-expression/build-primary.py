"""Rebuild review-only Direction B artwork, raster tests, and two visual passes.
Run: python3 directions/b-dwelling-expression/build-primary.py
Needs Python 3, Pillow, Inkscape. Shapes remain editable filled SVG paths.
DRAFT — NOT FOR PUBLICATION. No logo is approved.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import subprocess
P=Path(__file__).resolve().parent
DRAFT='DRAFT — NOT FOR PUBLICATION'
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
D4='M 24 101 C 68 78 111 83 148 111 C 184 138 199 164 234 169 L 222 205 C 184 196 158 169 137 141 C 126 127 119 122 109 123 C 100 125 98 133 103 146 C 114 166 140 179 166 190 L 157 212 C 123 197 86 194 58 204 C 47 208 43 205 44 193 C 48 164 66 143 88 132 C 66 131 44 143 24 155 Z M 157 101 C 181 81 190 38 233 35 V 76 C 208 81 194 112 175 127 Z'
D5='M 24 99 C 67 77 109 82 146 110 C 182 137 198 162 233 167 L 222 201 C 185 193 158 166 137 139 C 126 126 119 122 109 124 C 100 126 99 135 105 147 C 116 166 141 179 166 189 L 156 212 C 123 198 88 195 60 204 C 48 208 44 205 45 193 C 49 164 67 143 88 132 C 66 132 44 144 24 155 Z M 159 98 C 182 78 191 37 233 34 V 74 C 209 79 196 109 178 124 Z'
D6='M 24 99 C 67 77 109 82 146 110 C 182 137 198 162 233 167 L 223.89 201 C 185 193 158 166 137 139 C 126 126 119 122 109 124 C 100 126 99 135 105 147 C 116 166 141 179 166 189 L 159.84 212 C 123 198 88 195 60 204 C 48 208 44 205 45 193 C 49 164 67 143 88 132 C 66 132 44 144 24 155 Z M 158 98 C 182 78 191 37 233 34 V 74 C 209 79 196 109 181 121 Z'
DESCR='DRAFT — NOT FOR PUBLICATION. A broad sheltering surface turns inward around a shared interval, then passes outward in uplift. The integrated return belongs to the sheltering surface; the separated upper continuation makes the over-under passage legible. Original parish identity exploration.'
def svg(name,d,fill='#000000'):
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" role="img" aria-labelledby="title"><title id="title">B / {name} — {DRAFT}</title><desc>{DESCR}</desc><path fill="{fill}" d="{d}"/></svg>\n'
def render(stem,size=512):
 src=P/(stem+'.svg');out=P/(stem+'.png')
 subprocess.run(['inkscape',str(src),'--export-type=png',f'--export-filename={out}',f'--export-width={size}'],check=True,capture_output=True)
 return Image.open(out).convert('RGBA')
def board(stem,d):
 (P/(stem+'.svg')).write_text(svg('Passing Shelter / '+stem,d))
 im=render(stem,512)
 out=Image.new('RGB',(1260,750),'white');dr=ImageDraw.Draw(out)
 font=ImageFont.truetype(F,20);small=ImageFont.truetype(F,13)
 dr.text((28,20),DRAFT,font=small,fill='black');dr.text((28,55),'B / Passing Shelter',font=font,fill='black')
 out.paste(im,(15,115),im)
 for row,(label,fill,bg) in enumerate([('Black on white','#000000','#ffffff'),('White on black','#ffffff','#000000')]):
  y=155+row*250
  dr.rectangle((560,y-35,1230,y+195),fill=bg)
  dr.text((580,y-20),label,font=small,fill=fill)
  for j,size in enumerate([16,24,32,64]):
   name=f'{stem}-'+('black' if row==0 else 'reverse')+f'-{size}'
   (P/(name+'.svg')).write_text(svg('Passing Shelter / exact '+str(size)+' px',d,fill))
   z=render(name,size);x=605+j*145
   out.paste(z,(x,y+45),z);dr.text((x,y+125),str(size)+' px',font=small,fill=fill)
 dr.text((28,690),'Exact-size rasters; no enlargement. One filled-path master with an actual open interval.',font=small,fill='black')
 out.save(P/(stem+'-review.png'))
for stem,d in [('passing-v4',D4),('passing-v5',D5),('passing-v6',D6)]:board(stem,d)
(P/'primary.svg').write_text(svg('Passing Shelter / developed proposal',D6))
(P/'primary-reverse.svg').write_text(svg('Passing Shelter / reverse proposal',D6,'#ffffff'))
render('primary',1024);render('primary-reverse',1024)
# Primary exact-size SVG and PNG files are assets used by the creative review.
for variant,fill in [('black','#000000'),('reverse','#ffffff')]:
 for size in [16,24,32,64]:
  stem=f'primary-{variant}-{size}';(P/(stem+'.svg')).write_text(svg('Passing Shelter / '+variant+' '+str(size)+' px',D6,fill));render(stem,size)
