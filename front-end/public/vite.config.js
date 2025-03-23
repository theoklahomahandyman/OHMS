import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    cssCodeSplit: true,
    rollupOptions: {
      output: {
        manualChunks: (id) => {
          if (id.includes('node_modules')) {
            if (id.includes('react-bootstrap')) return 'react-bootstrap';
            if (id.includes('bootstrap')) return 'bootstrap';
            if (id.includes('react-icons')) return 'react-icons';
            return 'vendor';
          }
        },
        entryFileNames: `[name].[hash].js`,
        chunkFileNames: `[name].[hash].js`,
        assetFileNames: `[name].[hash].[ext]`
      }
    },
    brotliSize: true,
    chunkSizeWarningLimit: 1000
  }
});
