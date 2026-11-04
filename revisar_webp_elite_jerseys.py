from pathlib import Path
from collections import Counter
from PIL import Image

RAIZ = Path(__file__).resolve().parent / 'public'
CARPETAS = ('camisetas', 'miniaturas')
EXTENSIONES = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.gif', '.avif', '.webp'}

def main():
    resumen = Counter()
    informe = ['ELITE JERSEYS - AUDITORÍA DE IMÁGENES', 'Modo: SOLO LECTURA', '']
    for nombre in CARPETAS:
        carpeta = RAIZ / nombre
        informe.append(f'=== {nombre.upper()} ===')
        if not carpeta.is_dir():
            informe.append(f'ERROR: No existe {carpeta}')
            continue
        archivos = sorted(p for p in carpeta.rglob('*') if p.is_file() and p.suffix.lower() in EXTENSIONES)
        no_webp = [p for p in archivos if p.suffix.lower() != '.webp']
        webps = [p for p in archivos if p.suffix.lower() == '.webp']
        con_equivalente, sin_equivalente, webp_danados = [], [], []
        for p in no_webp:
            destino = p.with_suffix('.webp')
            if destino.is_file():
                con_equivalente.append((p, destino))
            else:
                sin_equivalente.append(p)
        for p in webps:
            try:
                with Image.open(p) as im:
                    im.verify()
            except Exception as exc:
                webp_danados.append((p, str(exc)))
        print(f'\n{nombre.upper()}: {len(archivos)} imágenes; {len(webps)} WebP; {len(no_webp)} no WebP')
        print(f'  No WebP con equivalente: {len(con_equivalente)}')
        print(f'  No WebP sin equivalente: {len(sin_equivalente)}')
        print(f'  WebP dañados o ilegibles: {len(webp_danados)}')
        informe.extend([f'Imágenes: {len(archivos)}', f'WebP: {len(webps)}', f'No WebP con equivalente: {len(con_equivalente)}', f'No WebP sin equivalente: {len(sin_equivalente)}', f'WebP dañados: {len(webp_danados)}', ''])
        for p, destino in con_equivalente:
            informe.append(f'CON EQUIVALENTE: {p.relative_to(RAIZ)} -> {destino.relative_to(RAIZ)}')
        for p in sin_equivalente:
            informe.append(f'SIN EQUIVALENTE: {p.relative_to(RAIZ)}')
        for p, error in webp_danados:
            informe.append(f'WEBP DAÑADO: {p.relative_to(RAIZ)} | {error}')
        informe.append('')
        resumen['con_equivalente'] += len(con_equivalente)
        resumen['sin_equivalente'] += len(sin_equivalente)
        resumen['webp_danados'] += len(webp_danados)
    informe_path = Path(__file__).resolve().parent / 'informe_auditoria_webp.txt'
    informe_path.write_text('\n'.join(informe), encoding='utf-8')
    print(f'\nTOTAL: {resumen["con_equivalente"]} no WebP con equivalente; {resumen["sin_equivalente"]} sin equivalente; {resumen["webp_danados"]} WebP dañados.')
    print(f'Informe guardado en: {informe_path.name}')
    print('No se ha modificado ni eliminado ninguna imagen.')

if __name__ == '__main__':
    main()
