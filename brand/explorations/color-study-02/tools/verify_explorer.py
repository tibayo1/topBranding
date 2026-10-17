#!/usr/bin/env python3
"""Exercise the actual explorer in Chromium, including downloads and offline use.

Run a local HTTP server for the project folder, then pass its URL as argv[1].
Requires the environment's Python Playwright and Chromium. No package install.
"""
from pathlib import Path
import json
import re
import sys
import tempfile
import xml.etree.ElementTree as ET

from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8765'
checks = []


def passed(message):
    checks.append(message)
    print('PASS:', message, flush=True)


def geometry_signature(root):
    """Compare path construction and inherited placement, ignoring titles and IDs."""
    paths = []

    def visit(element, transforms=()):
        transform = element.attrib.get('transform')
        transforms = transforms + ((transform,) if transform else ())
        if element.tag.rsplit('}', 1)[-1] == 'path':
            paths.append((element.attrib['d'], element.attrib.get('fill-rule', 'nonzero'), transforms))
        for child in element:
            visit(child, transforms)

    visit(root)
    return paths


def ratio(a, b):
    def luminance(value):
        channels = [int(value[index:index + 2], 16) / 255 for index in (1, 3, 5)]
        channels = [channel / 12.92 if channel <= .04045 else ((channel + .055) / 1.055) ** 2.4 for channel in channels]
        return sum(channel * weight for channel, weight in zip(channels, (.2126, .7152, .0722)))
    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return (high + .05) / (low + .05)


