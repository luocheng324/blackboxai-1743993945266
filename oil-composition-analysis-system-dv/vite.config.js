import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5300,
    strictPort: true,
    allowedHosts: ['localhost', 'hnvhcq-5219.csb.app']
  }
})