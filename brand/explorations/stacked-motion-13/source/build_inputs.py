#!/usr/bin/env python3
"""Prepare exact stacked logo frames and overlays for a draft motion handoff."""
from pathlib import Path
from copy import deepcopy
import hashlib,json,os,subprocess,tempfile
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
PREVIOUS=ROOT.parent/'teal-refinement-11'
OUT=ROOT/'animation-inputs'
NS='http://www.w3.org/2000/svg'
ET.register_namespace('',NS)
START_OFFSETS={'shared-rhythm':[22,26,30,24],'open-praise':[18]}
TEAL,IVORY='#10494C','#F6F3EC'


def art(path):
    root=ET.parse(path).getroot()
    for child in list(root):
        if child.tag.rsplit('}',1)[-1] in ('title','desc','rect'):root.remove(child)
    return root


def frame(source,slug,width,height,kind):
    root=deepcopy(source)
    if kind in ('symbol-only-end','symbol-only-start'):
        for child in list(root):
            if child.get('data-part')=='name':root.remove(child)
    if kind=='name-overlay':
        for child in list(root):
            if child.get('data-part')=='symbol':root.remove(child)
    if kind.endswith('start'):
        symbol=next(n for n in root.iter() if n.get('data-part')=='symbol')
        paths=list(symbol.iter('{'+NS+'}path'))
        assert len(paths)==len(START_OFFSETS[slug])
        for path,offset in zip(paths,START_OFFSETS[slug]):
            assert not path.get('transform')
            path.set('transform',f'translate(0 {offset})')
    body=''.join(ET.tostring(child,encoding='unicode') for child in root)
    x=(width-760)/2;y=(height-779)/2
    background='' if kind=='name-overlay' else f'<rect width="{width}" height="{height}" fill="{IVORY}"/>'
    return (f'<svg xmlns="{NS}" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img">'
            f'<title>{slug} / name below / {kind} / DRAFT</title>'
            '<desc>DRAFT — NOT FOR PUBLICATION. Clean manual animation input. Original parish geometry and outlined name; '
            'no official RCCG emblem included. Final identity and motion approval remain open.</desc>'
            +background+f'<g data-part="logo-frame" transform="translate({x} {y}) scale(1.9)">{body}</g></svg>\n')


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    data=json.loads((PREVIOUS/'exports/artwork.json').read_text())
    records=[]
    with tempfile.TemporaryDirectory(prefix='top-motion-inputs-') as scratch:
        env=os.environ.copy();env['XDG_CONFIG_HOME']=scratch+'/config';env['XDG_CACHE_HOME']=scratch+'/cache'
        for direction in data['directions']:
            slug=direction['id'];source=PREVIOUS/direction['lockups']['stacked'];parsed=art(source)
            layouts={}
            for label,(width,height) in {'square':(1080,1080),'landscape':(1920,1080)}.items():
                directory=OUT/slug/label;directory.mkdir(parents=True,exist_ok=True)
                formats={}
                for kind in ('full-logo-end','full-logo-start','symbol-only-end','symbol-only-start','name-overlay'):
                    svg=directory/f'{kind}-DRAFT.svg';png=svg.with_suffix('.png')
                    svg.write_text(frame(parsed,slug,width,height,kind))
                    subprocess.run(['inkscape',str(svg),'--export-type=png',f'--export-filename={png}',f'--export-width={width}'],check=True,capture_output=True,env=env)
                    formats[kind]={'svg':svg.relative_to(ROOT).as_posix(),'png':png.relative_to(ROOT).as_posix()}
                layouts[label]={'width':width,'height':height,'frameTransform':{'x':(width-760)/2,'y':150.5,'scale':1.9},'files':formats}
            records.append({'id':slug,'name':direction['name'],'sourceStacked':'../teal-refinement-11/'+direction['lockups']['stacked'],
                            'sourceSHA256':hashlib.sha256(source.read_bytes()).hexdigest(),'startOffsetsSourceUnits':START_OFFSETS[slug],
                            'meaning':'A rising response to praise: four unequal planes express the congregation responding together in worship.' if slug=='shared-rhythm' else 'An open name-based T/P gesture; motion preserves the counter rather than morphing its letters.',
                            'formats':layouts})
    result={'status':'DRAFT — NOT FOR PUBLICATION','layout':'Full parish name below the symbol, static throughout the proposed motion.',
            'durationSeconds':8,'holdSeconds':[6,8],'camera':'Static, flat vector presentation. Silent.',
            'colors':{'foreground':TEAL,'background':IVORY},'rccg':'Excluded from generative animation inputs. Keep any parent emblem separate and static in a later overlay.',
            'startFrameNote':'Lowered complete planes/name-static frame for tools accepting both start/end images. For a tool taking one image only, use exact full-logo-end and the supplied gentle-lift-and-return prompt.',
            'directions':records}
    (OUT/'manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('Prepared 20 clean PNGs, matching editable SVGs and motion-input manifest.')


if __name__=='__main__':main()
