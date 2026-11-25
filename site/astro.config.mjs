import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://uacp-site.rvcdax.workers.dev',
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ru', 'zh-cn', 'es', 'de'],
    routing: { prefixDefaultLocale: true },
  },
  integrations: [sitemap()],
  build: { format: 'directory' },
});