"""Export every board's schematic to kicad/<board>/PDF/<project>.pdf with kicad-cli.

Usage: python tools/export_pdfs.py [board ...]     (default: all boards under kicad/)
Set KICAD_CLI if kicad-cli isn't on PATH or in the default Windows location.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / 'kicad'


def kicad_cli():
    for c in (os.environ.get('KICAD_CLI'), shutil.which('kicad-cli'),
              'C:/Program Files/KiCad/10.0/bin/kicad-cli.exe'):
        if c and Path(c).exists():
            return c
    sys.exit('kicad-cli not found: set KICAD_CLI')


def main():
    cli = kicad_cli()
    boards = sys.argv[1:] or sorted(p.name for p in ROOT.iterdir() if list(p.glob('*.kicad_pro')))
    for b in boards:
        pro = next((ROOT / b).glob('*.kicad_pro'))
        sch = pro.with_suffix('.kicad_sch')
        out = ROOT / b / 'PDF' / (pro.stem + '.pdf')
        out.parent.mkdir(exist_ok=True)
        r = subprocess.run([cli, 'sch', 'export', 'pdf', '-o', str(out), str(sch)], capture_output=True, text=True)
        if r.returncode:
            sys.exit('%s: %s' % (b, r.stderr or r.stdout))
        print(out.relative_to(ROOT.parent))


if __name__ == '__main__':
    main()
