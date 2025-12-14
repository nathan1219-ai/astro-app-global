<template>
  <div class="wrap">
    <h2>Login</h2>
    <div class="row">
      <label>Email</label>
      <input v-model="email" type="email" />
    </div>
    <div class="row">
      <label>Password</label>
      <input v-model="password" type="password" />
    </div>
    <div class="row">
      <input id="agree" type="checkbox" v-model="agree" />
      <label for="agree">I agree to the <a href="/terms" target="_blank">Terms of Service</a> and <a href="/privacy" target="_blank">Privacy Policy</a></label>
    </div>
    <div class="row">
      <button :disabled="!agree" @click="register">Register</button>
      <button :disabled="!agree" @click="login">Login</button>
    </div>
    <div class="row">
      <div id="gbtn"></div>
      <button @click="appleLogin">Continue with Apple</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import http from '../http'
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
const email = ref('')
const password = ref('')
const agree = ref(false)
const googleClientId = (import.meta as any).env?.VITE_GOOGLE_CLIENT_ID || ''
const route = useRoute()
const router = useRouter()
const exists = ref<boolean | null>(null)

async function register() {
  const r = await http.post('/auth/register', { email: email.value, password: password.value })
  localStorage.setItem('token', r.data.token)
  if (agree.value) {
    try { await http.post('/profile/consent', { consent: true }) } catch {}
  }
  await syncLang()
  await postLoginRedirect()
}

async function login() {
  const r = await http.post('/auth/login', { email: email.value, password: password.value })
  localStorage.setItem('token', r.data.token)
  if (agree.value) {
    try { await http.post('/profile/consent', { consent: true }) } catch {}
  }
  await syncLang()
  await postLoginRedirect()
}

function loadGoogle() {
  if (!googleClientId) return
  const s = document.createElement('script')
  s.src = 'https://accounts.google.com/gsi/client'
  s.async = true
  s.onload = () => {
    // @ts-ignore
    google.accounts.id.initialize({ client_id: googleClientId, callback: async (resp:any) => {
      const idt = resp.credential
      const r = await http.post('/auth/oauth/google', { id_token: idt })
      localStorage.setItem('token', r.data.token)
      await syncLang()
      await postLoginRedirect()
    } })
    // @ts-ignore
    google.accounts.id.renderButton(document.getElementById('gbtn'), { theme: 'outline', size: 'large' })
  }
  document.head.appendChild(s)
}

async function appleLogin() {
  const idt = prompt('Paste Apple ID token') || ''
  if (!idt) return
  const r = await http.post('/auth/oauth/apple', { id_token: idt })
  localStorage.setItem('token', r.data.token)
  await syncLang()
  await postLoginRedirect()
}

onMounted(loadGoogle)

onMounted(async () => {
  const qemail = String(route.query.email || '')
  if (qemail) {
    email.value = qemail
    try { const r = await http.get('/auth/check', { params: { email: qemail } }); exists.value = !!r.data.exists } catch { exists.value = null }
  }
  if (!email.value) {
    const le = localStorage.getItem('email')
    if (le) email.value = le
  }
})

async function postLoginRedirect() {
  const last = localStorage.getItem('last_url')
  if (last && !/\/login$/.test(last)) { router.push(last); return }
  const uid = Number(localStorage.getItem('user_id')||'0')
  if (uid) {
    try { const f = await http.get('/user/fate/'+uid); const q = new URLSearchParams({ sign: f.data.sign, zodiac: f.data.zodiac, element: f.data.element }).toString(); router.push('/card?'+q); return } catch {}
  }
  router.push('/')
}

async function syncLang() {
  const lang = localStorage.getItem('lang') || 'en'
  try { await http.post('/profile/lang', { lang }) } catch {}
  if (email.value) localStorage.setItem('email', email.value)
}
</script>

<style scoped>
.wrap { max-width: 420px; margin: 0 auto; display: flex; flex-direction: column; gap: 12px }
.row { display: flex; align-items: center; gap: 12px }
</style>
