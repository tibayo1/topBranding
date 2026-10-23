from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import subprocess
P=Path(__file__).resolve().parent
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';DRAFT='DRAFT — NOT FOR PUBLICATION'
paths={
'passing-v1':('Passing Shelter / integrated fold','M 24 101 C 68 78 111 83 148 111 C 184 138 199 164 234 169 L 222 205 C 184 196 158 169 137 141 C 126 127 119 122 109 123 C 100 125 98 133 103 146 C 114 166 145 181 173 193 L 170 204 C 127 187 79 191 47 211 C 48 178 67 148 88 132 C 66 131 44 143 24 155 Z M 157 102 C 181 82 190 39 233 36 V 77 C 208 82 194 113 175 128 Z'),
'passing-v2':('Passing Shelter / open interval','M 24 101 C 68 78 111 83 148 111 C 184 138 199 164 234 169 L 222 205 C 184 196 158 169 137 141 C 126 127 119 122 109 123 C 100 125 98 133 103 146 C 114 166 143 179 172 191 L 162 210 C 123 191 79 196 47 215 C 49 180 67 148 88 132 C 66 131 44 143 24 155 Z M 157 101 C 181 81 190 38 233 35 V 76 C 208 81 194 112 175 127 Z'),
'passing-v3':('Passing Shelter / broadened return','M 24 101 C 68 78 111 83 148 111 C 184 138 199 164 234 169 L 222 205 C 184 196 158 169 137 141 C 126 127 119 122 109 123 C 100 125 98 133 103 146 C 114 166 140 179 166 190 L 157 212 C 119 193 80 199 47 218 C 48 181 67 148 88 132 C 66 131 44 143 24 155 Z M 157 101 C 181 81 190 38 233 35 V 76 C 208 81 194 112 175 127 Z'),
}
def svg(name,d,fill='#000000'):
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" role="img" aria-labelledby="title"><title id="title">B / {name} — {DRAFT}</title><desc>A sheltering surface turns inward to hold one shared interval and passes outward in uplift. Original direction B, not an approved identity.</desc><path fill="{fill}" d="{d}"/></svg>\n'
def render(stem,size=512):
 subprocess.run(['inkscape',str(P/(stem+'.svg')),'--export-type=png',f'--export-filename={P/(stem+".png")}',f'--export-width={size}'],check=True,capture_output=True)
 return Image.open(P/(stem+'.png')).convert('RGBA')
board=Image.new('RGB',(1500,700),'white');dr=ImageDraw.Draw(board)
font=ImageFont.truetype(F,18);small=ImageFont.truetype(F,14);dr.text((24,20),DRAFT,font=small,fill='black')
for i,(stem,(name,d)) in enumerate(paths.items()):
 (P/(stem+'.svg')).write_text(svg(name,d));im=render(stem,440);board.paste(im,(i*500+30,90),im);dr.text((i*500+35,590),name,font=font,fill='black')
board.save(P/'passing-integrated-review.png')
