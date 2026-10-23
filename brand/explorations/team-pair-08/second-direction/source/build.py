#!/usr/bin/env python3
"""Original vector development of the new figure–ground TP premise.

Sources: root-agent-generated four-concept raster board, candidate B. This is
an original open contour drawn here, not traced reference-logo geometry.
The user-supplied church logos inform principles only. No fonts, images,
white overlay masks, clipping paths or filters occur in the mark.
"""
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
VERSIONS = {
    'v1-counterform': 'M28 28H140C205 28 228 65 228 96C228 142 197 163 133 177V99H146C171 99 183 113 183 130C183 136 182 141 182 145C192 132 194 118 194 105V84C194 72 188 67 177 67H60C54 67 49 65 46 62C50 79 59 89 72 89H91V169C91 194 103 207 133 223H110C45 223 28 190 28 142Z',
    'v2-open-counter': 'M28 28H140C205 28 228 65 228 96C228 142 197 163 133 177V102H146C170 102 181 113 181 130V140C190 129 194 117 194 104V85C194 73 188 68 177 68H61C56 68 52 67 48 65C52 83 61 95 74 95H91V169C91 194 103 207 133 223H110C45 223 28 190 28 142Z',
}
SELECTED='v2-open-counter'
def svg(path, version, reverse=False):
    ink='#ffffff' if reverse else '#000000'
    bg='<rect width="256" height="256" fill="#000000"/>' if reverse else ''
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">\n<title>Open Praise '+version+' — DRAFT — NOT FOR PUBLICATION</title>\n<desc>A compact P-like contour holds an open negative T. The T-shaped white interior exits through the lower edge, so the artwork is one actual open contour. Letter recognition remains subject to review.</desc>\n'+bg+'\n<path fill="'+ink+'" d="'+path+'"/>\n</svg>\n'
for version, path in VERSIONS.items():
    (ROOT/(version+'.svg')).write_text(svg(path,version))
(ROOT/'primary.svg').write_text(svg(VERSIONS[SELECTED],SELECTED))
(ROOT/'reverse.svg').write_text(svg(VERSIONS[SELECTED],SELECTED,True))
(ROOT/'metadata.json').write_text(json.dumps({
  'id':'B','name':'Open Praise','status':'DRAFT — NOT FOR PUBLICATION','inReview':True,
  'primary':'primary.svg','reverse':'reverse.svg','viewBox':'0 0 256 256',
  'primaryType':'symbol','source':'source/build.py','selectedVersion':SELECTED,
  'idea':'A P-shaped outer gesture holds a T in its open negative interior.',
  'visible':'One compact black contour; a broad open white crossbar turns down into a clear stem and exits the lower edge.',
  'meaning':'The letters relate to Tabernacle and Praise. The held, open interior can support the idea of welcome and response. It is not a literal image of worship or a musical instrument.',
  'construction':'One closed path traces a shape with an open indentation. The white T is true unfilled geometry connected to the surrounding background, not a white overlay or mask.',
  'changes':{'v1':'Interprets candidate B from the original four-concept ideation board.','v2':'Widens the usable white bar by six units at its left end and three at the right, and shortens the narrow curved tip to reduce a fragile sliver.'},
  'risk':'The two letters may not be equally obvious at first glance, particularly at small sizes. A stylised monogram can suggest a creative studio, publisher or luxury identity. No trademark clearance is implied.',
  'smallSize':'Rendered and visually inspected at native 16/24/32/64 px in black and reverse. The broad T-shaped opening and outer silhouette survive. At 16 px the tapered right hook loses its fine curve; 24–32 px gives clearer letter reading. This is a draft test, not approval or a universal minimum-size standard.',
  'referencePrinciples':'Compact confidence and strong figure–ground contrast from the supplied references. Their shield, figure, book, star and NV geometry are not used.'
},ensure_ascii=False,indent=2)+'\n')
