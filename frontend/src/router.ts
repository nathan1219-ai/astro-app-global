import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import PushPreferences from './views/PushPreferences.vue'
import Membership from './views/Membership.vue'
import Community from './views/Community.vue'
import Login from './views/Login.vue'
import LanguageSelect from './views/LanguageSelect.vue'
import Welcome from './views/Welcome.vue'
import BirthInfo from './views/BirthInfo.vue'
import PushConsent from './views/PushConsent.vue'
import CardDetails from './views/CardDetails.vue'
import CardAdmin from './views/CardAdmin.vue'
import LineDetails from './views/LineDetails.vue'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Home },
    { path: '/welcome', component: Welcome },
    { path: '/onboarding/birth', component: BirthInfo },
    { path: '/onboarding/push', component: PushConsent },
    { path: '/card', component: CardDetails },
    { path: '/card/line', component: LineDetails },
    { path: '/card-admin', component: CardAdmin },
    { path: '/push', component: PushPreferences },
    { path: '/membership', component: Membership },
    { path: '/community', component: Community },
    { path: '/login', component: Login },
    { path: '/language', component: LanguageSelect },
  ]
})

router.beforeEach((to, from, next) => {
  const hasLang = !!localStorage.getItem('lang')
  const hasToken = !!localStorage.getItem('token')
  const allow = ['/welcome', '/language', '/login', '/onboarding/birth', '/onboarding/push']
  if ((!hasLang || !hasToken) && !allow.includes(to.path)) {
    next('/welcome')
    return
  }
  next()
})

router.afterEach((to) => {
  localStorage.setItem('last_url', to.path + (to.fullPath.includes('?') ? to.fullPath.slice(to.fullPath.indexOf('?')) : ''))
})
