from pathlib import Path
from PIL import Image, ImageChops

carpeta = Path(__file__).resolve().parent / 'public'
if not carpeta.is_dir():
    raise SystemExit('ERROR: coloca este script en la carpeta principal de elitejerseys, junto a public.')

convertidas = omitidas = errores = peso_original = peso_webp = 0
archivos = sorted(p for p in carpeta.rglob('*') if p.is_file() and p.suffix.lower() == '.png')
print(f'PNG encontrados: {len(archivos)}\n')

for origen in archivos:
    destino = origen.with_suffix('.webp')
    if destino.exists():
        print(f'OMITIDA (ya existe): {destino}')
        omitidas += 1
        continue
    try:
        with Image.open(origen) as imagen:
            if getattr(imagen, 'n_frames', 1) > 1:
                print(f'OMITIDA (animada): {origen}')
                omitidas += 1
                continue
            original = imagen.convert('RGBA')
            opciones = dict(lossless=True, quality=100, method=6, exact=True)
            if imagen.info.get('icc_profile'):
                opciones['icc_profile'] = imagen.info['icc_profile']
            original.save(destino, 'WEBP', **opciones)
            with Image.open(destino) as comprobacion:
                resultado = comprobacion.convert('RGBA')
                if resultado.size != original.size:
                    raise ValueError('Resolución diferente')
                if any(c.getbbox() for c in ImageChops.difference(original, resultado).split()):
                    raise ValueError('Diferencias en los píxeles')
        antes = origen.stat().st_size
        despues = destino.stat().st_size
        peso_original += antes
        peso_webp += despues
        convertidas += 1
        print(f'OK: {destino}')
    except Exception as error:
        errores += 1
        destino.unlink(missing_ok=True)
        print(f'ERROR: {origen} - {error}')

print('\n========== RESULTADOS ==========')
print(f'PNG encontrados: {len(archivos)}')
print(f'Convertidos: {convertidas}')
print(f'Omitidos: {omitidas}')
print(f'Errores: {errores}')
print(f'Peso original: {peso_original / 1048576:.2f} MB')
print(f'Peso WebP: {peso_webp / 1048576:.2f} MB')
print(f'Ahorro: {(peso_original - peso_webp) / 1048576:.2f} MB')
if peso_original:
    print(f'Reducción: {(1 - peso_webp / peso_original) * 100:.2f}%')
print('\nLos PNG originales se han conservado.')
