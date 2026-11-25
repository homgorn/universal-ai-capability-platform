// Submit sitemap URLs to IndexNow (Bing, Yandex, Seznam, etc.).
// Run after build/deploy: npm run indexnow
import { readFileSync } from 'node:fs';

const KEY = 'd4f8a9c2e7b14a6b8f0c3d5e7a9b1c24';
const HOST = 'uacp-site.rvcdax.workers.dev';
const xml = readFileSync('dist/sitemap-0.xml', 'utf8');
const urls = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);

if (!urls.length) {
  console.error('No URLs found in dist/sitemap-0.xml');
  process.exit(1);
}

const response = await fetch('https://api.indexnow.org/indexnow', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json; charset=utf-8' },
  body: JSON.stringify({ host: HOST, key: KEY, keyLocation: `https://${HOST}/${KEY}.txt`, urlList: urls }),
});

console.log(`IndexNow: HTTP ${response.status} for ${urls.length} URLs`);
if (!response.ok) {
  console.error(await response.text());
  process.exit(1);
}