import fs from "node:fs/promises";
import path from "node:path";
import sharp from "sharp";
import fg from "fast-glob";

const RAIZ = process.cwd();
const CARPETA_CAMISETAS = path.join(RAIZ, "public", "camisetas");

const ANCHO_MAXIMO = 800;
const ALTO_MAXIMO = 1000;
const CALIDAD_WEBP = 85;

console.log("");
console.log("======================================");
console.log("OPTIMIZADOR ELITE JERSEYS");
console.log("======================================");
console.log("Carpeta:", CARPETA_CAMISETAS);
console.log("Buscando imágenes...");
console.log("");

const archivos = await fg(
  ["**/*.png", "**/*.jpg", "**/*.jpeg"],
  {
    cwd: CARPETA_CAMISETAS,
    absolute: true,
    onlyFiles: true,
    followSymbolicLinks: false
  }
);

console.log(`Imágenes encontradas: ${archivos.length}`);
console.log("");

let convertidas = 0;
let omitidas = 0;
let errores = 0;
let ahorroOriginal = 0;
let ahorroWebp = 0;

for (const [indice, archivoOriginal] of archivos.entries()) {
  const parsed = path.parse(archivoOriginal);
  const archivoWebp = path.join(parsed.dir, `${parsed.name}.webp`);

  console.log(
    `[${indice + 1}/${archivos.length}] ${path.relative(
      RAIZ,
      archivoOriginal
    )}`
  );

  try {
    try {
      await fs.access(archivoWebp);
      console.log("   ⏭ Ya existe");
      omitidas++;
      continue;
    } catch {
      // Continúa porque todavía no existe.
    }

    const originalStats = await fs.stat(archivoOriginal);

    await sharp(archivoOriginal, {
      limitInputPixels: false
    })
      .rotate()
      .resize({
        width: ANCHO_MAXIMO,
        height: ALTO_MAXIMO,
        fit: "inside",
        withoutEnlargement: true
      })
      .webp({
        quality: CALIDAD_WEBP,
        effort: 4
      })
      .toFile(archivoWebp);

    const webpStats = await fs.stat(archivoWebp);

    ahorroOriginal += originalStats.size;
    ahorroWebp += webpStats.size;

    const porcentaje = Math.round(
      (1 - webpStats.size / originalStats.size) * 100
    );

    console.log(
      `   ✅ Convertida | ahorro aproximado: ${porcentaje}%`
    );

    convertidas++;
  } catch (error) {
    console.error("   ❌ Error");
    console.error(
      error instanceof Error ? error.message : error
    );
    errores++;
  }
}

const megabytes = (bytes) =>
  (bytes / 1024 / 1024).toFixed(2);

console.log("");
console.log("======================================");
console.log("RESUMEN");
console.log("======================================");
console.log(`✅ Convertidas: ${convertidas}`);
console.log(`⏭ Omitidas: ${omitidas}`);
console.log(`❌ Errores: ${errores}`);

if (convertidas > 0) {
  console.log(
    `📦 Peso original procesado: ${megabytes(ahorroOriginal)} MB`
  );
  console.log(
    `📦 Peso WebP generado: ${megabytes(ahorroWebp)} MB`
  );
}

console.log("");
console.log("Los archivos originales NO se han borrado.");
console.log("");