// Sync generated wiki content into the Astro site.
import { cpSync, mkdirSync } from 'node:fs';
import { resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..', '..');
mkdirSync(resolve(root, 'site/src/content/topics'), { recursive: true });
cpSync(resolve(root, 'wiki/pages'), resolve(root, 'site/src/content/topics'), { recursive: true, force: true });
cpSync(resolve(root, 'wiki/llms.txt'), resolve(root, 'site/public/llms.txt'));
cpSync(resolve(root, 'wiki/llms-full.txt'), resolve(root, 'site/public/llms-full.txt'));
console.log('wiki synced into site/');