// Auto health for the Astro site: build artifacts + SEO invariants.
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const required = [
  'dist/index.html',
  'dist/404.html',
  'dist/robots.txt',
  'dist/llms.txt',
  'dist/llms-full.txt',
  'dist/sitemap-index.xml',
  'dist/sitemap-0.xml',
  ...['en', 'ru', 'zh-cn', 'es', 'de'].map((l) => `dist/${l}/index.html`),
  'dist/en/docs/overview/index.html',
  'dist/ru/docs/overview/index.html',
];

const failures = [];
for (const rel of required) {
  if (!existsSync(resolve(root, rel))) failures.push(`missing ${rel}`);
}

const llms = readFileSync(resolve(root, 'dist/llms.txt'), 'utf8');
if (!llms.includes('/en/docs/domain-model/')) failures.push('llms.txt links not site-aware');

const sitemap = readFileSync(resolve(root, 'dist/sitemap-0.xml'), 'utf8');
if ((sitemap.match(/hreflang=/g) ?? []).length < 18) failures.push('sitemap hreflang missing');

const en = readFileSync(resolve(root, 'dist/en/index.html'), 'utf8');
for (const code of ['en', 'ru', 'zh-CN', 'es', 'de', 'x-default']) {
  if (!en.includes(`hreflang="${code}"`)) failures.push(`HTML hreflang ${code} missing`);
}

console.log(failures.length ? `HEALTH FAIL:\n${failures.join('\n')}` : 'HEALTH: PASS (site SEO artifacts)');
process.exit(failures.length ? 1 : 0);