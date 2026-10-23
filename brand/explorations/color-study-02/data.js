/* Draft comparison data. Edit these values to make another study; none are approved standards. */
window.TOPData = {
  title: 'Tabernacle of Praise',
  status: 'DRAFT — NOT FOR PUBLICATION',
  palettes: [
    { id: 'navy', number: '01', name: 'Navy & gold', family: 'Navy + Gold + Ivory', mood: 'Timeless · elegant · dignified', primary: '#14263D', secondary: '#946B2E', accent: '#C9A467', neutral: '#F6F1E8', recommended: true,
      names: { primary: 'Midnight navy', secondary: 'Antique gold', accent: 'Pale warm gold', neutral: 'Ivory' },
      note: 'A dignified, dependable foundation. The familiar church and luxury associations place more responsibility on the mark to feel distinctive.',
      print: 'Strong dark-on-light reproduction. Gold is a flat screen color here; foil or metallic ink would be a separate material decision.' },
    { id: 'forest', number: '02', name: 'Forest & cream', family: 'Forest Green + Warm Gold + Cream', mood: 'Welcoming · calm · grounded', primary: '#1C3D32', secondary: '#8B6838', accent: '#C2A069', neutral: '#F5F0E4', recommended: false,
      names: { primary: 'Deep forest', secondary: 'Warm bronze', accent: 'Warm gold', neutral: 'Cream' },
      note: 'Warm and grounded, with a generous feeling of welcome. It can lean toward heritage, nature, or hospitality rather than a distinctive contemporary church.',
      print: 'A useful everyday one-color foundation. Proof cream papers and dark green inks together; screen warmth is not a paper specification.' },
    { id: 'teal', number: '03', name: 'Teal & sand', family: 'Deep Teal + Sand + Soft Gold', mood: 'Contemporary · refined · distinctive', primary: '#10494C', secondary: '#D9CBB4', accent: '#B69255', neutral: '#F6F3EC', recommended: true,
      names: { primary: 'Deep teal', secondary: 'Sand', accent: 'Soft gold', neutral: 'Warm porcelain' },
      note: 'The strongest balance of contemporary distinction and tactile warmth. Sand softens the cool foundation, while gold adds a measured ceremonial note.',
      print: 'Test teal on the intended stock and sign material. Sand works as a supporting surface with dark teal type; it is not a text color on porcelain.' },
    { id: 'burgundy', number: '04', name: 'Burgundy & stone', family: 'Burgundy + Muted Gold + Light Stone', mood: 'Warm · expressive · ceremonial', primary: '#562C3B', secondary: '#96784D', accent: '#C7AA7D', neutral: '#F1EDE5', recommended: false,
      names: { primary: 'Deep burgundy', secondary: 'Muted gold', accent: 'Champagne gold', neutral: 'Light stone' },
      note: 'Expressive and ceremonial, with an intimate warmth. It feels more solemn than the other options; potentially useful seasonal territory.',
      print: 'Deep burgundy can gain density in print. Proof it on the real stock; keep small text on the high-contrast primary/neutral pair.' },
    { id: 'charcoal', number: '05', name: 'Charcoal & copper', family: 'Charcoal + Ivory + Copper Accent', mood: 'Sophisticated · minimal · versatile', primary: '#282C32', secondary: '#616A74', accent: '#C78362', neutral: '#F5F0E8', recommended: false,
      names: { primary: 'Warm charcoal', secondary: 'Slate', accent: 'Muted copper', neutral: 'Soft ivory' },
      note: 'The most neutral and versatile system. Copper supplies warmth; recognition depends heavily on the symbol and wordmark rather than the hue.',
      print: 'A practical signage and monochrome foundation. Copper is a flat accent, not a promise of a metallic finish.' }
  ],
  concepts: [
    { id: 'B', name: 'Sanctuary Strings', category: 'Instrument-led',
      description: 'A protective sweep becomes a harp: a direct, expressive reading of praise and music.',
      caution: 'Its musical emphasis can suggest a choir or worship ministry. At 16px, the individual strings begin to merge; color does not repair that geometry.',
      mark: '<g fill="#000000"><path fill-rule="evenodd" d="M24 20 C70 16 88 72 130 124 C158 158 200 166 214 196 L232 232 H44 V104 C44 78 38 68 24 64 Z M58 52 C78 106 62 188 84 216 H58 Z M76 66 C102 136 92 188 120 216 H94 Z M104 96 C126 142 184 174 162 202 C156 212 150 216 134 216 C116 194 112 144 104 96 Z"/></g>' },
    { id: 'C', name: 'Praise Ligature', category: 'Name-led',
      description: 'A sculpted T and nested P make the name the identifier, with a spacious counter and related contours.',
      caution: 'The terminals feel more editorial and classical than purely modern. The T/P channel still needs small-size refinement; the sanctuary reference is indirect.',
      mark: '<g fill="#000000"><path d="M20 34 H236 C232 46 220 54 204 54 H158 C138 54 126 72 126 94 V222 H80 C92 214 94 204 94 186 V66 H72 C48 66 32 70 28 86 C28 62 24 46 20 34 Z"/><path d="M144 70 H168 C210 70 232 92 232 118 C232 148 208 158 184 166 C160 174 146 188 146 204 C146 212 152 218 160 222 H144 Z M160 86 V168 C176 152 194 148 194 118 C194 100 182 86 160 86 Z" fill-rule="evenodd"/></g>' },
    {"id": "D", "name": "Resonant Sanctuary", "category": "Space + rhythm", "description": "Folded contours define a shared interior, then open into a rising rhythm: dwelling and praise in one abstract structure.", "caution": "The rising bands may read as leaves or growth. The shared-room association is abstract, and the fine seams need small-size and material testing.", "mark": "<g fill=\"#000000\" transform=\"translate(-7 0)\"><path d=\"M48 212 C38 226 44 236 60 236 H170 C204 236 220 218 220 184 V156 C209 162 193 167 184 175 C177 182 178 188 176 194 C174 201 170 204 164 204 H72 C60 204 54 208 48 212 Z\"/><path d=\"M32 92 C24 98 24 106 24 120 V202 C24 216 30 226 40 232 C34 218 50 204 60 196 V120 C60 108 50 100 42 96 C38 94 34 92 32 92 Z\"/><path d=\"M24 84 C28 68 42 56 60 56 H152 C172 56 184 68 184 84 V92 H92 C72 92 56 78 40 78 C34 78 28 80 24 84 Z\"/><path d=\"M190 86 V62 C190 44 218 36 234 20 V46 C234 64 202 66 190 86 Z\"/><path d=\"M188 122 V102 C188 84 218 78 246 52 V80 C246 98 202 102 188 122 Z\"/><path d=\"M192 160 V142 C192 122 222 116 232 104 V128 C232 144 200 144 192 160 Z\"/></g>"}
  ]
};

