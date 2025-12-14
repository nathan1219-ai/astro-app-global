export type CardSpec = {
  background: { palette: string[]; noiseDensity: number; noiseAlpha: number }
  decorations: { type: string; density: number; sizeMin: number; sizeMax: number; alpha: number }
  main: { metal: string[]; symbol: string; highlight: { x1: number; x2: number; y1: number; y2: number } }
  glow: { color: string; inner: number; outer: number; pulse?: number }
  border: { color: string; shadow: number; studsX: number; studsY: number }
}

const PALETTES: Record<string, string[]> = {
  '木': ['#0b3d2e','#1fa36b'],
  '火': ['#3d0b0b','#ff6b3d'],
  '土': ['#372c1a','#c2a36b'],
  '金': ['#3a330f','#ffd166'],
  '水': ['#0b2e3d','#6ec1ff']
}

const METAL: Record<string, string[]> = {
  brass: ['#a67c52','#d4af37','#a67c52'],
  rose: ['#a15d5d','#d79a8b','#a15d5d'],
  silver: ['#9ea7b0','#d0d3d6','#9ea7b0'],
  black: ['#2b2b2b','#4b4b4b','#2b2b2b']
}

const SIGN_SYMBOL: Record<string,string> = {
  '白羊座':'♈','金牛座':'♉','双子座':'♊','巨蟹座':'♋','狮子座':'♌','处女座':'♍',
  '天秤座':'♎','天蝎座':'♏','射手座':'♐','摩羯座':'♑','水瓶座':'♒','双鱼座':'♓'
}

const GLOW: Record<string,string> = {
  '木':'#7bd389','火':'#ff6b3d','土':'#c2a36b','金':'#ffd166','水':'#6ec1ff'
}

