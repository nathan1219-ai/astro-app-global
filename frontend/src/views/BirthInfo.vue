<template>
  <div class="wrap">
    <h2>{{ t('birthTitle') }}</h2>
    <div class="row">
      <label>Email</label>
      <input v-model="email" type="email" />
    </div>
    <div class="row">
      <label>{{ t('birthName') }}</label>
      <input v-model="name" />
    </div>
    <div class="row">
      <label>{{ t('birthDate') }}</label>
      <input v-model="birthday" type="date" />
    </div>
    <div class="row">
      <label>{{ t('birthCalendar') }}</label>
      <select v-model="calendar">
        <option value="gregorian">Gregorian</option>
        <option value="lunar">Lunar</option>
      </select>
    </div>
    <div class="row">
      <button class="primary" @click="save">{{ t('continue') }}</button>
      <router-link class="btn" to="/onboarding/push">{{ t('skip') }}</router-link>
    </div>
    <p class="hint">{{ t('gdprHint') }}</p>
  </div>
</template>

<script setup lang="ts">
import http from '../http'
import { useI18n } from 'vue-i18n'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const { t, locale } = useI18n()
const router = useRouter()
const name = ref(localStorage.getItem('name') || 'Explorer')
const birthday = ref(localStorage.getItem('birthday') || '')
const calendar = ref<'gregorian'|'lunar'>((localStorage.getItem('calendar') as any) || 'gregorian')
const email = ref(localStorage.getItem('email') || '')

async function save() {
  if (!birthday.value) return
  const r = await http.post('/calc', { name: name.value, birthday: birthday.value, calendar: calendar.value })
  localStorage.setItem('user_id', String(r.data.user_id))
  localStorage.setItem('name', name.value)
  localStorage.setItem('birthday', birthday.value)
  localStorage.setItem('calendar', calendar.value)
  localStorage.setItem('last_sign', r.data.sign)
  localStorage.setItem('last_zodiac', r.data.zodiac)
  localStorage.setItem('last_element', r.data.element)
  if (localStorage.getItem('token')) {
    await http.post('/profile/lang', { lang: locale.value })
  }
  const q = new URLSearchParams({ sign: r.data.sign, zodiac: r.data.zodiac, element: r.data.element }).toString()
  const target = '/card?' + q
  localStorage.setItem('last_url', target)
  const token = localStorage.getItem('token')
  if (token) { router.push(target); return }
  if (email.value) {
    try { await http.get('/auth/check', { params: { email: email.value } }) } catch {}
    router.push({ path: '/login', query: { email: email.value } })
  } else {
    router.push('/login')
  }
}
</script>

<style scoped>
.wrap { max-width: 520px; margin: 0 auto; display: flex; flex-direction: column; gap: 12px }
.row { display: flex; align-items: center; gap: 12px }
.primary { padding: 8px 12px; background: #222; color: #fff; border-radius: 6px }
.btn { padding: 8px 12px; border: 1px solid #ccc; border-radius: 6px; text-decoration: none }
.hint { font-size: 12px; color: #666 }
</style>
