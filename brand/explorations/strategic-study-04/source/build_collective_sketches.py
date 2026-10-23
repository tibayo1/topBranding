#!/usr/bin/env python3
"""Rebuild four initial monochrome studies. DRAFT, not a final identity."""
from pathlib import Path
import json
from html import escape
ROOT=Path(__file__).resolve().parents[1]
STUDIES=[
 {
 'id':'07','territory':'D','name':'Common Ground',
 'idea':'Unequal broad surfaces depend on one another to make a single generous room; gathering creates the dwelling.',
 'approach':'Sculpted interdependent planes',
 'construction':['Four unequal filled surfaces describe a shared room in an abstract oblique view.','The room and its front opening are actual transparent space; its perimeter belongs to all the parts.','Height and curve vary between contributions without introducing heads, figures, or a central leader.','The number of components is compositional, with no theological claim.'],
 'risk':'Can read as a vessel or amphitheater rather than a sacred dwelling; narrow upper seams need proof at 16px.',
 'why':'Strongest of the collective studies: the room exists because the contributions cooperate, and the silhouette avoids a crown or ring of people.',
 'markinnerSVG':'<path fill="#000000" d="M24 102 C24 74 42 54 78 26 L78 126 C57 128 40 136 39 147 C28 137 24 124 24 102 Z"/><path fill="#000000" d="M92 62 C124 92 170 104 212 106 V134 C201 143 190 150 180 154 V129 C145 124 118 123 92 124 Z"/><path fill="#000000" d="M24 126 C36 156 78 174 120 180 V226 C72 225 42 217 24 207 Z"/><path fill="#000000" d="M166 164 C197 153 221 137 238 118 V208 C215 221 194 225 166 227 Z"/>'
 },
 {
 'id':'08','territory':'D','name':'A Common Centre',
 'idea':'Unequal organic contributions orient toward one generous shared interior rather than orbiting a leader or figure.',
 'approach':'Organic negative-space gathering',
 'construction':['Five broad, unequal curved surfaces gather around an off-center open room.','Separate pieces leave visible joints and a generous lower opening.','The shared interior is transparent space, not a representation of God.'],
 'risk':'The lobed perimeter may read as a flower or a generic community organization; the assembly is less immediately memorable than 07.',
 'why':'Provides a soft welcoming counterpoint, but should be set aside unless the parish strongly prefers an organic gathering over architectural clarity.',
 'markinnerSVG':'<path fill="#000000" d="M68 77 C100 51 138 31 157 34 C168 38 162 79 177 101 C146 105 116 82 68 83 Z"/><path fill="#000000" d="M66 89 C84 83 92 122 90 157 C68 151 59 142 45 137 C43 113 53 98 66 89 Z"/><path fill="#000000" d="M38 147 C53 147 70 165 92 172 L120 181 Q126 184 126 190 V214 C85 219 51 211 31 201 C22 184 21 159 28 150 Q32 146 38 147 Z"/><path fill="#000000" d="M177 69 C196 70 219 80 222 99 V123 C215 125 207 129 199 132 C183 117 175 94 177 69 Z"/><path fill="#000000" d="M169 162 C191 157 210 146 229 133 Q239 127 241 141 V199 C223 214 203 224 175 228 V181 Q175 168 169 162 Z"/>'
 },
 {
 'id':'09','territory':'E','name':'Cadenced Wall',
 'idea':'A folded wall changes height and turns around a shared forecourt; the structure itself carries an expressive cadence.',
 'approach':'Architectural pleat and negative-space rhythm',
 'construction':['Five broad faces form a long pleated architectural surface, with different widths and heights.','The top and lower edges change together to describe a turned wall rather than independent equalizer bars.','Transparent triangular seams articulate the folds; the forecourt remains open in front of them.','This is a modern architectural metaphor, not a reconstruction of the biblical tabernacle.'],
 'risk':'Can suggest a cultural venue or civic building; its width and creases are less robust as a tiny avatar than a compact silhouette.',
 'why':'A credible non-instrument test of a dwelling that sings: rhythm belongs to the material and scale of the enclosure.',
 'markinnerSVG':'<path fill="#000000" d="M20 150 L54 120 V216 L20 230 Z"/><path fill="#000000" d="M66 128 L92 143 V204 L72 212 Z"/><path fill="#000000" d="M104 132 L130 108 L162 115 V194 L130 191 L104 201 Z"/><path fill="#000000" d="M174 96 L208 34 V224 L174 201 Z"/><path fill="#000000" d="M220 59 L236 93 V220 L220 224 Z"/>'
 },
 {
 'id':'10','territory':'E','name':'Lifted Surface',
 'idea':'A covering sweeps upward into one lifted fold, making shelter and expression arise from the same surface.',
 'approach':'Continuous sculpted covering',
 'construction':['A broad curved covering rises from a low left edge into one high fold.','The two end faces reveal the thickness and turn of the same surface.','A large opening below the covering is actual transparent space, with no attached praise icon.'],
 'risk':'Its shelter reading is clear, but it overlaps the broader canopy territory; the rise can suggest a sail or performance venue.',
 'why':'An expressive one-gesture alternative, set aside if the joined-covering territory already supplies the stronger and more distinctive version.',
 'markinnerSVG':'<path fill="#000000" d="M26 143 C97 119 158 77 204 25 C207 104 178 133 100 142 C70 146 46 145 26 143 Z"/><path fill="#000000" d="M26 143 L82 159 V208 C62 206 44 209 26 215 Z"/><path fill="#000000" d="M204 25 L236 147 V215 L204 203 Z"/>'
 }
]
for item in STUDIES:
    item['viewBox']='0 0 256 256'
    filename=f"{item['id']}-{item['name'].lower().replace(' ','-')}-v2.svg"
    item['file']=f'sketches/{filename}'
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" role="img" aria-labelledby="title desc"><title id="title">{escape(item['id']+' — '+item['name'])} — DRAFT — NOT FOR PUBLICATION</title><desc id="desc">{escape(item['idea']+' Initial strategic sketch, not an approved identity.')}</desc>{item['markinnerSVG']}</svg>\n'''
    (ROOT/item['file']).write_text(svg)
    if item['id'] in ('07','09'):
        item['conceptFile']='concepts/'+filename
        (ROOT/item['conceptFile']).write_text(svg)
(ROOT/'source/collective-sketches.json').write_text(json.dumps(STUDIES,indent=2,ensure_ascii=False)+'\n')
