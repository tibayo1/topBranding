#!/usr/bin/env python3
"""Editable geometric studies. DRAFT — NOT FOR PUBLICATION."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
def svg(name, idea, paths):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" role="img"><title>{name} — DRAFT</title><desc>DRAFT — NOT FOR PUBLICATION. {idea}</desc><g fill="#000000">{paths}</g></svg>'''

studies={
 'a1-open-court.svg': ('Open Court', 'A canted court holds a generous shared interior, and one opening joins entering with response.', '''<path d="M124 22 C130 19 135 21 140 26 L218 103 C230 115 232 128 224 141 L187 202 L162 187 L195 133 C198 128 196 123 192 119 L129 56 L72 112 L48 90 Z"/><path d="M35 115 L62 131 L50 153 C47 159 49 164 55 167 L125 208 C130 211 135 211 140 207 L153 197 L177 216 L156 231 C141 241 127 240 114 232 L33 184 C20 176 16 164 22 151 Z"/>'''),
 'a2-resonant-chamber.svg': ('Resonant Chamber', 'Two enclosing forms make a room whose opening widens upward: the interior and its outward response share one contour.', '''<path d="M112 22 L112 54 C78 57 55 81 51 112 C46 150 66 176 100 185 L100 218 C48 209 16 169 20 120 C24 67 59 29 112 22 Z"/><path d="M136 39 C190 41 232 80 236 131 C241 187 205 226 150 234 L150 201 C184 196 207 170 204 136 C201 103 175 77 136 73 Z"/><path d="M76 110 C88 95 104 90 124 91 L169 91 L169 120 L124 120 C107 120 97 127 92 138 Z"/>'''),
 'a3-common-centre.svg': ('Common Centre', 'Three inward-turning boundaries make one common room while leaving broad ways through its perimeter.', '''<path d="M126 18 C131 17 136 20 140 26 L193 103 L168 120 L127 61 L82 85 L62 57 Z"/><path d="M218 90 C224 91 228 96 228 103 L225 191 C225 203 219 208 207 209 L122 215 L120 182 L190 178 L192 111 Z"/><path d="M98 230 C93 233 87 231 83 226 L29 157 C21 147 23 139 31 132 L94 81 L114 108 L63 151 L106 207 Z"/>''')
}

def write():
    for filename,(name,idea,paths) in studies.items():
        (ROOT/filename).write_text(svg(name,idea,paths))
    (ROOT/'developed-v1.svg').write_text(svg('Open Court / development 1', 'A room takes shape between two turning boundaries. The enclosing structure opens toward the upper right, carrying the gathering outward.', '''<path d="M30 74 L169 29 L228 59 L228 210 L197 220 L197 91 L167 76 L30 116 Z"/><path d="M30 96 L64 111 L64 177 L126 199 L176 185 L176 219 L126 235 L30 201 Z"/>'''))
    (ROOT/'developed-v2.svg').write_text(svg('Gathered Interval / development 2', 'A nonrectangular shared room is made between two shaped enclosing masses. The boundaries turn outward at the same places where the room opens.', '''<path d="M136 24 C102 16 75 28 56 54 L26 103 C10 131 14 163 40 183 L84 218 L102 190 L63 158 C51 148 48 134 57 119 L82 79 C92 63 106 59 126 63 L170 72 L181 36 Z"/><path d="M203 57 L174 80 L199 112 C210 126 209 142 196 153 L163 181 C149 193 135 195 119 187 L100 218 C128 234 157 231 184 211 L222 180 C252 155 252 122 230 92 Z"/>'''))
    (ROOT/'test-open-crossing.svg').write_text(svg('Open Crossing / study', 'An explicitly Christian sacred interior opens upward through the surrounding form. This is contemporary spatial symbolism, not a historical tabernacle plan.', '''<path d="M108 25 C75 27 47 47 31 77 L20 124 C14 163 36 200 68 219 C101 239 155 239 188 219 C220 200 242 163 236 124 L225 77 C209 47 181 27 148 25 L148 96 L186 96 L186 133 L148 133 L148 187 L108 187 L108 133 L70 133 L70 96 L108 96 Z"/>'''))

if __name__=='__main__': write()
