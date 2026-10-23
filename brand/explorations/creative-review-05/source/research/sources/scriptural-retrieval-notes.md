# Scriptural source retrieval notes

**DRAFT — NOT FOR PUBLICATION.** Retrieved 17 October 2026.

## Retrieved evidence

The selected verse data in [scriptural-excerpts.json](scriptural-excerpts.json) records source URLs, HTTP status, UTC retrieval time, the SHA-256 hash of each full source response, and the cited verse text. It stores selected verses rather than a downloaded whole Bible. Verse sections were joined in section-number order and repeated whitespace was collapsed; words and punctuation were not rewritten.

The World English Bible is a public-domain translation. Its text was obtained through a third-party mirror that identifies the translation and links to eBible:

- <https://raw.githubusercontent.com/TehShrike/world-english-bible/master/readme.md> — HTTP 200; describes the repository as a programmatic version of the World English Bible.
- <https://raw.githubusercontent.com/TehShrike/world-english-bible/master/json/exodus.json> — HTTP 200.
- <https://raw.githubusercontent.com/TehShrike/world-english-bible/master/json/numbers.json> — HTTP 200.
- <https://raw.githubusercontent.com/TehShrike/world-english-bible/master/json/psalms.json> — HTTP 200.
- <https://raw.githubusercontent.com/TehShrike/world-english-bible/master/json/hebrews.json> — HTTP 200.

This is mirror verification, not a claim to have checked the publisher's current edition in this session. Only verse text was extracted. The mirror's programming code was not copied; its `package.json` identifies that code as `UNLICENSED`, which is separate from the public-domain status of the underlying WEB text.

The five requested passages were also checked against <https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_web.json> (HTTP 200). Its [README](https://raw.githubusercontent.com/thiagobodruk/bible/master/README.md) identifies `en_web` as World English Bible (American Edition) and warns that crawled source files can contain encoding and syntax problems. The same core wording was found, but its punctuation spacing is noisy, so no quotation was copied from that source. The repository's MIT license does not override any translation owner's rights; it was not used as evidence for the licensing of other translations.

## Blocked publisher and comparison access

The following requests failed with `Tunnel connection failed: 403 Forbidden` at the environment's network proxy:

- <https://ebible.org/engwebp/EXO25.htm>
- <https://ebible.org/engwebp/EXO40.htm>
- <https://ebible.org/engwebp/PSA100.htm>
- <https://ebible.org/engwebp/PSA150.htm>
- <https://ebible.org/engwebp/HEB09.htm>
- <https://ebible.org/engwebp/copyright.htm>
- <https://ebible.org/web/EXO25.htm>
- <https://www.biblegateway.com/passage/?search=Exodus%2025%3A8&version=WEB>
- <https://biblehub.com/web/exodus/25.htm>
- <https://bible-api.com/exodus%2025:8?translation=web>

These failed addresses are retrieval records, not evidence claimed to have been read. Missing publisher access was worked around by retrieving and checking the named translation through available mirrors. Source response hashes allow the local evidence to be distinguished from future edits to the mirror's `master` branch.

## Review limits

No Hebrew or Greek lexical study, manuscript comparison, archaeological dating, or official RCCG doctrinal review was conducted. Architectural descriptions are statements about the biblical text, not confirmation of an excavated structure. Creative implications are explicitly labeled as interpretations. Any Scripture used in future public-facing materials should follow the church's preferred approved translation and be checked again before publication.
