#!/usr/bin/env python3
"""Validate the actual Creative Review 05 artwork and browser delivery.

Serve the review folder, then run: python tools/verify_review.py [http://127.0.0.1:8767]
Checks exercise source fidelity, downloads, keyboard access, responsive proofs,
local review notes, and the standalone HTML with every network route blocked.
They do not establish artistic quality, recognition, originality, or approval.
"""
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
import hashlib
import json
import re
import sys
import tempfile
import traceback
import xml.etree.ElementTree as ET

from PIL import Image
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8767'
REPORT = ROOT / 'exports/validation-report.json'
OFFLINE = ROOT / 'exports/tabernacle-creative-review-05.html'
CRITERIA = ('distinctiveness', 'nameConnection', 'integration', 'churchSuitability',
            'craft', 'endurance', 'smallScale', 'monochrome', 'industryRisk', 'explainability')
checks, evidence = [], {}


def passed(message):
    checks.append(message)
    print('PASS:', message, flush=True)


def tag(element):
    return element.tag.rsplit('}', 1)[-1]


def svg_root(text, fragment=False):
    return ET.fromstring('<svg>' + text + '</svg>' if fragment else text)


def geometry(root):
    """Ignore paint/metadata but preserve shapes, order, transforms and fill rules."""
    primitives = {'path', 'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'use'}
    ignored = {'id', 'fill', 'stroke', 'style', 'class', 'aria-label', 'role', 'color'}
    result = []

    def visit(element, transforms=(), rule='nonzero', clip_rule='nonzero'):
        transform = element.get('transform')
        transforms += (transform,) if transform else ()
        rule, clip_rule = element.get('fill-rule', rule), element.get('clip-rule', clip_rule)
        if tag(element) in primitives:
            attrs = tuple(sorted((key, value) for key, value in element.attrib.items()
                                 if key not in ignored and not key.startswith('data-')
                                 and key not in ('transform', 'fill-rule', 'clip-rule')))
            result.append((tag(element), attrs, transforms, rule, clip_rule))
        for child in element:
            visit(child, transforms, rule, clip_rule)

    visit(root)
    return result


def has_paths(root):
    return any(tag(element) == 'path' and element.get('d', '').strip() for element in root.iter())


def outlined(root, label, allow_label_text=False):
    assert has_paths(root), f'Missing vector artwork: {label}'
    forbidden = {'image', 'foreignObject', 'script', 'filter'}
    if not allow_label_text:
        forbidden.add('text')
    assert not any(tag(element) in forbidden
                   for element in root.iter()), f'Live type or nonvector artwork: {label}'


def monochrome(text, label):
    for value in re.findall(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b', text):
        value = ''.join(character * 2 for character in value) if len(value) == 3 else value
        assert value[:2].lower() == value[2:4].lower() == value[4:].lower(), f'Chromatic artwork introduced: {label}/#{value}'
    assert not re.search(r'<(?:linearGradient|radialGradient)\b', text), f'Gradient in monochrome study: {label}'


def source_path(item):
    reference = item.get('sourceFile')
    assert reference, f'Missing editable source: {item.get("id", item.get("label"))}'
    path = (ROOT / reference).resolve()
    assert path.is_relative_to(ROOT) and path.is_file(), f'Invalid source: {reference}'
    return path


def primary(item):
    return svg_root(item['mark'], fragment=True)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect_data(page):
    page.wait_for_function('window.TOPReview05 && document.querySelectorAll(".direction").length === 5')
    page.evaluate('document.fonts.ready')
    return page.evaluate('window.TOPReview05')


def validate_data(data, page):
    directions = data['directions']
    assert len(directions) == 5 and {item['id'] for item in directions} == set('ABCDE')
    source_files, counts, fingerprints = {}, {}, {}
    for item in directions:
        identity = item['id']
        sketches = item.get('sketches', [])
        assert len(sketches) >= (6 if identity == 'E' else 3), f'Insufficient exploration: {identity}'
        counts[identity] = len(sketches)
        assert item.get('primaryType') == ('wordmark' if identity == 'D' else 'symbol')
        assert item.get('name') and item.get('idea') and item.get('risk') and item.get('smallSize')
        assert item.get('construction') and item.get('parts'), f'Missing construction: {identity}'
        assert all(str(item.get('evaluation', {}).get(key, '')).strip() for key in CRITERIA), f'Incomplete ten-question evaluation: {identity}'
        for drawing in [item] + sketches:
            reference = source_path(drawing)
            source = ET.parse(reference).getroot()
            fragment = primary(drawing)
            outlined(fragment, drawing.get('id'))
            monochrome(drawing['mark'], drawing.get('id'))
            assert geometry(source) == geometry(fragment), f'Source geometry/transform mismatch: {drawing.get("id")} / {reference.name}'
            assert source.get('viewBox') == drawing.get('viewBox'), f'Source viewBox mismatch: {drawing.get("id")}'
            source_files[str(reference.relative_to(ROOT))] = sha(reference)
            if drawing is not item:
                assert drawing.get('idea') and drawing.get('reason'), f'Unexplained sketch: {drawing.get("id")}'
        signatures = {hashlib.sha256(repr(geometry(primary(sketch))).encode()).hexdigest() for sketch in sketches}
        assert len(signatures) == len(sketches), f'Duplicate sketch geometry within direction {identity}'
        fingerprints[identity] = len(signatures)
        for kind in ('horizontal', 'stacked'):
            art = item.get('lockups', {}).get(kind)
            assert art and re.search(r'Tabernacle\s+of\s+Praise', art, re.I), f'Missing complete-name identity: {identity}/{kind}'
            outlined(svg_root(art), f'{identity}/{kind}')
            monochrome(art, f'{identity}/{kind}')
        assert item.get('type', {}).get('family') and item.get('type', {}).get('license'), f'Undisclosed typography source: {identity}'
        for kind in ('signage', 'paper'):
            outlined(svg_root(item.get('applications', {}).get(kind, '')), f'{identity}/{kind}', allow_label_text=True)
            monochrome(item['applications'][kind], f'{identity}/{kind}')
        for part in item['parts']:
            outlined(primary(part), f'{identity}/{part.get("label")}')
        section = page.locator(f'#direction-{identity.lower()}')
        assert section.locator('.sketch-card').count() == len(sketches)
        for index, sketch in enumerate(sketches):
            inline = section.locator('.sketch-art > svg').nth(index).evaluate('(el) => el.outerHTML')
            assert geometry(svg_root(inline)) == geometry(primary(sketch)), f'Inline sketch changed: {sketch["id"]}'
            assert 'DRAFT — NOT FOR PUBLICATION' in inline
        for index in (0, 1):
            inline = section.locator('.stage-art > svg').nth(index).evaluate('(el) => el.outerHTML')
            assert geometry(svg_root(inline)) == geometry(primary(item)), f'Inline developed art changed: {identity}'
            assert 'DRAFT — NOT FOR PUBLICATION' in inline
        for index, kind in enumerate(('horizontal', 'stacked')):
            inline = section.locator('.lockup-grid .full-artwork > svg').nth(index).evaluate('(el) => el.outerHTML')
            assert geometry(svg_root(inline)) == geometry(svg_root(item['lockups'][kind])), f'Inline lockup changed: {identity}/{kind}'
    evidence.update(sketchCounts=counts, distinctSourceGeometries=fingerprints, sourceArtworkSha256=source_files)
    passed('All five directions have distinct source-backed sketches (E at least six), developed artwork, construction, outlined complete-name lockups, applications and ten qualitative evaluations')
    passed('Every displayed sketch, developed mark and full-name lockup preserves editable source geometry, viewBox, ancestor transforms and fill rules; no font substitution is used in the identities')
    return directions


def check_fair_proofs(page, directions):
    expect(page.locator('.overview-card')).to_have_count(5)
    expect(page.locator('.art-stage')).to_have_count(10)
    stages = page.locator('.art-stage').evaluate_all('(els) => els.map(el => ({w:el.getBoundingClientRect().width,h:el.getBoundingClientRect().height,bg:getComputedStyle(el).backgroundColor}))')
    assert len({round(item['w'], 1) for item in stages}) == 1, stages
    assert len({round(item['h'], 1) for item in stages}) == 1, stages
    assert [item['bg'] for item in stages] == ['rgb(255, 255, 255)', 'rgb(17, 17, 17)'] * 5
    for index, stage in enumerate(page.locator('.art-stage').all()):
        paints = stage.locator('.stage-art svg path').evaluate_all('(els) => els.map(el => getComputedStyle(el).fill)')
        expected = 'rgb(255, 255, 255)' if index % 2 else 'rgb(17, 17, 17)'
        assert paints and all(paint == expected for paint in paints), f'Incorrect visible primary/reverse ink: stage {index + 1}/{paints}'
    expect(page.locator('#evaluation-table tbody tr')).to_have_count(10)
    assert page.locator('#evaluation-table tbody td').count() == 50
    assert all(value.strip() for value in page.locator('#evaluation-table tbody td').all_text_contents())
    expect(page.locator('.rccg-placeholder')).to_have_count(5)
    assert all('ASSET NEEDED' in text for text in page.locator('.rccg-placeholder').all_text_contents())
    assert page.locator('.rccg-emblem img, .rccg-emblem svg').count() == 0
    manifest = ROOT / 'source/rccg-emblem-manifest.md'
    emblem = ROOT.parents[1] / 'assets/rccg-emblem/rccg-emblem-user-supplied.png'
    assert manifest.is_file() and 'IMAGE FILE STILL TO BE TRANSFERRED' in manifest.read_text(), 'Missing documented emblem-availability audit'
    assert not emblem.is_file(), 'The authorized emblem is now available; replace reservations with the untouched source asset'
    evidence['rccgReservation'] = {'manifest': str(manifest.relative_to(ROOT)),
                                 'expectedAssetPath': str(emblem), 'assetPresent': False}
    assert 'DRAFT — NOT FOR PUBLICATION' in page.locator('.site-header').inner_text()
    assert not page.locator('input[type=color], [data-palette], .palette-choice').count()
    assert not re.search(r'weekly flyer|flyer template', page.locator('main').inner_text(), re.I)
    assert (ROOT / 'assets/UI-FONT-LICENSE.txt').is_file()
    for mode in ('dark', 'light'):
        page.locator(f'[data-mode="{mode}"]').click()
        expect(page.locator(f'.overview-card[data-dark="{str(mode == "dark").lower()}"]')).to_have_count(5)
    for item in directions:
        section = page.locator(f'#direction-{item["id"].lower()}')
        section.locator('[role=tab]').nth(1).click()
        widths = section.locator('.name-width-art').evaluate_all('(els) => els.map(el => el.getBoundingClientRect().width)')
        assert widths == [320, 240], f'Full-name proofs are not native widths: {item["id"]}/{widths}'
        if item['primaryType'] == 'wordmark' and not item.get('compact'):
            assert section.locator('.size-art').count() == 0
            expect(section.locator('.wordmark-limit')).to_contain_text('cannot carry the parish name at 16 px')
        else:
            sizes = section.locator('.size-art').evaluate_all('(els) => els.map(el => [el.getBoundingClientRect().width,el.getBoundingClientRect().height])')
            assert sizes == [[size, size] for size in (64, 32, 24, 16)], sizes
            if item['primaryType'] == 'wordmark':
                assert item['compact'].get('caution') and 'full' in section.locator('.size-sheet').first.inner_text().lower()
        section.locator('[role=tab]').first.click()
    evidence['equalStageDimensions'] = {'width': stages[0]['w'], 'height': stages[0]['h']}
    passed('Five directions receive the same monochrome stage dimensions and ten-question comparison; native 64/32/24/16px symbols and 320/240px full names disclose D’s wordmark limits; RCCG remains an explicit missing-asset reservation')


def keyboard_checks(page, directions):
    opener = page.locator('.art-stage [data-inspect]').first
    opener.click()
    expect(page.locator('#art-dialog')).to_be_visible()
    expect(page.locator('#close-dialog')).to_be_focused()
    page.keyboard.press('Shift+Tab')
    expect(page.locator('#dialog-download')).to_be_focused()
    page.keyboard.press('Tab')
    expect(page.locator('#close-dialog')).to_be_focused()
    for _ in range(5):
        page.keyboard.press('Tab')
        assert page.evaluate('document.querySelector("#art-dialog").contains(document.activeElement)')
    page.locator('#dialog-reverse').click()
    expect(page.locator('#dialog-reverse')).to_have_attribute('aria-pressed', 'true')
    expect(page.locator('#dialog-art')).to_have_attribute('data-dark', 'true')
    page.keyboard.press('Escape')
    expect(page.locator('#art-dialog')).not_to_be_visible()
    expect(opener).to_be_focused()
    for item in directions:
        section = page.locator(f'#direction-{item["id"].lower()}')
        tabs = section.locator('[role=tab]')
        tabs.first.focus()
        page.keyboard.press('ArrowRight')
        expect(tabs.nth(1)).to_have_attribute('aria-selected', 'true')
        expect(section.locator('[role=tabpanel]:visible')).to_have_count(1)
        page.keyboard.press('End')
        expect(tabs.last).to_have_attribute('aria-selected', 'true')
        page.keyboard.press('ArrowLeft')
        expect(tabs.nth(2)).to_have_attribute('aria-selected', 'true')
        page.keyboard.press('Home')
        expect(tabs.first).to_have_attribute('aria-selected', 'true')
    sketch = page.locator('.sketch-art').last
    sketch.click()
    expect(page.locator('#art-dialog')).to_be_visible()
    page.locator('#close-dialog').click()
    expect(sketch).to_be_focused()
    passed('Developed and sketch dialogs trap Tab/Shift+Tab, reverse, close with Escape or close button, and restore their opener; every tablist supports arrows, Home and End')


def raster_check(page, text, dark, label):
    page.set_content('<style>html,body{margin:0;background:transparent}svg{width:640px;height:auto;display:block}</style>' + text)
    pixels = Image.open(BytesIO(page.locator('svg').screenshot(omit_background=True))).convert('RGBA')
    histogram = pixels.getdata()
    opaque = sum(1 for r, g, b, alpha in histogram if alpha > 250)
    ink = sum(1 for r, g, b, alpha in pixels.getdata()
              if alpha > 250 and ((r > 245 and g > 245 and b > 245) if dark else (r < 35 and g < 35 and b < 35)))
    assert ink > 30, f'Rasterized ink absent or incorrect: {label}'
    if dark:
        assert opaque > pixels.width * pixels.height * .97, f'Reverse canvas is transparent: {label}'
        # Fractional SVG aspect ratios antialias the outermost pixel; sample
        # inside the canvas rather than treating that raster edge as paper.
        assert pixels.getpixel((1, 1)) == (17, 17, 17, 255), f'Reverse background is incorrect: {label}'


def check_download(page, raster_page, item, kind, temporary, dark=False, context_label='online'):
    button = page.locator(f'#direction-{item["id"].lower()} .direction-downloads [data-kind="{kind}"]')
    if kind == 'primary':
        button = button.nth(1 if dark else 0)
    else:
        button = button.first
    with page.expect_download(timeout=15000) as pending:
        button.click()
    download = pending.value
    assert download.suggested_filename.endswith('-DRAFT.svg'), download.suggested_filename
    target = temporary / f'{context_label}-{download.suggested_filename}'
    download.save_as(target)
    text = target.read_text()
    root = svg_root(text)
    outlined(root, f'{item["id"]}/{kind}', allow_label_text=kind in ('signage', 'paper'))
    assert 'DRAFT — NOT FOR PUBLICATION' in text
    assert 'currentColor' not in text, f'Unresolved currentColor: {item["id"]}/{kind}'
    expected = primary(item) if kind == 'primary' else svg_root(item['lockups' if kind in ('horizontal', 'stacked') else 'applications'][kind])
    if dark:
        values = [float(value) for value in root.get('viewBox').split()]
        children = list(root)
        assert tag(children[0]) == 'desc' and tag(children[1]) == 'rect', 'Reverse export must add its canvas behind artwork'
        background = children[1]
        assert background.get('fill') == '#111111'
        assert [float(background.get(key)) for key in ('x', 'y', 'width', 'height')] == values
        root.remove(background)
    assert geometry(root) == geometry(expected), f'Download geometry changed: {item["id"]}/{kind}/reverse={dark}'
    if kind == 'primary':
        raster_check(raster_page, text, dark, f'{context_label}/{item["id"]}/{kind}/reverse={dark}')
    # Chrome limits bursts of automatic downloads. These distinct user clicks
    # are paced to avoid attributing the browser's suppression to the app.
    page.wait_for_timeout(1100)
    return {'direction': item['id'], 'kind': kind, 'reverse': dark,
            'filename': download.suggested_filename, 'sha256': sha(target)}


def download_all(page, raster_page, directions, temporary, label):
    result = []
    for item in directions:
        kinds = [('primary', False), ('primary', True), ('horizontal', False),
                 ('stacked', False), ('signage', False), ('paper', False)]
        for kind, dark in kinds:
            result.append(check_download(page, raster_page, item, kind, temporary, dark, label))
    return result


def feedback_checks(page, temporary, reload=True):
    page.locator('[data-choice="A"]').click()
    page.locator('#review-choices input[value="E"]').check()
    note = 'Validation note: shared dwelling and praise remain open for review; no identity approval.'
    page.locator('#review-notes').fill(note)
    page.wait_for_timeout(350)
    page.locator('[data-mode="dark"]').click()
    if reload:
        page.wait_for_function('JSON.parse(localStorage.getItem("top-creative-review-05")).notes.length > 0')
        page.reload(wait_until='networkidle')
        collect_data(page)
    expect(page.locator('#review-notes')).to_have_value(note)
    expect(page.locator('[data-choice="A"]')).to_have_attribute('aria-pressed', 'true')
    expect(page.locator('#review-choices input[value="E"]')).to_be_checked()
    expect(page.locator('[data-mode="dark"]')).to_have_attribute('aria-pressed', 'true')
    with page.expect_download() as pending:
        page.locator('#feedback-form button[type=submit]').click()
    target = temporary / ('online-notes.json' if reload else 'offline-notes.json')
    pending.value.save_as(target)
    review = json.loads(target.read_text())
    assert review['notes'] == note
    assert {item['id'] for item in review['directionsToDiscuss']} == {'A', 'E'}
    assert review['status'] == 'DRAFT — NOT FOR PUBLICATION'
    assert all(review[key] is False for key in ('identityApproved', 'typographyApproved', 'colorApproved', 'publicationApproved'))
    page.wait_for_timeout(1100)
    page.locator('#clear-feedback').click()
    expect(page.locator('#review-notes')).to_have_value('')
    assert page.locator('#review-choices input:checked').count() == 0


def responsive_checks(page, directions):
    for width in (1440, 900, 390, 320):
        page.set_viewport_size({'width': width, 'height': 1000})
        for item in directions:
            section = page.locator(f'#direction-{item["id"].lower()}')
            for tab in section.locator('[role=tab]').all():
                tab.click()
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), f'Page overflow at {width}px/{item["id"]}/{tab.inner_text()}'
            section.locator('.art-stage [data-inspect]').first.click()
            bounds = page.locator('#art-dialog').bounding_box()
            assert bounds['x'] >= -.5 and bounds['x'] + bounds['width'] <= width + .5, bounds
            assert page.locator('#art-dialog').evaluate('(el) => el.scrollWidth <= el.clientWidth + 1'), f'Dialog overflow at {width}px'
            page.keyboard.press('Escape')
            section.locator('[role=tab]').first.click()
    passed('All five directions, all four proof panels and artwork dialogs fit 1440/900/390/320px viewports without page or dialog horizontal overflow')


def local_reference_checks(page):
    references = page.locator('a[href]').evaluate_all('''(els) => [...new Set(els
        .filter(el => el.getAttribute('href') && !el.getAttribute('href').startsWith('#'))
        .map(el => el.href).filter(url => new URL(url).origin === location.origin))]''')
    for url in references:
        response = page.request.get(url)
        assert response.ok, f'Broken local source/delivery link: {url} ({response.status})'
    evidence['localReferenceLinksChecked'] = references
    passed('Every local source, file-guide, PDF and ZIP link resolves to a successful response')


def run():
    assert (ROOT / 'data.js').is_file(), 'Build data.js before validation'
    assert OFFLINE.is_file(), 'Build the standalone HTML before validation'
    with tempfile.TemporaryDirectory(prefix='top-review-05-check-') as directory, sync_playwright() as playwright:
        temporary = Path(directory)
        browser = playwright.chromium.launch(executable_path='/usr/bin/chromium', headless=True,
                    args=['--no-sandbox', '--disable-dev-shm-usage'])
        context = browser.new_context(viewport={'width': 1440, 'height': 1000}, accept_downloads=True, reduced_motion='reduce')
        page, raster_page = context.new_page(), context.new_page()
        errors, remote, failed = [], [], []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('request', lambda request: remote.append(request.url) if request.url.startswith(('http:', 'https:')) and not request.url.startswith(URL.rstrip('/') + '/') and request.url != URL else None)
        page.on('requestfailed', lambda request: failed.append(request.url))
        response = page.goto(URL, wait_until='networkidle')
        assert response and response.ok, f'Review HTTP response failed: {URL}'
        data = collect_data(page)
        directions = validate_data(data, page)
        check_fair_proofs(page, directions)
        keyboard_checks(page, directions)
        evidence['onlineDownloads'] = download_all(page, raster_page, directions, temporary, 'online')
        passed('All thirty offered online SVG downloads preserve actual geometry; primary/reverse symbols and D wordmark rasterize with correct dark/white inks and opaque black reverse backgrounds, including C currentColor')
        feedback_checks(page, temporary)
        passed('Selections, checkboxes, notes and view mode survive reload; notes JSON explicitly records four false approval flags and clearing removes saved notes')
        responsive_checks(page, directions)
        local_reference_checks(page)

        offline_context = browser.new_context(viewport={'width': 1440, 'height': 1000}, accept_downloads=True, reduced_motion='reduce')
        blocked, offline_errors = [], []
        def block(route):
            blocked.append(route.request.url)
            route.abort()
        offline_context.route('**/*', block)
        offline_page, offline_raster = offline_context.new_page(), offline_context.new_page()
        offline_page.on('pageerror', lambda error: offline_errors.append(str(error)))
        standalone = OFFLINE.read_text()
        assert not re.search(r'<(?:script[^>]+src|link[^>]+href)\s*=', standalone, re.I), 'Standalone contains external script/style references'
        assert 'data:font/' in standalone or 'data:application/' in standalone, 'Standalone UI fonts are not embedded'
        offline_page.set_content(standalone, wait_until='networkidle')
        offline_data = collect_data(offline_page)
        assert offline_data == data, 'Offline artifact contains stale/different artwork data'
        assert offline_page.locator('.sketch-card').count() == sum(len(item['sketches']) for item in directions)
        keyboard_checks(offline_page, directions)
        offline_page.locator('[data-mode="dark"]').click()
        expect(offline_page.locator('.overview-card[data-dark=true]')).to_have_count(5)
        evidence['offlineDownloads'] = download_all(offline_page, offline_raster, directions, temporary, 'offline')
        feedback_checks(offline_page, temporary, reload=False)
        offline_page.set_viewport_size({'width': 320, 'height': 1000})
        assert offline_page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
        assert not blocked, f'Standalone attempted network access: {blocked}'
        assert not offline_errors, offline_errors
        assert not errors, errors
        assert not remote, remote
        assert not failed, failed
        evidence['browser'] = browser.version
        evidence['networkRequestsOutsideReview'] = remote
        evidence['offlineRequestsAttempted'] = blocked
        evidence['consolePageErrors'] = errors + offline_errors
        passed('Standalone HTML contains identical artwork and embedded UI fonts; with every route blocked all thirty SVG downloads, reversal, keyboard dialogs/tabs, notes export and mobile layout work without network requests or JavaScript errors')
        exports = list((ROOT / 'exports').rglob('*.svg'))
        for path in exports:
            assert tag(ET.parse(path).getroot()) == 'svg', f'Invalid exported SVG: {path}'
        evidence['exportSvgCount'] = len(exports)
        browser.close()
    artifacts = [ROOT / name for name in ('index.html', 'styles.css', 'app.js', 'data.js', 'tools/verify_review.py')]
    artifacts += [path for path in (ROOT / 'exports').rglob('*') if path.is_file() and path != REPORT]
    evidence['deliveryArtifactSha256'] = {str(path.relative_to(ROOT)): sha(path) for path in sorted(artifacts)}
    passed('Exported SVGs parse successfully and final review sources plus delivery artifacts are recorded with SHA-256 checksums')


if __name__ == '__main__':
    status, failure = 'passed', None
    try:
        run()
    except Exception as error:
        status, failure = 'failed', f'{type(error).__name__}: {error}'
        traceback.print_exc()
    REPORT.write_text(json.dumps({
        'study': 'RCCG Tabernacle of Praise — Creative Review 05', 'status': status,
        'checkedAtUtc': datetime.now(timezone.utc).isoformat(), 'browser': 'Chromium / Python Playwright',
        'checksPassed': len(checks), 'checks': checks, 'evidence': evidence, 'failure': failure,
        'limits': 'Functional delivery and source-fidelity checks only. Human assessment of artistic quality, meaningful symbolism, unintended associations and small-size recognition remains necessary. No identity approval, theological endorsement, originality guarantee or trademark clearance is implied.'
    }, ensure_ascii=False, indent=2) + '\n')
    print(f'Validation report: {REPORT}', flush=True)
    sys.exit(0 if status == 'passed' else 1)
