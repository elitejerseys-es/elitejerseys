from pathlib import Path
import argparse
import shutil
from datetime import datetime

ROOT = Path(__file__).resolve().parent
MINI = ROOT / 'public' / 'miniaturas'
CAMI = ROOT / 'public' / 'camisetas'
BACKUP = ROOT / 'respaldo_miniaturas_sobrantes'
REPORT = ROOT / 'informe_miniaturas_solo_01.txt'


def main():
    parser = argparse.ArgumentParser(description='Dejar solo 01.webp en cada carpeta de miniaturas.')
    parser.add_argument('--aplicar', action='store_true', help='Mover miniaturas sobrantes a un respaldo fuera de public')
    args = parser.parse_args()
    if not MINI.is_dir() or not CAMI.is_dir():
        print('ERROR: No encuentro public/miniaturas o public/camisetas. Ejecuta desde la raiz del proyecto.')
        return

    extras, sin_copia, portadas, otros = [], [], [], []
    for f in sorted(MINI.rglob('*')):
        if not f.is_file():
            continue
        if f.suffix.lower() != '.webp':
            otros.append(f)
            continue
        if f.name.lower() == '01.webp':
            portadas.append(f)
            continue
        rel = f.relative_to(MINI)
        if (CAMI / rel).is_file():
            extras.append(f)
        else:
            sin_copia.append(f)

    movidas, errores = [], []
    if args.aplicar:
        for f in extras:
            rel = f.relative_to(MINI)
            dest = BACKUP / rel
            try:
                dest.parent.mkdir(parents=True, exist_ok=True)
                if dest.exists():
                    errores.append(f'{rel}: ya existe en respaldo, no se ha movido')
                    continue
                shutil.move(str(f), str(dest))
                movidas.append(str(rel))
            except OSError as e:
                errores.append(f'{rel}: {e}')

    lines = [
        'ELITE JERSEYS - REVISION DE MINIATURAS',
        f'Fecha: {datetime.now():%Y-%m-%d %H:%M:%S}',
        f'Modo: {"APLICAR" if args.aplicar else "SIMULACION"}',
        f'Portadas 01.webp conservadas: {len(portadas)}',
        f'Miniaturas sobrantes con copia en camisetas: {len(extras)}',
        f'Miniaturas adicionales SIN copia en camisetas (se conservan): {len(sin_copia)}',
        f'Archivos no WebP (se conservan): {len(otros)}',
        f'Miniaturas movidas a respaldo: {len(movidas)}',
        f'Errores: {len(errores)}',
        '', 'SOBRANTES CON COPIA EN CAMISETAS:',
        *[str(f.relative_to(MINI)) for f in extras],
        '', 'SIN COPIA EN CAMISETAS (NO TOCAR):',
        *[str(f.relative_to(MINI)) for f in sin_copia],
        '', 'OTROS ARCHIVOS (NO TOCAR):',
        *[str(f.relative_to(MINI)) for f in otros],
        '', 'ERRORES:', *errores,
    ]
    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    for line in lines[:9]:
        print(line)
    print(f'Informe: {REPORT.name}')
    if not args.aplicar:
        print('SIMULACION: No se ha movido ni eliminado ninguna imagen.')
        print('Para aplicar: python limpiar_miniaturas_solo_01.py --aplicar')
    else:
        print(f'Respaldo: {BACKUP}')
        print('Los archivos se han movido al respaldo, no se han eliminado definitivamente.')


if __name__ == '__main__':
    main()
