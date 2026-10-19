# Color application studies — Review 10

**DRAFT — NOT FOR PUBLICATION.** Teal and navy are two provisional color families for comparison. No logo, palette, typography or publishing template is approved.

Each family applies Shared Rhythm and Open Praise to the same four contexts, with identical placements and copy:

- Imagined entrance proportion diagram; no actual church premises or fabrication specification.
- Editable A4 correspondence layout; `[CORRESPONDENCE TEXT]` and `[CONTACT DETAILS]` remain placeholders.
- Square welcome identity post; no date, event or service schedule is invented.
- Avatar and profile study; `[CHURCH HANDLE]` is a placeholder. Primary contours remain in normal avatars; the smaller dark avatar contexts use ivory ink for stronger contrast.

The actual outlined symbols and names are embedded from the current colored masters. Their source paths and SHA-256 values are recorded in [manifest.json](manifest.json). Smaller avatars embed the dedicated high-contrast ivory primary master, retaining the primary drawing rather than enlarging a compact symbol. Application builders do not modify the source contours or fills.

Main text uses the checked primary/neutral pair. Gold is a restrained flat-color accent; teal's soft gold is reserved for a large symbol or decoration rather than small text. No material, metallic finish or paper stock is specified. The original authorized RCCG emblem is absent and is not recreated; only verified textual affiliation is shown.

Open [teal applications](applications-teal.png) or [navy applications](applications-navy.png). The sixteen application SVGs and the two comparison-board SVGs remain editable. Supporting labels are outlined Instrument Sans 450; the parish wordmark retains the existing Review 09 Instrument Sans 470 contours. Original font and license remain in the preserved Review 09 type study.

Rebuild after `../exports/artwork.json` exists:

```sh
python3 applications/build.py
```

The builder reuses rendering and outlined-label utilities from the preserved `identity-development-09/applications/build.py`; it never changes that study or its artwork.
