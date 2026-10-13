from pathlib import Path
from PIL import Image

CARPETA = Path(__file__).resolve().parent / 'public' / 'camisetas'
EXTENSIONES = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.gif'}


def webp_valido(ruta):
    try:
        with Image.open(ruta) as imagen:
            if imagen.format != 'WEBP':
                return False
            imagen.verify()
        return True
    except (OSError, ValueError):
        return False


def main():
    if not CARPETA.is_dir():
        print(f'ERROR: No existe la carpeta {CARPETA}')
        return

    candidatos = sorted(p for p in CARPETA.rglob('*') if p.is_file() and p.suffix.lower() in EXTENSIONES)
    seguros, conservados = [], []
    for original in candidatos:
        destino = original.with_suffix('.webp')
        if destino.is_file() and webp_valido(destino):
            seguros.append(original)
        else:
            conservados.append(original)

    print(f'Carpeta: {CARPETA}')
    print(f'Originales encontrados: {len(candidatos)}')
    print(f'Con WebP válido: {len(seguros)}')
    print(f'Sin WebP válido (se conservarán): {len(conservados)}')
    print(f'Espacio recuperable: {sum(p.stat().st_size for p in seguros) / 1024**2:.1f} MB')
    if conservados:
        print('\nArchivos conservados sin WebP válido:')
        for ruta in conservados[:30]:
            print(' -', ruta.relative_to(CARPETA))
        if len(conservados) > 30:
            print(f' ... y {len(conservados) - 30} más')

    if not seguros:
        print('\nNo hay originales seguros que eliminar.')
        return
    print('\nATENCIÓN: La eliminación es permanente. Se recomienda una copia de seguridad.')
    confirmacion = input('Para eliminar solo los originales verificados, escribe ELIMINAR: ').strip()
    if confirmacion != 'ELIMINAR':
        print('Cancelado. No se ha eliminado ningún archivo.')
        return

    eliminados, errores = 0, 0
    for original in seguros:
        try:
            original.unlink()
            eliminados += 1
        except OSError as error:
            errores += 1
            print(f'No se pudo eliminar {original}: {error}')
    print(f'RESULTADO: {eliminados} originales eliminados; {len(conservados)} conservados; {errores} errores.')


if __name__ == '__main__':
    main()
