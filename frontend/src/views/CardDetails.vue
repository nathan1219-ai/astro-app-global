<template>
  <div class="wrap">
    <h2>Card Details</h2>
  <div class="row">
    <CardCanvas :sign="sign" :zodiac="zodiac" :element="element" :spec="spec" ref="canvasRef" />
  </div>
    <div class="row">
      <label>Decoration</label>
      <select v-model="decorationSel">
        <option v-for="d in decorations" :key="d" :value="d">{{ d }}</option>
      </select>
      <label>Glow</label>
      <select v-model="glowSel">
        <option v-for="g in glows" :key="g" :value="g">{{ g }}</option>
      </select>
      <button @click="applyMaterialsSel">Apply</button>
      <button v-if="credits>0" class="primary" @click="consumeCredit">Generate Premium Free ({{ credits }})</button>
    </div>
    <SharePanel :sign="sign" :zodiac="zodiac" :element="element" :energy="expanded.energy_state || ''" :getImage="getImage" :getImageFor="getImageFor" />
    <div class="grid">
      <div>
        <h3>Energy State</h3>
        <p>{{ expanded.energy_state }}</p>
        <button class="link" @click="goLine('energy')">View Energy Detail</button>
      </div>
      <div>
        <h3>Action</h3>
        <p>{{ expanded.action_suggestions }}</p>
        <button class="link" @click="goLine('social')">View Social Guidance</button>
      </div>
      <div>
        <h3>Exploration</h3>
        <p>{{ expanded.self_exploration }}</p>
        <button class="link" @click="goLine('relax')">View Relaxation Tips</button>
      </div>
    </div>
    <div class="grid" v-if="freePack">
      <div>
        <h3>Love</h3>
        <p>{{ freePack.love }}</p>
      </div>
      <div>
        <h3>Career</h3>
        <p>{{ freePack.career }}</p>
      </div>
      <div>
        <h3>Wealth</h3>
        <p>{{ freePack.wealth }}</p>
      </div>
      <div>
        <h3>Health</h3>
        <p>{{ freePack.health }}</p>
      </div>
      <div>
        <h3>Energy</h3>
        <p>{{ freePack.energy_state }}</p>
        <button class="link" @click="goLine('energy')">View Energy Detail</button>
      </div>
    </div>
    <div class="grid" v-if="premiumPack">
      <div>
        <h3>Monthly Trend</h3>
        <p>{{ premiumPack.monthly_trend }}</p>
      </div>
      <div>
        <h3>Balancing Advice</h3>
        <p>{{ premiumPack.balancing_advice }}</p>
      </div>
      <div>
        <h3>Social Fit</h3>
        <p>{{ premiumPack.social_fit }}</p>
        <button class="link" @click="goLine('social')">View Social Guidance</button>
      </div>
    </div>
    <div class="row">
      <button class="link" @click="goLine('decision')">View Decision Advice</button>
      <button class="link" @click="goLine('relax')">View Relaxation Tips</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useRouter } from 'vue-router'
import CardCanvas from '../components/CardCanvas.vue'
import SharePanel from '../components/SharePanel.vue'
import http from '../http'
import { getCardSpec, applyMaterials } from '../cardSpec'
import { useI18n } from 'vue-i18n'

const route = useRoute()
const router = useRouter()
const { t } = useI18n()
const sign = ref(String(route.query.sign||'白羊座'))
const zodiac = ref(String(route.query.zodiac||'龙'))
const element = ref(String(route.query.element||'木'))
const spec = ref(getCardSpec(sign.value, zodiac.value, element.value))
const canvasRef = ref<any>(null)
const expanded = ref<any>({})
const freePack = ref<any>(null)
const premiumPack = ref<any>(null)
const decorations = ref<string[]>([])
const glows = ref<string[]>([])
const decorationSel = ref('')
const glowSel = ref('')
const credits = ref(0)

async function load() {
  const lang = localStorage.getItem('lang') || 'en'
  const e = await http.get('/card/details', { params: { sign: sign.value, zodiac: zodiac.value, element: element.value, language: lang } })
  expanded.value = e.data
  const uid = Number(localStorage.getItem('user_id')||'1')
  const m = await http.get('/membership/'+uid)
  freePack.value = (await http.get('/card/free-pack', { params: { user_id: uid, sign: sign.value, zodiac: zodiac.value, element: element.value, language: lang } })).data
  if (m.data.level && m.data.level.toLowerCase() !== 'free') {
    spec.value = getCardSpec(sign.value, zodiac.value, element.value, 'premium')
    premiumPack.value = (await http.get('/card/premium-pack', { params: { user_id: uid, sign: sign.value, zodiac: zodiac.value, element: element.value, material: 'rose', language: lang } })).data
  }
  try {
    const p = await http.get('/share/permissions/'+uid)
    const decs = JSON.parse(p.data.decorations || '[]')
    const gls = JSON.parse(p.data.glow || '[]')
    decorations.value = decs
    glows.value = gls
    credits.value = Number(p.data.credits || 0)
  } catch {}
}

onMounted(load)

function getImage() {
  return canvasRef.value?.export('image/jpeg')
}

function getImageFor(type: string, w: number, h: number, mode?: string, quality?: number) {
  return canvasRef.value?.exportSized(type, w, h, mode, quality)
}

function goLine(type: string) {
  const q = new URLSearchParams({ sign: sign.value, zodiac: zodiac.value, element: element.value, type }).toString()
  router.push('/card/line?'+q)
}

function applyMaterialsSel() {
  spec.value = applyMaterials(getCardSpec(sign.value, zodiac.value, element.value), decorationSel.value, glowSel.value)
}

async function consumeCredit() {
  const uid = Number(localStorage.getItem('user_id')||'1')
  const r = await http.post('/share/consume-credit', { user_id: uid })
  credits.value = Number(r.data.credits_left || 0)
  spec.value = getCardSpec(sign.value, zodiac.value, element.value, 'premium')
  try {
    const url = getImage() || ''
    if (url) {
      const a = document.createElement('a')
      a.href = url
      a.download = 'premium-card.jpg'
      a.click()
    }
  } catch {}
  alert(t('genSuccess'))
}
</script>

<style scoped>
.wrap { max-width: 900px; margin: 0 auto; display: flex; flex-direction: column; gap: 16px }
.row { display: flex; justify-content: center }
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px }
p { white-space: pre-wrap }
button.link { background: none; border: none; color: #0066cc; cursor: pointer; padding: 0; }
</style>
