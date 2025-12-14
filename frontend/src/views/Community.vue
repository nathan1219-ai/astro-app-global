<template>
  <div class="wrap">
    <h2>Community</h2>
    <div class="row">
      <label>Sign</label>
      <input v-model="sign" />
      <label>Zodiac</label>
      <input v-model="zodiac" />
      <label>Language</label>
      <select v-model="language">
        <option value="en">English</option>
        <option value="es">Español</option>
        <option value="fr">Français</option>
      </select>
    </div>
    <div class="row">
      <input v-model="content" maxlength="100" placeholder="Share your thoughts" />
      <button @click="publish">Share</button>
    </div>
    <div class="row">
      <label>Limit</label>
      <input type="number" v-model.number="limit" min="1" max="100" />
      <label>Offset</label>
      <input type="number" v-model.number="offset" min="0" />
      <button @click="load">Load</button>
    </div>
    <div class="feed">
      <div class="card" v-for="p in posts" :key="p.id">
        <div class="meta">{{ p.sign }} / {{ p.zodiac }} · {{ p.language }}</div>
        <div class="text">{{ p.content }}</div>
        <div class="actions">
          <button @click="like(p.id)">♥ {{ p.likes }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import http from '../http'
import { ref } from 'vue'
const userId = 1
const sign = ref('白羊座')
const zodiac = ref('龙')
const language = ref('en')
const content = ref('')
const posts = ref<any[]>([])
const limit = ref(50)
const offset = ref(0)

async function publish() {
  await http.post('/community/post', { user_id: userId, sign: sign.value, zodiac: zodiac.value, language: language.value, content: content.value })
  content.value = ''
}

async function load() {
  const r = await http.get('/community/list', { params: { sign: sign.value, zodiac: zodiac.value, language: language.value, limit: limit.value, offset: offset.value } })
  posts.value = r.data
}

async function like(id: number) {
  await http.post('/community/like/'+id)
  await load()
}
</script>

<style scoped>
.wrap { max-width: 640px; margin: 0 auto; display: flex; flex-direction: column; gap: 12px }
.row { display: flex; align-items: center; gap: 12px }
.feed { display: grid; gap: 12px }
.card { border: 1px solid #ddd; border-radius: 8px; padding: 12px }
.meta { font-size: 12px; color: #666 }
.text { margin: 8px 0 }
</style>
