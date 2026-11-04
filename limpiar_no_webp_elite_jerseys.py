from pathlib import Path
from PIL import Image, UnidentifiedImageError
import argparse
from datetime import datetime

RAIZ = Path(__file__).resolve().parent
CARPETAS = [RAIZ / 'public' / 'camisetas', RAIZ / 'public' / 'miniaturas']
EXTENSIONES = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tif', '.tiff', '.avif', '.heic'}
INFORME = RAIZ / 'informe_limpieza_no_webp.txt'


def webp_valido(ruta):
    try:
        with Image.open(ruta) as img:
            if img.format != 'WEBP':
                return False
            img.verify()
        with Image.open(ruta) as img:
            img.load()
        return True
    except (OSError, ValueError, UnidentifiedImageError):
        return False


def main():
    parser = argparse.ArgumentParser(description='Elimina fotos no WebP solo si existe WebP valido en la misma carpeta.')
    parser.add_argument('--aplicar', action='store_true', help='Eliminar archivos comprobados; sin esta opcion solo simula.')
    args = parser.parse_args()
    lineas = [f'ELITE JERSEYS - LIMPIEZA NO WEBP - {datetime.now():%Y-%m-%d %H:%M:%S}',
              f'MODO: {"ELIMINACION" if args.aplicar else "SIMULACION"}', '']
    encontrados = eliminados = protegidos = errores = 0
    for carpeta in CARPETAS:
        if not carpeta.is_dir():
            lineas.append(f'ERROR: no existe {carpeta}')
            errores += 1
            continue
        candidatos = sorted((p for p in carpeta.rglob('*') if p.is_file() and p.suffix.lower() in EXTENSIONES))
        lineas.append(f'{carpeta.relative_to(RAIZ)}: {len(candidatos)} imagenes no WebP')
        for origen in candidatos:
            encontrados += 1
            destino = origen.with_suffix('.webp')
            relativa = origen.relative_to(RAIZ)
            if not destino.is_file() or not webp_valido(destino):
                protegidos += 1
                lineas.append(f'CONSERVADA (sin WebP valido): {relativa}')
                continue
            if not args.aplicar:
                lineas.append(f'ELIMINARIA: {relativa}')
                continue
            try:
                origen.unlink()
                eliminados += 1
                lineas.append(f'ELIMINADA: {relativa}')
            except OSError as exc:
                errores += 1
                lineas.append(f'ERROR al eliminar {relativa}: {exc}')
        lineas.append('')
    lineas.extend([f'No WebP encontrados: {encontrados}',
                   f'Eliminados: {eliminados}',
                   f'Conservados por seguridad: {protegidos}',
                   f'Errores: {errores}',
                   'El script no modifica ningun archivo WebP.'])
    INFORME.write_text('\n'.join(lineas) + '\n', encoding='utf-8')
    print('\n'.join(lineas[-5:]))
    print(f'Informe: {INFORME.name}')
    if not args.aplicar:
        print('SIMULACION: no se ha borrado nada. Para eliminar: python limpiar_no_webp_elite_jerseys.py --aplicar')


if __name__ == '__main__':
    main()
