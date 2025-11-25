
// Update this URL to match your bridge frontend WS endpoint
const WEBSOCKET_URL = 'ws://127.0.0.1:8765/ws/frontend'
let ws;
const connEl = document.getElementById('conn')
const signalList = document.getElementById('signal_list')
const canvas = document.getElementById('chartCanvas')
const ctx = canvas.getContext('2d')
let candles = []

function connect(){
  ws = new WebSocket(WEBSOCKET_URL)
  ws.onopen = ()=>{ connEl.textContent = 'Connected' }
  ws.onclose = ()=>{ connEl.textContent = 'Disconnected'; setTimeout(connect,2000) }
  ws.onmessage = (ev)=>{ try{ const data = JSON.parse(ev.data); handleMessage(data) }catch(e){} }
}

function handleMessage(data){
  if(data.type === 'signal'){
    addSignal(data.signal)
  }
  if(data.type === 'candles'){
    // accept a single candle or array
    const incoming = Array.isArray(data.candles)? data.candles : [data.candle]
    for(const c of incoming){ candles.push(c); if(candles.length>100) candles.shift() }
    drawChart()
  }
}

function addSignal(sig){
  const li = document.createElement('li')
  li.textContent = `${new Date(sig.ts*1000).toLocaleTimeString()} — ${sig.pair} — ${sig.direction} — ${ (sig.confidence||0).toFixed(2) }`
  signalList.prepend(li)
}

function drawChart(){
  ctx.clearRect(0,0,canvas.width,canvas.height)
  if(candles.length===0) return
  const w = canvas.width; const h = canvas.height
  const min = Math.min(...candles.map(c=>c.low)); const max = Math.max(...candles.map(c=>c.high))
  const range = max-min || 1
  const barW = w / Math.max(1,candles.length)
  candles.forEach((c,i)=>{
    const x = i*barW
    const openY = h - ((c.open - min)/range)*h
    const closeY = h - ((c.close - min)/range)*h
    const highY = h - ((c.high - min)/range)*h
    const lowY = h - ((c.low - min)/range)*h
    // wick
    ctx.strokeStyle = '#9fb8c8'
    ctx.beginPath(); ctx.moveTo(x+barW/2, highY); ctx.lineTo(x+barW/2, lowY); ctx.stroke()
    // body
    ctx.fillStyle = c.close>=c.open? '#3ddc84' : '#ff6b6b'
    ctx.fillRect(x+1, Math.min(openY,closeY), barW-2, Math.max(1, Math.abs(closeY-openY)))
  })
}

connect()
