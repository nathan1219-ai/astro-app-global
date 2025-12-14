<template>
  <div class="wrap">
    <h2>{{ t('pushConsentTitle') }}</h2>
    <p>{{ t('pushConsentDesc') }}</p>
    <div class="row">
      <button class="primary" @click="allow">{{ t('pushAllow') }}</button>
      <button @click="decline">{{ t('pushDecline') }}</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import http from '../http'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
const { t, locale } = useI18n()
const router = useRouter()
function uid() { return Number(localStorage.getItem('user_id')||'1') }
async function allow() {
  await http.post('/push/prefs', { user_id: uid(), hour: 8, enabled: true, language: locale.value })
  router.push('/push')
}
async function decline() {
  await http.post('/push/prefs', { user_id: uid(), hour: 8, enabled: false, language: locale.value })
  router.push('/')
}
</script>

<style scoped>
.wrap { max-width: 520px; margin: 0 auto; display: flex; flex-direction: column; gap: 12px }
.row { display: flex; gap: 12px }
.primary { padding: 8px 12px; background: #222; color: #fff; border-radius: 6px }
</style>
