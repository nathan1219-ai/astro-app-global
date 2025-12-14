<template>
  <canvas ref="c" width="1080" height="1350"></canvas>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
const emit = defineEmits<{(e:'lineClick', type:string):void}>()
import { getCardSpec, CardSpec } from '../cardSpec'
const props = defineProps<{ sign: string; zodiac: string; element: string; back?: boolean; backLines?: string[]; spec?: CardSpec }>()
const c = ref<HTMLCanvasElement | null>(null)

function drawFront(ctx: CanvasRenderingContext2D) {
  const w = ctx.canvas.width
  const h = ctx.canvas.height
  ctx.clearRect(0,0,w,h)
  const spec = props.spec || getCardSpec(props.sign, props.zodiac, props.element)

  const metal = ctx.createLinearGradient(0, 0, w, 0)
  metal.addColorStop(0, '#a67c52')
  metal.addColorStop(0.5, '#d4af37')
  metal.addColorStop(1, '#a67c52')

  const bg = ctx.createLinearGradient(0,0,w,h)
  bg.addColorStop(0,spec.background.palette[0])
  bg.addColorStop(1,spec.background.palette[1])
  ctx.fillStyle = bg
  ctx.fillRect(0,0,w,h)

  ctx.globalAlpha = spec.background.noiseAlpha
  ctx.fillStyle = '#ffffff'
  for (let i=0;i<Math.floor(spec.background.noiseDensity*160); i++) {
    ctx.beginPath()
    const x = Math.random()*w
    const y = Math.random()*h
    const r = Math.random()*5
    ctx.arc(x,y,r,0,Math.PI*2)
    ctx.fill()
  }
  ctx.globalAlpha = spec.decorations.alpha*0.2
  ctx.strokeStyle = '#ffffff'
  for (let i=0;i<Math.floor(spec.decorations.density*25); i++) {
    ctx.beginPath()
    const x = Math.random()*w
    const y = Math.random()*h
    ctx.moveTo(x,y)
    ctx.lineTo(x+80*Math.random(), y+80*Math.random())
    ctx.stroke()
  }
  ctx.globalAlpha = 1

  ctx.save()
  ctx.strokeStyle = '#7a5a2e'
  ctx.lineWidth = 24
  ctx.shadowColor = '#00000055'
  ctx.shadowBlur = 24
  ctx.beginPath()
  ctx.roundRect(60,60,w-120,h-120,40)
  ctx.stroke()
  ctx.restore()

  for (let i=0;i<spec.border.studsX;i++) {
    const t = i/(14)
    const x = 60 + t*(w-120)
    ctx.fillStyle = '#7a5a2e'
    ctx.beginPath()
    ctx.arc(x,60,6,0,Math.PI*2)
    ctx.arc(x,h-60,6,0,Math.PI*2)
    ctx.fill()
  }
  for (let i=0;i<spec.border.studsY;i++) {
    const t = i/(20)
    const y = 60 + t*(h-120)
    ctx.fillStyle = '#7a5a2e'
    ctx.beginPath()
    ctx.arc(60,y,6,0,Math.PI*2)
    ctx.arc(w-60,y,6,0,Math.PI*2)
    ctx.fill()
  }

  const glow = ctx.createRadialGradient(w/2,h/2,spec.glow.inner,w/2,h/2,spec.glow.outer)
  glow.addColorStop(0, spec.glow.color+'99')
  glow.addColorStop(1, '#00000000')
  ctx.fillStyle = glow
  ctx.beginPath()
  ctx.arc(w/2,h/2,spec.glow.outer,0,Math.PI*2)
  ctx.fill()

  const metal = ctx.createLinearGradient(0, 0, w, 0)
  metal.addColorStop(0, spec.main.metal[0])
  metal.addColorStop(0.5, spec.main.metal[1])
  metal.addColorStop(1, spec.main.metal[2])
  ctx.fillStyle = metal
  ctx.beginPath()
  ctx.arc(w/2,h/2,220,0,Math.PI*2)
  ctx.fill()

  const signSymbol = spec.main.symbol
  const zodiacText = props.zodiac

  ctx.textAlign = 'center'
  ctx.fillStyle = '#000'
  ctx.font = 'bold 104px serif'
  ctx.fillText(`${zodiacText}`, w/2, h/2+110)
  ctx.save()
  ctx.shadowColor = '#00000066'
  ctx.shadowBlur = 16
  ctx.fillStyle = '#2b2b2b'
  ctx.font = 'bold 160px serif'
  ctx.fillText(signSymbol, w/2, h/2-20)
  ctx.restore()
}

