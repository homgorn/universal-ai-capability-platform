// Sync generated wiki content into the Astro site.
// Run from the site/ directory (cwd) to avoid non-ASCII path issues.
import { cpSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';

mkdirSync('src/content/topics', { recursive: true });
cpSync('../wiki/pages', 'src/content/topics', { recursive: true, force: true });
const llms = readFileSync('../wiki/llms.txt', 'utf8');
writeFileSync('public/llms.txt', llms);
const full = readFileSync('../wiki/llms-full.txt', 'utf8');
writeFileSync('public/llms-full.txt', full);
console.log('wiki synced into site/');