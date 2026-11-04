from pathlib import Path
from PIL import Image, ImageOps, UnidentifiedImageError
import argparse

RAIZ = Path(__file__).resolve().parent / 'public'
CARPETAS = ('camisetas', 'miniaturas')
EXTENSIONES = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.gif'}


def convertir(origen, calidad):
    destino = origen.with_suffix('.webp')
    if destino.exists():
        return 'omitida', 'Ya existe WebP: ' + str(destino)
    temporal = destino.with_name(destino.stem + '.temporal.webp')
    try:
        with Image.open(origen) as imagen:
            if getattr(imagen, 'n_frames', 1) > 1:
                imagen.seek(0)
            imagen = ImageOps.exif_transpose(imagen)
            imagen.load()
            imagen = imagen.convert('RGBA' if imagen.mode in ('RGBA', 'LA') or 'transparency' in imagen.info else 'RGB')
            imagen.save(temporal, 'WEBP', quality=calidad, method=6)
        with Image.open(temporal) as prueba:
            prueba.verify()
        temporal.replace(destino)
        return 'convertida', str(destino)
    except (OSError, ValueError, UnidentifiedImageError) as error:
        temporal.unlink(missing_ok=True)
        return 'error', f'{origen}: {error}'


def main():
    parser = argparse.ArgumentParser(description='Convierte imágenes de camisetas y miniaturas a WebP.')
    parser.add_argument('--aplicar', action='store_true', help='Convierte sin borrar los originales.')
    args = parser.parse_args()
    total = {'convertida': 0, 'omitida': 0, 'error': 0}
    for nombre in CARPETAS:
        carpeta = RAIZ / nombre
        if not carpeta.is_dir():
            print(f'ERROR: No existe {carpeta}')
            total['error'] += 1
            continue
        archivos = sorted(p for p in carpeta.rglob('*') if p.is_file() and p.suffix.lower() in EXTENSIONES)
        pendientes = [p for p in archivos if not p.with_suffix('.webp').exists()]
        print(f'\n{nombre.upper()}: {len(archivos)} archivos no WebP; {len(pendientes)} sin versión WebP.')
        if not args.aplicar:
            for archivo in pendientes:
                print('PENDIENTE:', archivo.relative_to(RAIZ))
            continue
        for i, archivo in enumerate(archivos, 1):
            estado, mensaje = convertir(archivo, 85 if nombre == 'camisetas' else 78)
            total[estado] += 1
            print(f'[{i}/{len(archivos)}] {estado.upper()}: {mensaje}')
    if args.aplicar:
        print('\nRESULTADO: {convertida} convertidas; {omitida} omitidas; {error} errores.'.format(**total))
        print('Los originales se conservan. No se ha eliminado ni sobrescrito ningún archivo existente.')
    else:
        print('\nSIMULACIÓN: no se ha modificado ningún archivo. Para convertir: python convertir_camisetas_y_miniaturas_webp.py --aplicar')


if __name__ == '__main__':
    main()
