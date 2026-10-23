from pathlib import Path
import importlib.util,json,base64
from playwright.sync_api import sync_playwright
from PIL import Image
p=Path(__file__).resolve().parent/'build.py'
spec=importlib.util.spec_from_file_location('shared',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
root=m.ROOT
counts={}
with sync_playwright() as playwright:
 browser=playwright.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 page=browser.new_page()
 for name,paths in (('primary',m.PRIMARY),('compact',m.OPEN_COMPACT)):
  counts[name]={}
  for rev in (False,True):
   mode='reverse' if rev else 'black';counts[name][mode]={}
   for size in (16,20,24,32,64,512):
    data=page.evaluate('''async ({source,size})=>{ const image=new Image(); image.src='data:image/svg+xml,'+encodeURIComponent(source); await image.decode();const c=document.createElement('canvas');c.width=size;c.height=size;c.getContext('2d').drawImage(image,0,0,size,size); return c.toDataURL('image/png').split(',')[1];}''',{'source':m.svg(paths,reverse=rev),'size':size})
    out=root/'renders'/f'chromium-{name}-{mode}-{size}.png';out.write_bytes(base64.b64decode(data))
    image=Image.open(out)
    counts[name][mode][str(size)]={str(t):len(m.component_count(image,t)) for t in (1,32,64,128,192,224)}
 browser.close()
(root/'source'/'chromium-pixel-components.json').write_text(json.dumps(counts,indent=2)+'\n')
print('Chromium native-size proofs and component records rebuilt.')
