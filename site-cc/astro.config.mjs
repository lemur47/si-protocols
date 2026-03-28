import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://spiritualintelligence.cc',
  build: { format: 'directory' },
  integrations: [sitemap()],
});
