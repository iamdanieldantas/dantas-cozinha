import { existsSync, readFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import sharp from 'sharp';

const root = resolve('.');
const iconFolder = join(root, 'ios', 'App', 'App', 'Assets.xcassets', 'AppIcon.appiconset');
const contentsFile = join(iconFolder, 'Contents.json');
const logo = join(root, 'assets', 'logo-mark.svg');

if (!existsSync(contentsFile)) {
  throw new Error('Projeto iOS ainda não existe. Execute npm run ios:add antes de gerar ícones.');
}
const rawSvg = readFileSync(logo, 'utf8');
const fullBleedSvg = rawSvg.replace(
  /<rect x="1" y="1" width="94" height="94" rx="25" fill="#254735"\/>/,
  '<rect x="0" y="0" width="96" height="96" fill="#254735"/>'
);
if (fullBleedSvg === rawSvg) throw new Error('Não foi possível preparar o fundo opaco do logo.');
const metadata = JSON.parse(readFileSync(contentsFile, 'utf8'));
let produced = 0;
for (const image of metadata.images || []) {
  if (!image.filename) continue;
  const size = Number((image.size || '1024x1024').split('x')[0]);
  const scale = Number(String(image.scale || '1x').replace('x', ''));
  const px = Math.round(size * scale);
  if (!Number.isInteger(px) || px < 16 || px > 2048) throw new Error('Tamanho de ícone inválido: ' + px);
  await sharp(Buffer.from(fullBleedSvg)).resize(px, px).png().toFile(join(iconFolder, image.filename));
  produced++;
}
if (!produced) throw new Error('Nenhum ícone configurado no catálogo do Xcode.');
console.log('Ícones iOS gerados do logo existente: ' + produced);
