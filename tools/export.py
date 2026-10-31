"""Export each board's outputs into kicad/<board>/output/ with kicad-cli.

Usage: python tools/export.py [--pcb] [board ...]     (default: all boards under kicad/)

Always (from the schematic):
    <project>.pdf             schematic
    <project>-bom.csv         BOM, JLCPCB column names (Comment, Designator, Footprint, LCSC Part #),
                              one row per value + footprint + LCSC part, not-fitted (DNP) parts left out
With --pcb (from the layout; only once the board is laid out):
    <project>-gerbers.zip     Gerbers + Excellon drill files
    <project>-cpl.csv         placement, JLCPCB column names (Designator, Mid X, Mid Y, Layer, Rotation)
    <project>.step            3D model
Set KICAD_CLI if kicad-cli isn't on PATH or in the default Windows location.
"""
import argparse
import csv
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / 'kicad'


def kicad_cli():
    for c in (os.environ.get('KICAD_CLI'), shutil.which('kicad-cli'),
              'C:/Program Files/KiCad/10.0/bin/kicad-cli.exe'):
        if c and Path(c).exists():
            return c
    sys.exit('kicad-cli not found: set KICAD_CLI')


CLI = kicad_cli()


def run(*args):
    r = subprocess.run([CLI, *map(str, args)], capture_output=True, text=True)
    if r.returncode:
        sys.exit('kicad-cli %s failed: %s' % (' '.join(map(str, args[:3])), r.stderr or r.stdout))


def refkey(ref):
    m = re.match(r'(\D*)(\d*)(.*)', ref)
    return m.group(1), int(m.group(2) or 0), m.group(3)


def bom(sch, out):
    """One row per LCSC part (or per value + footprint when there is none). Returns refs with no LCSC number."""
    tmp = out.with_suffix('.tmp')
    run('sch', 'export', 'bom', '-o', tmp, '--exclude-dnp', '--fields', 'Reference,Value,Footprint,LCSC',
        '--labels', 'Reference,Value,Footprint,LCSC', '--ref-range-delimiter', '', sch)
    with open(tmp, encoding='utf-8', newline='') as f:
        parts = list(csv.DictReader(f))
    tmp.unlink()
    groups = {}
    for p in parts:
        lcsc = p['LCSC'].strip()
        key = (lcsc,) if lcsc else ('', p['Value'], p['Footprint'])
        groups.setdefault(key, []).append(p)
    rows = []
    for key, ps in groups.items():
        refs = sorted((p['Reference'] for p in ps), key=refkey)
        values = list(dict.fromkeys(p['Value'] for p in ps if p['Value']))
        fps = list(dict.fromkeys(p['Footprint'] for p in ps))
        rows.append([' / '.join(values), ','.join(refs), ' / '.join(fps), key[0], len(refs)])
    rows.sort(key=lambda r: refkey(r[1].split(',')[0]))
    with open(out, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['Comment', 'Designator', 'Footprint', 'LCSC Part #', 'Quantity'])
        w.writerows(rows)
    return [r[1] for r in rows if not r[3]]


def cpl(pcb, out):
    tmp = out.with_suffix('.tmp')
    run('pcb', 'export', 'pos', '-o', tmp, '--format', 'csv', '--units', 'mm', '--side', 'both',
        '--exclude-dnp', pcb)
    with open(tmp, encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f))
    tmp.unlink()
    with open(out, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['Designator', 'Mid X', 'Mid Y', 'Layer', 'Rotation'])
        for r in rows:
            w.writerow([r['Ref'], r['PosX'], r['PosY'], 'Top' if r['Side'] == 'top' else 'Bottom', r['Rot']])


def gerbers(pcb, out):
    with tempfile.TemporaryDirectory() as d:
        run('pcb', 'export', 'gerbers', '-o', d, '--board-plot-params', pcb)
        run('pcb', 'export', 'drill', '-o', d + os.sep, pcb)
        with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
            for p in sorted(Path(d).iterdir()):
                z.write(p, p.name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pcb', action='store_true', help='also export Gerbers, placement and STEP from the layout')
    ap.add_argument('boards', nargs='*')
    a = ap.parse_args()
    boards = a.boards or sorted(p.name for p in ROOT.iterdir() if list(p.glob('*.kicad_pro')))
    for b in boards:
        pro = next((ROOT / b).glob('*.kicad_pro'))
        sch, pcb = pro.with_suffix('.kicad_sch'), pro.with_suffix('.kicad_pcb')
        out = ROOT / b / 'output'
        out.mkdir(exist_ok=True)
        run('sch', 'export', 'pdf', '-o', out / (pro.stem + '.pdf'), sch)
        missing = bom(sch, out / (pro.stem + '-bom.csv'))
        made = ['pdf', 'bom']
        if a.pcb:
            gerbers(pcb, out / (pro.stem + '-gerbers.zip'))
            cpl(pcb, out / (pro.stem + '-cpl.csv'))
            run('pcb', 'export', 'step', '-o', out / (pro.stem + '.step'), '--subst-models', '--no-dnp', pcb)
            made += ['gerbers', 'cpl', 'step']
        print('%s: %s' % (out.relative_to(ROOT.parent).as_posix(), ', '.join(made)))
        if missing:
            print('  no LCSC part number: %s' % ', '.join(missing))


if __name__ == '__main__':
    main()
