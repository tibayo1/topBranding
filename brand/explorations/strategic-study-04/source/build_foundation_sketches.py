"""Initial monochrome hypotheses: meaning and construction precede selection."""
from pathlib import Path
import json
from html import escape
ROOT=Path(__file__).resolve().parents[1]
P=lambda d:'<path d="'+d+'"/>'
studies=[
 {'id':'01','territory':'A','name':'Responsive Cover','idea':'Two broad textile folds make a shared interior and turn their meeting into an upward opening.','approach':'Organic material / containing gesture','mark':P('M24 112 C50 68 83 56 124 72 L108 100 C76 90 58 110 48 140 L88 184 L60 208 L20 160 C10 144 12 130 24 112 Z')+P('M134 42 C171 50 198 70 220 102 C239 132 237 160 222 184 L195 166 C209 145 205 124 192 106 C178 86 160 77 142 74 L126 124 L98 114 Z'),'construction':['Two substantial, asymmetric curved panels, not an arch with a separate figure.','The space held between the panels is part of the construction.'],'risk':'The organic embrace can suggest a general care charity; the covering is abstract.'},
 {'id':'02','territory':'A','name':'Coupled Fabric','idea':'Separate textile lengths become one woven dwelling through a visible over-and-under relationship.','approach':'Interdependence / geometric weave','mark':P('M32 40 H168 V72 H64 V168 H32 Z')+P('M184 40 H224 V184 H192 V80 H184 Z')+P('M88 88 H160 V120 H120 V192 H224 V224 H88 Z'),'construction':['Broad orthogonal textile lengths turn around a shared center.','Alternating interruptions suggest coupling rather than extra ornament.'],'risk':'Its woven logic can look like an industrial or technology monogram.'},
 {'id':'03','territory':'B','name':'Processional Court','idea':'A generous open perimeter brings entering and a common interior into one plan-like sign.','approach':'Architectural plan / negative-space threshold','mark':P('M104 232 H24 V24 H232 V232 H152 V200 H200 V56 H56 V200 H104 Z')+P('M88 92 H120 V144 H88 Z')+P('M136 92 H168 V144 H136 Z'),'construction':['One continuous court perimeter with a broad unclosed threshold.','Two interior panels establish rhythm without drawing worshippers.'],'risk':'Could read as a maze, venue plan, or a closed institution; literal sanctuary access is not implied.'},
 {'id':'04','territory':'B','name':'Returning Thanks','idea':'A continuous spatial gesture enters, gathers, and turns outward: thanksgiving as a response rather than a gate icon.','approach':'Calligraphic procession / continuous form','mark':P('M40 56 H176 C210 56 232 78 232 112 C232 146 208 168 174 168 H88 V136 H174 C190 136 200 126 200 112 C200 98 190 88 176 88 H72 V168 C72 192 88 208 112 208 H152 V240 H112 C68 240 40 212 40 168 Z'),'construction':['A single broad path folds from enclosure into an open outward return.','No discrete doorway, arrow, person, or musical symbol is added.'],'risk':'A continuous return can read as a letter or a general wayfinding symbol.'},
 {'id':'05','territory':'C','name':'Held Light','idea':'A substantial surrounding form gives a white interior room to open upward, exploring presence through attention to space.','approach':'Sculpted negative space / organic enclosure','mark':P('M112 24 C95 68 62 78 46 120 C26 174 60 224 112 232 V196 C80 186 66 166 74 138 C84 112 104 104 112 80 Z')+P('M136 24 C152 60 188 88 206 122 C226 170 198 220 144 232 V196 C174 184 188 162 178 138 C166 112 144 104 136 80 Z'),'construction':['Two curved masses hold one continuous white interior, open at top and base.','The opening is material absence; it is not labeled as God.'],'risk':'A vessel, flame, or seed is an alternative reading. Divine presence cannot be reduced to a white aperture.'},
 {'id':'06','territory':'C','name':'Room in the Veil','idea':'The meeting of folded screens makes a luminous room rather than a façade; the unseen interior becomes the focal point.','approach':'Planar textile / figure-ground reversal','mark':P('M32 32 H128 V72 L80 104 V184 L32 216 Z')+P('M144 32 H224 V216 H112 L144 184 H184 V80 H144 Z')+P('M96 120 L128 100 V152 L96 172 Z'),'construction':['Offset screen planes hold a larger unfilled chamber and a secondary inner fold.','The geometry is a contemporary spatial abstraction, not a historical reconstruction.'],'risk':'A portal or architectural app symbol may dominate; extra inner detail may weaken the essential idea.'}
]
for s in studies:
 s['mark']='<g fill="#000000">'+s['mark']+'</g>'
 s['viewBox']='0 0 256 256'
 s['why']='Tested as a research-led hypothesis before shortlist selection.'
 slug=s['name'].lower().replace(' ','-')
 s['file']=f"sketches/{s['id']}-{slug}-v1.svg"
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{s["viewBox"]}" role="img"><title>{escape(s["name"])} — DRAFT</title><desc>DRAFT — NOT FOR PUBLICATION. {escape(s["idea"])}</desc>{s["mark"]}</svg>\n'
 (ROOT/s['file']).write_text(svg)
(ROOT/'sketches/foundation-sketches.json').write_text(json.dumps(studies,ensure_ascii=False,indent=2)+'\n')
# A neutral working sheet for actual visual selection; no palette or type decisions.
parts=['<rect width="1500" height="1000" fill="white"/>']
for i,s in enumerate(studies):
 x=(i%3)*500;y=(i//3)*500
 parts.append(f'<svg x="{x+122}" y="{y+35}" width="256" height="256" viewBox="0 0 256 256">{s["mark"]}</svg>')
 parts.append(f'<text x="{x+35}" y="{y+345}" font-family="sans-serif" font-size="24">{s["id"]} / {escape(s["name"])}</text>')
 parts.append(f'<text x="{x+35}" y="{y+385}" font-family="sans-serif" font-size="15">Territory {s["territory"]} · DRAFT — NOT FOR PUBLICATION</text>')
(ROOT/'exports/foundation-working-sheet.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1500 1000">'+''.join(parts)+'</svg>\n')
print('Built six distinct research hypotheses, 01–06.')
