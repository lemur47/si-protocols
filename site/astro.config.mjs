import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';

export default defineConfig({
  site: 'https://spiritualintelligence.dev',
  build: { format: 'directory' },
  integrations: [svelte()],
});
