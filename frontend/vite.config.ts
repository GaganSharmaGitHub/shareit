import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';
import { viteSingleFile } from 'vite-plugin-singlefile';
export default defineConfig({
  plugins: [svelte({
    experimental: {
      // @ts-ignore
      useVitePreprocess: true
    }
  }), viteSingleFile()],

  build: {
    target: 'esnext',
    assetsInlineLimit: 100000000, // large enough to inline all assets
    cssCodeSplit: false,          // avoid separate CSS files
    outDir: '../public/'
  }
});
