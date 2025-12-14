<template>
  <div class="wrap">
    <h1>{{ t('title') }}</h1>
    <div class="card" @click="flip = !flip" :class="{ flip }">
      <CardCanvas :sign="sign" :zodiac="zodiac" :element="element" :back="flip" :backLines="backLines" ref="canvasRef" @lineClick="goDetail" />
    </div>
    <div class="toolbar">
      <button @click="download('image/webp')">{{ t('exportWebp') }}</button>
      <button @click="download('image/jpeg')">{{ t('exportJpg') }}</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import CardCanvas from '../components/CardCanvas.vue'
import { calcFate } from '../api'
import http from '../http'

const { t } = useI18n()
const flip = ref(false)
const sign = ref('白羊座')
const zodiac = ref('龙')
const element = ref('木')
const canvasRef = ref<any>(null)
const backLines = ref<string[]>([])

onMounted(async () => {
  try {
    const r = await calcFate('Demo', '2024-02-10')
    sign.value = r.sign
    zodiac.value = r.zodiac
    element.value = r.element
    const d = await http.get('/bedrock/test', { params: { sign: r.sign, zodiac: r.zodiac, element: r.element, language: 'en' } })
    backLines.value = [d.data.energy, d.data.social, d.data.decision, d.data.relax]
  } catch {}
})

function download(type: string) {
  const url = canvasRef.value.export(type)
  const a = document.createElement('a')
  a.href = url
  a.download = type === 'image/webp' ? 'card.webp' : 'card.jpg'
  a.click()
}

function goDetail(type: string) {
  const q = new URLSearchParams({ sign: sign.value, zodiac: zodiac.value, element: element.value, type }).toString()
  window.location.href = '/card/line?'+q
}
</script>

<style scoped>
.wrap { display: flex; flex-direction: column; align-items: center; gap: 12px; }
.card { width: 320px; height: 400px; perspective: 1000px; }
.card.flip canvas { transform: rotateY(180deg); }
.toolbar { display: flex; gap: 12px; }
</style>
