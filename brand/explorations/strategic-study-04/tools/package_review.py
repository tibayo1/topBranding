#!/usr/bin/env python3
"""Package editable sources, evidence, licensed fonts and rendered review files."""
from pathlib import Path
import zipfile,re,posixpath
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1]
target=ROOT/'exports/strategic-study-04-editable.zip';prefix=Path('Tabernacle-of-Praise-Strategic-Study-04')
files=[p for p in sorted(ROOT.rglob('*')) if p.is_file() and p!=target and '__pycache__' not in p.parts]
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files:
  name=prefix/p.relative_to(ROOT)
  if p==ROOT/'README.md':
   text='\n'.join(line for line in p.read_text().splitlines() if not line.startswith('- [Complete editable study ZIP]'))+'\n'
   z.writestr(str(name),text)
  else:z.write(p,arcname=name)
with zipfile.ZipFile(target) as z:
 assert z.testzip() is None
 names=set(z.namelist());assert len(names)==len(z.namelist())
 for name in names:
  if not name.endswith('.md') or name.endswith('user-brief.md'):continue
  for link in re.findall(r'\]\(([^)]+)\)',z.read(name).decode()):
   if link.startswith(('http','mailto:','#','skill:')):continue
   link=unquote(link.split('#')[0]);expected=posixpath.normpath(posixpath.join(posixpath.dirname(name),link))
   assert expected in names or any(n.startswith(expected.rstrip('/')+'/') for n in names),(name,link)
 print('Verified archive CRC, unique entries and local Markdown links:',len(names),'files')
