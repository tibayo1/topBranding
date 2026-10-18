(function () {
  'use strict';
  const $ = (query, root) => (root || document).querySelector(query);
  const $$ = (query, root) => Array.from((root || document).querySelectorAll(query));
  const esc = value => String(value == null ? '' : value).replace(/[&<>"']/g, character => ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'}[character]));
  const list = value => Array.isArray(value) ? value : value ? [value] : [];
  const prose = value => Array.isArray(value) ? value.join(' ') : String(value || '');
  const assetHref = value => {
    const reference = String(value || '');
    const base = window.TOPReview05AssetBase;
    return base && reference && !/^(?:[a-z][a-z0-9+.-]*:|#|\/)/i.test(reference) ? new URL(reference, base).href : reference;
  };
  const slug = value => String(value || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  const data = window.TOPReview05;
  if (!data || !Array.isArray(data.directions) || !data.directions.length) {
    $('#review-lead').innerHTML = '<span class="data-error">The artwork could not load. Keep data.js beside index.html and open the complete review folder.</span>';
    return;
  }
  const directions = data.directions;
  const storageKey = 'top-creative-review-05';
  const validIds = new Set(directions.map(direction => String(direction.id)));
  let saved = {};
  try { saved = JSON.parse(localStorage.getItem(storageKey) || '{}') || {}; } catch (_) { /* Private browsing can disable storage. */ }
  const state = {
    mode: saved.mode === 'dark' ? 'dark' : 'light',
    choices: new Set(list(saved.choices).map(String).filter(id => validIds.has(id))),
    notes: typeof saved.notes === 'string' ? saved.notes : ''
  };
  let svgCounter = 0;
  let toastTimer;
  let saveTimer;
  let dialogItem = null;
  let dialogDark = false;
  let dialogOpener = null;
  const directionFor = id => directions.find(direction => String(direction.id) === String(id));
  const boxFor = item => {
    const values = String(item && item.viewBox || '0 0 256 256').trim().split(/[\s,]+/).map(Number);
    return values.length === 4 && values.every(Number.isFinite) && values[2] > 0 && values[3] > 0 ? values.join(' ') : '0 0 256 256';
  };
  const recolor = (art, dark) => String(art || '')
    .replace(/#(?:000000|111111|000|111)(?![0-9a-f])/gi, '__TOP_INK__')
    .replace(/#(?:ffffff|fff)(?![0-9a-f])/gi, '__TOP_PAPER__')
    .replace(/\b(fill|stroke)=(['"])black\2/gi, '$1=$2__TOP_INK__$2')
    .replace(/\b(fill|stroke)=(['"])white\2/gi, '$1=$2__TOP_PAPER__$2')
    .replace(/__TOP_INK__/g, dark ? '#ffffff' : '#111111')
    .replace(/__TOP_PAPER__/g, dark ? '#111111' : '#ffffff')
    .replace(/\bcurrentColor\b/gi, dark ? '#ffffff' : '#111111');
  // Several SVGs share a page. Give embedded definitions their own IDs.
  function uniqueSvg(art) {
    const prefix = `review-art-${++svgCounter}-`;
    const ids = [];
    let result = String(art).replace(/\bid=(['"])([^'"]+)\1/g, (match, quote, id) => { ids.push(id); return `id=${quote}${prefix}${id}${quote}`; });
    ids.forEach(id => {
      const pattern = id.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      result = result.replace(new RegExp(`url\\(\\s*(['"]?)#${pattern}\\1\\s*\\)`, 'g'), `url(#${prefix}${id})`)
        .replace(new RegExp(`((?:xlink:)?href=['"])#${pattern}(['"])`, 'g'), `$1#${prefix}${id}$2`);
    });
    return result;
  }
  function svgMark(item, dark) {
    return uniqueSvg(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="${esc(boxFor(item))}" fill="${dark ? '#ffffff' : '#111111'}" role="img" aria-label="${esc(item.name || item.label)}"><title>${esc(item.name || item.label)} — DRAFT — NOT FOR PUBLICATION</title>${recolor(item.mark, dark)}</svg>`);
  }
  function fullArtwork(art, dark, title) {
    const clean = recolor(art, dark).replace(/<\?xml[^>]*\?>/gi, '').trim();
    return uniqueSvg(clean.replace(/<svg\b([^>]*)>/i, (match, attributes) => `<svg${attributes.replace(/\s(?:role|aria-label)=(['"])[^'"]*\1/gi, '')} role="img" aria-label="${esc(title || 'Draft parish identity')}"><title>${esc(title || 'Draft parish identity')} — DRAFT — NOT FOR PUBLICATION</title>`));
  }
  function artworkFor(direction, kind, index) {
    if (!direction) return null;
    if (kind === 'horizontal' || kind === 'stacked') return {full:true, art:direction.lockups && direction.lockups[kind], name:`${direction.name} / ${kind} full name`, caption:'Complete parish name / unapproved lettering.', filename:`${direction.id}-${direction.name}-${kind}`};
    if (kind === 'signage' || kind === 'paper') return {full:true, art:direction.applications && direction.applications[kind], name:`${direction.name} / ${kind} study`, caption:'Hypothetical identity application. Not an actual church property, service, or printed announcement.', filename:`${direction.id}-${direction.name}-${kind}`};
    if (kind === 'sketch') {
      const item = list(direction.sketches)[Number(index)];
      return item ? {item, name:`${item.id} / ${item.name}`, caption:prose(item.idea), filename:`${item.id}-${item.name}`} : null;
    }
    if (kind === 'part') {
      const item = list(direction.parts)[Number(index)];
      return item ? {item, name:`${direction.name} / ${item.label}`, caption:'Construction fragment of an unapproved identity direction.', filename:`${direction.id}-construction-${item.label}`} : null;
    }
    if (kind === 'compact') return direction.compact ? {item:direction.compact, name:direction.compact.label || 'Compact study', caption:prose(direction.compact.caution), filename:`${direction.id}-compact-study`} : null;
    return {item:direction, name:direction.name, caption:prose(direction.visible || direction.idea), filename:`${direction.id}-${direction.name}-${direction.primaryType === 'wordmark' ? 'wordmark' : 'symbol'}`};
  }
  function artHtml(art, dark) { return art.full ? fullArtwork(art.art, dark, art.name) : svgMark(art.item, dark); }
  function toast(message) {
    $('#toast').textContent = message;
    $('#toast').classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => $('#toast').classList.remove('show'), 2600);
  }
  function persist(announce) {
    try {
      localStorage.setItem(storageKey, JSON.stringify({version:1, mode:state.mode, choices:Array.from(state.choices), notes:state.notes, identityApproved:false}));
      if (announce) $('#save-status').textContent = 'Saved in this browser. Nothing has been submitted or approved.';
    } catch (_) { $('#save-status').textContent = 'Browser storage is unavailable. Download your review notes to keep them.'; }
  }
  function triggerDownload(filename, contents, mime) {
    const url = URL.createObjectURL(new Blob([contents], {type:mime}));
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1500);
  }
  function svgFile(art, dark) {
    const description = `<desc>DRAFT — NOT FOR PUBLICATION. Unapproved identity exploration for RCCG Tabernacle of Praise. ${esc(art.name)}.</desc>`;
    let svg = art.full ? recolor(art.art, dark).replace(/<\?xml[^>]*\?>/gi, '').trim() : `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${esc(boxFor(art.item))}" fill="${dark ? '#ffffff' : '#111111'}"><title>${esc(art.name)} — DRAFT</title>${recolor(art.item.mark, dark)}</svg>`;
    const match = svg.match(/\bviewBox=(['"])([^'"]+)\1/i);
    const values = match ? match[2].trim().split(/[\s,]+/).map(Number) : [0,0,256,256];
    const background = dark && values.length === 4 && values.every(Number.isFinite) ? `<rect x="${values[0]}" y="${values[1]}" width="${values[2]}" height="${values[3]}" fill="#111111"/>` : '';
    svg = svg.replace(/<svg\b[^>]*>/i, opening => opening + description + background);
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + svg;
  }
  function downloadArtwork(art, dark) {
    if (!art || (art.full ? !art.art : !art.item.mark)) { toast('This artwork is not available in this draft.'); return; }
    triggerDownload(`${slug(art.filename)}${dark ? '-reverse' : ''}-DRAFT.svg`, svgFile(art, dark), 'image/svg+xml');
    toast('Editable draft SVG downloaded.');
  }
  function renderOverview() {
    const dark = state.mode === 'dark';
    $('#direction-overview').innerHTML = directions.map(direction => `<a class="overview-card" href="#direction-${esc(slug(direction.id))}" data-dark="${dark}"><div class="overview-art">${svgMark(direction, dark)}</div><div class="overview-caption"><span>${esc(direction.id)} / ${esc(direction.title)}</span><strong>${esc(direction.name)}</strong></div></a>`).join('');
    $$('[data-mode]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.mode === state.mode)));
  }
  function artCard(direction, kind, label, application) {
    const art = artworkFor(direction, kind);
    return `<figure class="art-card ${application ? 'application' : ''}"><figcaption><span>${esc(label)}</span><button type="button" data-inspect="${esc(direction.id)}" data-kind="${kind}" aria-label="Inspect ${esc(direction.name)} ${kind}">Inspect</button></figcaption><div class="full-artwork">${art && art.art ? artHtml(art, false) : ''}</div></figure>`;
  }
  function constructionPanel(direction) {
    return `<div class="construction-layout"><ol class="construction-list">${list(direction.construction).map(text => `<li>${esc(prose(text))}</li>`).join('')}</ol><div class="parts-grid">${list(direction.parts).map((part, index) => `<figure class="part-card"><div class="part-art">${svgMark({...part,name:part.label}, false)}</div><p>${esc(part.label)}</p></figure>`).join('')}</div></div><p class="panel-note">${esc(prose(direction.visible))}</p>`;
  }
  function sizesPanel(direction) {
    const isWordmark = direction.primaryType === 'wordmark';
    const compact = direction.compact;
    const sample = isWordmark ? compact : direction;
    const symbols = sample ? `<div class="size-sheet"><span class="small-label">${esc(isWordmark ? compact.label || 'Compact study / not the full name' : 'Symbol / actual CSS pixel sizes')}</span><div class="size-row">${[64,32,24,16].map(size => `<figure class="size-case"><div class="size-art" style="width:${size}px;height:${size}px">${svgMark({...sample,name:sample.name || sample.label || direction.name}, false)}</div><span>${size} px</span></figure>`).join('')}</div><p>${esc(isWordmark ? prose(compact.caution) : prose(direction.smallSize))}</p></div>` : `<div class="size-sheet"><span class="small-label">Full-name identity / practical limits</span><p class="wordmark-limit">A full-name wordmark cannot carry the parish name at 16 px. Read the complete name at practical widths alongside.</p><p>${esc(prose(direction.smallSize))}</p></div>`;
    return `<div class="size-layout">${symbols}<div class="size-sheet width-tests"><span class="small-label">Complete parish name / actual widths</span>${[320,240].map(width => `<figure class="name-width-case"><span>${width} px wide</span><div class="name-width-art" style="width:${width}px">${fullArtwork(direction.lockups && direction.lockups.horizontal, false, `${direction.name} / complete parish name at ${width} px`)}</div></figure>`).join('')}<p>${esc(isWordmark ? prose(direction.smallSize) : 'Full name at practical browser widths. Printing and fabrication still need material proofs.')}</p></div></div>`;
  }
  function pairingPanel(direction) {
    const rccg = data.rccg || {};
    return `<div class="rccg-layout"><div class="rccg-emblem"><div class="rccg-placeholder" role="img" aria-label="Official RCCG emblem missing. Reserved position only.">OFFICIAL RCCG<br>EMBLEM<br>ASSET NEEDED</div></div><span class="rccg-divider" aria-hidden="true"></span><div class="rccg-parish">${fullArtwork(direction.lockups && direction.lockups.horizontal, false, `${direction.name} / parish identity beside reserved emblem position`)}</div></div><p class="panel-note">${esc(prose(rccg.note) || 'Reservation only. The authorized official RCCG emblem is unavailable; this placeholder is not a reconstruction. Balance with the actual emblem remains untested.')}</p>`;
  }
  function sketchesPanel(direction) {
    const sketches = list(direction.sketches);
    return `<div class="sketches-heading"><h3>Exploratory constructions</h3><p>${sketches.length} distinct studies / same monochrome scale</p></div><div class="sketch-grid">${sketches.map((sketch, index) => `<article class="sketch-card"><button type="button" class="sketch-art" data-inspect="${esc(direction.id)}" data-kind="sketch" data-index="${index}" aria-label="Inspect ${esc(sketch.id)} ${esc(sketch.name)}"><span class="sketch-id">${esc(sketch.id)}</span>${svgMark(sketch,false)}<span class="sketch-inspect">Inspect drawing</span></button><div class="sketch-caption"><div class="sketch-name"><h4>${esc(sketch.name)}</h4>${sketch.selected ? '<span class="developed-tag">DEVELOPED FURTHER</span>' : ''}</div><p>${esc(prose(sketch.idea))}</p><details><summary>${sketch.selected ? 'Why it advances' : 'Why it pauses'}</summary><p>${esc(prose(sketch.reason))}</p></details><div class="sketch-actions"><button type="button" class="text-button" data-download="${esc(direction.id)}" data-kind="sketch" data-index="${index}" aria-label="Download ${esc(sketch.name)} draft SVG">SVG</button>${sketch.sourceFile ? `<a href="${esc(assetHref(sketch.sourceFile))}" download>Source drawing</a>` : ''}</div></div></article>`).join('')}</div>`;
  }
  function renderDirections() {
    $('#directions').innerHTML = directions.map(direction => {
      const id = slug(direction.id);
      const type = direction.type || {};
      const panels = [{id:'construction',label:'Construction',html:constructionPanel(direction)},{id:'sizes',label:'Small sizes',html:sizesPanel(direction)},{id:'applications',label:'In use',html:`<div class="applications-grid">${artCard(direction,'signage','Hypothetical wall sign / proportion study',true)}${artCard(direction,'paper','Hypothetical stationery / proportion study',true)}</div><p class="panel-note">Hypothetical identity studies. No actual premises, church events, or contact information are depicted.</p>`},{id:'rccg',label:'RCCG pairing',html:pairingPanel(direction)}];
      return `<section class="direction" id="direction-${esc(id)}" aria-labelledby="title-${esc(id)}"><div class="page-width"><header class="direction-heading"><div><p class="eyebrow">Direction ${esc(direction.id)} / ${esc(direction.title)}</p><h2 id="title-${esc(id)}">${esc(direction.name)}</h2><p class="idea">${esc(prose(direction.idea))}</p></div><button type="button" class="save-button" data-choice="${esc(direction.id)}" aria-pressed="${state.choices.has(String(direction.id))}">${state.choices.has(String(direction.id)) ? 'Kept for discussion' : 'Keep for discussion +'}</button></header><div class="main-proofs">${[false,true].map(dark => `<figure class="art-stage ${dark ? 'dark' : ''} ${direction.primaryType === 'wordmark' ? 'wordmark-stage' : ''}"><figcaption class="stage-top"><span>${dark ? 'Reversed / white on black' : 'Primary / black on white'}</span><span>${esc(direction.id)}</span></figcaption><div class="stage-art">${svgMark(direction,dark)}</div><div class="stage-bottom"><span>DRAFT — NOT FOR PUBLICATION</span><button type="button" data-inspect="${esc(direction.id)}" data-kind="primary" data-dark="${dark}">Inspect drawing</button></div></figure>`).join('')}</div><div class="meaning-row"><p class="meaning">${esc(prose(direction.meaning))}</p><p class="watch"><span class="small-label">Unintended reading to test</span>${esc(prose(direction.risk))}</p></div><div class="proof-heading"><h3>The complete name</h3><span class="eyebrow">Tabernacle of Praise</span></div><div class="lockup-grid">${artCard(direction,'horizontal','Horizontal / full parish name')}${artCard(direction,'stacked','Stacked / full parish name')}</div><div class="type-line"><p><strong>${esc(type.family)}</strong>${type.edits ? ` / ${esc(prose(type.edits))}` : ''}</p><details><summary>Type source &amp; license</summary><p>${esc(prose(type.license))}</p></details></div><div class="proof-tabs" role="tablist" aria-label="${esc(direction.name)} proof studies">${panels.map((panel,index) => `<button type="button" role="tab" id="tab-${id}-${panel.id}" aria-controls="panel-${id}-${panel.id}" aria-selected="${index === 0}" tabindex="${index === 0 ? '0' : '-1'}">${panel.label}</button>`).join('')}</div>${panels.map((panel,index) => `<div class="proof-panel" role="tabpanel" id="panel-${id}-${panel.id}" aria-labelledby="tab-${id}-${panel.id}" tabindex="0" ${index ? 'hidden' : ''}>${panel.html}</div>`).join('')}${sketchesPanel(direction)}<div class="direction-downloads"><button type="button" class="button" data-download="${esc(direction.id)}" data-kind="primary">${direction.primaryType === 'wordmark' ? 'Wordmark' : 'Symbol'} SVG</button><button type="button" class="button" data-download="${esc(direction.id)}" data-kind="primary" data-dark="true">Reverse SVG</button><button type="button" class="button" data-download="${esc(direction.id)}" data-kind="horizontal">Horizontal SVG</button><button type="button" class="button" data-download="${esc(direction.id)}" data-kind="stacked">Stacked SVG</button><button type="button" class="button" data-download="${esc(direction.id)}" data-kind="signage">Signage SVG</button><button type="button" class="button" data-download="${esc(direction.id)}" data-kind="paper">Paper SVG</button></div></div></section>`;
    }).join('');
  }
  function renderEvaluation() {
    const criteria = [['distinctiveness','Distinctive & memorable'],['nameConnection','Relationship to the name'],['integration','Tabernacle + Praise'],['churchSuitability','Christian church character'],['craft','Design craft'],['endurance','10–20 year relevance'],['smallScale','Small-scale use'],['monochrome','Without color'],['industryRisk','Industry associations'],['explainability','Explaining it to the congregation']];
    $('#evaluation-table').innerHTML = `<caption>Qualitative assessment of the developed artwork. No direction is approved or automatically preferred.</caption><thead><tr><th scope="col">Same questions,<br>five directions</th>${directions.map(direction => `<th scope="col"><span>${esc(direction.id)} / ${esc(direction.title)}</span>${esc(direction.name)}</th>`).join('')}</tr></thead><tbody>${criteria.map(([key,label]) => `<tr><th scope="row">${esc(label)}</th>${directions.map(direction => `<td>${esc(prose(direction.evaluation && direction.evaluation[key]))}</td>`).join('')}</tr>`).join('')}</tbody>`;
    $('#assessment').innerHTML = list(data.assessment).map(text => `<p>${esc(prose(text))}</p>`).join('');
    $('#source-list').innerHTML = list(data.sources).map(source => `<li><h3>${source.url ? `<a href="${esc(assetHref(source.url))}" target="_blank" rel="noopener noreferrer">${esc(source.title)}</a>` : esc(source.title)}</h3><p>${esc(prose(source.note))}</p></li>`).join('');
  }
  function syncChoices() {
    $$('[data-choice]').forEach(button => {
      const selected = state.choices.has(button.dataset.choice);
      button.setAttribute('aria-pressed', String(selected));
      button.textContent = selected ? 'Kept for discussion' : 'Keep for discussion +';
    });
    $$('#review-choices input').forEach(input => { input.checked = state.choices.has(input.value); });
  }
  function choose(id, selected) {
    if (!validIds.has(id)) return;
    if (selected) state.choices.add(id); else state.choices.delete(id);
    syncChoices(); persist(true);
  }
  function activateTab(tab, focus) {
    const tablist = tab.closest('[role="tablist"]');
    $$('[role="tab"]', tablist).forEach(item => {
      const active = item === tab;
      item.setAttribute('aria-selected', String(active));
      item.tabIndex = active ? 0 : -1;
      const panel = document.getElementById(item.getAttribute('aria-controls'));
      if (panel) panel.hidden = !active;
    });
    if (focus) tab.focus();
  }
  function paintDialog() {
    if (!dialogItem) return;
    $('#dialog-title').textContent = dialogItem.name;
    $('#dialog-art').innerHTML = artHtml(dialogItem, dialogDark);
    $('#dialog-art').dataset.dark = String(dialogDark);
    $('#dialog-caption').textContent = dialogItem.caption;
    $('#dialog-reverse').setAttribute('aria-pressed', String(dialogDark));
    $('#dialog-reverse').textContent = dialogDark ? 'Show black on white' : 'Reverse artwork';
  }
  function openDialog(art, dark, opener) {
    if (!art || (art.full ? !art.art : !art.item.mark)) return;
    dialogItem = art; dialogDark = !!dark; dialogOpener = opener || document.activeElement;
    paintDialog();
    const dialog = $('#art-dialog');
    if (typeof dialog.showModal === 'function') dialog.showModal();
    else { dialog.setAttribute('open',''); dialog.setAttribute('aria-modal','true'); }
    $('#close-dialog').focus();
  }
  function closeDialog() {
    const dialog = $('#art-dialog');
    if (typeof dialog.close === 'function' && dialog.open) dialog.close();
    else { dialog.removeAttribute('open'); restoreDialogFocus(); }
  }
  function restoreDialogFocus() {
    if (dialogOpener && document.contains(dialogOpener)) dialogOpener.focus();
    dialogOpener = null;
  }
  if (data.lead) $('#review-lead').textContent = prose(data.lead);
  renderOverview(); renderDirections(); renderEvaluation();
  $('#review-choices').innerHTML = directions.map(direction => `<label class="review-choice"><input type="checkbox" value="${esc(direction.id)}" ${state.choices.has(String(direction.id)) ? 'checked' : ''}><span>${esc(direction.id)} / ${esc(direction.name)}</span></label>`).join('');
  $('#review-notes').value = state.notes;
  document.addEventListener('click', event => {
    const button = event.target.closest('button');
    if (!button) return;
    if (button.dataset.mode) { state.mode = button.dataset.mode; renderOverview(); persist(false); }
    if (button.hasAttribute('data-choice')) choose(button.dataset.choice, !state.choices.has(button.dataset.choice));
    if (button.getAttribute('role') === 'tab') activateTab(button, false);
    if (button.hasAttribute('data-inspect')) openDialog(artworkFor(directionFor(button.dataset.inspect), button.dataset.kind, button.dataset.index), button.dataset.dark === 'true', button);
    if (button.hasAttribute('data-download')) downloadArtwork(artworkFor(directionFor(button.dataset.download), button.dataset.kind, button.dataset.index), button.dataset.dark === 'true');
  });
  document.addEventListener('keydown', event => {
    const tab = event.target.closest('[role="tab"]');
    if (!tab) return;
    const tabs = $$('[role="tab"]',tab.closest('[role="tablist"]'));
    const index = tabs.indexOf(tab);
    let next;
    if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
    if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
    if (event.key === 'Home') next = 0;
    if (event.key === 'End') next = tabs.length - 1;
    if (next !== undefined) { event.preventDefault(); activateTab(tabs[next],true); }
  });
  $('#review-choices').addEventListener('change', event => { if (event.target.matches('input[type="checkbox"]')) choose(event.target.value,event.target.checked); });
  $('#review-notes').addEventListener('input', event => {
    state.notes = event.target.value;
    clearTimeout(saveTimer); saveTimer = setTimeout(() => persist(true),250);
  });
  window.addEventListener('pagehide', () => persist(false));
  $('#feedback-form').addEventListener('submit', event => {
    event.preventDefault();
    state.notes = $('#review-notes').value;
    persist(true);
    const review = {project:'RCCG Tabernacle of Praise',study:'Creative Review 05',status:'DRAFT — NOT FOR PUBLICATION',createdAt:new Date().toISOString(),directionsToDiscuss:directions.filter(direction => state.choices.has(String(direction.id))).map(direction => ({id:direction.id,name:direction.name})),notes:state.notes,identityApproved:false,typographyApproved:false,colorApproved:false,publicationApproved:false};
    triggerDownload('tabernacle-of-praise-creative-review-05-notes.json',JSON.stringify(review,null,2),'application/json');
    toast('Review notes downloaded. No identity approval is recorded.');
  });
  $('#clear-feedback').addEventListener('click', () => {
    clearTimeout(saveTimer); state.choices.clear(); state.notes = '';
    $('#review-notes').value = ''; syncChoices(); persist(false);
    $('#save-status').textContent = 'Local notes cleared. Nothing has been submitted or approved.';
    toast('Local selections and notes cleared.');
  });
  $('#close-dialog').addEventListener('click',closeDialog);
  $('#art-dialog').addEventListener('close',restoreDialogFocus);
  $('#art-dialog').addEventListener('cancel',event => { event.preventDefault(); closeDialog(); });
  $('#art-dialog').addEventListener('click',event => {
    if (event.target !== $('#art-dialog')) return;
    const bounds = event.target.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) closeDialog();
  });
  $('#art-dialog').addEventListener('keydown',event => {
    if (event.key === 'Escape') { event.preventDefault(); closeDialog(); return; }
    if (event.key !== 'Tab') return;
    const controls = $$('button:not([disabled]), a[href], input:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])',$('#art-dialog')).filter(element => !element.hidden && element.getClientRects().length);
    if (!controls.length) { event.preventDefault(); return; }
    const first = controls[0], last = controls[controls.length - 1];
    if (event.shiftKey && (document.activeElement === first || !controls.includes(document.activeElement))) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && (document.activeElement === last || !controls.includes(document.activeElement))) { event.preventDefault(); first.focus(); }
  });
  $('#dialog-reverse').addEventListener('click',() => { dialogDark = !dialogDark; paintDialog(); });
  $('#dialog-download').addEventListener('click',() => downloadArtwork(dialogItem,dialogDark));
}());
