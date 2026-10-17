(function () {
  'use strict';

  const DATA = window.TOPData;
  const ROLES = ['primary', 'secondary', 'accent', 'neutral'];
  const STORAGE = 'top-color-study-02-v1';
  const basePalettes = JSON.parse(JSON.stringify(DATA.palettes));
  const palettes = JSON.parse(JSON.stringify(DATA.palettes));
  const concepts = DATA.concepts;
  const state = { palette: 'teal', mode: 'light', monochrome: false, application: 'flyer', saved: [], edited: {}, preview: null };
  const $ = (selector) => document.querySelector(selector);
  const $$ = (selector) => Array.from(document.querySelectorAll(selector));
  const esc = (value) => String(value).replace(/[&<>"']/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[character]));
  const paletteById = (id) => palettes.find((palette) => palette.id === id);
  const conceptById = (id) => concepts.find((concept) => concept.id === id);
  let toastTimer;
  let lastPreviewTrigger;

  function luminance(hex) {
    const values = hex.replace('#', '').match(/.{2}/g).map((part) => parseInt(part, 16) / 255);
    const linear = values.map((value) => value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4);
    return linear[0] * 0.2126 + linear[1] * 0.7152 + linear[2] * 0.0722;
  }

  function contrast(a, b) {
    const values = [luminance(a), luminance(b)].sort((x, y) => y - x);
    return (values[0] + 0.05) / (values[1] + 0.05);
  }

  function colors(palette, mode, monochrome) {
    if (monochrome) return mode === 'dark' ? { background: '#000000', ink: '#FFFFFF', accent: '#FFFFFF' } : { background: '#FFFFFF', ink: '#000000', accent: '#000000' };
    return { background: mode === 'dark' ? palette.primary : palette.neutral, ink: mode === 'dark' ? palette.neutral : palette.primary, accent: palette.accent };
  }

  function mark(concept, color, size, extraClass) {
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="${size || 256}" height="${size || 256}" class="brand-mark ${extraClass || ''}" role="img" aria-label="${esc(concept.name)} — draft"><title>${esc(concept.name)} — DRAFT</title>${concept.mark.replace(/#000000/gi, color)}</svg>`;
  }

  function wordmark() {
    return '<div class="brand-wordmark">Tabernacle<br>of Praise</div>';
  }

  function isSaved(palette, concept) {
    return state.saved.includes(`${palette.id}:${concept.id}`);
  }

  function loadState() {
    try {
      const exportedState = document.getElementById('study-export-state');
      const saved = exportedState ? JSON.parse(exportedState.textContent) : JSON.parse(localStorage.getItem(STORAGE));
      if (!saved || typeof saved !== 'object') return;
      if (paletteById(saved.palette)) state.palette = saved.palette;
      if (['light', 'dark'].includes(saved.mode)) state.mode = saved.mode;
      if (['flyer', 'instagram', 'avatar', 'signage'].includes(saved.application)) state.application = saved.application;
      state.saved = Array.isArray(saved.saved) ? saved.saved.filter((key) => typeof key === 'string' && /^(navy|forest|teal|burgundy|charcoal):[BCD]$/.test(key)) : [];
      if (saved.edited && typeof saved.edited === 'object') {
        for (const [id, values] of Object.entries(saved.edited)) {
          const palette = paletteById(id);
          if (!palette || !values || !ROLES.every((role) => /^#[0-9a-f]{6}$/i.test(values[role] || ''))) continue;
          const valid = Object.fromEntries(ROLES.map((role) => [role, values[role].toUpperCase()]));
          Object.assign(palette, valid);
          state.edited[id] = valid;
        }
      }
    } catch (_) { /* Local-file browser settings can disable persistence. The study still works. */ }
  }

  function persist() {
    try {
      localStorage.setItem(STORAGE, JSON.stringify({ palette: state.palette, mode: state.mode, application: state.application, saved: state.saved, edited: state.edited }));
    } catch (_) { /* Edits remain in memory; export is always available. */ }
  }

  function toast(message) {
    $('#toast').textContent = message;
    $('#toast').classList.add('is-visible');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => $('#toast').classList.remove('is-visible'), 2600);
  }

  function renderPalettes() {
    $('#palette-selector').innerHTML = palettes.map((palette) => `<button type="button" class="palette-choice" data-action="palette" data-value="${palette.id}" data-focus-key="palette-${palette.id}" aria-pressed="${state.palette === palette.id}"><span class="palette-chip" aria-hidden="true"><i style="background:${palette.primary}"></i><i style="background:${palette.accent}"></i></span><span><strong>${esc(palette.name)}</strong><small>${palette.number} / ${state.edited[palette.id] ? 'Edited locally' : palette.recommended ? 'Shortlisted direction' : 'Color direction'}</small></span>${state.palette === palette.id ? '<span class="choice-indicator" aria-hidden="true">✓</span>' : ''}</button>`).join('');
  }

  function renderFocus(palette) {
    const treatment = colors(palette, state.mode, state.monochrome);
    $('#active-palette-heading').innerHTML = `<h3>${esc(palette.family)}</h3><p>${state.monochrome ? 'Monochrome control · pure black and white' : esc(palette.mood)}</p>`;
    $('#focus-previews').innerHTML = concepts.map((concept) => `<article class="focus-card" data-concept="${concept.id}" style="background:${treatment.background};color:${treatment.ink}"><div class="focus-label"><strong>${concept.id} / ${esc(concept.name)}</strong><span class="concept-category">${esc(concept.category)}</span></div><div class="focus-art">${mark(concept, treatment.ink)}${wordmark()}</div><div class="accent-line" style="background:${treatment.accent}"></div><div class="focus-bottom" style="border-color:${treatment.ink}25"><button type="button" class="save-button" data-action="save" data-palette="${palette.id}" data-concept="${concept.id}" data-focus-key="save-${concept.id}" aria-pressed="${isSaved(palette, concept)}"><span aria-hidden="true">${isSaved(palette, concept) ? '★' : '☆'}</span>${isSaved(palette, concept) ? 'Saved pairing' : 'Save pairing'}</button><button type="button" class="inspect-button" data-action="inspect" data-palette="${palette.id}" data-concept="${concept.id}" data-mode="${state.mode}" data-focus-key="inspect-${concept.id}">Larger view ↗</button></div></article>`).join('');
    $$('.segmented [data-action=mode]').forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.value === state.mode)));
    $('#mono-button').setAttribute('aria-pressed', String(state.monochrome));
    $('#color-swatches').innerHTML = ROLES.map((role) => `<button type="button" class="color-swatch" data-action="copy" data-value="${palette[role]}" data-focus-key="swatch-${role}" aria-label="Copy ${role} ${palette[role]}"><span class="swatch-paint" style="background:${palette[role]}"></span><span class="swatch-info"><span><strong>${role[0].toUpperCase() + role.slice(1)}</strong><small>${esc(palette.names[role])}</small></span><code>${palette[role]}</code></span></button>`).join('');
    $('#palette-reading').innerHTML = `<p class="eyebrow">THE FEELING</p><p>${esc(palette.note)}${state.edited[palette.id] ? ' <strong>Colors have been adjusted locally; the original reading is a reference, not a fresh assessment of your edits.</strong>' : ''}<span class="print-reading"><strong>In print:</strong> ${esc(palette.print)}</span></p>`;
  }

  function renderMeanings() {
    $('#meaning-cards').innerHTML = concepts.map((concept) => {
      const meaning = DATA.meanings[concept.id];
      const paths = concept.mark.match(/<path\b[^>]*>/g);
      let pieces;
      if (concept.id === 'B') {
        const subpaths = paths[0].match(/ d="([^"]+)"/)[1].match(/M.*?Z/g);
        pieces = [`<path d="${subpaths[0]}"/>`, subpaths.slice(1).map((path) => `<path d="${path}"/>`).join(''), concept.mark];
      } else if (concept.id === 'C') {
        pieces = [paths[0], paths[1], concept.mark];
      } else {
        const wrap = (paths) => `<g transform="translate(-7 0)">${paths.join('')}</g>`;
        pieces = [wrap(paths.slice(0, 3)), wrap(paths.slice(3)), concept.mark];
      }
      return `<article class="meaning-card" data-concept="${concept.id}"><p class="eyebrow">${concept.id} / ${esc(concept.category)}</p><h3>${esc(concept.name)}</h3><div class="meaning-construction">${pieces.map((piece, index) => `<figure><svg viewBox="0 0 256 256" width="72" height="72" role="img" aria-label="${esc(meaning.labels[index])}"><g fill="#000000">${piece}</g></svg><figcaption>${esc(meaning.labels[index])}</figcaption></figure>${index < 2 ? `<span class="meaning-operation" aria-hidden="true">${index === 0 ? meaning.operation : '='}</span>` : ''}`).join('')}</div><dl><dt>Visible in the drawing</dt><dd>${esc(meaning.visible)}</dd><dt>Intended association</dt><dd>${esc(meaning.intended)}</dd><dt>What needs testing</dt><dd>${esc(meaning.limit)}</dd></dl></article>`;
    }).join('');
  }

  function renderMatrix() {
    $('.matrix-head').innerHTML = '<span role="columnheader">PALETTE DIRECTION</span>' + concepts.map((concept) => `<span role="columnheader">${concept.id} / ${esc(concept.name.toUpperCase())}</span>`).join('');
    $('#matrix-rows').innerHTML = palettes.map((palette) => `<div class="matrix-row" role="row" data-palette="${palette.id}"><div class="matrix-palette" role="rowheader"><span class="eyebrow">${palette.number} / ${palette.recommended ? 'SHORTLIST' : 'EXPLORE'}</span><h3>${esc(palette.name)}</h3><p>${esc(palette.mood)}</p><div class="matrix-values">${ROLES.map((role) => `<button type="button" data-action="copy" data-value="${palette[role]}" aria-label="Copy ${esc(palette.name)} ${role} ${palette[role]}"><i style="background:${palette[role]}" aria-hidden="true"></i><span><small>${role}</small><code>${palette[role]}</code></span></button>`).join('')}</div><span class="ratio-label">${contrast(palette.primary, palette.neutral).toFixed(2)}:1 · primary / neutral</span></div>${concepts.map((concept) => `<div class="matrix-cell" role="cell" data-concept="${concept.id}">${['light', 'dark'].map((mode) => {
      const treatment = colors(palette, mode, false);
      return `<button type="button" class="matrix-sample" data-action="inspect" data-palette="${palette.id}" data-concept="${concept.id}" data-mode="${mode}" style="background:${treatment.background};color:${treatment.ink}" aria-label="Inspect ${esc(palette.name)}, concept ${concept.id}, ${mode} background"><span class="sample-mode">${mode}</span>${mark(concept, treatment.ink, 61)}${wordmark()}<span class="sample-accent" style="background:${treatment.accent}"></span></button>`;
    }).join('')}</div>`).join('')}</div>`).join('');
  }

  function renderChecks(palette) {
    const core = contrast(palette.primary, palette.neutral);
    const accent = contrast(palette.accent, palette.neutral);
    const accentDark = contrast(palette.accent, palette.primary);
    const secondary = contrast(palette.secondary, palette.neutral);
    $('#contrast-summary').innerHTML = `<article class="contrast-card primary"><p class="eyebrow">PRIMARY / NEUTRAL</p><div class="contrast-number">${core.toFixed(2)}<small>:1</small></div><p>${core >= 4.5 ? 'A clear foundation for normal-sized text in either direction.' : 'This edited pair needs revision for normal-sized text.'}</p><span class="contrast-chip"><i class="tiny-status ${core < 4.5 ? 'caution' : ''}"></i>${core >= 4.5 ? 'Meets the 4.5:1 text threshold' : 'Below the 4.5:1 text threshold'}</span></article><article class="contrast-card"><p class="eyebrow">ACCENT / LIGHT GROUND</p><div class="contrast-number">${accent.toFixed(2)}<small>:1</small></div><p>${accent >= 4.5 ? 'Meets normal-text contrast in this edited pair.' : 'Decorative detail, not body text or fine logo structure.'}</p><span class="contrast-chip"><i class="tiny-status ${accent < 4.5 ? 'caution' : ''}"></i>${accent >= 4.5 ? 'Normal-text contrast' : 'Below normal-text contrast'}</span></article><article class="contrast-card"><p class="eyebrow">SUPPORTING COLORS</p><p>Secondary on neutral <strong>${secondary.toFixed(2)}:1</strong><br>Accent on primary <strong>${accentDark.toFixed(2)}:1</strong></p><p>Text needs 4.5:1; large text 3:1. Ratios are calculated from sRGB HEX values. A logo exemption is not a reason to use fragile low-contrast detail.</p></article>`;
    const treatment = colors(palette, state.mode, state.monochrome);
    $('#size-tests').innerHTML = concepts.map((concept) => `<div class="size-row"><div class="size-row-label"><strong>${concept.id} / ${esc(concept.name)}</strong><small>${concept.id === 'B' ? 'Watch the strings, not just the silhouette.' : concept.id === 'C' ? 'Watch the T/P channel and the inner counter.' : 'Watch the shared room, fine seams, and rising bands.'}</small></div>${[64, 32, 24, 16].map((size) => `<div class="size-case"><div class="size-art" style="background:${treatment.background};color:${treatment.ink}">${mark(concept, treatment.ink, size)}</div><span>${size}px · actual CSS size</span></div>`).join('')}</div>`).join('');
    $('#rccg-reservation').innerHTML = concepts.map((concept) => `<div class="pairing-example" style="background:${palette.neutral}"><span class="pairing-label">${concept.id}</span><div class="rccg-placeholder">AUTHORIZED<br>RCCG EMBLEM<br><strong>ASSET PENDING</strong><br>Placeholder only</div><span class="reservation-divider" aria-hidden="true"></span><div class="reservation-parish" style="color:${palette.primary}">${mark(concept, palette.primary, 48)}${wordmark()}</div></div>`).join('');
  }

  function renderApplications() {
    $('#application-mode-label').textContent = `${state.mode === 'dark' ? 'Dark' : 'Light'} treatment · change in the workbench`;
    $$('.application-tabs button').forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.value === state.application)));
    const selected = ['teal', 'navy'].flatMap((id) => concepts.map((concept) => ({ palette: paletteById(id), concept })));
    $('#application-gallery').innerHTML = selected.map(({ palette, concept }) => `<article class="application-card" data-type="${state.application}"><button type="button" class="application-art" data-action="application-preview" data-palette="${palette.id}" data-concept="${concept.id}" aria-label="Enlarge ${esc(palette.name)} and ${esc(concept.name)} ${state.application}">${window.TOPApplications.render({ type: state.application, palette, concept, mode: state.mode })}</button><div class="application-info"><div><h3>${concept.id} / ${esc(concept.name)}</h3><p>${esc(palette.name)} · ${state.mode} ↗</p></div></div></article>`).join('');
  }

  function renderRecommendations() {
    $('#recommendation-cards').innerHTML = ['teal', 'navy'].map((id, index) => {
      const palette = paletteById(id);
      const neutral = id === 'teal' ? palette.secondary : palette.neutral;
      return `<article class="recommendation-card"><div class="recommendation-art" style="background:${palette.primary};color:${neutral}">${mark(conceptById('C'), neutral)}<span class="recommendation-strip" style="background:${palette.accent}"></span></div><div class="recommendation-copy"><p class="eyebrow">${index === 0 ? 'FIRST / CONTEMPORARY DISTINCTION' : 'SECOND / TIMELESS DIGNITY'}</p><h3>${esc(palette.name)}</h3><p>${index === 0 ? 'Deep teal gives the identity a distinct contemporary foundation. Sand adds warmth; soft gold makes a quiet ceremonial accent.' : 'Navy brings clarity and quiet authority. Ivory keeps it open; measured gold brings warmth without turning the whole identity ornate.'}</p><button type="button" class="text-link" data-action="study-palette" data-value="${id}">Explore this palette <span aria-hidden="true">↗</span></button></div></article>`;
    }).join('');
    $('#shortlist').innerHTML = state.saved.map((key) => {
      const [id, concept] = key.split(':');
      return `<span class="saved-tag">${esc(paletteById(id).name)} / ${concept}<button type="button" data-action="save" data-palette="${id}" data-concept="${concept}" aria-label="Remove ${esc(paletteById(id).name)} and concept ${concept} from saved pairings">×</button></span>`;
    }).join('');
  }

  function render() {
    const focusKey = document.activeElement && document.activeElement.dataset.focusKey;
    const palette = paletteById(state.palette);
    renderMeanings();
    renderPalettes();
    renderFocus(palette);
    renderMatrix();
    renderChecks(palette);
    renderApplications();
    renderRecommendations();
    persist();
    if (focusKey) {
      const target = document.querySelector(`[data-focus-key="${focusKey}"]`);
      if (target) target.focus({ preventScroll: true });
    }
  }

  function showPreview({ palette, concept, mode, kind, type, monochrome = false }) {
    const paletteData = paletteById(palette);
    const conceptData = conceptById(concept);
    if (!paletteData || !conceptData) return;
    lastPreviewTrigger = document.activeElement;
    state.preview = { palette, concept, mode, kind, type, monochrome: kind === 'logo' && monochrome };
    $('#preview-title').textContent = `${concept} / ${conceptData.name} · ${paletteData.name}`;
    if (kind === 'application') {
      $('#preview-content').innerHTML = `<div class="application-preview">${window.TOPApplications.render({ type, palette: paletteData, concept: conceptData, mode })}</div>`;
      $('#preview-caption').textContent = 'Editable layout study. Bracketed event details are placeholders. Type is provisional.';
    } else {
      const treatment = colors(paletteData, mode, state.preview.monochrome);
      $('#preview-content').innerHTML = `<div class="large-logo-preview" style="background:${treatment.background};color:${treatment.ink}">${mark(conceptData, treatment.ink)}${wordmark()}</div>`;
      $('#preview-caption').textContent = `${mode === 'dark' ? 'Dark' : 'Light'} ground. ${conceptData.caution} SVG download contains the symbol, with a separate background.`;
    }
    $('#preview-dialog').showModal();
  }

  function closePreview() {
    $('#preview-dialog').close();
    state.preview = null;
    if (lastPreviewTrigger && lastPreviewTrigger.isConnected) lastPreviewTrigger.focus({ preventScroll: true });
  }

  function download(contents, type, filename) {
    const url = URL.createObjectURL(new Blob([contents], { type }));
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = filename;
    document.body.append(anchor);
    anchor.click();
    anchor.remove();
    setTimeout(() => URL.revokeObjectURL(url), 5000);
  }

  function downloadPreview() {
    const preview = state.preview;
    if (!preview) return;
    const palette = paletteById(preview.palette);
    const concept = conceptById(preview.concept);
    let svg;
    if (preview.kind === 'application') {
      svg = window.TOPApplications.render({ type: preview.type, palette, concept, mode: preview.mode });
    } else {
      const treatment = colors(palette, preview.mode, preview.monochrome);
      svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256"><title>${esc(concept.name)} · ${esc(palette.name)} — DRAFT</title><desc>DRAFT — NOT FOR PUBLICATION. Referenced draft geometry with proposed color. B/C retain exploration-01 v3; D is new exploration-03. No approval implied.</desc><rect id="background" width="256" height="256" fill="${treatment.background}"/>${concept.mark.replace(/#000000/gi, treatment.ink)}</svg>`;
    }
    download(svg, 'image/svg+xml', `DRAFT-${preview.concept}-${palette.id}-${preview.kind === 'application' ? preview.type : 'mark'}-${preview.mode}.svg`);
    toast('Editable draft SVG downloaded');
  }

  function exportNotes() {
    const output = { study: 'Tabernacle of Praise — color study 02', status: DATA.status, approval: 'None. Logo, palette, and typography remain unapproved.', selectedPalette: state.palette, background: state.mode, savedPairings: state.saved, palettes: palettes.map((palette) => ({ id: palette.id, family: palette.family, primary: palette.primary, secondary: palette.secondary, accent: palette.accent, neutral: palette.neutral, contrastPrimaryNeutral: Number(contrast(palette.primary, palette.neutral).toFixed(4)) })), recommendations: { palettes: ['teal', 'navy'], concept: 'C', thirdConcept: 'D — Resonant Sanctuary introduces shared space and rising rhythm. Compare D against C; no replacement is approved.' } };
    download(JSON.stringify(output, null, 2), 'application/json', 'DRAFT-Tabernacle-of-Praise-color-study.json');
    toast('Study notes and HEX values downloaded');
  }

  function saveHTML() {
    const clone = document.documentElement.cloneNode(true);
    clone.querySelectorAll('dialog[open]').forEach((dialog) => dialog.removeAttribute('open'));
    const oldState = clone.querySelector('#study-export-state');
    if (oldState) oldState.remove();
    const exported = document.createElement('script');
    exported.type = 'application/json';
    exported.id = 'study-export-state';
    exported.textContent = JSON.stringify({ palette: state.palette, mode: state.mode, application: state.application, saved: state.saved, edited: state.edited });
    clone.querySelector('head').append(exported);
    download('<!doctype html>\n' + clone.outerHTML, 'text/html', 'DRAFT-Tabernacle-color-explorer.html');
    toast('Offline explorer saved with your current study choices');
  }

  async function copy(value) {
    try {
      await navigator.clipboard.writeText(value);
    } catch (_) {
      const input = document.createElement('textarea');
      input.value = value;
      input.style.position = 'fixed';
      input.style.opacity = '0';
      document.body.append(input);
      input.select();
      const success = document.execCommand('copy');
      input.remove();
      if (!success) { toast(`HEX value: ${value}`); return; }
    }
    toast(`${value} copied`);
  }

  function editColors() {
    const palette = paletteById(state.palette);
    $('#color-dialog-title').textContent = `Adjust ${palette.name.toLowerCase()}`;
    $('#color-inputs').innerHTML = ROLES.map((role) => `<div class="color-input-row"><label for="hex-${role}">${role[0].toUpperCase() + role.slice(1)}<small>${esc(palette.names[role])}</small></label><input type="color" value="${palette[role]}" data-role="${role}" aria-label="${role} color picker"><input type="text" id="hex-${role}" name="${role}" data-role="${role}" value="${palette[role]}" pattern="#[0-9a-fA-F]{6}" maxlength="7" required aria-label="${role} HEX value" spellcheck="false" autocomplete="off"></div>`).join('');
    $('#color-dialog').showModal();
  }

  document.addEventListener('click', (event) => {
    const target = event.target.closest('[data-action]');
    if (!target) return;
    const { action, value, palette, concept, mode } = target.dataset;
    if (action === 'palette' || action === 'study-palette') {
      if (!paletteById(value)) return;
      state.palette = value;
      state.monochrome = false;
      render();
      if (action === 'study-palette') $('#workbench').scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else if (action === 'mode') {
      state.mode = value;
      render();
    } else if (action === 'mono') {
      state.monochrome = !state.monochrome;
      render();
    } else if (action === 'save') {
      const key = `${palette}:${concept}`;
      if (!paletteById(palette) || !conceptById(concept)) return;
      state.saved = state.saved.includes(key) ? state.saved.filter((entry) => entry !== key) : [...state.saved, key];
      render();
      toast(state.saved.includes(key) ? 'Pairing saved for your review' : 'Pairing removed');
    } else if (action === 'inspect') {
      showPreview({ palette, concept, mode, kind: 'logo', monochrome: Boolean(target.closest('#focus-previews')) && state.monochrome });
    } else if (action === 'application-preview') {
      showPreview({ palette, concept, mode: state.mode, kind: 'application', type: state.application });
    } else if (action === 'close-preview') {
      closePreview();
    } else if (action === 'application') {
      state.application = value;
      renderApplications();
      persist();
    } else if (action === 'download-svg') {
      downloadPreview();
    } else if (action === 'copy') {
      copy(value);
    } else if (action === 'export-notes') {
      exportNotes();
    } else if (action === 'save-html') {
      event.preventDefault();
      saveHTML();
    } else if (action === 'edit-colors') {
      editColors();
    } else if (action === 'close-colors') {
      $('#color-dialog').close();
    } else if (action === 'reset-colors') {
      Object.assign(paletteById(state.palette), JSON.parse(JSON.stringify(basePalettes.find((entry) => entry.id === state.palette))));
      delete state.edited[state.palette];
      $('#color-dialog').close();
      render();
      toast('Original proposed palette restored');
    }
  });

  $('#color-form').addEventListener('input', (event) => {
    if (!event.target.dataset.role) return;
    const role = event.target.dataset.role;
    const value = event.target.value;
    const otherType = event.target.type === 'color' ? 'text' : 'color';
    if (/^#[0-9a-f]{6}$/i.test(value)) $(`#color-inputs input[type=${otherType}][data-role=${role}]`).value = value;
  });

  $('#color-form').addEventListener('submit', (event) => {
    event.preventDefault();
    if (!event.target.reportValidity()) return;
    const values = Object.fromEntries(ROLES.map((role) => [role, $(`#hex-${role}`).value.toUpperCase()]));
    Object.assign(paletteById(state.palette), values);
    state.edited[state.palette] = values;
    $('#color-dialog').close();
    render();
    toast('Draft colors updated; contrast recalculated');
  });

  $('#preview-dialog').addEventListener('click', (event) => { if (event.target === $('#preview-dialog')) closePreview(); });
  $('#preview-dialog').addEventListener('cancel', () => { state.preview = null; });
  $('#color-dialog').addEventListener('click', (event) => { if (event.target === $('#color-dialog')) $('#color-dialog').close(); });

  loadState();
  render();
  if (window.TOPStandalone) {
    const offline = $('#offline-download');
    offline.href = '#';
    offline.removeAttribute('download');
    offline.dataset.action = 'save-html';
    offline.textContent = 'Save this explorer ↗';
  }
  window.TOPExplorer = { contrast, getState: () => JSON.parse(JSON.stringify(state)), getPalettes: () => JSON.parse(JSON.stringify(palettes)) };
}());
