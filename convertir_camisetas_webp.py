from pathlib import Path
from PIL import Image, ImageOps

CARPETA = Path(__file__).resolve().parent / 'public' / 'camisetas'
CALIDAD = 82

def main():
    if not CARPETA.is_dir():
        print(f'ERROR: No existe {CARPETA}')
        print('Coloca este script en la carpeta principal del proyecto, junto a package.json.')
        return
    fotos = sorted(p for p in CARPETA.rglob('*') if p.is_file() and p.suffix.lower() in ('.jpg', '.jpeg'))
    print(f'JPG/JPEG encontrados: {len(fotos)}')
    convertidas = existentes = errores = 0
    for i, origen in enumerate(fotos, 1):
        destino = origen.with_suffix('.webp')
        if destino.exists():
            print(f'OMITIDO (ya existe): {destino.relative_to(CARPETA)}')
            existentes += 1
            continue
        try:
            with Image.open(origen) as img:
                img = ImageOps.exif_transpose(img)
                if img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGBA' if 'A' in img.getbands() else 'RGB')
                img.save(destino, 'WEBP', quality=CALIDAD, method=6)
            convertidas += 1
            print(f'[{i}/{len(fotos)}] {origen.relative_to(CARPETA)} -> {destino.name}')
        except Exception as exc:
            errores += 1
            destino.unlink(missing_ok=True)
            print(f'ERROR: {origen}: {exc}')
    print(f'\nRESULTADO: {convertidas} convertidas; {existentes} omitidas; {errores} errores.')
    print('Los JPG originales se han conservado. Comprueba las rutas en la web antes de eliminarlos.')

if __name__ == '__main__':
    main()
