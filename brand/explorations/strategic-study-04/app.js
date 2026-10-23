(function () {
  'use strict';
  const data = window.TOPStudy;
  const $ = (query, root) => (root || document).querySelector(query);
  const $$ = (query, root) => Array.from((root || document).querySelectorAll(query));
  const escape = value => String(value == null ? '' : value).replace(/[&<>"']/g, character => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[character]));
  const list = value => Array.isArray(value) ? value : value ? [value] : [];
  const prose = value => Array.isArray(value) ? value.join(' ') : String(value || '');
  const slug = value => String(value || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  if (!data || !Array.isArray(data.concepts)) {
    $('#strategy-lead').innerHTML = '<span class="data-error">The study artwork could not load. Keep data.js beside this HTML file and open the complete project folder.</span>';
    return;
  }
  const concepts = data.concepts;
  const sketches = list(data.sketches);
  const territories = list(data.territories);
  const sources = list(data.sources);
  const storageKey = 'top-strategic-study-04-review';
  let saved = {};
  try { saved = JSON.parse(localStorage.getItem(storageKey) || '{}'); } catch (_) { saved = {}; }
  const validIds = new Set(concepts.map(concept => String(concept.id)));
  const state = {mode:saved.mode === 'dark' ? 'dark' : 'light', filter:'all', choices:new Set(list(saved.choices).map(String).filter(id => validIds.has(id))), notes:typeof saved.notes === 'string' ? saved.notes : ''};
  let dialogArtwork = null;
  let dialogReturnFocus = null;
  let toastTimer;
  let saveTimer;
  const territoryFor = id => territories.find(territory => String(territory.id) === String(id));
  const conceptFor = id => concepts.find(concept => String(concept.id) === String(id));
  const sourceFor = id => sources.find(source => String(source.id) === String(id));
  const viewBox = item => /^[-\d.\s]+$/.test(item && item.symbolViewBox || '') ? item.symbolViewBox : '0 0 256 256';
  const recolor = (art, dark) => String(art || '').replace(/#(?:000000|111111|000|111)(?![0-9a-f])/gi, '__TOP_INK__').replace(/#(?:ffffff|fff)(?![0-9a-f])/gi, '__TOP_PAPER__').replace(/(fill|stroke)=(['"])black\2/gi, '$1=$2__TOP_INK__$2').replace(/(fill|stroke)=(['"])white\2/gi, '$1=$2__TOP_PAPER__$2').replace(/__TOP_INK__/g, dark ? '#ffffff' : '#111111').replace(/__TOP_PAPER__/g, dark ? '#111111' : '#ffffff');
  const svgMark = (mark, title, dark, box) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${escape(box || '0 0 256 256')}" fill="${dark ? '#ffffff' : '#111111'}" role="img" aria-label="${escape(title)}"><title>${escape(title)} — DRAFT — NOT FOR PUBLICATION</title>${recolor(mark, dark)}</svg>`;
  const symbol = (item, dark) => svgMark(item.mark, item.name, dark, viewBox(item));
  const fullArtwork = (art, dark) => recolor(art, dark);
  function toast(message) {
    const element = $('#toast');
    element.textContent = message;
    element.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => element.classList.remove('show'), 2500);
  }
  function persist(announce) {
    try {
      localStorage.setItem(storageKey, JSON.stringify({version:1, mode:state.mode, choices:Array.from(state.choices), notes:state.notes}));
      if (announce) $('#save-status').textContent = 'Notes saved in this browser. No feedback has been submitted.';
    } catch (_) { $('#save-status').textContent = 'Browser storage is unavailable. Download your feedback to keep it.'; }
  }
  function triggerDownload(filename, contents, mime) {
    const url = URL.createObjectURL(new Blob([contents], {type:mime}));
    const link = document.createElement('a');
    link.href = url; link.download = filename;
    document.body.appendChild(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  function svgFile(mark, title, box, full) {
    const desc = `<desc>DRAFT — NOT FOR PUBLICATION. ${escape(title)}. Unapproved strategic identity exploration for RCCG Tabernacle of Praise.</desc>`;
    if (full) return '<?xml version="1.0" encoding="UTF-8"?>\n' + String(mark).replace(/<\?xml[^>]*\?>/gi,'').trim().replace(/<svg\b[^>]*>/, opening => opening + desc);
    return `<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="${escape(box || '0 0 256 256')}"><title>${escape(title)} — DRAFT</title>${desc}${mark}</svg>`;
  }
  function downloadArtwork(item, kind) {
    if (!item) return;
    let art = item.mark, full = false;
    if (kind === 'horizontal' || kind === 'stacked') { art = item.lockups && item.lockups[kind]; full = true; }
    if (kind === 'signage' || kind === 'paper') { art = item.applications && item.applications[kind]; full = true; }
    if (!art) { toast('That artwork is not available in this draft.'); return; }
    triggerDownload(`${slug(item.id)}-${slug(item.name)}-${item.primaryType === 'wordmark' && kind === 'symbol' ? 'wordmark' : kind || 'artwork'}-DRAFT.svg`, svgFile(art, item.name, viewBox(item), full), 'image/svg+xml');
    toast('Editable draft SVG downloaded.');
  }
  function sourceLinks(ids) {
    return list(ids).map(id => {
      const source = sourceFor(id);
      return source ? `<a href="#source-${escape(slug(id))}" aria-label="Source: ${escape(source.title)}">[${escape(id)}]</a>` : '';
    }).join('');
  }
  function renderFoundations() {
    const strategy = data.strategy || {};
    $('#strategy-lead').textContent = prose(strategy.lead);
    $('#strategy-principle').textContent = prose(strategy.principle);
    $('#research-findings').innerHTML = list(strategy.findings).map((finding,index) => `<article class="finding"><span class="finding-index">${String(index+1).padStart(2,'0')} / Research finding</span><h3>${escape(finding.title)}</h3><p>${escape(prose(finding.text))}</p><div class="citations">${sourceLinks(finding.sourceIds)}</div></article>`).join('');
    $('#territory-grid').innerHTML = territories.map(territory => `<article class="territory-card" id="territory-${escape(slug(territory.id))}"><header><span class="territory-letter">${escape(territory.id)}</span><h3>${escape(territory.title)}</h3></header><p>${escape(prose(territory.intent))}</p><p class="risk"><strong>Watch for:</strong> ${escape(prose(territory.risk))}</p></article>`).join('');
    $('#source-list').innerHTML = sources.map(source => `<li class="source-item" id="source-${escape(slug(source.id))}"><div><h3>${source.url ? `<a href="${escape(source.url)}" target="_blank" rel="noopener noreferrer">${escape(source.title)} <span aria-hidden="true" class="diagonal-arrow"></span></a>` : escape(source.title)}</h3><p>${escape(prose(source.note))}</p></div></li>`).join('');
    if (data.selectionNotes) $('#selection-notes').textContent = prose(data.selectionNotes);
    $('#sketch-count').textContent = `${sketches.length} initial ideas`;
  }
  function renderSketches() {
    $('#territory-filters').innerHTML = [{id:'all',title:'All ideas'}, ...territories].map(territory => `<button type="button" data-filter="${escape(territory.id)}" aria-pressed="${state.filter === String(territory.id)}">${territory.id === 'all' ? 'All ideas' : `${escape(territory.id)} / ${escape(territory.title)}`}</button>`).join('');
    const shown = sketches.filter(sketch => state.filter === 'all' || String(sketch.territory) === state.filter);
    $('#sketch-results').textContent = `${shown.length} of ${sketches.length} initial explorations${state.filter === 'all' ? ' / equal-scale monochrome studies' : ` / Territory ${state.filter}`}`;
    $('#sketch-grid').innerHTML = shown.map(sketch => `<article class="sketch-card ${sketch.decision === 'shortlisted' ? 'shortlisted' : ''}" id="sketch-${escape(slug(sketch.id))}"><button type="button" class="sketch-art" data-inspect-sketch="${escape(sketch.id)}" aria-label="Inspect ${escape(sketch.name)}"><span class="sketch-number">${escape(sketch.id)}</span>${symbol(sketch,false)}<span class="sketch-enlarge diagonal-arrow" aria-hidden="true"></span></button><div class="sketch-copy"><div class="sketch-meta"><span>Territory ${escape(sketch.territory)}</span><span>${sketch.decision === 'shortlisted' ? 'Develop further' : 'Set aside'}</span></div><h3>${escape(sketch.name)}</h3><p class="sketch-idea">${escape(prose(sketch.idea))}</p><p class="sketch-approach">${escape(prose(sketch.approach))}</p><div class="sketch-decision"><strong>${sketch.decision === 'shortlisted' ? 'Why it advances' : 'Why it pauses'}</strong>${escape(prose(sketch.reason))}</div></div></article>`).join('');
  }
  function lockupsPanel(concept) {
    const type = concept.type || {};
    return `<div class="lockup-grid">${['horizontal','stacked'].map(kind => `<figure class="lockup-proof"><figcaption class="proof-label"><span>${kind} / Full parish name</span><button type="button" data-download="${escape(concept.id)}" data-kind="${kind}" aria-label="Download ${escape(concept.name)} ${kind} SVG">SVG</button></figcaption><div class="full-artwork">${fullArtwork(concept.lockups && concept.lockups[kind],false)}</div></figure>`).join('')}</div><div class="type-note"><h4>Type direction<br><strong>${escape(type.family || 'Exploratory lettering')}</strong></h4><p>${escape(prose(type.rationale))}<span class="license">${escape(prose(type.license))}</span></p></div><div class="rccg-proof"><div class="rccg-placeholder">AUTHORIZED<br>RCCG EMBLEM<br>RESERVED<br>NOT SUPPLIED</div><div class="rccg-divider"></div><div class="rccg-parish">${fullArtwork(concept.lockups && concept.lockups.horizontal,false)}</div></div><p class="rccg-note">Layout reservation only. An authorized, unchanged RCCG emblem must be supplied before the official pairing can be assessed or approved.</p>`;
  }
  function constructionPanel(concept) {
    return `<div class="construction-layout"><ol class="construction-list">${list(concept.construction).map(text => `<li>${escape(prose(text))}</li>`).join('')}</ol><div class="parts-grid">${list(concept.parts).map(part => `<div class="part-card"><div class="part-art">${svgMark(part.mark,part.label,false,part.symbolViewBox || viewBox(concept))}</div><p>${escape(part.label)}</p></div>`).join('')}</div></div><p class="construction-footnote">The parts explain the drawing and its intended associations. They are not separate logos, hidden theological claims, or a claim that the form depicts historical tabernacle architecture.</p>`;
  }
  function sizesPanel(concept) {
    const compact = concept.compact;
    const testArtwork = compact ? {mark:compact.mark,name:compact.label || `${concept.name} / compact test`,symbolViewBox:compact.viewBox || compact.symbolViewBox || '0 0 256 256'} : concept;
    return `${compact ? `<div class="compact-note"><span class="small-label">${escape(compact.label || 'Separate compact study')}</span><p>${escape(prose(compact.caution || 'This compact form is an exploratory companion; it does not establish that the full parish name is legible at icon size.'))}</p></div>` : ''}<div class="size-proof"><div class="size-row">${[64,32,24,16].map(size => `<div class="size-case"><div class="size-art" style="width:${size}px;height:${size}px" data-size="${size}">${symbol(testArtwork,false)}</div><span>${size}px</span></div>`).join('')}</div><p class="size-caption">Actual CSS pixels${compact ? ' / compact companion only' : ''}. View at 100% browser zoom; gaps and silhouette must survive without enlarging the drawing.</p></div><div class="name-width-tests"><span class="small-label">Full parish name / practical width tests</span>${[320,240].map(width => `<div class="name-width-case"><span>${width}px wide</span><div class="name-width-art" style="width:${width}px" data-name-width="${width}">${fullArtwork(concept.lockups && concept.lockups.horizontal,false)}</div></div>`).join('')}<p>Actual CSS widths. Read the complete name without zooming. A compact companion is not a substitute for full-name readability.</p></div><div class="reverse-grid"><div class="reverse-card ${concept.primaryType === 'wordmark' ? 'wordmark-proof' : ''}">${symbol(concept,false)}<span>Positive / Black on white</span></div><div class="reverse-card dark ${concept.primaryType === 'wordmark' ? 'wordmark-proof' : ''}">${symbol(concept,true)}<span>Reversed / White on black</span></div></div><p class="application-note">${escape(prose(concept.smallSize || concept.risk))}</p>`;
  }
  function applicationsPanel(concept) {
    const applications = concept.applications || {};
    return `<div class="applications-grid">${[{id:'signage',label:'Illustrative building sign'},{id:'paper',label:'Simple printed identity'}].map(application => `<figure class="application-proof"><figcaption class="proof-label"><span>${application.label}</span><button type="button" data-download="${escape(concept.id)}" data-kind="${application.id}" aria-label="Download ${escape(concept.name)} ${application.label} SVG">SVG</button></figcaption><div class="full-artwork">${fullArtwork(applications[application.id],false)}</div></figure>`).join('')}</div><p class="application-note">Hypothetical monochrome applications test recognition and proportion. These are illustrative identity studies, not photographs of the parish, verified church premises, approved stationery, or publication templates.</p>`;
  }
  function renderConcepts() {
    $('#shortlist-overview').innerHTML = concepts.map(concept => `<a class="overview-card" href="#concept-${escape(slug(concept.id))}" data-overview="${escape(concept.id)}" data-dark="${state.mode === 'dark'}"><div class="overview-symbol">${symbol(concept,state.mode === 'dark')}</div><span class="overview-id">${escape(concept.id)}</span><span class="overview-name">${escape(concept.name)}</span></a>`).join('');
    $('#shortlisted-concepts').innerHTML = concepts.map((concept,index) => {
      const territory = territoryFor(concept.territory);
      const base = `concept-${slug(concept.id)}`;
      const tabs = [{id:'lockups',label:'Name & typography'},{id:'construction',label:'Construction'},{id:'sizes',label:'Size & reversal'},{id:'applications',label:'In context'}];
      return `<article class="concept" id="${escape(base)}" data-concept="${escape(concept.id)}"><header class="concept-title"><div><span class="concept-index">${String(index+1).padStart(2,'0')} / ${escape(concept.id)} / ${escape(territory ? territory.title : concept.territory)}</span><h3>${escape(concept.name)}</h3><p>${escape(prose(concept.idea))}</p></div><button type="button" class="save-concept" data-save="${escape(concept.id)}" aria-pressed="${state.choices.has(String(concept.id))}">${state.choices.has(String(concept.id)) ? 'Saved for review' : '+ Save for review'}</button></header><div class="concept-stage" data-dark="${state.mode === 'dark'}"><span class="stage-label">${escape(concept.id)} / ${concept.primaryType === 'wordmark' ? 'Wordmark' : 'Symbol'} study / Monochrome</span><div class="symbol-art ${concept.primaryType === 'wordmark' ? 'wordmark-art' : ''}">${symbol(concept,state.mode === 'dark')}</div><span class="stage-draft">DRAFT — NOT FOR PUBLICATION</span><button type="button" class="stage-inspect" data-inspect-concept="${escape(concept.id)}">Inspect drawing</button></div><div class="concept-summary"><div><span class="small-label">The name, made visible</span><p class="meaning-text">${escape(prose(concept.meaning))}</p></div><div><span class="small-label">What still needs proving</span><p class="risk">${escape(prose(concept.risk))}</p></div></div><div class="proof-tabs" role="tablist" aria-label="${escape(concept.name)} studies">${tabs.map((tab,tabIndex) => `<button type="button" role="tab" id="${escape(base)}-tab-${tab.id}" aria-selected="${tabIndex === 0}" aria-controls="${escape(base)}-panel-${tab.id}" tabindex="${tabIndex === 0 ? 0 : -1}" data-tab="${tab.id}">${tab.label}</button>`).join('')}</div>${tabs.map((tab,tabIndex) => `<div class="concept-panel" role="tabpanel" id="${escape(base)}-panel-${tab.id}" aria-labelledby="${escape(base)}-tab-${tab.id}" ${tabIndex === 0 ? '' : 'hidden'}>${tab.id === 'lockups' ? lockupsPanel(concept) : tab.id === 'construction' ? constructionPanel(concept) : tab.id === 'sizes' ? sizesPanel(concept) : applicationsPanel(concept)}</div>`).join('')}<div class="concept-actions"><button type="button" class="button button-dark" data-download="${escape(concept.id)}" data-kind="symbol">Download editable artwork</button><button type="button" class="button" data-download="${escape(concept.id)}" data-kind="horizontal">Horizontal SVG</button><button type="button" class="button" data-download="${escape(concept.id)}" data-kind="stacked">Stacked SVG</button></div></article>`;
    }).join('');
    $$('[data-mode]').forEach(button => button.setAttribute('aria-pressed',String(button.dataset.mode === state.mode)));
  }
  function renderEvaluation() {
    const criteria = [
      {label:'Connection to the name',get:concept => concept.meaning},
      {label:'Long-term recognition',get:concept => concept.longevity},
      {label:'Unresolved risk',get:concept => concept.risk},
      {label:'Small-scale test',get:concept => concept.smallSize || 'Inspect the actual 64 / 32 / 24 / 16px tests. Micro-size refinement remains open.'},
      {label:'RCCG compatibility',get:() => 'Separate emblem reservation shown. Authorized asset and official pairing still need review.'}
    ];
    $('#evaluation-table').innerHTML = `<caption>Qualitative comparison for discussion; no numeric score or final ranking is implied.</caption><thead><tr><th scope="col">What to consider</th>${concepts.map(concept => `<th scope="col">${escape(concept.id)}<br>${escape(concept.name)}</th>`).join('')}</tr></thead><tbody>${criteria.map(criterion => `<tr><th scope="row">${criterion.label}</th>${concepts.map(concept => `<td>${escape(prose(criterion.get(concept)))}</td>`).join('')}</tr>`).join('')}</tbody>`;
    $('#review-choices').innerHTML = concepts.map(concept => `<label class="review-choice"><input type="checkbox" value="${escape(concept.id)}" ${state.choices.has(String(concept.id)) ? 'checked' : ''}><span>${escape(concept.id)} / ${escape(concept.name)}</span></label>`).join('');
    $('#review-notes').value = state.notes;
  }
  function syncChoices() {
    $$('[data-save]').forEach(button => { const selected = state.choices.has(button.dataset.save); button.setAttribute('aria-pressed',String(selected)); button.textContent = selected ? 'Saved for review' : '+ Save for review'; });
    $$('#review-choices input').forEach(input => { input.checked = state.choices.has(input.value); });
  }
  function toggleChoice(id, force) {
    if (!validIds.has(String(id))) return;
    const selected = typeof force === 'boolean' ? force : !state.choices.has(String(id));
    if (selected) state.choices.add(String(id)); else state.choices.delete(String(id));
    syncChoices(); persist(true);
    toast(selected ? 'Saved for the next conversation. No approval recorded.' : 'Removed from your review shortlist.');
  }
  function setMode(mode) {
    state.mode = mode;
    $$('[data-mode]').forEach(button => button.setAttribute('aria-pressed',String(button.dataset.mode === mode)));
    $$('.concept').forEach(element => {
      const concept = conceptFor(element.dataset.concept);
      $('.concept-stage',element).dataset.dark = String(mode === 'dark');
      $('.symbol-art',element).innerHTML = symbol(concept,mode === 'dark');
    });
    $$('[data-overview]').forEach(element => {
      element.dataset.dark = String(mode === 'dark');
      $('.overview-symbol',element).innerHTML = symbol(conceptFor(element.dataset.overview),mode === 'dark');
    });
    persist(false);
  }
  function setTab(button, focus) {
    const article = button.closest('.concept');
    $$('[role=tab]',article).forEach(tab => { const selected = tab === button; tab.setAttribute('aria-selected',String(selected)); tab.tabIndex = selected ? 0 : -1; });
    $$('.concept-panel',article).forEach(panel => { panel.hidden = panel.id !== button.getAttribute('aria-controls'); });
    if (focus) button.focus();
  }
  function inspect(item, sketch) {
    dialogArtwork = item;
    dialogReturnFocus = document.activeElement;
    const dark = !sketch && state.mode === 'dark';
    $('#dialog-title').textContent = `${item.id} / ${item.name}`;
    $('#dialog-art').innerHTML = symbol(item,dark);
    $('#dialog-art').dataset.dark = String(dark);
    $('#dialog-caption').textContent = prose(item.meaning || item.idea) + (item.risk ? ` Open question: ${prose(item.risk)}` : ' Initial exploration, not a developed or approved identity.');
    $('#art-dialog').showModal();
  }
  document.addEventListener('click', event => {
    const button = event.target.closest('button');
    if (!button) return;
    if (button.dataset.filter) { state.filter = button.dataset.filter; renderSketches(); }
    if (button.dataset.mode) setMode(button.dataset.mode);
    if (button.dataset.save) toggleChoice(button.dataset.save);
    if (button.dataset.tab) setTab(button,false);
    if (button.dataset.download) downloadArtwork(conceptFor(button.dataset.download),button.dataset.kind);
    if (button.dataset.inspectSketch) inspect(sketches.find(sketch => String(sketch.id) === button.dataset.inspectSketch),true);
    if (button.dataset.inspectConcept) inspect(conceptFor(button.dataset.inspectConcept),false);
  });
  document.addEventListener('keydown', event => {
    const dialog = $('#art-dialog');
    if (event.key === 'Tab' && dialog.open) {
      const focusable = $$('button:not([disabled]),a[href],input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])',dialog).filter(element => element.getClientRects().length > 0);
      const first = focusable[0];
      const last = focusable[focusable.length-1];
      if (first && event.shiftKey && (document.activeElement === first || !dialog.contains(document.activeElement))) {
        event.preventDefault(); last.focus();
      } else if (first && !event.shiftKey && (document.activeElement === last || !dialog.contains(document.activeElement))) {
        event.preventDefault(); first.focus();
      }
      return;
    }
    const tab = event.target.closest('[role=tab]');
    if (!tab || !['ArrowLeft','ArrowRight','Home','End'].includes(event.key)) return;
    event.preventDefault();
    const tabs = $$('[role=tab]',tab.closest('[role=tablist]'));
    const index = tabs.indexOf(tab);
    const next = event.key === 'Home' ? 0 : event.key === 'End' ? tabs.length-1 : (index + (event.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
    setTab(tabs[next],true);
  });
  $('#close-dialog').addEventListener('click',() => $('#art-dialog').close());
  $('#art-dialog').addEventListener('close',() => { if (dialogReturnFocus && dialogReturnFocus.isConnected) dialogReturnFocus.focus(); });
  $('#art-dialog').addEventListener('click',event => { if (event.target === $('#art-dialog')) { const bounds = $('#art-dialog').getBoundingClientRect(); if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) $('#art-dialog').close(); } });
  $('#dialog-download').addEventListener('click',() => downloadArtwork(dialogArtwork,'symbol'));
  $('#review-choices').addEventListener('change',event => { if (event.target.matches('input')) toggleChoice(event.target.value,event.target.checked); });
  $('#review-notes').addEventListener('input',event => { state.notes = event.target.value; clearTimeout(saveTimer); saveTimer = setTimeout(() => persist(true),300); });
  $('#feedback-form').addEventListener('submit',event => {
    event.preventDefault(); persist(false);
    const feedback = {study:'RCCG Tabernacle of Praise — Strategic Identity Study 04',status:'DRAFT — NOT FOR PUBLICATION',identityApproved:false,selectedForFurtherReview:Array.from(state.choices).map(id => ({id,name:conceptFor(id).name})),notes:state.notes,decisionsStillOpen:['Logo direction','Geometry refinement','Typeface','Color palette','Authorized RCCG emblem pairing']};
    triggerDownload('tabernacle-strategic-study-04-feedback.json',JSON.stringify(feedback,null,2)+'\n','application/json');
    $('#save-status').textContent = 'Feedback file downloaded. Share it when you are ready; no identity has been approved.';
  });
  $('#clear-feedback').addEventListener('click',() => { state.choices.clear(); state.notes = ''; $('#review-notes').value = ''; syncChoices(); persist(false); $('#save-status').textContent = 'Local review notes cleared.'; toast('Local review notes cleared.'); });
  renderFoundations(); renderSketches(); renderConcepts(); renderEvaluation();
  if (state.notes || state.choices.size) $('#save-status').textContent = 'Your previous local notes have been restored. No feedback has been submitted.';
  if ('IntersectionObserver' in window) {
    const sections = $$('.section');
    const observer = new IntersectionObserver(entries => { entries.forEach(entry => { if (entry.isIntersecting) $$('.side-nav nav a').forEach(link => link.classList.toggle('active',link.getAttribute('href') === '#'+entry.target.id)); }); },{rootMargin:'-10% 0px -70% 0px',threshold:0});
    sections.forEach(section => observer.observe(section));
  }
  window.TOPStudyUI = {getState:() => ({mode:state.mode,filter:state.filter,choices:Array.from(state.choices),notes:state.notes}),downloadArtwork,recolor};
}());
