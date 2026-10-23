/*
 * RCCG Tabernacle of Praise — editable application studies.
 * DRAFT — NOT FOR PUBLICATION. No event, palette, logo or type approval implied.
 * Classic script; no dependencies, external artwork, images or network fonts.
 * All four layouts use the same 256-unit symbol size and shared wordmark treatment.
 */
(function () {
  'use strict';

  const SANS = "'Study Sans', 'Noto Sans', Arial, sans-serif";
  const SERIF = "'Study Serif', 'Noto Serif', Georgia, serif";
  const DRAFT = 'DRAFT — NOT FOR PUBLICATION';
  let nextId = 0;

  function esc(value) {
    return String(value == null ? '' : value).replace(/[&<>"']/g, function (character) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;' }[character];
    });
  }

  function hex(value, fallback) {
    return /^#[0-9a-f]{6}$/i.test(String(value)) ? value : fallback;
  }

  function text(x, y, content, size, color, options) {
    const config = options || {};
    return '<text x="' + x + '" y="' + y + '" fill="' + color + '" font-family="' + esc(config.serif ? SERIF : SANS) + '" font-size="' + size + '" font-weight="' + (config.weight || 400) + '"' + (config.tracking ? ' letter-spacing="' + config.tracking + '"' : '') + (config.anchor ? ' text-anchor="' + config.anchor + '"' : '') + '>' + esc(content) + '</text>';
  }

  function rect(x, y, width, height, color, attributes) {
    return '<rect x="' + x + '" y="' + y + '" width="' + width + '" height="' + height + '" fill="' + color + '"' + (attributes ? ' ' + attributes : '') + '/>';
  }

  function line(x1, y1, x2, y2, color, width) {
    return '<path d="M' + x1 + ' ' + y1 + 'H' + x2 + '" fill="none" stroke="' + color + '" stroke-width="' + (width || 1) + '"/>';
  }

  function symbol(mark, x, y, size, color) {
    // The established source geometries remain intact, including B's string gaps.
    const recolored = String(mark || '').replace(/#000000/gi, color).replace(/\s+id="[^"]*"/g, '');
    return '<g transform="translate(' + x + ' ' + y + ') scale(' + size / 256 + ')">' + recolored + '</g>';
  }

  function lockup(context, x, y, size, fontSize) {
    const baseline = y + size * 0.35;
    const left = x + size + size * 0.28;
    return symbol(context.mark, x, y, size, context.ink) +
      text(left, baseline, 'Tabernacle', fontSize, context.ink, { weight: 500 }) +
      text(left, baseline + fontSize * 1.19, 'of Praise', fontSize, context.ink, { weight: 500 });
  }

  function footer(context, width, y, details) {
    return line(72, y - 31, width - 72, y - 31, context.ink, 1) +
      text(72, y, DRAFT, 15, context.ink, { tracking: 1.2, weight: 600 }) +
      text(width - 72, y, details || 'LOGO + COLOR STUDY', 13, context.ink, { anchor: 'end', tracking: 1 });
  }

  function flyer(c) {
    return rect(0, 0, 1080, 1350, c.paper) +
      // The rail is architectural composition, not a proposed new logo motif.
      rect(792, 0, 288, 1174, c.ink) +
      rect(1056, 0, 24, 1174, c.secondary) +
      lockup(c, 72, 66, 88, 35) +
      text(72, 218, 'RCCG · ISTANBUL, TÜRKİYE', 18, c.ink, { tracking: 1.8 }) +
      rect(72, 320, 72, 5, c.accent) +
      text(72, 411, 'SERVICE INVITATION', 19, c.ink, { tracking: 3, weight: 500 }) +
      text(66, 562, 'Sunday', 136, c.ink, { serif: true }) +
      text(66, 711, 'Worship', 136, c.ink, { serif: true }) +
      symbol(c.mark, 806, 459, 245, c.paper) +
      line(72, 831, 712, 831, c.ink, 1) +
      text(72, 895, '[DATE]', 31, c.ink, { weight: 500 }) +
      text(400, 895, '[TIME]', 31, c.ink, { weight: 500 }) +
      text(72, 931, 'DATE PLACEHOLDER', 13, c.ink, { tracking: 1.4 }) +
      text(400, 931, 'TIME PLACEHOLDER', 13, c.ink, { tracking: 1.4 }) +
      text(72, 1015, '[VENUE]', 31, c.ink, { weight: 500 }) +
      text(72, 1051, 'VENUE PLACEHOLDER', 13, c.ink, { tracking: 1.4 }) +
      text(72, 1131, 'Redeemed Christian Church of God', 19, c.ink) +
      footer(c, 1080, 1278, 'SERVICE DETAILS UNCONFIRMED');
  }

  function instagram(c) {
    return rect(0, 0, 1080, 1080, c.paper) +
      lockup(c, 72, 62, 88, 35) +
      text(1008, 91, 'RCCG', 18, c.ink, { anchor: 'end', tracking: 2.2, weight: 500 }) +
      text(1008, 121, 'ISTANBUL', 15, c.ink, { anchor: 'end', tracking: 1.6 }) +
      rect(72, 234, 72, 5, c.accent) +
      text(72, 312, 'SUNDAY WORSHIP', 19, c.ink, { tracking: 3, weight: 500 }) +
      text(66, 455, '[SERVICE', 111, c.ink, { serif: true }) +
      text(66, 582, 'THEME]', 111, c.ink, { serif: true }) +
      text(74, 648, 'THEME PLACEHOLDER', 15, c.ink, { tracking: 1.8 }) +
      rect(72, 726, 936, 189, c.ink) +
      rect(984, 726, 24, 189, c.secondary) +
      symbol(c.mark, 766, 747, 145, c.paper) +
      text(108, 792, '[DATE]  /  [TIME]', 25, c.paper, { weight: 500 }) +
      text(108, 838, '[VENUE]', 25, c.paper, { weight: 500 }) +
      text(108, 878, 'EVENT DETAILS ARE PLACEHOLDERS', 12, c.paper, { tracking: 1.1 }) +
      footer(c, 1080, 1010, 'RCCG TABERNACLE OF PRAISE');
  }

  function avatar(c) {
    return rect(0, 0, 512, 512, c.paper) +
      // The avatar tests the entire existing mark; no crop or simplified strings.
      symbol(c.mark, 100, 92, 312, c.ink) +
      rect(232, 443, 48, 4, c.accent) +
      text(256, 484, 'DRAFT', 15, c.ink, { anchor: 'middle', tracking: 3, weight: 500 });
  }

  function signage(c) {
    // A flat vector elevation, explicitly not a photograph of the actual premises.
    return rect(0, 0, 1400, 840, c.paper) +
      line(0, 140, 1400, 140, c.ink, 1) +
      line(0, 645, 1400, 645, c.ink, 1) +
      '<path d="M126 140V645M1274 140V645" fill="none" stroke="' + c.ink + '" stroke-width="1"/>' +
      rect(184, 203, 1032, 378, c.ink) +
      rect(184, 561, 1032, 20, c.secondary) +
      symbol(c.mark, 248, 272, 216, c.paper) +
      text(520, 337, 'Tabernacle', 67, c.paper, { weight: 500 }) +
      text(520, 415, 'of Praise', 67, c.paper, { weight: 500 }) +
      rect(522, 456, 52, 4, c.accent) +
      text(596, 468, 'RCCG · ISTANBUL, TÜRKİYE', 20, c.paper, { tracking: 1.2 }) +
      text(72, 707, 'ILLUSTRATIVE FACADE — NOT THE ACTUAL CHURCH PREMISES', 16, c.ink, { tracking: 1.1 }) +
      footer(c, 1400, 784, 'AUTHORIZED RCCG EMBLEM STILL REQUIRED');
  }

  const layouts = {
    flyer: { width: 1080, height: 1350, draw: flyer, label: 'Sunday service flyer' },
    instagram: { width: 1080, height: 1080, draw: instagram, label: 'Instagram post' },
    avatar: { width: 512, height: 512, draw: avatar, label: 'Social media avatar' },
    signage: { width: 1400, height: 840, draw: signage, label: 'Illustrative church signage' }
  };

  function render(options) {
    const request = options || {};
    const layout = layouts[request.type] || layouts.flyer;
    const palette = request.palette || {};
    const concept = request.concept || {};
    const primary = hex(palette.primary, '#142838');
    const neutral = hex(palette.neutral, '#F6F2E9');
    const dark = request.mode === 'dark';
    const context = {
      paper: dark ? primary : neutral,
      ink: dark ? neutral : primary,
      secondary: hex(palette.secondary, '#B7A37B'),
      accent: hex(palette.accent, '#B88B46'),
      mark: concept.mark
    };
    const id = 'top-application-' + (++nextId);
    const title = concept.name + ' · ' + palette.name + ' · ' + layout.label + ' · draft';
    const description = 'DRAFT — NOT FOR PUBLICATION. Editable color application study. All service details in square brackets are placeholders. The typeface is a provisional common specimen, not an approved typography system. The official RCCG emblem is not reproduced. No logo, palette, service facts or publication is approved.';
    return '<svg xmlns="http://www.w3.org/2000/svg" width="' + layout.width + '" height="' + layout.height + '" viewBox="0 0 ' + layout.width + ' ' + layout.height + '" role="img" aria-labelledby="' + id + '-title ' + id + '-desc"><title id="' + id + '-title">' + esc(title) + '</title><desc id="' + id + '-desc">' + esc(description) + '</desc>' + layout.draw(context) + '</svg>';
  }

  window.TOPApplications = { render: render };
}());
