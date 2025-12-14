type Style = 'fun'|'healing'|'explore'
type Platform = 'ins'|'tiktok'|'fb'
import { SIGN_LOCAL, ZODIAC_LOCAL, ELEMENT_LOCAL, chooseLocale, resolveLocal } from './vocab'

const limits: Record<Platform, number> = { ins: 220, tiktok: 140, fb: 280 }
const tags: Record<Platform, Record<string, string>> = {
  ins: { en: '#cosmiccard', 'en-US': '#cosmiccard', es: '#tarjetacósmica', 'es-ES': '#tarjetacósmica', fr: '#cartecosmique', 'fr-FR': '#cartecosmique', de: '#kosmischekarte', 'de-DE': '#kosmischekarte', it: '#cartacosmica', 'it-IT': '#cartacosmica', pt: '#cartacosmica', 'pt-BR': '#cartacosmica', 'pt-PT': '#cartacosmica', ru: '#космическаякарта', 'ru-RU': '#космическаякарта' },
  tiktok: { en: '#cosmic #energy', 'en-US': '#cosmic #energy', es: '#cosmico #energia', 'es-ES': '#cosmico #energia', fr: '#cosmique #energie', 'fr-FR': '#cosmique #energie', de: '#kosmisch #energie', 'de-DE': '#kosmisch #energie', it: '#cosmico #energia', 'it-IT': '#cosmico #energia', pt: '#cosmico #energia', 'pt-BR': '#cosmico #energia', 'pt-PT': '#cosmico #energia', ru: '#космос #энергия', 'ru-RU': '#космос #энергия' },
  fb: { en: '#energyInsights', 'en-US': '#energyInsights', es: '#perspectivasEnergia', 'es-ES': '#perspectivasEnergia', fr: '#insightsEnergie', 'fr-FR': '#insightsEnergie', de: '#energieInsights', 'de-DE': '#energieInsights', it: '#insightsEnergia', 'it-IT': '#insightsEnergia', pt: '#insightsEnergia', 'pt-BR': '#insightsEnergia', 'pt-PT': '#insightsEnergia', ru: '#инсайтыЭнергии', 'ru-RU': '#инсайтыЭнергии' }
}


const T: Record<string, Record<Style, string>> = {
  en: {
    fun: 'Your cosmic card is ready — {sign}/{zodiac}. Explore your {element} energy: {energy}. Tap to see full details!',
    healing: 'Gentle guidance for {sign}/{zodiac}. Your {element} energy today: {energy}. Breathe, reflect, and explore your card.',
    explore: 'Discover {element} energy for {sign}/{zodiac}. {energy}. Open the full embossed card and dive deeper.'
  },
  es: {
    fun: 'Tu tarjeta cósmica está lista — {sign}/{zodiac}. Explora tu energía {element}: {energy}. ¡Toca para ver detalles!',
    healing: 'Guía suave para {sign}/{zodiac}. Tu energía {element} de hoy: {energy}. Respira, reflexiona y explora tu tarjeta.',
    explore: 'Descubre la energía {element} para {sign}/{zodiac}. {energy}. Abre la tarjeta en relieve y profundiza.'
  },
  fr: {
    fun: 'Ta carte cosmique est prête — {sign}/{zodiac}. Explore ton énergie {element} : {energy}. Clique pour les détails !',
    healing: 'Guidance douce pour {sign}/{zodiac}. Ton énergie {element} aujourd’hui : {energy}. Respire, réfléchis et explore ta carte.',
    explore: 'Découvre l’énergie {element} pour {sign}/{zodiac}. {energy}. Ouvre la carte gaufrée et va plus loin.'
  },
  de: {
    fun: 'Deine kosmische Karte ist bereit — {sign}/{zodiac}. Entdecke deine {element}-Energie: {energy}. Tippe für Details!',
    healing: 'Sanfte Guidance für {sign}/{zodiac}. Deine {element}-Energie heute: {energy}. Atme, reflektiere und erkunde deine Karte.',
    explore: 'Entdecke {element}-Energie für {sign}/{zodiac}. {energy}. Öffne die geprägte Karte und tauche tiefer ein.'
  },
  it: {
    fun: 'La tua carta cosmica è pronta — {sign}/{zodiac}. Esplora la tua energia {element}: {energy}. Tocca per i dettagli!',
    healing: 'Guida gentile per {sign}/{zodiac}. La tua energia {element} di oggi: {energy}. Respira, rifletti ed esplora la carta.',
    explore: 'Scopri l’energia {element} per {sign}/{zodiac}. {energy}. Apri la carta in rilievo e approfondisci.'
  },
  pt: {
    fun: 'Sua carta cósmica está pronta — {sign}/{zodiac}. Explore sua energia {element}: {energy}. Toque para ver detalhes!',
    healing: 'Orientação suave para {sign}/{zodiac}. Sua energia {element} hoje: {energy}. Respire, reflita e explore a carta.',
    explore: 'Descubra a energia {element} para {sign}/{zodiac}. {energy}. Abra a carta em relevo e aprofunde-se.'
  },
  ru: {
    fun: 'Твоя космическая карта готова — {sign}/{zodiac}. Исследуй свою энергию {element}: {energy}. Нажми, чтобы увидеть детали!',
    healing: 'Мягкое руководство для {sign}/{zodiac}. Твоя энергия {element} сегодня: {energy}. Дыши, размышляй и исследуй карту.',
    explore: 'Открой энергию {element} для {sign}/{zodiac}. {energy}. Открой рельефную карту и погрузись глубже.'
  }
}

function fill(t: string, m: Record<string,string>) {
  return t.replace(/\{(\w+)\}/g, (_, k) => m[k] ?? '')
}

export function buildShareText(style: Style, platform: Platform, lang: string, sign: string, zodiac: string, element: string, energy: string, link: string): string {
  const baseLang = T[lang] ? lang : 'en'
  const locale = chooseLocale(baseLang)
  const el = resolveLocal(ELEMENT_LOCAL, element, locale, baseLang)
  const signL = resolveLocal(SIGN_LOCAL, sign, locale, baseLang)
  const zodiacL = resolveLocal(ZODIAC_LOCAL, zodiac, locale, baseLang)
  const baseText = fill(T[baseLang][style], { sign: signL, zodiac: zodiacL, element: el, energy })
  const tag = tags[platform][locale] || tags[platform][baseLang] || tags[platform]['en']
  const limit = limits[platform]
  if (platform === 'tiktok') {
    // TikTok: prefer text + tags, omit link to fit short captions
    let text = `${baseText}\n${tag}`
    if (text.length > limit) text = text.slice(0, limit)
    return text
  }
  // Instagram: include link if fits; otherwise omit link
  if (platform === 'ins') {
    let withLink = `${baseText}\n${tag}\n${link}`
    if (withLink.length <= limit) return withLink
    let withoutLink = `${baseText}\n${tag}`
    if (withoutLink.length > limit) withoutLink = withoutLink.slice(0, limit)
    return withoutLink
  }
  // Facebook: include link, place link first line
  let fbText = `${link}\n${baseText}\n${tag}`
  if (fbText.length > limit) fbText = fbText.slice(0, limit)
  return fbText
}
