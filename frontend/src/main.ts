import { createApp } from 'vue'
import { createI18n } from 'vue-i18n'
import App from './App.vue'
import { messages } from './messages'
import { router } from './router'

function pickLocale() {
  const saved = localStorage.getItem('lang')
  if (saved) return saved
  const nav = navigator.language || 'en'
  if (nav.startsWith('es')) return 'es'
  if (nav.startsWith('fr')) return 'fr'
  if (nav.startsWith('de')) return 'de'
  if (nav.startsWith('it')) return 'it'
  if (nav.startsWith('pt')) return 'pt'
  if (nav.startsWith('ru')) return 'ru'
  return 'en'
}
const i18n = createI18n({ legacy: false, locale: pickLocale(), messages })

createApp(App).use(i18n).use(router).mount('#app')
