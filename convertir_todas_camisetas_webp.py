from pathlib import Path
from PIL import Image, ImageOps, UnidentifiedImageError

CARPETA = Path(__file__).resolve().parent / 'public' / 'camisetas'
EXTENSIONES = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.gif'}
CALIDAD = 85


def convertir(origen: Path):
    destino = origen.with_suffix('.webp')
    if destino.exists():
        return 'omitida', f'Ya existe: {destino.name}'
    temporal = destino.with_name(destino.stem + '.temporal.webp')
    try:
        with Image.open(origen) as imagen:
            if getattr(imagen, 'is_animated', False) and getattr(imagen, 'n_frames', 1) > 1:
                return 'omitida', f'Animación no convertida: {origen}'
            imagen = ImageOps.exif_transpose(imagen)
            if imagen.mode in ('RGBA', 'LA') or ('transparency' in imagen.info):
                imagen = imagen.convert('RGBA')
            else:
                imagen = imagen.convert('RGB')
            imagen.save(temporal, 'WEBP', quality=CALIDAD, method=6)
        with Image.open(temporal) as comprobacion:
            comprobacion.verify()
        temporal.replace(destino)
        return 'convertida', str(destino.relative_to(CARPETA))
    except (OSError, ValueError, UnidentifiedImageError) as error:
        temporal.unlink(missing_ok=True)
        return 'error', f'{origen}: {error}'


def main():
    if not CARPETA.is_dir():
        print(f'ERROR: No encuentro la carpeta {CARPETA}')
        print('Coloca este script en la raíz de tu proyecto Elite Jerseys.')
        return
    archivos = sorted((p for p in CARPETA.rglob('*') if p.is_file() and p.suffix.lower() in EXTENSIONES))
    print(f'Imágenes no WebP encontradas: {len(archivos)}')
    conteo = {'convertida': 0, 'omitida': 0, 'error': 0}
    for numero, archivo in enumerate(archivos, 1):
        estado, mensaje = convertir(archivo)
        conteo[estado] += 1
        print(f'[{numero}/{len(archivos)}] {estado.upper()}: {mensaje}')
    print('\nRESULTADO: {convertida} convertidas; {omitida} omitidas; {error} errores.'.format(**conteo))
    print('Los archivos originales se han conservado. Comprueba la web antes de eliminarlos.')


if __name__ == '__main__':
    main()
