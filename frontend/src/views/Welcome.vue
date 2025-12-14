<template>
  <div class="wrap">
    <h1>Cosmic Totem Arcana</h1>
    <p>{{ t('welcomeValue') }}</p>
    <div class="row">
      <router-link class="btn" to="/login">{{ t('loginSignin') }}</router-link>
      <router-link class="btn" to="/language">{{ t('selectLanguage') }}</router-link>
      <router-link class="btn primary" to="/onboarding/birth">{{ t('startOnboarding') }}</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
</script>

<style scoped>
.wrap { max-width: 640px; margin: 0 auto; display: flex; flex-direction: column; gap: 16px; text-align: center }
.row { display: flex; gap: 12px; justify-content: center }
.btn { padding: 8px 12px; border: 1px solid #ccc; border-radius: 6px; text-decoration: none }
.primary { background: #222; color: #fff }
</style>
