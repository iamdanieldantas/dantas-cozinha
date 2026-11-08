import { cpSync, existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { buildSync } from 'esbuild';
import { fileURLToPath } from 'node:url';
import { dirname, join, resolve } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const webDir = join(root, 'www');
const indexPath = join(root, 'index.html');
const assetsPath = join(root, 'assets');

if (!existsSync(indexPath) || !existsSync(assetsPath)) {
  throw new Error('O site precisa ter index.html e assets/ antes de gerar o aplicativo.');
}
rmSync(webDir, { recursive: true, force: true });
mkdirSync(webDir, { recursive: true });
cpSync(assetsPath, join(webDir, 'assets'), { recursive: true });
cpSync(join(root, 'mobile', 'mobile.css'), join(webDir, 'assets', 'mobile.css'));
buildSync({
  entryPoints: [join(root, 'mobile', 'mobile.js')],
  outfile: join(webDir, 'assets', 'mobile.js'),
  bundle: true,
  platform: 'browser',
  format: 'iife',
  target: 'es2020'
});

let html = readFileSync(indexPath, 'utf8');
if (!html.includes('</head>') || !html.includes('</body>')) {
  throw new Error('Estrutura HTML incompatível com a geração do aplicativo.');
}
html = html.replace('width=device-width,initial-scale=1', 'width=device-width,initial-scale=1,viewport-fit=cover');
html = html.replace('</head>', '  <meta name="apple-mobile-web-app-capable" content="yes">\n  <link rel="stylesheet" href="assets/mobile.css">\n</head>');
html = html.replace('</body>', '  <script defer src="assets/mobile.js"></script>\n</body>');
writeFileSync(join(webDir, 'index.html'), html);
console.log('App web preparado em www/; receitas e aulas incluídas offline.');
