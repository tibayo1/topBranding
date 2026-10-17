#!/usr/bin/env python3
"""Inline the exact source app and local UI fonts; artwork is already self-contained."""
from pathlib import Path
import base64,re
ROOT=Path(__file__).resolve().parents[1]
css=(ROOT/'styles.css').read_text()
for name in ('noto-sans-regular.ttf','noto-serif-regular.ttf'):
 encoded=base64.b64encode((ROOT/'assets'/name).read_bytes()).decode()
 css=css.replace(f"url('assets/{name}')",f"url('data:font/ttf;base64,{encoded}')").replace(f'url("assets/{name}")',f'url("data:font/ttf;base64,{encoded}")')
html=(ROOT/'index.html').read_text().replace('<link rel="stylesheet" href="styles.css">','<style>'+css+'</style>')
names=re.findall(r'<script defer src="([^"]+)"></script>',html)
base='https://github.com/tibayo1/topBranding/blob/codex/top-logo-exploration-01/brand/explorations/strategic-study-04/'
html=html.replace('href="README.md"','href="'+base+'README.md"').replace('href="research/','href="'+base+'research/').replace('Study notes &amp; editable files','Study notes on GitHub')
inline=''
for name in names:
 html=html.replace(f'<script defer src="{name}"></script>','')
 contents=(ROOT/name).read_text().replace('</script','<\\/script')
 if name=='data.js':contents=contents.replace('"url": "research/','"url": "'+base+'research/')
 inline+='<script>\n'+contents+'\n</script>\n'
html=html.replace('</body>',inline+'</body>')
html='\n'.join(line.rstrip() for line in html.splitlines())+'\n'
(ROOT/'exports/tabernacle-strategic-explorer.html').write_text(html)
print('Built single-file offline explorer; no artwork fetches or font installation required.')
