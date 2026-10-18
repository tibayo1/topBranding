#!/usr/bin/env python3
"""Build the self-contained review without changing its artwork data.

Run after build_review.py. Optional editable sources and reference documents link
back to the repository; viewing and using the review requires no network access.
"""
from pathlib import Path
from html import escape
from urllib.parse import urljoin
import base64
import re

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'exports/tabernacle-creative-review-05.html'
ASSET_BASE = ('https://github.com/tibayo1/topBranding/blob/'
              'codex/top-logo-exploration-01/brand/explorations/creative-review-05/')


def inline_font(match):
    reference = match.group(2)
    if reference.startswith(('data:', 'https:', 'http:')):
        raise ValueError(f'Unexpected nonlocal font asset: {reference}')
    path = (ROOT / reference).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        raise FileNotFoundError(f'Missing local stylesheet asset: {reference}')
    mime = {'ttf': 'font/ttf', 'woff': 'font/woff', 'woff2': 'font/woff2'}[path.suffix[1:]]
    encoded = base64.b64encode(path.read_bytes()).decode('ascii')
    return f'url("data:{mime};base64,{encoded}")'


def script(text):
    # An escaped closing tag preserves JS string contents inside an HTML script.
    return '<script>\n' + re.sub(r'</script', r'<\\/script', text, flags=re.I) + '\n</script>\n'


def main():
    css = (ROOT / 'styles.css').read_text()
    css = re.sub(r'url\(([\'"]?)([^\s)\'"]+)\1\)', inline_font, css)
    html = (ROOT / 'index.html').read_text()
    stylesheet = '<link rel="stylesheet" href="styles.css">'
    assert stylesheet in html, 'Expected the source stylesheet link'
    html = html.replace(stylesheet, '<style>\n' + css + '\n</style>')
    # Keep the source data byte-for-byte intact. The app applies this base solely
    # to optional hyperlinks; sourceFile and source URLs retain their fidelity.
    scripts = script('window.TOPReview05AssetBase = ' + repr(ASSET_BASE) + ';')
    names = re.findall(r'<script defer src="([^"]+)"></script>', html)
    assert names == ['data.js', 'app.js'], f'Unexpected source scripts: {names}'
    for name in names:
        scripts += script((ROOT / name).read_text())
        html = html.replace(f'<script defer src="{name}"></script>', '')

    def optional_link(match):
        reference = match.group(1)
        if reference.startswith(('#', '/', 'http:', 'https:', 'data:', 'mailto:')):
            return match.group(0)
        return 'href="' + escape(urljoin(ASSET_BASE, reference), quote=True) + '"'

    html = re.sub(r'href="([^"]+)"', optional_link, html)
    notice = (ROOT / 'assets/UI-FONT-LICENSE.txt').read_text()
    license_template = '<template id="embedded-ui-font-license">' + escape(notice) + '</template>\n'
    html = html.replace('</body>', license_template + scripts + '</body>')
    html = re.sub(r'(?m)^[ \t]+$', '', html)
    assert not re.search(r'<(?:script|link)\b[^>]+(?:src|href)=', html), 'A core dependency remains external'
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(html, encoding='utf-8')
    print(f'Built {OUTPUT.relative_to(ROOT)} ({OUTPUT.stat().st_size:,} bytes).')
    print('Embedded CSS, both UI fonts and their license, unchanged artwork data, and the source app. Optional sources/documents link to GitHub.')


if __name__ == '__main__':
    main()
