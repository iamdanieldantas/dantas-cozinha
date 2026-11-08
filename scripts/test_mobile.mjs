import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const html = readFileSync('www/index.html', 'utf8');
const data = readFileSync('www/assets/data.js', 'utf8');
const script = readFileSync('www/assets/mobile.js', 'utf8');
for (const asset of ['styles.css', 'data.js', 'app.js', 'mobile.css', 'mobile.js']) {
  assert(existsSync(join('www', 'assets', asset)), 'Arquivo não incluído: ' + asset);
}
assert(html.includes('viewport-fit=cover'), 'Viewport iOS não configurado');
assert(html.includes('assets/mobile.js'), 'Bootstrap mobile ausente');
assert(existsSync('www/privacy.html'), 'Política de privacidade ausente do app');
for (const topic of [
  'Antipasto, entrada, couvert e aperitivo',
  'Contaminação direta dos alimentos',
  'Contaminação cruzada: direta e indireta'
]) assert(data.includes(topic), 'Aula não encontrada no pacote offline: ' + topic);
assert(script.includes('mobile-app-tabs'), 'Navegação ausente');
assert(script.includes('Share'), 'Compartilhamento nativo ausente');
assert(readFileSync('mobile/mobile.js', 'utf8').includes("from '@capacitor/share'"), 'O plugin Share não foi importado');
console.log('Mobile OK: assets, aulas offline, navegação e compartilhamento.');
