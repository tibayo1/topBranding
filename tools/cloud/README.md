# Cloud setup records

These files retain the installation and startup instructions prepared during environment onboarding:

- `install-logo-design.sh`: installs upstream `kaankiziltug/logo-design-skill` at revision `0ecf52e9a4b3ac92b714f7cc6e3148ab8c774134`, preserving different existing skill contents, and checks the catalog, search, and PNG rendering.
- `start-instructions.md`: startup and skill-discovery guidance saved in the environment configuration draft.

The installation is also vendored in `.agents/skills/logo-design/`, including its MIT license and logo-library trademark notice. A clone can discover that project skill without downloading the upstream repository again.

The installer records the tested cloud checkout location `/workspace/topBranding`. Python 3, Git, and an SVG renderer are needed for its checks; Inkscape and Chromium were present in the prepared image. Geometry-builder scripts use the installed skill's Python helpers; the comparison lettering builder additionally uses FontTools and the image's Noto Sans font. No credentials or values are stored in these instructions.

These records do not publish or activate a cloud environment configuration. The logo explorations remain **DRAFT — NOT FOR PUBLICATION**.
