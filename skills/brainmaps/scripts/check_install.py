#!/usr/bin/env python3
"""Check an extracted BrainMaps skill and its local tools."""
from pathlib import Path
import importlib.util, shutil, sys, struct
root = Path(__file__).resolve().parent.parent
issues = []
skill = root / "SKILL.md"
if not skill.is_file(): issues.append("Missing SKILL.md")
else:
    head = skill.read_text(encoding="utf-8").split("---", 2)
    if len(head) < 3 or "name: brainmaps" not in head[1] or "description:" not in head[1]:
        issues.append("Invalid skill frontmatter")
for path in [root/'agents/openai.yaml', root/'scripts/build_board.py', root/'scripts/audit_board.py', root/'reference/style-gallery/INDEX.md']:
    if not path.is_file(): issues.append(f"Missing {path.relative_to(root)}")
for i in range(1, 15):
    if not list((root/'reference/style-gallery').glob(f'G{i}-*.png')): issues.append(f'Missing G{i} image')
for i in range(1, 4):
    if not list((root/'reference/style-gallery').glob(f'B{i}-*.png')): issues.append(f'Missing B{i} image')
images = sorted((root/'reference/style-gallery').glob('*.png'))
for f in images:
    with f.open('rb') as src:
        if src.read(8) != bytes.fromhex('89504e470d0a1a0a'):
            issues.append(f'Invalid PNG: {f.name}')
for f in (root/'scripts').glob('*.py'):
    try: compile(f.read_text(encoding='utf-8'), str(f), 'exec')
    except SyntaxError as exc: issues.append(f'{f.name} syntax error: {exc}')
try:
    from PIL import Image
    print(f'Pillow: installed ({Image.__version__ if hasattr(Image,"__version__") else "available"})')
except ImportError: issues.append('Pillow not found. Run: python -m pip install Pillow')
for cmd in ('pdflatex','pdftocairo'):
    print(f'{cmd}: {shutil.which(cmd) or "not found (optional; math falls back to text)"}')
print(f'Gallery PNGs: {len(images)}; skill: {root}')
if issues:
    print('INSTALL CHECK FAILED:')
    for i in issues: print(' - ' + i)
    sys.exit(1)
print('INSTALL CHECK PASSED')
