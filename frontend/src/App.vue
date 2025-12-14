<template>
  <div class="layout">
    <header class="topbar">
      <nav class="nav">
        <router-link to="/welcome">{{ $t('navWelcome') }}</router-link>
        <router-link to="/">{{ $t('navHome') }}</router-link>
        <router-link to="/push">{{ $t('navPush') }}</router-link>
        <router-link to="/membership">{{ $t('navMembership') }}</router-link>
        <router-link to="/community">{{ $t('navCommunity') }}</router-link>
        <router-link to="/login">{{ $t('navLogin') }}</router-link>
        <router-link to="/language">Lang</router-link>
        <router-link to="/card-admin">Admin</router-link>
      </nav>
    </header>
    <main class="main">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.layout { display: flex; flex-direction: column; min-height: 100vh }
.topbar { padding: 8px 12px; border-bottom: 1px solid #eee }
.nav { display: flex; gap: 12px }
.main { flex: 1; padding: 12px }
</style>
