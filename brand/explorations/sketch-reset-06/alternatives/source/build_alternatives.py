from pathlib import Path
import json, shutil
ROOT=Path(__file__).resolve().parents[1]
ROOT.joinpath('renders').mkdir(exist_ok=True)

def svg(name,body,box='0 0 256 256'):
    out=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{box}"><title>{name} — DRAFT — NOT FOR PUBLICATION</title><g fill="#000000" fill-rule="evenodd">{body}</g></svg>'
    return out

def p(d,**attrs):
    return '<path d="'+d+'"'+''.join(f' {k}="{v}"' for k,v in attrs.items())+'/>'

# Every glyph below is an original sketch drawing. No font outlines are used.
# Calligraphic stress is built with broad left strokes, slimmer right return,
# and blunt diagonal exits rather than a stock serif underneath.
G={
'T':(78,'M1 6 Q34 -1 78 1 L74 15 L47 17 L43 139 L24 146 L29 19 L0 24 Z'),
'a':(76,'M60 65 L76 58 L70 139 L55 146 L55 129 Q44 146 26 144 Q1 141 3 110 Q5 77 40 62 L59 55 Z M58 72 Q25 80 22 109 Q20 129 32 128 Q46 127 56 109 Z'),
'b':(74,'M9 9 L29 1 L23 74 Q36 56 51 58 Q76 61 73 94 Q70 125 42 141 Q25 151 6 140 Z M23 94 L20 126 Q34 132 46 116 Q56 103 55 87 Q53 69 43 76 Q31 81 23 94 Z'),
'e':(70,'M63 72 Q69 91 47 105 L21 118 Q26 133 42 126 Q55 120 66 109 L64 127 Q48 147 26 145 Q0 143 3 111 Q5 77 31 62 Q53 49 63 72 Z M20 103 L41 91 Q53 84 47 75 Q41 69 32 78 Q23 87 20 103 Z'),
'r':(56,'M8 68 L27 59 L25 79 Q39 53 55 59 L52 79 Q40 73 29 92 L20 141 L2 147 Z'),
'n':(77,'M9 69 L28 59 L26 78 Q43 55 58 58 Q74 61 72 82 L65 139 L46 147 L52 91 Q54 76 46 76 Q36 77 24 97 L19 140 L1 147 Z'),
'c':(65,'M62 62 L60 81 Q42 68 30 87 Q18 105 22 119 Q26 138 49 123 L63 111 L61 130 Q45 148 25 146 Q0 143 4 112 Q7 82 30 65 Q47 54 62 62 Z'),
'l':(34,'M14 10 L34 1 L21 124 Q21 132 31 129 L28 142 Q2 153 2 130 Z'),
'o':(75,'M47 57 Q77 56 72 94 Q68 130 43 143 Q12 157 5 131 Q-1 105 17 78 Q30 59 47 57 Z M44 73 Q32 73 25 95 Q14 125 29 130 Q42 133 51 111 Q62 80 49 74 Z'),
'f':(54,'M7 63 L19 61 L21 43 Q25 11 48 3 L59 2 L55 19 Q40 18 38 41 L36 59 L55 55 L52 71 L34 74 L25 145 L7 152 L16 77 L5 80 Z'),
'P':(83,'M13 8 Q52 -6 72 10 Q92 29 78 59 Q65 83 33 89 L28 139 L8 147 Z M37 20 L34 73 Q52 70 62 54 Q76 28 59 20 Q49 16 37 20 Z'),
'i':(31,'M10 70 L29 60 L20 141 L1 148 Z M18 31 Q24 23 31 28 Q38 34 31 43 Q24 50 18 44 Q12 38 18 31 Z'),
's':(64,'M59 61 L57 80 Q42 69 31 79 Q20 88 36 96 Q60 106 51 126 Q43 146 20 147 L2 142 L5 123 Q21 137 33 125 Q42 115 27 108 Q2 98 14 78 Q27 54 59 61 Z')
}

