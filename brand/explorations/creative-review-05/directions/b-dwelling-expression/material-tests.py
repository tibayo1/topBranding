exec((__import__('pathlib').Path(__file__).parent/'build.py').read_text().split("v1=")[0])
new={
'new-B4-gathering-fold':('B4 / Gathering Fold','M 24 62 C 66 64 100 84 125 113 C 148 139 176 141 226 113 L 235 144 C 190 178 148 173 118 142 C 94 117 70 100 39 101 L 49 150 C 57 181 91 198 121 187 C 111 200 98 210 78 210 C 49 210 28 190 23 162 L 8 81 Z M 235 144 C 217 173 192 193 161 197 C 134 200 114 188 96 169 C 124 180 149 175 167 162 C 192 170 214 163 235 144 Z'),
'new-B5-common-bearing':('B5 / Common Bearing','M 20 70 C 56 70 82 79 109 100 L 151 135 C 171 152 194 162 235 163 L 235 195 C 186 195 156 181 130 159 L 88 124 C 65 105 44 100 20 102 Z M 235 57 V 89 C 195 89 173 102 151 123 L 130 143 C 111 162 90 178 61 183 L 22 190 L 16 158 L 52 151 C 77 147 95 134 109 120 L 130 100 C 158 73 187 57 235 57 Z'),
'new-B6-turning-screen':('B6 / Turning Screen','M 19 93 C 58 51 89 38 122 51 C 158 65 175 110 211 104 L 236 98 L 244 128 L 217 135 C 176 145 150 112 130 92 C 113 75 96 73 78 82 C 64 89 52 100 42 113 Z M 217 135 C 191 181 153 214 114 206 C 81 199 64 170 31 178 L 16 182 L 8 150 L 24 146 C 64 136 91 168 116 174 C 143 180 168 162 185 140 C 197 141 207 139 217 135 Z'),
}
board=Image.new('RGB',(1500,650),'white');dr=ImageDraw.Draw(board)
for i,(stem,(name,d)) in enumerate(new.items()):
 (P/(stem+'.svg')).write_text(svg(name,d))
 im=render(stem);board.paste(im,(500*i,50),im);dr.text((500*i+35,590),name,fill='black')
dr.text((35,25),DRAFT,fill='black');board.save(P/'new-material-review.png')
b7='M 18 63 C 52 64 65 95 94 97 C 108 98 122 92 135 85 L 124 105 C 102 127 80 129 58 120 C 43 113 31 108 18 105 Z M 30 150 C 69 146 85 104 116 87 C 145 71 164 79 182 103 C 207 137 218 141 239 137 V 170 C 210 176 190 162 170 136 C 155 116 145 105 132 111 C 112 120 99 147 76 159 C 61 167 45 169 30 167 Z M 87 165 C 111 174 139 174 161 160 L 179 179 C 143 198 112 194 87 183 Z'
(P/'new-B7-gathered-release.svg').write_text(svg('B7 / Gathered Release',b7))
im=render('new-B7-gathered-release')
board=Image.new('RGB',(700,650),'white');dr=ImageDraw.Draw(board);board.paste(im,(80,30),im);dr.text((30,25),DRAFT,fill='black');board.save(P/'new-B7-review.png')
