<template>
  <div class="wrap">
    <h2>Membership</h2>
    <div class="row">
      <label>Level</label>
      <select v-model="level">
        <option value="free">Free</option>
        <option value="Premium">Premium</option>
        <option value="VIP">VIP</option>
      </select>
      <button @click="upgrade">Upgrade</button>
      <button @click="pay">Pay</button>
      <button @click="payPaypal">PayPal</button>
    </div>
    <p v-if="info">Current: {{ info.level }} {{ info.expires_at ? '('+info.expires_at+')' : '' }}</p>
    <div class="row">
      <label>Price ID</label>
      <input v-model="priceId" placeholder="price_..." />
    </div>
    <div class="benefits">
      <p>{{ t('membershipBenefits') }}</p>
      <div class="row">
        <button @click="shareBenefits">Share Benefits</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import http from '../http'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
const userId = 1
const level = ref('Premium')
const info = ref<any>(null)
const months = ref(1)
const priceId = ref('')

async function upgrade() {
  await http.post('/membership/upgrade', { user_id: userId, level: level.value, months: 1 })
  await load()
}

async function load() {
  const r = await http.get('/membership/'+userId)
  info.value = r.data
}

async function pay() {
  const r = await http.post('/pay/stripe/checkout', { user_id: userId, level: level.value, months: months.value, success_base: window.location.origin + '/membership', cancel_url: window.location.origin + '/membership', price_id: priceId.value || null })
  window.location.href = r.data.url
}

const route = useRoute()
onMounted(async () => {
  await load()
  const qs = route.query as any
  if (qs.session_id && qs.user_id && qs.level) {
    try {
      await http.get('/pay/stripe/confirm', { params: { session_id: qs.session_id, user_id: Number(qs.user_id), level: String(qs.level), months: Number(qs.months || 1) } })
      await load()
    } catch {}
  }
  if (qs.token) {
    try {
      await http.get('/pay/paypal/capture', { params: { order_id: String(qs.token), user_id: userId, level: level.value, months: months.value } })
      await load()
    } catch {}
  }
})

async function payPaypal() {
  const base = window.location.origin + '/membership'
  const r = await http.post('/pay/paypal/order', { user_id: userId, level: level.value, months: months.value, return_url: base, cancel_url: base })
  window.location.href = r.data.url
}

async function shareBenefits() {
  const lang = localStorage.getItem('lang') || 'en'
  try {
    const s = await http.post('/share/shorten', { sign: '白羊座', zodiac: '龙', element: '木', language: lang })
    await navigator.clipboard.writeText(s.data.short_url)
  } catch {}
  const r = await http.post('/share/membership-share', { user_id: userId, language: lang })
  alert(r.data.message || 'Shared')
}
</script>

<style scoped>
.wrap { max-width: 520px; margin: 0 auto; display: flex; flex-direction: column; gap: 12px }
.row { display: flex; align-items: center; gap: 12px }
.benefits { border: 1px dashed #ccc; padding: 12px; border-radius: 6px }
</style>
