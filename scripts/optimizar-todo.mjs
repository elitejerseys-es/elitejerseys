import fs from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';
const base=process.cwd();
const dir=path.join(base,'public','camisetas');
const thumbs=path.join(base,'public','miniaturas');
let count=0, before=0, after=0, errors=0, thumbsMade=0;
async function walk(folder){
 for(const entry of await fs.readdir(folder,{withFileTypes:true})){
  const p=path.join(folder,entry.name);
  if(entry.isDirectory()){await walk(p);continue;}
  if(!entry.name.toLowerCase().endsWith('.webp'))continue;
  try{
   const input=await fs.readFile(p);before+=input.length;
   const img=sharp(input,{limitInputPixels:100000000}).rotate();
   const optimized=await img.resize({width:1200,height:1500,fit:'inside',withoutEnlargement:true}).webp({quality:80,effort:2}).toBuffer();
   if(optimized.length<input.length){await fs.writeFile(p,optimized);after+=optimized.length;}else after+=input.length;
   if(entry.name.toLowerCase()==='01.webp'){
    const relative=path.relative(dir,path.dirname(p));const target=path.join(thumbs,relative,'01.webp');
    await fs.mkdir(path.dirname(target),{recursive:true});
    const t=await sharp(optimized.length<input.length?optimized:input).resize({width:360,height:450,fit:'inside',withoutEnlargement:true}).webp({quality:73,effort:2}).toBuffer();
    await fs.writeFile(target,t);thumbsMade++;
   }
   count++;if(count%100===0)console.log(`Procesadas ${count} imágenes`);
  }catch(e){errors++;console.error('Error',p,e.message);}
 }
}
await walk(dir);
console.log(`Listo: ${count} fotos, ${thumbsMade} miniaturas, ${errors} errores.`);
console.log(`Peso originales: ${(before/1048576).toFixed(1)} MB; optimizados: ${(after/1048576).toFixed(1)} MB`);