// Literal reading, intended association, and limitations remain separate.
window.TOPData.meanings = {
  B: { labels: ['Harp-like outline', 'Negative openings', 'Combined mark'], operation: '−', visible: 'A harp-like silhouette and a rhythm of strings: musical praise is the clearest reading.', intended: 'The enclosing curve was intended as shelter. A tabernacle is not yet clear in the drawing.', limit: 'Music may suggest a choir rather than the whole parish. The three openings are a compositional choice, with no approved theological meaning.' },
  C: { labels: ['T / Tabernacle', 'P / Praise', 'Nested T + P'], operation: '+', visible: 'The T and P identify Tabernacle of Praise through its initials.', intended: 'A broad head and spacious counter were intended to suggest room and shelter. Sanctuary and worship remain indirect associations.', limit: 'The white channel keeps the letters separate; it is not a hidden religious symbol. It needs refinement at small sizes.' },
  D: { labels: ['Enclosing folds', 'Rising rhythm', 'Space + praise'], operation: '+', visible: 'Folded forms surround a shared interior, with an open edge that rises in a repeated rhythm.', intended: 'The protected interior explores dwelling and gathering; the rising bands explore collective praise. These are creative associations, not official doctrine.', limit: 'The bands may suggest leaves or growth. The sanctuary reading is abstract, and the fine seams need small-size testing.' }
};
