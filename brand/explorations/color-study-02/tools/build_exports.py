#!/usr/bin/env python3
"""Build a genuinely offline HTML explorer, palette JSON, and editable SVG studies.

Python 3 and Node are needed to build; the resulting explorer needs only a browser.
No network requests, package installations, or third-party services are used.
"""
from pathlib import Path
import base64
from html import escape
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
EXPORTS = ROOT / 'exports'
EXPORTS.mkdir(exist_ok=True)

css = (ROOT / 'styles.css').read_text()
for font in ('noto-sans-regular.ttf', 'noto-serif-regular.ttf', 'ui-arrows.ttf', 'ui-symbols.ttf'):
    encoded = base64.b64encode((ROOT / 'assets' / font).read_bytes()).decode()
    css = css.replace(f"url('assets/{font}')", f"url('data:font/ttf;base64,{encoded}')")

html = (ROOT / 'index.html').read_text()
html = html.replace('<link rel="stylesheet" href="styles.css">', f'<style>{css}</style>')
scripts = re.findall(r'<script defer src="([^"]+)"></script>', html)
for name in scripts:
    html = html.replace(f'<script defer src="{name}"></script>', '')
inline = '<script>window.TOPStandalone = true;</script>\n'
for name in scripts:
    contents = (ROOT / name).read_text().replace('</script', '<\\/script')
    inline += f'<script data-source="{name}">\n{contents}\n</script>\n'
html = html.replace('<a href="README.md">Study notes & sources ↗</a>', '<a href="#recommendations">Review notes ↗</a>')
html = html.replace('</body>', inline + '</body>')
html = '\n'.join(line.rstrip() for line in html.splitlines()) + '\n'
(EXPORTS / 'tabernacle-color-explorer.html').write_text(html)

runner = r"""
global.window = {};
require(process.argv[1] + '/data.js');
require(process.argv[1] + '/applications.js');
const data = window.TOPData;
const output = {data, applications: []};
for (const palette of data.palettes.filter(p => p.recommended)) {
  for (const concept of data.concepts) {
    for (const type of ['flyer','instagram','avatar','signage']) {
      for (const mode of ['light','dark']) {
        output.applications.push({ name: `DRAFT-${concept.id}-${palette.id}-${type}-${mode}.svg`, svg: window.TOPApplications.render({type,palette,concept,mode}) });
      }
    }
  }
}
process.stdout.write(JSON.stringify(output));
"""
result = subprocess.run(['node', '-e', runner, str(ROOT)], check=True, text=True, capture_output=True)
data = json.loads(result.stdout)
palette_data = {'status': 'DRAFT — NOT FOR PUBLICATION', 'palettes': data['data']['palettes'], 'recommendations': {'palettes': ['teal', 'navy'], 'concept': 'C', 'challenger': 'D', 'note': 'C is the current durability benchmark. D introduces a stronger shared-space association, with a possible leaf/growth reading. No replacement is approved.'}, 'approved': False}
(EXPORTS / 'proposed-palettes.json').write_text(json.dumps(palette_data, indent=2) + '\n')
applications = EXPORTS / 'applications'
applications.mkdir(exist_ok=True)
for item in data['applications']:
    (applications / item['name']).write_text(item['svg'] + '\n')

marks = EXPORTS / 'marks'
marks.mkdir(exist_ok=True)
mark_count = 0
for palette in data['data']['palettes']:
    for concept in data['data']['concepts']:
        for mode in ('light', 'dark'):
            ground, ink = (palette['neutral'], palette['primary']) if mode == 'light' else (palette['primary'], palette['neutral'])
            name = f"DRAFT-{concept['id']}-{palette['id']}-{mode}.svg"
            provenance = ('New exploration-03 geometry with proposed color.' if concept['id'] == 'D'
                          else 'Original exploration-01 geometry is unchanged; proposed color only.')
            svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">'
                   f"<title>{escape(concept['name'])} — {escape(palette['name'])} — DRAFT</title>"
                   f'<desc>DRAFT — NOT FOR PUBLICATION. {provenance} No approval implied.</desc>'
                   f'<rect id="background" width="256" height="256" fill="{ground}"/>'
                   + concept['mark'].replace('#000000', ink) + '</svg>\n')
            (marks / name).write_text(svg)
            mark_count += 1
print(f'Built offline HTML, palette data, {len(data["applications"])} application SVGs, and {mark_count} mark SVGs.')
