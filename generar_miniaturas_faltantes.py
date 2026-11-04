from pathlib import Path
from PIL import Image, ImageOps, UnidentifiedImageError

RAIZ = Path(__file__).resolve().parent
CAMISETAS = RAIZ / 'public' / 'camisetas'
MINIATURAS = RAIZ / 'public' / 'miniaturas'
TAMANO_MAXIMO = (420, 525)
CALIDAD = 78

def main():
    if not CAMISETAS.is_dir() or not MINIATURAS.is_dir():
        print('ERROR: No encuentro public/camisetas o public/miniaturas. Coloca el script en la raiz del proyecto.')
        return
    pendientes = []
    for origen in sorted(CAMISETAS.rglob('01.webp')):
        destino = MINIATURAS / origen.relative_to(CAMISETAS)
        if not destino.exists():
            pendientes.append((origen, destino))
    print(f'Miniaturas pendientes: {len(pendientes)}')
    for origen, destino in pendientes:
        print(f'PENDIENTE: {destino.relative_to(RAIZ)}')
    import sys
    if '--aplicar' not in sys.argv:
        print('SIMULACION: No se ha modificado nada. Para crear: python generar_miniaturas_faltantes.py --aplicar')
        return
    creadas = errores = 0
    for origen, destino in pendientes:
        temporal = destino.with_name(destino.stem + '.temporal.webp')
        try:
            destino.parent.mkdir(parents=True, exist_ok=True)
            with Image.open(origen) as imagen:
                imagen = ImageOps.exif_transpose(imagen)
                imagen.seek(0)
                imagen = imagen.convert('RGBA' if 'A' in imagen.getbands() or 'transparency' in imagen.info else 'RGB')
                imagen.thumbnail(TAMANO_MAXIMO, Image.Resampling.LANCZOS)
                imagen.save(temporal, 'WEBP', quality=CALIDAD, method=6)
            with Image.open(temporal) as prueba:
                prueba.verify()
            if destino.exists():
                temporal.unlink(missing_ok=True)
                print(f'OMITIDA (ya existe): {destino.relative_to(RAIZ)}')
                continue
            temporal.replace(destino)
            creadas += 1
            print(f'CREADA: {destino.relative_to(RAIZ)}')
        except (OSError, ValueError, UnidentifiedImageError) as error:
            errores += 1
            temporal.unlink(missing_ok=True)
            print(f'ERROR: {origen.relative_to(RAIZ)}: {error}')
    print(f'RESULTADO: {creadas} miniaturas creadas; {errores} errores. Originales y miniaturas existentes intactos.')

if __name__ == '__main__':
    main()
