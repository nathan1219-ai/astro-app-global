<template>
  <div class="wrap">
    <h2>Card Admin</h2>
    <div class="row">
      <label>Sign</label>
      <input v-model="sign" />
      <label>Zodiac</label>
      <input v-model="zodiac" />
      <label>Element</label>
      <select v-model="element">
        <option>木</option>
        <option>火</option>
        <option>土</option>
        <option>金</option>
        <option>水</option>
      </select>
      <label>Membership</label>
      <select v-model="membership">
        <option value="free">free</option>
        <option value="premium">premium</option>
      </select>
    </div>
    <div class="grid">
      <div class="box">
        <h3>Background</h3>
        <div class="row">
          <label>Noise Density</label><input type="number" step="0.01" v-model.number="spec.background.noiseDensity" />
          <label>Noise Alpha</label><input type="number" step="0.01" v-model.number="spec.background.noiseAlpha" />
        </div>
      </div>
      <div class="box">
        <h3>Decorations</h3>
        <div class="row">
          <label>Type</label><select v-model="spec.decorations.type"><option>spark</option><option>flame</option></select>
          <label>Density</label><input type="number" step="0.01" v-model.number="spec.decorations.density" />
          <label>SizeMin</label><input type="number" v-model.number="spec.decorations.sizeMin" />
          <label>SizeMax</label><input type="number" v-model.number="spec.decorations.sizeMax" />
          <label>Alpha</label><input type="number" step="0.01" v-model.number="spec.decorations.alpha" />
        </div>
      </div>
      <div class="box">
        <h3>Main</h3>
        <div class="row">
          <label>Metal</label>
          <select v-model="metalName">
            <option value="brass">brass</option>
            <option value="rose">rose</option>
            <option value="silver">silver</option>
            <option value="black">black</option>
          </select>
          <label>Symbol</label><input v-model="spec.main.symbol" />
        </div>
        <div class="row">
          <label>Highlight x1</label><input type="number" v-model.number="spec.main.highlight.x1" />
          <label>x2</label><input type="number" v-model.number="spec.main.highlight.x2" />
          <label>y1</label><input type="number" v-model.number="spec.main.highlight.y1" />
          <label>y2</label><input type="number" v-model.number="spec.main.highlight.y2" />
        </div>
      </div>
      <div class="box">
        <h3>Glow</h3>
        <div class="row">
          <label>Color</label><input v-model="spec.glow.color" />
          <label>Inner</label><input type="number" v-model.number="spec.glow.inner" />
          <label>Outer</label><input type="number" v-model.number="spec.glow.outer" />
          <label>Pulse</label><input type="number" step="0.01" v-model.number="spec.glow.pulse" />
        </div>
      </div>
      <div class="box">
        <h3>Border</h3>
        <div class="row">
          <label>Color</label><input v-model="spec.border.color" />
          <label>Shadow</label><input type="number" v-model.number="spec.border.shadow" />
          <label>StudsX</label><input type="number" v-model.number="spec.border.studsX" />
          <label>StudsY</label><input type="number" v-model.number="spec.border.studsY" />
        </div>
      </div>
    </div>
    <div class="row">
      <button @click="apply">Apply</button>
      <button @click="save">Save</button>
      <button @click="exportJson">Export JSON</button>
      <input type="file" @change="importJson" />
    </div>
    <div class="preview">
      <CardCanvas :sign="sign" :zodiac="zodiac" :element="element" :spec="spec" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import CardCanvas from '../components/CardCanvas.vue'
import { getCardSpec, setOverride, saveOverrides } from '../cardSpec'
import { messages } from '../messages'

const sign = ref('白羊座')
const zodiac = ref('龙')
const element = ref('木')
const membership = ref<'free'|'premium'>('free')
const spec = ref(getCardSpec(sign.value, zodiac.value, element.value, membership.value))
const metalName = ref('brass')

watch([sign, zodiac, element, membership], () => {
  spec.value = getCardSpec(sign.value, zodiac.value, element.value, membership.value)
}, { immediate: true })

watch(metalName, () => {
  const m = {
    brass: ['#a67c52','#d4af37','#a67c52'],
    rose: ['#a15d5d','#d79a8b','#a15d5d'],
    silver: ['#9ea7b0','#d0d3d6','#9ea7b0'],
    black: ['#2b2b2b','#4b4b4b','#2b2b2b']
  }[metalName.value]
  spec.value.main.metal = m
})

function apply() {
  setOverride(sign.value, zodiac.value, element.value, membership.value, spec.value)
}

function save() {
  saveOverrides()
}

function exportJson() {
  const s = localStorage.getItem('card_overrides') || '{}'
  const blob = new Blob([s], { type: 'application/json' })
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  a.download = 'card_overrides.json'
  a.click()
}

function importJson(e: any) {
  const f = e.target.files?.[0]
  if (!f) return
  const r = new FileReader()
  r.onload = () => {
    try {
      localStorage.setItem('card_overrides', String(r.result))
      location.reload()
    } catch {}
  }
  r.readAsText(f)
}
</script>

<style scoped>
.wrap { max-width: 980px; margin: 0 auto; display: flex; flex-direction: column; gap: 12px }
.row { display: flex; align-items: center; gap: 12px; flex-wrap: wrap }
.grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px }
.box { border: 1px solid #eee; border-radius: 8px; padding: 12px }
.preview { display: flex; justify-content: center; padding: 12px }
input, select { padding: 6px }
button { padding: 8px 12px }
</style>
