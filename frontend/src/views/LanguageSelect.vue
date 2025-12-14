<template>
  <div class="wrap">
    <h2>{{ t('selectLanguage') }}</h2>
    <div class="grid">
      <button v-for="l in langs" :key="l.code" :class="{ active: l.code===sel }" @click="sel=l.code">{{ l.name }}</button>
    </div>
    <div class="row">
      <button :disabled="!sel" @click="save">{{ t('continue') }}</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import http from '../http'
import { useI18n } from 'vue-i18n'
import { ref } from 'vue'
const { t, locale } = useI18n()
const langs = [
  { code: 'en', name: 'English' },
  { code: 'es', name: 'Español' },
  { code: 'fr', name: 'Français' },
  { code: 'de', name: 'Deutsch' },
  { code: 'it', name: 'Italiano' },
  { code: 'pt', name: 'Português (BR)' },
  { code: 'ru', name: 'Русский' },
]
const sel = ref('')

async function save() {
  if (!sel.value) return
  localStorage.setItem('lang', sel.value)
  locale.value = sel.value
  try { await http.post('/profile/lang', { lang: sel.value }) } catch {}
}
</script>

<style scoped>
.wrap { max-width: 520px; margin: 0 auto; display: flex; flex-direction: column; gap: 12px }
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px }
.row { display: flex; justify-content: center }
button.active { border: 2px solid #333 }
</style>