export function getCardSpec(sign: string, zodiac: string, element: string, membership?: 'free'|'premium'): CardSpec {
  const key = `${element}|${zodiac}|${sign}|${membership||'free'}`
  const ov = overrides[key]
  if (ov) return ov
  const combo = `${element}+${zodiac}+${sign}`
  if (membership === 'premium') {
    if (combo.includes('火') && combo.includes('龙') && combo.includes('白羊')) {
      return {
        background: { palette: PALETTES['火'], noiseDensity: 0.6, noiseAlpha: 0.35 },
        decorations: { type: 'flame', density: 0.8, sizeMin: 10, sizeMax: 16, alpha: 0.7 },
        main: { metal: METAL.rose, symbol: SIGN_SYMBOL[sign] || '★', highlight: { x1: 600, x2: 700, y1: 200, y2: 800 } },
        glow: { color: GLOW['火'], inner: 80, outer: 320, pulse: 0.6 },
        border: { color: '#7a5a2e', shadow: 24, studsX: 14, studsY: 20 }
      }
    }
    if (combo.includes('水') && combo.includes('兔') && combo.includes('双鱼')) {
      return {
        background: { palette: PALETTES['水'], noiseDensity: 0.5, noiseAlpha: 0.28 },
        decorations: { type: 'spark', density: 0.7, sizeMin: 8, sizeMax: 14, alpha: 0.6 },
        main: { metal: METAL.silver, symbol: SIGN_SYMBOL[sign] || '★', highlight: { x1: 560, x2: 740, y1: 260, y2: 780 } },
        glow: { color: GLOW['水'], inner: 90, outer: 340, pulse: 0.4 },
        border: { color: '#9ea7b0', shadow: 26, studsX: 16, studsY: 22 }
      }
    }
    if (combo.includes('金') && combo.includes('猴') && combo.includes('天秤')) {
      return {
        background: { palette: PALETTES['金'], noiseDensity: 0.55, noiseAlpha: 0.32 },
        decorations: { type: 'spark', density: 0.75, sizeMin: 9, sizeMax: 13, alpha: 0.65 },
        main: { metal: METAL.black, symbol: SIGN_SYMBOL[sign] || '★', highlight: { x1: 610, x2: 700, y1: 240, y2: 760 } },
        glow: { color: GLOW['金'], inner: 85, outer: 330, pulse: 0.5 },
        border: { color: '#2b2b2b', shadow: 28, studsX: 18, studsY: 24 }
      }
    }
    if (combo.includes('土') && combo.includes('牛') && combo.includes('金牛')) {
      return {
        background: { palette: PALETTES['土'], noiseDensity: 0.58, noiseAlpha: 0.33 },
        decorations: { type: 'spark', density: 0.7, sizeMin: 9, sizeMax: 15, alpha: 0.6 },
        main: { metal: METAL.brass, symbol: SIGN_SYMBOL[sign] || '★', highlight: { x1: 600, x2: 700, y1: 220, y2: 760 } },
        glow: { color: GLOW['土'], inner: 85, outer: 330, pulse: 0.4 },
        border: { color: '#7a5a2e', shadow: 26, studsX: 16, studsY: 22 }
      }
    }
    if (combo.includes('木') && combo.includes('蛇') && combo.includes('双子')) {
      return {
        background: { palette: PALETTES['木'], noiseDensity: 0.52, noiseAlpha: 0.3 },
        decorations: { type: 'spark', density: 0.72, sizeMin: 8, sizeMax: 14, alpha: 0.6 },
        main: { metal: METAL.silver, symbol: SIGN_SYMBOL[sign] || '★', highlight: { x1: 570, x2: 730, y1: 250, y2: 780 } },
        glow: { color: GLOW['木'], inner: 85, outer: 320, pulse: 0.45 },
        border: { color: '#9ea7b0', shadow: 24, studsX: 15, studsY: 22 }
      }
    }
    if (combo.includes('火') && combo.includes('马') && combo.includes('狮子')) {
      return {
        background: { palette: PALETTES['火'], noiseDensity: 0.64, noiseAlpha: 0.36 },
        decorations: { type: 'flame', density: 0.85, sizeMin: 11, sizeMax: 17, alpha: 0.75 },
        main: { metal: METAL.rose, symbol: SIGN_SYMBOL[sign] || '★', highlight: { x1: 610, x2: 700, y1: 230, y2: 770 } },
        glow: { color: GLOW['火'], inner: 90, outer: 340, pulse: 0.7 },
        border: { color: '#7a5a2e', shadow: 28, studsX: 18, studsY: 24 }
      }
    }
    if (combo.includes('水') && combo.includes('猪') && combo.includes('双鱼')) {
      return {
        background: { palette: PALETTES['水'], noiseDensity: 0.5, noiseAlpha: 0.28 },
        decorations: { type: 'spark', density: 0.7, sizeMin: 9, sizeMax: 13, alpha: 0.6 },
        main: { metal: METAL.silver, symbol: SIGN_SYMBOL[sign] || '★', highlight: { x1: 560, x2: 740, y1: 260, y2: 780 } },
        glow: { color: GLOW['水'], inner: 95, outer: 350, pulse: 0.5 },
        border: { color: '#9ea7b0', shadow: 26, studsX: 16, studsY: 22 }
      }
    }
    if (combo.includes('金') && combo.includes('鸡') && combo.includes('处女')) {
      return {
        background: { palette: PALETTES['金'], noiseDensity: 0.56, noiseAlpha: 0.34 },
        decorations: { type: 'spark', density: 0.76, sizeMin: 8, sizeMax: 12, alpha: 0.65 },
        main: { metal: METAL.black, symbol: SIGN_SYMBOL[sign] || '★', highlight: { x1: 600, x2: 700, y1: 240, y2: 760 } },
        glow: { color: GLOW['金'], inner: 85, outer: 330, pulse: 0.5 },
        border: { color: '#2b2b2b', shadow: 30, studsX: 18, studsY: 24 }
      }
    }
    if (combo.includes('土') && combo.includes('狗') && combo.includes('摩羯')) {
      return {
        background: { palette: PALETTES['土'], noiseDensity: 0.6, noiseAlpha: 0.32 },
        decorations: { type: 'spark', density: 0.72, sizeMin: 9, sizeMax: 15, alpha: 0.6 },
        main: { metal: METAL.brass, symbol: SIGN_SYMBOL[sign] || '★', highlight: { x1: 590, x2: 710, y1: 230, y2: 760 } },
        glow: { color: GLOW['土'], inner: 90, outer: 340, pulse: 0.45 },
        border: { color: '#7a5a2e', shadow: 26, studsX: 16, studsY: 22 }
      }
    }
    if (combo.includes('木') && combo.includes('羊') && combo.includes('天秤')) {
      return {
        background: { palette: PALETTES['木'], noiseDensity: 0.54, noiseAlpha: 0.31 },
        decorations: { type: 'spark', density: 0.74, sizeMin: 8, sizeMax: 14, alpha: 0.62 },
        main: { metal: METAL.brass, symbol: SIGN_SYMBOL[sign] || '★', highlight: { x1: 580, x2: 720, y1: 240, y2: 780 } },
        glow: { color: GLOW['木'], inner: 88, outer: 330, pulse: 0.45 },
        border: { color: '#7a5a2e', shadow: 26, studsX: 16, studsY: 22 }
      }
    }
    if (combo.includes('水') && combo.includes('鼠') && combo.includes('水瓶')) {
      return {
        background: { palette: PALETTES['水'], noiseDensity: 0.5, noiseAlpha: 0.28 },
        decorations: { type: 'spark', density: 0.78, sizeMin: 8, sizeMax: 12, alpha: 0.6 },
        main: { metal: METAL.silver, symbol: SIGN_SYMBOL[sign] || '★', highlight: { x1: 560, x2: 740, y1: 260, y2: 780 } },
        glow: { color: GLOW['水'], inner: 95, outer: 350, pulse: 0.52 },
        border: { color: '#9ea7b0', shadow: 26, studsX: 16, studsY: 22 }
      }
    }
    if (combo.includes('火') && combo.includes('虎') && combo.includes('射手')) {
      return {
        background: { palette: PALETTES['火'], noiseDensity: 0.66, noiseAlpha: 0.37 },
        decorations: { type: 'flame', density: 0.88, sizeMin: 11, sizeMax: 18, alpha: 0.78 },
        main: { metal: METAL.rose, symbol: SIGN_SYMBOL[sign] || '★', highlight: { x1: 610, x2: 700, y1: 230, y2: 770 } },
        glow: { color: GLOW['火'], inner: 92, outer: 360, pulse: 0.72 },
        border: { color: '#7a5a2e', shadow: 30, studsX: 18, studsY: 24 }
      }
    }
    if (combo.includes('木') && combo.includes('马') && combo.includes('处女')) {
      return {
        background: { palette: PALETTES['木'], noiseDensity: 0.55, noiseAlpha: 0.32 },
        decorations: { type: 'spark', density: 0.7, sizeMin: 8, sizeMax: 14, alpha: 0.6 },
        main: { metal: METAL.silver, symbol: SIGN_SYMBOL[sign] || '★', highlight: { x1: 580, x2: 720, y1: 240, y2: 770 } },
        glow: { color: GLOW['木'], inner: 88, outer: 330, pulse: 0.46 },
        border: { color: '#9ea7b0', shadow: 24, studsX: 16, studsY: 22 }
      }
    }
    if (combo.includes('木') && combo.includes('猴') && combo.includes('双子')) {
      return {
        background: { palette: PALETTES['木'], noiseDensity: 0.53, noiseAlpha: 0.3 },
        decorations: { type: 'spark', density: 0.73, sizeMin: 8, sizeMax: 14, alpha: 0.62 },
        main: { metal: METAL.brass, symbol: SIGN_SYMBOL[sign] || '★', highlight: { x1: 570, x2: 730, y1: 250, y2: 780 } },
        glow: { color: GLOW['木'], inner: 86, outer: 325, pulse: 0.44 },
        border: { color: '#7a5a2e', shadow: 26, studsX: 16, studsY: 22 }
      }
    }
    if (combo.includes('火') && combo.includes('兔') && combo.includes('白羊')) {
      return {
        background: { palette: PALETTES['火'], noiseDensity: 0.65, noiseAlpha: 0.36 },
        decorations: { type: 'flame', density: 0.86, sizeMin: 11, sizeMax: 17, alpha: 0.76 },
        main: { metal: METAL.rose, symbol: SIGN_SYMBOL[sign] || '★', highlight: { x1: 610, x2: 700, y1: 230, y2: 770 } },
        glow: { color: GLOW['火'], inner: 92, outer: 350, pulse: 0.71 },
        border: { color: '#7a5a2e', shadow: 29, studsX: 18, studsY: 24 }
      }
    }
    if (combo.includes('火') && combo.includes('牛') && combo.includes('金牛')) {
      return {
        background: { palette: PALETTES['火'], noiseDensity: 0.62, noiseAlpha: 0.35 },
        decorations: { type: 'flame', density: 0.82, sizeMin: 10, sizeMax: 16, alpha: 0.74 },
        main: { metal: METAL.brass, symbol: SIGN_SYMBOL[sign] || '★', highlight: { x1: 600, x2: 710, y1: 230, y2: 760 } },
        glow: { color: GLOW['火'], inner: 90, outer: 340, pulse: 0.68 },
        border: { color: '#7a5a2e', shadow: 28, studsX: 17, studsY: 23 }
      }
    }
    if (combo.includes('水') && combo.includes('龙') && combo.includes('巨蟹')) {
      return {
        background: { palette: PALETTES['水'], noiseDensity: 0.52, noiseAlpha: 0.29 },
        decorations: { type: 'spark', density: 0.76, sizeMin: 8, sizeMax: 13, alpha: 0.6 },
        main: { metal: METAL.silver, symbol: SIGN_SYMBOL[sign] || '★', highlight: { x1: 560, x2: 740, y1: 260, y2: 780 } },
        glow: { color: GLOW['水'], inner: 96, outer: 360, pulse: 0.53 },
        border: { color: '#9ea7b0', shadow: 26, studsX: 16, studsY: 22 }
      }
    }
    if (combo.includes('水') && combo.includes('羊') && combo.includes('双鱼')) {
      return {
        background: { palette: PALETTES['水'], noiseDensity: 0.5, noiseAlpha: 0.28 },
        decorations: { type: 'spark', density: 0.74, sizeMin: 8, sizeMax: 12, alpha: 0.6 },
        main: { metal: METAL.silver, symbol: SIGN_SYMBOL[sign] || '★', highlight: { x1: 560, x2: 740, y1: 260, y2: 780 } },
        glow: { color: GLOW['水'], inner: 94, outer: 350, pulse: 0.5 },
        border: { color: '#9ea7b0', shadow: 25, studsX: 16, studsY: 22 }
      }
    }
    if (combo.includes('金') && combo.includes('虎') && combo.includes('天秤')) {
      return {
        background: { palette: PALETTES['金'], noiseDensity: 0.57, noiseAlpha: 0.34 },
        decorations: { type: 'spark', density: 0.77, sizeMin: 8, sizeMax: 12, alpha: 0.66 },
        main: { metal: METAL.black, symbol: SIGN_SYMBOL[sign] || '★', highlight: { x1: 600, x2: 700, y1: 240, y2: 760 } },
        glow: { color: GLOW['金'], inner: 86, outer: 330, pulse: 0.51 },
        border: { color: '#2b2b2b', shadow: 30, studsX: 18, studsY: 24 }
      }
    }
    if (combo.includes('金') && combo.includes('蛇') && combo.includes('射手')) {
      return {
        background: { palette: PALETTES['金'], noiseDensity: 0.56, noiseAlpha: 0.33 },
        decorations: { type: 'spark', density: 0.75, sizeMin: 8, sizeMax: 12, alpha: 0.65 },
        main: { metal: METAL.black, symbol: SIGN_SYMBOL[sign] || '★', highlight: { x1: 600, x2: 700, y1: 240, y2: 760 } },
        glow: { color: GLOW['金'], inner: 85, outer: 330, pulse: 0.5 },
        border: { color: '#2b2b2b', shadow: 29, studsX: 18, studsY: 24 }
      }
    }
    if (combo.includes('土') && combo.includes('鸡') && combo.includes('摩羯')) {
      return {
        background: { palette: PALETTES['土'], noiseDensity: 0.6, noiseAlpha: 0.32 },
        decorations: { type: 'spark', density: 0.72, sizeMin: 9, sizeMax: 15, alpha: 0.6 },
        main: { metal: METAL.brass, symbol: SIGN_SYMBOL[sign] || '★', highlight: { x1: 590, x2: 710, y1: 230, y2: 760 } },
        glow: { color: GLOW['土'], inner: 90, outer: 340, pulse: 0.45 },
        border: { color: '#7a5a2e', shadow: 27, studsX: 16, studsY: 22 }
      }
    }
    if (combo.includes('土') && combo.includes('猪') && combo.includes('处女')) {
      return {
        background: { palette: PALETTES['土'], noiseDensity: 0.59, noiseAlpha: 0.33 },
        decorations: { type: 'spark', density: 0.73, sizeMin: 9, sizeMax: 15, alpha: 0.6 },
        main: { metal: METAL.brass, symbol: SIGN_SYMBOL[sign] || '★', highlight: { x1: 590, x2: 710, y1: 230, y2: 760 } },
        glow: { color: GLOW['土'], inner: 88, outer: 335, pulse: 0.44 },
        border: { color: '#7a5a2e', shadow: 26, studsX: 16, studsY: 22 }
      }
    }
  }
  return {
    background: { palette: PALETTES[element] || PALETTES['木'], noiseDensity: 0.5, noiseAlpha: 0.3 },
    decorations: { type: element==='火'?'flame':'spark', density: 0.6, sizeMin: 8, sizeMax: 14, alpha: 0.5 },
    main: { metal: METAL.brass, symbol: SIGN_SYMBOL[sign] || '★', highlight: { x1: 580, x2: 720, y1: 240, y2: 760 } },
    glow: { color: GLOW[element] || GLOW['木'], inner: 80, outer: 300 },
    border: { color: '#7a5a2e', shadow: 24, studsX: 14, studsY: 20 }
  }
}

