#!/usr/bin/env bash
set -euo pipefail

# Install the reviewed upstream revision without changing application files.
logo_revision=0ecf52e9a4b3ac92b714f7cc6e3148ab8c774134
logo_stage=$(mktemp -d /tmp/logo-design-install.XXXXXX)
trap 'rm -rf "$logo_stage"' EXIT
git init --quiet "$logo_stage/source"
git -C "$logo_stage/source" fetch --quiet --depth 1 https://github.com/kaankiziltug/logo-design-skill.git "$logo_revision"
test "$(git -C "$logo_stage/source" rev-parse FETCH_HEAD)" = "$logo_revision"
git -C "$logo_stage/source" checkout --quiet --detach FETCH_HEAD

python3 - "$logo_stage/source" <<'PY'
import hashlib
import os
from pathlib import Path
import shutil
import sys
import tempfile

source = Path(sys.argv[1])
target = Path('/workspace/topBranding/.agents/skills/logo-design')
target.parent.mkdir(parents=True, exist_ok=True)

def fingerprint(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}

with tempfile.TemporaryDirectory(prefix='.logo-design-', dir=target.parent) as temp:
    prepared = Path(temp) / 'logo-design'
    shutil.copytree(source / 'skills/logo-design', prepared)
    for name in ('LICENSE', 'TRADEMARKS.md'):
        shutil.copy2(source / name, prepared / name)
    if target.is_symlink():
        raise SystemExit(f'Refusing to replace an existing symlink: {target}')
    if target.exists():
        if not target.is_dir() or fingerprint(target) != fingerprint(prepared):
            raise SystemExit(f'Existing skill differs; preserving it for review: {target}')
        print(f'Skill already installed at {target}')
    else:
        os.rename(prepared, target)
        print(f'Installed skill at {target}')
PY

cd /workspace/topBranding/.agents/skills/logo-design
python3 scripts/build_catalog.py --check
python3 scripts/search_library.py --technique negative-space --summary
python3 scripts/render_png.py --which
python3 scripts/render_png.py assets/library/svg/xero.svg --size 64 -o "$logo_stage/render.png"
python3 - "$logo_stage/render.png" <<'PY'
from pathlib import Path
import struct
import sys
header = Path(sys.argv[1]).read_bytes()[:24]
assert header[:8] == b'\x89PNG\r\n\x1a\n'
assert struct.unpack('>II', header[16:24]) == (64, 64)
print('Verified 64 x 64 PNG export')
PY