function drawBack(ctx: CanvasRenderingContext2D) {
  const w = ctx.canvas.width
  const h = ctx.canvas.height
  ctx.clearRect(0,0,w,h)
  ctx.fillStyle = '#222'
  ctx.fillRect(0,0,w,h)
  ctx.fillStyle = '#d4af37'
  ctx.font = 'bold 160px serif'
  ctx.textAlign = 'center'
  const symbol = props.sign
  const signSymbol = {
    '白羊座': '♈', '金牛座': '♉', '双子座': '♊', '巨蟹座': '♋', '狮子座': '♌', '处女座': '♍',
    '天秤座': '♎', '天蝎座': '♏', '射手座': '♐', '摩羯座': '♑', '水瓶座': '♒', '双鱼座': '♓'
  }[symbol] || '★'
  ctx.save()
  ctx.fillStyle = '#1a1a1a'
  ctx.fillText(signSymbol, w/2+6, h/2+6)
  ctx.fillStyle = '#d4af37'
  ctx.fillText(signSymbol, w/2, h/2)
  ctx.restore()
  ctx.fillStyle = '#ccc'
  ctx.font = '48px sans-serif'
  const lines = props.backLines && props.backLines.length ? props.backLines : ['Your daily insights']
  const startY = h/2 + 120
  const lh = 56
  lines.slice(0,4).forEach((line, i) => {
    ctx.fillText(line, w/2, startY + i*lh)
  })
}

function render() {
  const ctx = c.value!.getContext('2d')!
  if (props.back) drawBack(ctx)
  else drawFront(ctx)
}

onMounted(render)
watch(() => [props.sign, props.zodiac, props.element, props.back], render)

function handleClick(ev: MouseEvent) {
  if (!props.back) return
  const el = c.value!
  const rect = el.getBoundingClientRect()
  const scaleX = el.width / rect.width
  const scaleY = el.height / rect.height
  const x = (ev.clientX - rect.left) * scaleX
  const y = (ev.clientY - rect.top) * scaleY
  const w = el.width
  const h = el.height
  const startY = h/2 + 120
  const lh = 56
  if (y >= startY - 30 && y <= startY + 3*lh + 30) {
    const idx = Math.floor((y - startY) / lh)
    const types = ['energy','social','decision','relax']
    const t = types[idx] || 'energy'
    emit('lineClick', t)
  }
}

onMounted(() => {
  c.value?.addEventListener('click', handleClick)
})

function exportImage(type: string) {
  return c.value!.toDataURL(type, 0.92)
}

function exportSized(type: string, w: number, h: number, mode?: string, quality?: number) {
  const src = c.value!
  const oc = document.createElement('canvas')
  oc.width = w
  oc.height = h
  const ctx = oc.getContext('2d')!
  if (mode === 'tiktok') {
    ctx.clearRect(0,0,w,h)
  } else {
    ctx.fillStyle = '#00000000'
    ctx.clearRect(0,0,w,h)
  }
  const scale = Math.min(w/src.width, h/src.height)
  const dw = Math.floor(src.width * scale)
  const dh = Math.floor(src.height * scale)
  const dx = Math.floor((w - dw)/2)
  const dy = Math.floor((h - dh)/2)
  ctx.drawImage(src, 0, 0, src.width, src.height, dx, dy, dw, dh)
  if (mode === 'tiktok') {
    const g = ctx.createRadialGradient(w/2, h/2, 120, w/2, h/2, Math.max(w,h)/2)
    g.addColorStop(0, '#ffffff22')
    g.addColorStop(1, '#00000000')
    ctx.fillStyle = g
    ctx.beginPath()
    ctx.arc(w/2,h/2,Math.max(w,h)/2,0,Math.PI*2)
    ctx.fill()
  }
  const q = typeof quality === 'number' ? quality : 0.92
  return oc.toDataURL(type, q)
}

defineExpose({ export: exportImage, exportSized })
</script>

<style scoped>
canvas { width: 320px; height: 400px; transform-style: preserve-3d; transition: transform .6s; box-shadow: 0 8px 30px rgba(0,0,0,.35); }
</style>
