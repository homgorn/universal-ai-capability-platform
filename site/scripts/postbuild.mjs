// Post-build SEO fixes: hreflang in sitemap + site-aware llms.txt links.
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const site = 'https://uacp-site.rvcdax.workers.dev';

// 1. sitemap hreflang for landing pages
const mapPath = resolve(root, 'dist/sitemap-0.xml');
let xml = readFileSync(mapPath, 'utf8');
const tags = { en: 'en', ru: 'ru', 'zh-cn': 'zh-CN', es: 'es', de: 'de' };
xml = xml.replace(/<url><loc>([^<]+)<\/loc><\/url>/g, (_match, loc) => {
  const path = new URL(loc).pathname;
  const found = path.match(/^\/(en|ru|zh-cn|es|de)\/$/);
  if (!found) return `<url><loc>${loc}</loc></url>`;
  const alts = Object.entries(tags)
    .map(([slug, code]) => `<xhtml:link rel="alternate" hreflang="${code}" href="${site}/${slug}/"/>`)
    .join('');
  return `<url><loc>${loc}</loc>${alts}<xhtml:link rel="alternate" hreflang="x-default" href="${site}/en/"/></url>`;
});
writeFileSync(mapPath, xml);

// 2. llms.txt links -> real documentation routes
const llmsPath = resolve(root, 'public/llms.txt');
let llms = readFileSync(llmsPath, 'utf8');
llms = llms.replace(/\]\(pages\/([a-z-]+)\.md\)/g, `](${site}/en/docs/$1/)`);
writeFileSync(resolve(root, 'dist/llms.txt'), llms);

console.log('postbuild SEO fixes applied');