with tempfile.TemporaryDirectory(prefix='top-study-checks-') as temporary:
    temporary = Path(temporary)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path='/usr/bin/chromium', headless=True,
                                             args=['--no-sandbox', '--disable-dev-shm-usage'])
        context = browser.new_context(viewport={'width': 1440, 'height': 1000}, accept_downloads=True,
                                      reduced_motion='reduce')
        page = context.new_page()
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto(URL, wait_until='networkidle')
        page.evaluate('document.fonts.ready')
        expect(page).to_have_title('Tabernacle of Praise — Color Study 02')
        expect(page.locator('.palette-choice')).to_have_count(5)
        expect(page.locator('.focus-card')).to_have_count(3)
        expect(page.locator('#meaning-cards > *')).to_have_count(3)
        expect(page.locator('.matrix-row')).to_have_count(5)
        expect(page.locator('.matrix-sample')).to_have_count(30)
        expect(page.locator('.matrix-values code')).to_have_count(20)
        assert not errors, errors
        passed('Five palettes, B/C/D, three meaning breakdowns, all 30 light/dark matrix studies, and all role HEX values render')
        expect(page.locator('.pairing-example')).to_have_count(3)
        expect(page.locator('.rccg-placeholder')).to_have_count(3)
        expect(page.locator('.rccg-placeholder').first).to_contain_text('ASSET PENDING')

        data = page.evaluate('window.TOPData')
        assert [concept['id'] for concept in data['concepts']] == ['B', 'C', 'D']
        sources = {
            'B': 'exploration-01/b-sanctuary-strings-v3.svg',
            'C': 'exploration-01/c-praise-ligature-v3.svg',
            'D': 'exploration-03/d-resonant-sanctuary-v1.svg',
        }
        for concept in data['concepts']:
            path = ROOT.parents[2] / 'brand/concepts' / sources[concept['id']]
            source = ET.parse(path).getroot()
            fragment = ET.fromstring('<svg>' + concept['mark'] + '</svg>')
            assert geometry_signature(source) == geometry_signature(fragment), concept['id']
        passed('B/C match existing v3 path construction, and D matches its new source including inherited transforms')

        for palette in data['palettes']:
            page.locator(f'.palette-choice[data-value="{palette["id"]}"]').click()
            expect(page.locator('#active-palette-heading h3')).to_have_text(palette['family'])
            expect(page.locator('#color-swatches code')).to_have_text([palette[role] for role in ('primary', 'secondary', 'accent', 'neutral')])
            actual = page.evaluate('([a,b]) => window.TOPExplorer.contrast(a,b)', [palette['primary'], palette['neutral']])
            assert abs(actual - ratio(palette['primary'], palette['neutral'])) < 1e-9
            assert actual > 9
            row = page.locator(f'.matrix-row[data-palette="{palette["id"]}"]')
            sizes = row.locator('.brand-mark').evaluate_all('(elements) => elements.map(element => [element.getBoundingClientRect().width,element.getBoundingClientRect().height])')
            assert all(size == sizes[0] for size in sizes)
        passed('Every palette selects correctly, core contrast independently matches, and all matrix symbol boxes match')

        page.locator('.palette-choice[data-value=teal]').focus()
        page.keyboard.press('Space')
        expect(page.locator('.palette-choice[data-value=teal]')).to_have_attribute('aria-pressed', 'true')
        page.locator('[data-action=mode][data-value=dark]').click()
        expect(page.locator('[data-action=mode][data-value=dark]')).to_have_attribute('aria-pressed', 'true')
        page.locator('#mono-button').click()
        expect(page.locator('#mono-button')).to_have_attribute('aria-pressed', 'true')
        assert page.locator('.focus-card').first.evaluate('(element) => getComputedStyle(element).backgroundColor') == 'rgb(0, 0, 0)'
        assert page.locator('.matrix-row[data-palette=teal] .matrix-sample[data-mode=dark]').first.evaluate('(element) => getComputedStyle(element).backgroundColor') == 'rgb(16, 73, 76)'
        page.locator('.matrix-row[data-palette=teal] .matrix-sample[data-concept=B][data-mode=dark]').click()
        assert page.locator('.large-logo-preview').evaluate('(element) => getComputedStyle(element).backgroundColor') == 'rgb(16, 73, 76)'
        page.keyboard.press('Escape')
        page.locator('.focus-card[data-concept=B] [data-action=inspect]').click()
        assert page.locator('.large-logo-preview').evaluate('(element) => getComputedStyle(element).backgroundColor') == 'rgb(0, 0, 0)'
        page.keyboard.press('Escape')
        page.locator('#mono-button').click()
        passed('Keyboard selection, dark background, and monochrome control work without altering matrix colors')

        page.locator('.matrix-row[data-palette=navy] .matrix-sample[data-concept=C][data-mode=dark]').click()
        expect(page.locator('#preview-dialog')).to_be_visible()
        expect(page.locator('#preview-title')).to_contain_text('Praise Ligature')
        with page.expect_download() as download:
            page.locator('[data-action=download-svg]').click()
        target = temporary / download.value.suggested_filename
        download.value.save_as(target)
        svg = ET.parse(target).getroot()
        assert any(element.tag.endswith('path') for element in svg.iter())
        assert 'DRAFT' in target.read_text()
        page.keyboard.press('Escape')
        expect(page.locator('#preview-dialog')).not_to_be_visible()
        assert page.evaluate('document.activeElement.classList.contains("matrix-sample")')
        passed('Large previews, editable mark SVG download, Escape, and focus return work')

        page.locator('.focus-card[data-concept=B] [data-action=save]').click()
        expect(page.locator('.focus-card[data-concept=B] [data-action=save]')).to_have_attribute('aria-pressed', 'true')
        page.locator('.focus-card[data-concept=D] [data-action=save]').click()
        expect(page.locator('.focus-card[data-concept=D] [data-action=save]')).to_have_attribute('aria-pressed', 'true')
        page.locator('.focus-card[data-concept=D] [data-action=inspect]').click()
        expect(page.locator('#preview-title')).to_contain_text('Resonant Sanctuary')
        with page.expect_download() as download:
            page.locator('[data-action=download-svg]').click()
        target = temporary / download.value.suggested_filename
        download.value.save_as(target)
        assert download.value.suggested_filename.startswith('DRAFT-D-')
        assert geometry_signature(ET.parse(target).getroot()) == geometry_signature(ET.parse(ROOT.parents[2] / 'brand/concepts' / sources['D']).getroot())
        page.keyboard.press('Escape')
        with page.expect_download() as download:
            page.locator('[data-action=export-notes]').click()
        target = temporary / download.value.suggested_filename
        download.value.save_as(target)
        notes = json.loads(target.read_text())
        assert 'teal:B' in notes['savedPairings']
        assert 'teal:D' in notes['savedPairings']
        assert len(notes['palettes']) == 5
        assert notes['approval'].startswith('None')
        passed('D enlarges and downloads with source placement intact; B/D saved pairings export with five palettes and draft status')

        page.locator('[data-action=edit-colors]').click()
        page.locator('#hex-primary').fill('#FFFFFF')
        page.locator('#hex-neutral').fill('#FFFFFF')
        page.locator('#color-form button[type=submit]').click()
        expect(page.locator('#contrast-summary')).to_contain_text('1.00')
        expect(page.locator('#contrast-summary')).to_contain_text('needs revision')
        assert page.evaluate('window.TOPExplorer.getPalettes().find(p=>p.id==="teal").primary') == '#FFFFFF'
        page.locator('[data-action=edit-colors]').click()
        page.locator('#hex-primary').fill('#GGGGGG')
        assert not page.locator('#hex-primary').evaluate('(element) => element.checkValidity()')
        page.locator('[data-action=reset-colors]').click()
        expect(page.locator('#color-dialog')).not_to_be_visible()
        assert page.evaluate('window.TOPExplorer.getPalettes().find(p=>p.id==="teal").primary') == '#10494C'
        passed('Color editor exposes a deliberately failing 1:1 pair, rejects invalid HEX, and resets safely')

        for application in ('flyer', 'instagram', 'avatar', 'signage'):
            page.locator(f'[data-action=application][data-value={application}]').click()
            expect(page.locator('.application-card')).to_have_count(6)
            page.locator('.application-art[data-concept=D]').first.click()
            expect(page.locator('#preview-dialog')).to_be_visible()
            expect(page.locator('.application-preview svg')).to_have_count(1)
            if application in ('flyer', 'instagram'):
                expect(page.locator('.application-preview')).to_contain_text('[DATE]')
                expect(page.locator('.application-preview')).to_contain_text('[VENUE]')
            with page.expect_download() as download:
                page.locator('[data-action=download-svg]').click()
            target = temporary / download.value.suggested_filename
            download.value.save_as(target)
            assert download.value.suggested_filename.startswith('DRAFT-D-')
            ET.parse(target)
            assert 'DRAFT' in target.read_text()
            page.locator('[data-action=close-preview]').click()
        passed('Four application types each show all six shortlisted pairings; D enlarges and exports valid editable SVG in each')

        for width in (1440, 768, 390):
            page.set_viewport_size({'width': width, 'height': 900})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Page overflow at {width}px'
            page.locator('.focus-card[data-concept=D] [data-action=inspect]').click()
            expect(page.locator('#preview-dialog')).to_be_visible()
            assert page.locator('#preview-dialog').evaluate('(element) => element.getBoundingClientRect().width') <= width
            page.keyboard.press('Escape')
        passed('Desktop, tablet, and 390px mobile layouts and dialogs fit without page overflow')

        offline = (ROOT / 'exports/tabernacle-color-explorer.html').read_text()
        offline_page = context.new_page()
        offline_errors, remote_requests = [], []
        offline_page.on('pageerror', lambda error: offline_errors.append(str(error)))
        offline_page.on('request', lambda request: remote_requests.append(request.url) if request.url.startswith(('http://', 'https://', 'file://')) else None)
        offline_page.set_content(offline, wait_until='networkidle')
        offline_page.evaluate('document.fonts.ready')
        expect(offline_page.locator('.matrix-sample')).to_have_count(30)
        expect(offline_page.locator('#offline-download')).to_have_text('Save this explorer ↗')
        offline_page.locator('.palette-choice[data-value=forest]').click()
        offline_page.locator('.focus-card[data-concept=C] [data-action=save]').click()
        offline_page.locator('.focus-card[data-concept=D] [data-action=save]').click()
        with offline_page.expect_download() as download:
            offline_page.locator('#offline-download').click()
        target = temporary / download.value.suggested_filename
        download.value.save_as(target)
        reopened = context.new_page()
        reopened.set_content(target.read_text(), wait_until='networkidle')
        assert reopened.evaluate('window.TOPExplorer.getState().palette') == 'forest'
        assert 'forest:C' in reopened.evaluate('window.TOPExplorer.getState().saved')
        assert 'forest:D' in reopened.evaluate('window.TOPExplorer.getState().saved')
        expect(reopened.locator('.focus-card[data-concept=D] [data-action=save]')).to_have_attribute('aria-pressed', 'true')
        reopened.locator('.focus-card[data-concept=D] [data-action=inspect]').click()
        with reopened.expect_download() as download:
            reopened.locator('[data-action=download-svg]').click()
        target = temporary / download.value.suggested_filename
        download.value.save_as(target)
        assert download.value.suggested_filename.startswith('DRAFT-D-forest-')
        assert geometry_signature(ET.parse(target).getroot()) == geometry_signature(ET.parse(ROOT.parents[2] / 'brand/concepts' / sources['D']).getroot())
        assert not offline_errors, offline_errors
        assert not remote_requests, remote_requests
        passed('Single-file explorer needs no external requests, retains saved C/D choices after reopening, and downloads D with source placement intact')

        assert not errors, errors
        browser.close()

marks = list((ROOT / 'exports/marks').glob('*.svg'))
applications = list((ROOT / 'exports/applications').glob('*.svg'))
assert len(marks) == 30, len(marks)
assert len(applications) == 48, len(applications)
for svg in marks + applications:
    parsed = ET.parse(svg).getroot()
    assert 'DRAFT' in svg.read_text()
    assert not any(element.tag.endswith('image') for element in parsed.iter())
passed('All 78 exported SVGs (30 marks and 48 applications) parse, retain draft labeling, and contain no raster images')

report = {'status': 'passed', 'checks': checks, 'count': len(checks),
          'method': 'Chromium with Python Playwright; local HTTP for source, in-memory self-contained HTML for offline validation.',
          'limit': 'The managed browser blocks file:// navigation. A direct double-click in an unmanaged desktop browser was not tested.'}
(ROOT / 'exports/validation-report.json').write_text(json.dumps(report, indent=2) + '\n')
print(f'Completed {len(checks)} substantive browser and export checks.', flush=True)
