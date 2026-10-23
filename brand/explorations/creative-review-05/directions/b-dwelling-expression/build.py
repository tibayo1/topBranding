from pathlib import Path
import json, subprocess
from PIL import Image, ImageDraw, ImageFont
P=Path(__file__).resolve().parent
DRAFT='DRAFT — NOT FOR PUBLICATION'
shapes={
'initial-B1-unfurling-house': ('B1 / Unfurling House', 'M 197 28 C 177 69 180 99 183 125 C 188 170 166 203 129 215 C 85 229 40 202 34 161 C 29 125 50 97 80 83 C 104 72 127 65 140 44 C 141 78 122 101 92 115 C 68 126 57 141 62 159 C 68 185 98 195 122 186 C 149 176 154 151 150 127 C 144 86 160 51 197 28 Z'),
'initial-B2-joined-welcome': ('B2 / Joined Welcome', 'M 124 29 C 73 39 37 75 30 123 C 25 162 46 199 78 217 L 94 192 C 70 179 57 154 61 129 C 66 95 90 70 124 61 Z M 132 29 L 132 61 C 167 66 192 90 197 123 C 201 150 187 177 164 191 L 148 162 C 134 178 117 191 98 198 L 114 228 C 176 218 217 183 226 135 C 236 82 194 39 132 29 Z'),
'initial-B3-breathing-court': ('B3 / Breathing Court', 'M 47 50 H 144 C 177 50 198 40 220 24 C 207 62 183 82 148 82 H 78 V 174 H 174 V 110 C 174 94 190 78 206 72 V 183 C 206 199 198 206 182 206 H 66 C 34 206 26 190 26 163 V 78 C 26 59 31 50 47 50 Z'),
}
def svg(name,d):
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" role="img" aria-labelledby="title"><title id="title">{name} — {DRAFT}</title><desc>Tabernacle of Praise creative review 05, Direction B. Exploratory original drawing.</desc><path fill="#000000" fill-rule="evenodd" d="{d}"/></svg>\n'
for stem,(name,d) in shapes.items():
 (P/(stem+'.svg')).write_text(svg(name,d))

def render(stem):
 out=P/(stem+'.png')
 subprocess.run(['inkscape',str(P/(stem+'.svg')),'--export-type=png',f'--export-filename={out}','--export-width=512'],check=True,capture_output=True)
 return Image.open(out).convert('RGBA')
if __name__=='__main__':
 board=Image.new('RGB',(1500,700),'white');dr=ImageDraw.Draw(board)
 for i,stem in enumerate(shapes):
  im=render(stem); board.paste(im,(i*500,70),im)
  dr.text((i*500+35,610),shapes[stem][0],fill='black')
 dr.text((35,30),DRAFT,fill='black')
 board.save(P/'initials-review.png')

v1='M 73 54 C 103 54 128 65 151 63 C 172 61 188 47 201 30 L 222 50 C 203 79 179 95 152 95 C 125 95 103 84 78 84 H 68 V 158 C 68 178 82 190 104 190 H 143 C 166 190 181 176 181 155 V 128 C 181 112 188 101 200 92 L 222 111 C 215 117 213 124 213 137 V 157 C 213 195 187 221 145 221 H 103 C 61 221 35 196 35 159 V 87 C 35 65 50 54 73 54 Z'
(P/'developed-v1.svg').write_text(svg('B / Opening Offering / First refinement',v1))
im=render('developed-v1')
board=Image.new('RGB',(1100,680),'white');dr=ImageDraw.Draw(board)
board.paste(im,(0,80),im)
dr.text((30,30),DRAFT,fill='black')
for row,(fill,bg) in enumerate([('#000000','#ffffff'),('#ffffff','#000000')]):
 for j,size in enumerate([16,24,32,64]):
  src=svg('B / true size stress test',v1).replace('#000000',fill)
  f=P/f'test-v1-{row}-{size}.svg'; f.write_text(src)
  out=f.with_suffix('.png')
  subprocess.run(['inkscape',str(f),'--export-type=png',f'--export-filename={out}',f'--export-width={size}'],check=True,capture_output=True)
  x=570+j*120;y=155+row*160
  dr.rectangle((x-15,y-35,x+85,y+100),fill=bg)
  z=Image.open(out).convert('RGBA');board.paste(z,(x,y),z)
  dr.text((x,y+size+12),str(size)+' px',fill=fill)
board.save(P/'refinement-v1-review.png')

v2='M 66 62 C 95 50 128 70 152 62 C 171 54 187 38 200 23 L 222 44 C 205 77 177 97 149 98 C 124 99 104 85 81 90 C 63 94 56 108 56 127 C 56 160 77 182 109 190 C 143 199 176 177 179 145 C 180 124 188 108 202 95 L 224 115 C 214 126 213 139 210 157 C 205 198 168 226 128 225 C 73 222 30 181 27 136 C 24 97 39 72 66 62 Z'
(P/'developed-v2.svg').write_text(svg('B / Opening Offering / Second refinement',v2))
im=render('developed-v2')
board=Image.new('RGB',(1100,680),'white');dr=ImageDraw.Draw(board)
board.paste(im,(0,80),im)
dr.text((30,30),DRAFT,fill='black')
for row,(fill,bg) in enumerate([('#000000','#ffffff'),('#ffffff','#000000')]):
 for j,size in enumerate([16,24,32,64]):
  src=svg('B / true size stress test',v2).replace('#000000',fill)
  f=P/f'test-v2-{row}-{size}.svg';f.write_text(src)
  out=f.with_suffix('.png')
  subprocess.run(['inkscape',str(f),'--export-type=png',f'--export-filename={out}',f'--export-width={size}'],check=True,capture_output=True)
  x=570+j*120;y=155+row*160
  dr.rectangle((x-15,y-35,x+85,y+100),fill=bg)
  z=Image.open(out).convert('RGBA');board.paste(z,(x,y),z)
  dr.text((x,y+size+12),str(size)+' px',fill=fill)
board.save(P/'refinement-v2-review.png')
