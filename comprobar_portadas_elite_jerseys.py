from pathlib import Path
from datetime import datetime
from PIL import Image

RAIZ = Path(__file__).resolve().parent
CAMISETAS = RAIZ / 'public' / 'camisetas'
MINIATURAS = RAIZ / 'public' / 'miniaturas'
INFORME = RAIZ / 'informe_portadas_elite_jerseys.txt'


def verificar(ruta):
    try:
        with Image.open(ruta) as img:
            img.verify()
        return True
    except Exception:
        return False


def main():
    if not CAMISETAS.is_dir() or not MINIATURAS.is_dir():
        print('ERROR: Debes guardar este script en la raíz del proyecto, junto a package.json.')
        return

    portadas_camisetas = {p.relative_to(CAMISETAS) for p in CAMISETAS.rglob('*') if p.is_file() and p.name.lower() == '01.webp'}
    portadas_miniaturas = {p.relative_to(MINIATURAS) for p in MINIATURAS.rglob('*') if p.is_file() and p.name.lower() == '01.webp'}
    faltan = sorted(portadas_camisetas - portadas_miniaturas, key=str)
    huerfanas = sorted(portadas_miniaturas - portadas_camisetas, key=str)
    coinciden = sorted(portadas_camisetas & portadas_miniaturas, key=str)
    danadas = sorted((r for r in portadas_miniaturas if not verificar(MINIATURAS / r)), key=str)
    adicionales = sorted((p.relative_to(MINIATURAS) for p in MINIATURAS.rglob('*.webp') if p.name.lower() != '01.webp'), key=str)
    productos_sin_portada = sorted((p.relative_to(CAMISETAS) for p in CAMISETAS.rglob('*') if p.is_dir() and any(c.is_file() and c.suffix.lower() == '.webp' for c in p.iterdir()) and not (p / '01.webp').is_file()), key=str)

    resumen = [
        'ELITE JERSEYS - AUDITORÍA DE PORTADAS',
        f'Fecha: {datetime.now():%Y-%m-%d %H:%M:%S}',
        f'Portadas 01.webp en camisetas: {len(portadas_camisetas)}',
        f'Portadas 01.webp en miniaturas: {len(portadas_miniaturas)}',
        f'Portadas con ambas copias: {len(coinciden)}',
        f'FALTAN en miniaturas: {len(faltan)}',
        f'Miniaturas sin portada correspondiente en camisetas: {len(huerfanas)}',
        f'Miniaturas 01.webp dañadas: {len(danadas)}',
        f'Otras imágenes WebP en miniaturas: {len(adicionales)}',
        f'Carpetas de productos con imágenes pero sin 01.webp en camisetas: {len(productos_sin_portada)}',
        '',
        'Este script solo revisa. No modifica ni borra archivos.',
    ]
    secciones = [
        ('PORTADAS QUE FALTAN EN MINIATURAS', faltan),
        ('MINIATURAS SIN PORTADA EN CAMISETAS', huerfanas),
        ('MINIATURAS DAÑADAS', danadas),
        ('IMÁGENES ADICIONALES EN MINIATURAS', adicionales),
        ('PRODUCTOS SIN 01.WEBP EN CAMISETAS', productos_sin_portada),
    ]
    contenido = resumen[:]
    for titulo, rutas in secciones:
        contenido.extend(['', f'=== {titulo} ({len(rutas)}) ==='])
        contenido.extend(str(r) for r in rutas)
    INFORME.write_text('\n'.join(contenido) + '\n', encoding='utf-8')
    print('\n'.join(resumen))
    print(f'Informe guardado: {INFORME.name}')

if __name__ == '__main__':
    main()
