from pathlib import Path
import re
import unicodedata
from collections import Counter

RAIZ = Path(__file__).resolve().parent
CATALOGO = RAIZ / 'src' / 'data' / 'catalogo.ts'
CAMISETAS = RAIZ / 'public' / 'camisetas'
INFORME = RAIZ / 'informe_equipos_sin_fotos.txt'


def slug(texto):
    if texto == 'Otros clubes':
        return 'otros-clubes-liga-espanola'
    texto = unicodedata.normalize('NFD', texto.lower())
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    texto = texto.replace('&', 'and')
    return re.sub(r'^-+|-+$', '', re.sub(r'[^a-z0-9]+', '-', texto))


def extraer_categorias(texto):
    # Extrae los bloques de categorías y sus listas de equipos del catálogo actual.
    patron = re.compile(
        r'nombre\s*:\s*[\'\"]([^\'\"]+)[\'\"](?:(?!\bequipos\s*:).)*?'
        r'\bequipos\s*:\s*\[([^\]]*)\]', re.S
    )
    resultado = []
    for coincidencia in patron.finditer(texto):
        liga, bloque = coincidencia.groups()
        equipos = re.findall(r'[\'\"]([^\'\"]+)[\'\"]', bloque)
        resultado.append((liga, equipos))
    return resultado


def main():
    if not CATALOGO.is_file() or not CAMISETAS.is_dir():
        print('ERROR: Coloca este script en la raíz del proyecto, junto a package.json.')
        return

    categorias = extraer_categorias(CATALOGO.read_text(encoding='utf-8'))
    if not categorias:
        print('ERROR: No he podido leer las listas de equipos de catalogo.ts. No se genera informe vacío.')
        return

    total = 0
    problemas = []
    resumen = []
    for liga, equipos in categorias:
        conteo = Counter()
        for equipo in equipos:
            total += 1
            carpeta = CAMISETAS / slug(equipo)
            if not carpeta.is_dir():
                estado = 'SIN CARPETA'
            elif not any(p.is_file() and p.suffix.lower() == '.webp' for p in carpeta.rglob('*')):
                estado = 'SIN FOTOS WEBP'
            else:
                estado = 'CON FOTOS'
            conteo[estado] += 1
            if estado != 'CON FOTOS':
                problemas.append((liga, equipo, estado, carpeta.relative_to(RAIZ)))
        resumen.append((liga, len(equipos), conteo))

    lineas = ['ELITE JERSEYS - EQUIPOS DEL CATALOGO SIN FOTOGRAFIAS',
              'No se ha modificado ningun archivo ni carpeta.', '',
              f'Categorias: {len(categorias)}', f'Equipos y selecciones: {total}',
              f'Equipos sin fotografias WebP: {len(problemas)}', '', 'RESUMEN POR CATEGORIA']
    for liga, n, c in resumen:
        lineas.append(f'{liga}: {n} equipos | {c["SIN CARPETA"]} sin carpeta | {c["SIN FOTOS WEBP"]} sin fotos WebP | {c["CON FOTOS"]} con fotos')
    lineas += ['', 'EQUIPOS QUE NECESITAN REVISION']
    for liga, equipo, estado, carpeta in problemas:
        lineas.append(f'[{liga}] {equipo} | {estado} | {carpeta}')
    if not problemas:
        lineas.append('Ninguno: todos los equipos tienen al menos una imagen WebP.')
    lineas += ['', 'NOTA: Se cuentan fotos WebP en subcarpetas de cada equipo.',
              'No se comprueba que la web muestre correctamente cada imagen.']
    INFORME.write_text('\n'.join(lineas) + '\n', encoding='utf-8')
    print('\n'.join(lineas))
    print(f'\nInforme guardado: {INFORME.name}')


if __name__ == '__main__':
    main()
