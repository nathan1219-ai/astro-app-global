<template>
  <div class="wrap">
    <h2>{{ title }}</h2>
    <p class="meta">{{ sign }} / {{ zodiac }} · {{ element }}</p>
    <p class="detail">{{ detail }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import http from '../http'
const route = useRoute()
const sign = ref(String(route.query.sign||''))
const zodiac = ref(String(route.query.zodiac||''))
const element = ref(String(route.query.element||''))
const type = String(route.query.type||'energy')
const detail = ref('')
const titleMap: Record<string,string> = { energy: 'Energy Detail', social: 'Social Guidance', decision: 'Decision Advice', relax: 'Relaxation Tips' }
const title = ref(titleMap[type]||'Detail')

async function load() {
  const lang = localStorage.getItem('lang') || 'en'
  const r = await http.get('/card/line-detail', { params: { sign: sign.value, zodiac: zodiac.value, element: element.value, line_type: type, language: lang } })
  detail.value = r.data.detail
}

onMounted(load)
</script>

<style scoped>
.wrap { max-width: 820px; margin: 0 auto; display: flex; flex-direction: column; gap: 12px }
.meta { color: #666 }
.detail { white-space: pre-wrap; line-height: 1.6 }
</style>
