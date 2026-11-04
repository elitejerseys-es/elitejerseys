const fs = require('node:fs');
const path = require('node:path');

const raiz = process.cwd();
const miniaturas = path.join(raiz, 'public', 'miniaturas');
const camisetas = path.join(raiz, 'public', 'camisetas');
const aplicar = process.argv.includes('--aplicar');

if (!fs.existsSync(miniaturas) || !fs.existsSync(camisetas)) {
  console.error('ERROR: Ejecuta el script desde la carpeta raíz del proyecto Elite Jerseys.');
  process.exit(1);
}
const extensiones = new Set(['.webp', '.jpg', '.jpeg', '.png', '.avif']);
const pendientes = [];
const incidencias = [];
let revisadas = 0;

function recorrer(dir) {
  for (const entrada of fs.readdirSync(dir, { withFileTypes: true })) {
    const origen = path.join(dir, entrada.name);
    if (entrada.isDirectory()) { recorrer(origen); continue; }
    if (!entrada.isFile() || !extensiones.has(path.extname(entrada.name).toLowerCase())) continue;
    revisadas++;
    const relativo = path.relative(miniaturas, origen);
    const destino = path.join(camisetas, relativo);
    if (fs.existsSync(destino)) continue;
    pendientes.push({ origen, destino, relativo });
    if (path.basename(origen).toLowerCase() === '01.webp') {
      incidencias.push(`PORTADA SIN ORIGINAL: ${relativo}`);
    }
  }
}
recorrer(miniaturas);

let copiadas = 0;
let fallos = 0;
if (aplicar) {
  for (const { origen, destino, relativo } of pendientes) {
    try {
      fs.mkdirSync(path.dirname(destino), { recursive: true });
      fs.copyFileSync(origen, destino, fs.constants.COPYFILE_EXCL);
      copiadas++;
    } catch (error) {
      fallos++;
      incidencias.push(`ERROR COPIANDO ${relativo}: ${error.message}`);
    }
  }
}
const lineas = [
  `ELITE JERSEYS - RECUPERACIÓN DE FOTOGRAFÍAS`,
  `Fecha: ${new Date().toLocaleString('es-ES')}`,
  `Modo: ${aplicar ? 'COPIA (sin sobrescribir)' : 'SIMULACIÓN (sin cambios)'}`,
  `Imágenes revisadas en miniaturas: ${revisadas}`,
  `Imágenes ausentes en camisetas: ${pendientes.length}`,
  `Imágenes copiadas: ${copiadas}`,
  `Errores de copia: ${fallos}`,
  '',
  'FOTOGRAFÍAS DETECTADAS:',
  ...pendientes.map(({ relativo }) => `- ${relativo}`),
  '',
  'AVISOS:',
  ...(incidencias.length ? incidencias : ['Ninguno']),
  '',
  'NOTA: Una miniatura puede tener menor resolución que la foto original.',
  'No se elimina ni se sobrescribe ningún archivo existente.'
];
const informe = path.join(raiz, aplicar ? 'informe_recuperacion_fotos.txt' : 'informe_revision_fotos.txt');
fs.writeFileSync(informe, lineas.join('\n'), 'utf8');
console.log(lineas.slice(0, 8).join('\n'));
console.log(`Informe guardado en: ${informe}`);
if (!aplicar) console.log('Para copiar las imágenes detectadas: node recuperar_fotos_miniaturas.cjs --aplicar');
