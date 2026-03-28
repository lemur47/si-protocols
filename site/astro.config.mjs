import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://spiritualintelligence.dev',
  build: { format: 'directory' },
  integrations: [svelte(), sitemap()],
});
