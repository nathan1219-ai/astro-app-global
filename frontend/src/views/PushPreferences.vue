<template>
  <div class="wrap">
    <h2>Push Preferences</h2>
    <div class="row">
      <label>Hour</label>
      <input type="number" v-model.number="hour" min="0" max="23" />
    </div>
    <div class="row">
      <label>Enabled</label>
      <input type="checkbox" v-model="enabled" />
    </div>
    <div class="row">
      <label>Language</label>
      <select v-model="language">
        <option value="en">English</option>
        <option value="es">Español</option>
        <option value="fr">Français</option>
      </select>
    </div>
    <button @click="save">Save</button>
    <button @click="loadToday">Load Today</button>
    <button @click="sendToday">Send Today</button>
    <div class="row">
      <label>Token</label>
      <input v-model="token" placeholder="FCM device token" />
      <button @click="register">Register</button>
    </div>
    <div class="row">
      <label>Bulk</label>
      <textarea v-model="bulk" placeholder="one token per line" rows="4"></textarea>
      <button @click="batchRegister">Batch Register</button>
    </div>
    <div class="row">
      <button @click="listTokens">List Tokens</button>
    </div>
    <div v-if="tokens.length">
      <div class="token" v-for="it in tokens" :key="it.token">
        <input type="checkbox" v-model="selected" :value="it.token" />
        <span>{{ it.platform }} · {{ it.language }}</span>
        <code>{{ it.token }}</code>
        <button @click="remove(it.token)">Delete</button>
      </div>
      <div class="row">
        <button @click="batchDelete">Delete Selected</button>
      </div>
    </div>
    <div class="row">
      <button @click="sendDetail">Send Detail</button>
      <button @click="viewDetails">View Details</button>
    </div>
    <div v-if="results.length">
      <div class="token" v-for="r in results" :key="r.token">
        <span>{{ r.ok ? 'OK' : 'FAIL' }}</span>
        <code>{{ r.token }}</code>
        <span>{{ r.id || r.error }}</span>
      </div>
    </div>
    <div class="row">
      <button @click="retryFailed">Retry Failed</button>
    </div>
    <ul v-if="today">
      <li>{{ today.energy }}</li>
      <li>{{ today.social }}</li>
      <li>{{ today.decision }}</li>
      <li>{{ today.relax }}</li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import http from '../http'
import { ref, watch } from 'vue'
const userId = 1
const hour = ref(8)
const enabled = ref(true)
const language = ref('en')
const today = ref<any>(null)
const token = ref('')
const tokens = ref<any[]>([])
const bulk = ref('')
const selected = ref<string[]>([])
const results = ref<any[]>([])

async function save() {
  await http.post('/push/prefs', { user_id: userId, hour: hour.value, enabled: enabled.value, language: language.value })
  localStorage.setItem('push_hour', String(hour.value))
  localStorage.setItem('push_enabled', String(enabled.value))
  localStorage.setItem('push_lang', language.value)
}

async function loadToday() {
  const d = new Date().toISOString().slice(0,10)
  const r = await http.get('/push/today/'+userId, { params: { day: d, language: language.value } })
  today.value = r.data
}

async function register() {
  if (!token.value) return
  await http.post('/push/token', { user_id: userId, token: token.value, platform: 'android', language: language.value })
}

async function sendToday() {
  const d = new Date().toISOString().slice(0,10)
  await http.post('/push/send', { user_id: userId, day: d, language: language.value })
}

async function listTokens() {
  const r = await http.get('/push/tokens/'+userId, { params: { language: language.value } })
  tokens.value = r.data
}

async function remove(tok: string) {
  await http.delete('/push/token', { data: { user_id: userId, token: tok } })
  await listTokens()
}

async function batchRegister() {
  const list = bulk.value.split(/\r?\n/).map(s => s.trim()).filter(Boolean)
  if (!list.length) return
  await http.post('/push/tokens', { user_id: userId, tokens: list, platform: 'android', language: language.value })
  await listTokens()
}

async function batchDelete() {
  if (!selected.value.length) return
  await http.delete('/push/tokens', { data: { user_id: userId, tokens: selected.value } })
  selected.value = []
  await listTokens()
}

async function sendDetail() {
  const d = new Date().toISOString().slice(0,10)
  const r = await http.post('/push/send-detail', { user_id: userId, day: d, language: language.value })
  results.value = r.data.results
}

async function retryFailed() {
  const d = new Date().toISOString().slice(0,10)
  const fails = results.value.filter((x:any) => !x.ok).map((x:any) => x.token)
  if (!fails.length) return
  const r = await http.post('/push/send-detail-tokens', { user_id: userId, day: d, language: language.value, tokens: fails })
  results.value = r.data.results
}

watch(language, async () => {
  await listTokens()
})

async function viewDetails() {
  const f = await http.get('/user/fate/'+userId)
  const q = new URLSearchParams({ sign: f.data.sign, zodiac: f.data.zodiac, element: f.data.element }).toString()
  window.location.href = '/card?'+q
}

;(() => {
  const ph = localStorage.getItem('push_hour')
  const pe = localStorage.getItem('push_enabled')
  const pl = localStorage.getItem('push_lang')
  if (ph) hour.value = Number(ph)
  if (pe) enabled.value = pe === 'true'
  if (pl) language.value = pl
})()
</script>

<style scoped>
.wrap { max-width: 520px; margin: 0 auto; display: flex; flex-direction: column; gap: 12px }
.row { display: flex; align-items: center; gap: 12px }
.token { display: grid; grid-template-columns: auto auto 1fr auto; gap: 8px; align-items: center; border: 1px solid #eee; padding: 8px; border-radius: 6px }
</style>
