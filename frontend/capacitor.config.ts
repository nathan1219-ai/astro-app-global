import { CapacitorConfig } from '@capacitor/cli'

const config: CapacitorConfig = {
  appId: 'com.cosmictotem.arcana',
  appName: 'Cosmic Totem Arcana',
  webDir: 'dist',
  server: {
    androidScheme: 'https'
  }
}

export default config