# Letter geometry is hand spaced, not font metrics. Bottom and top lines use
# the same unscaled glyph grammar. The slightly open rhythm is intentional.
def run(text):
    x=0; body=[]
    for i,ch in enumerate(text):
        if ch==' ': x+=27; continue
        w,d=G[ch]
        body.append('<g transform="translate(%s 0)">%s</g>'%(x,p(d)))
        gap=5
        if i+1<len(text) and ch+text[i+1] in ('ra','ac','le','Pr','of'): gap=1
        if i+1<len(text) and ch+text[i+1]=='Ta': gap=-12
        x+=w+gap
    return ''.join(body),x-5
line1,w1=run('Tabernacle'); line2,w2=run('of Praise')
W=max(w1,w2)+16
wordbody='<g transform="translate(8 6)">'+line1+'</g><g transform="translate(%s 164)">%s</g>'%((W-w2)/2,line2)
word=svg('Broad Voice — original lettering sketch',wordbody,f'0 0 {W} 324')
ROOT.joinpath('broad-voice-v2.svg').write_text(word)
# An open compact T/P: unequal shoulders echo handwriting, no ring or extra emblem.
tpbody=p('M32 95 Q28 95 28 100 V115 Q28 122 35 122 H69 V211 Q69 218 76 218 H98 Q105 218 105 211 V114 Q105 95 86 95 Z')+p('M117 48 Q117 39 126 39 H163 Q219 39 221 91 Q223 144 165 147 H145 Q133 147 133 159 V183 Q133 190 126 190 H111 V146 Q111 119 137 118 H161 Q190 117 189 93 Q188 69 163 69 H148 V100 H127 Q117 100 117 90 Z')
ROOT.joinpath('open-voice-tp-v1.svg').write_text(svg('Open Voice TP — rough letterform',tpbody))
# Retained alternatives expose the choices rather than presenting a generator's
# default as an approved identity.
tp2=p('M31 55 H111 V89 H89 V214 H55 V89 H31 Z')+p('M126 42 H165 Q221 42 221 96 Q221 146 166 146 H157 V213 H126 V115 H165 Q188 115 188 95 Q188 74 165 74 H126 Z')
ROOT.joinpath('open-voice-tp-v2.svg').write_text(svg('Open Voice TP — shared cut alternative',tp2))
meta={
 'status':'DRAFT — NOT FOR PUBLICATION',
 'wordmark':{'name':'Broad Voice','source':'broad-voice-v2.svg','construction':'Every displayed glyph drawn as original paths in source/build_alternatives.py; no font outlines. Broad left strokes, slimmer returns and cut exits form one handwriting grammar.','idea':'Make the full name a warm, visibly drawn voice.','risks':['Can lean toward a café or cultural festival identity; lettering may feel too informal for the parish.','Spacing and the f/P junction remain rough.','The first line is deliberately wider; optical rhythm needs user judgment before refinement.']},
 'letterform':{'name':'Open Voice TP','source':'open-voice-tp-v1.svg','construction':'A lower T shoulder answers a taller P. The open P counter exits through a broad left cut; no enclosing seal.','idea':'A compact open letterform as a counterpart to the full-name and architectural options.','risks':['The lower T can read lowercase r in isolation.','Rounded compact geometry can suggest an app or creative studio.','The initial letters need recognition testing before this deserves refinement.']}
}
ROOT.joinpath('alternatives.json').write_text(json.dumps(meta,indent=2)+'\n')
for src,name in [('/workspace/generated_images/exec-10860bef-0604-4469-b2cc-6cef8562093f.png','01-lettering-gathered-raw.png'),('/workspace/generated_images/exec-b80f8d86-4d1e-457d-abf6-d9233d91873d.png','02-different-starts-raw.png'),('/workspace/generated_images/exec-9942372d-bf1f-4a08-8f5e-02e67c5979f1.png','03-open-p-raw.png'),('/workspace/generated_images/exec-363e8be6-c12f-4d8b-9c26-ff60e3cec897.png','04-tp-raw.png')]:
    dest=ROOT/'ideation'/name
    if Path(src).exists() and not dest.exists(): shutil.copy2(src,dest)
print('Built original lettering and TP roughs in',ROOT)