const overrides: Record<string, CardSpec> = {}

export function setOverride(sign: string, zodiac: string, element: string, membership: 'free'|'premium', spec: CardSpec) {
  const key = `${element}|${zodiac}|${sign}|${membership}`
  overrides[key] = spec
}

export function clearOverride(sign: string, zodiac: string, element: string, membership: 'free'|'premium') {
  const key = `${element}|${zodiac}|${sign}|${membership}`
  delete overrides[key]
}

export function exportOverrides(): string {
  return JSON.stringify(overrides)
}

export function importOverrides(json: string) {
  const obj = JSON.parse(json)
  for (const k of Object.keys(obj)) {
    overrides[k] = obj[k]
  }
}

export function saveOverrides() {
  localStorage.setItem('card_overrides', exportOverrides())
}

export function loadOverrides() {
  const s = localStorage.getItem('card_overrides')
  if (s) importOverrides(s)
}

loadOverrides()

export function applyMaterials(spec: CardSpec, decoration?: string, glowName?: string): CardSpec {
  const s = JSON.parse(JSON.stringify(spec))
  if (decoration) {
    if (decoration.includes('Starlight')) { s.decorations.type = 'spark'; s.decorations.density = 0.8; s.decorations.alpha = 0.7 }
    else if (decoration.includes('Vine')) { s.decorations.type = 'spark'; s.decorations.density = 0.7; s.decorations.alpha = 0.6 }
    else if (decoration.includes('Waterdrop')) { s.decorations.type = 'spark'; s.decorations.sizeMin = 6; s.decorations.sizeMax = 12; s.decorations.alpha = 0.65 }
  }
  if (glowName) {
    if (glowName.includes('Nebula')) s.glow.color = '#a7b7ff'
    else if (glowName.includes('Crystal')) s.glow.color = '#cfefff'
    else if (glowName.includes('Flame')) s.glow.color = '#ff6b3d'
  }
  return s
}
