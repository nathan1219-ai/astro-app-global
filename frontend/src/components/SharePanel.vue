<template>
  <div class="panel">
    <div class="row">
      <label>Style</label>
      <select v-model="style">
        <option value="fun">Fun</option>
        <option value="healing">Healing</option>
        <option value="explore">Explore</option>
      </select>
      <label>Platform</label>
      <select v-model="platform">
        <option value="ins">Instagram</option>
        <option value="tiktok">TikTok</option>
        <option value="fb">Facebook</option>
      </select>
    </div>
    <div class="row">
      <button @click="copyText">Copy Text</button>
      <button @click="exportImg">Export Image</button>
      <button @click="shareNative">Share</button>
    </div>
    <div class="row">
      <button @click="expIns">Export Instagram</button>
      <button @click="expTiktok">Export TikTok</button>
      <button @click="expFb">Export Facebook</button>
      <button @click="expWa">Export WhatsApp</button>
    </div>
    <textarea v-model="text" rows="6"></textarea>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import http from '../http'
import { buildShareText } from '../share'
import http from '../http'
const props = defineProps<{ sign: string; zodiac: string; element: string; energy: string; getImage: () => string; getImageFor?: (type:string,w:number,h:number,mode?:string,quality?:number)=>string|undefined }>()
const style = ref<'fun'|'healing'|'explore'>('explore')
const platform = ref<'ins'|'tiktok'|'fb'>('ins')
const text = ref('')

function build() {
  const lang = localStorage.getItem('lang') || 'en'
  const link = `${location.origin}/card?sign=${encodeURIComponent(props.sign)}&zodiac=${encodeURIComponent(props.zodiac)}&element=${encodeURIComponent(props.element)}`
  text.value = buildShareText(style.value, platform.value, lang, props.sign, props.zodiac, props.element, props.energy, link)
  try {
    http.post('/share/shorten', { sign: props.sign, zodiac: props.zodiac, element: props.element, language: lang }).then(r => {
      const shortUrl = r.data.short_url || link
      text.value = buildShareText(style.value, platform.value, lang, props.sign, props.zodiac, props.element, props.energy, shortUrl)
    }).catch(()=>{})
  } catch {}
}

watch([style, platform, () => props.energy], build, { immediate: true })

async function copyText() {
  await navigator.clipboard.writeText(text.value)
  try {
    const uid = Number(localStorage.getItem('user_id')||'1')
    const lang = localStorage.getItem('lang')||'en'
    const r = await http.post('/share/success', { user_id: uid, language: lang })
    alert(r.data.message)
  } catch {}
}

function exportImg() {
  const url = props.getImage()
  const a = document.createElement('a')
  a.href = url
  a.download = 'card-share.jpg'
  a.click()
}

function expIns() {
  const fn = props.getImageFor
  if (!fn) return exportImg()
  const url = fn('image/jpeg', 1080, 1350, 'ins', 0.92) || ''
  const a = document.createElement('a')
  a.href = url
  a.download = 'instagram.jpg'
  a.click()
}

function expTiktok() {
  const fn = props.getImageFor
  if (!fn) return exportImg()
  const url = fn('image/png', 1080, 1920, 'tiktok') || ''
  const a = document.createElement('a')
  a.href = url
  a.download = 'tiktok.png'
  a.click()
}

function expFb() {
  const fn = props.getImageFor
  if (!fn) return exportImg()
  const url = fn('image/jpeg', 1200, 630, 'fb', 0.92) || ''
  const a = document.createElement('a')
  a.href = url
  a.download = 'facebook.jpg'
  a.click()
}

function expWa() {
  const fn = props.getImageFor
  if (!fn) return exportImg()
  let url = fn('image/webp', 750, 1000, 'wa', 0.75) || ''
  const a = document.createElement('a')
  a.href = url
  a.download = 'whatsapp.webp'
  a.click()
}

async function shareNative() {
  try {
    if ((navigator as any).canShare && (navigator as any).canShare()) {
      await (navigator as any).share({ text: text.value })
    } else {
      await copyText()
    }
    try {
      const uid = Number(localStorage.getItem('user_id')||'1')
      const lang = localStorage.getItem('lang')||'en'
      const r = await http.post('/share/success', { user_id: uid, language: lang })
      alert(r.data.message)
    } catch {}
  } catch {}
}
</script>

<style scoped>
.panel { border: 1px solid #eee; padding: 12px; border-radius: 8px; display: grid; gap: 12px }
.row { display: flex; gap: 12px; align-items: center }
textarea { width: 100% }
</style>
