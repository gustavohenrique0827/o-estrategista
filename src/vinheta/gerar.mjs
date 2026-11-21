// Gera as vinhetas MP4 da logo Licenciado Fora da Curva.
// Sem dependencias: usa o Chrome (DevTools Protocol) + ffmpeg.
// Uso: node src/vinheta/gerar.mjs
import { spawn, spawnSync } from 'child_process';
import { mkdirSync, rmSync, writeFileSync, mkdtempSync } from 'fs';
import { fileURLToPath } from 'url';
import { tmpdir } from 'os';
import path from 'path';

const dir = path.dirname(fileURLToPath(import.meta.url));
const outDir = path.join(dir, '../../logos/licenciado-laranja');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9333, FPS = 30, DUR = 5;
const sleep = ms => new Promise(r => setTimeout(r, ms));

const profile = mkdtempSync(path.join(tmpdir(), 'vinheta-'));
const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`,
  '--disable-gpu', '--hide-scrollbars', '--no-first-run', 'about:blank'], { stdio: 'ignore' });

let targets;
for (let i = 0; i < 50; i++) {
  try { targets = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json(); if (targets.find(t => t.type === 'page')) break; } catch {}
  await sleep(200);
}
const ws = new WebSocket(targets.find(t => t.type === 'page').webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener('open', r));
let id = 0; const pend = new Map(); const events = [];
ws.addEventListener('message', m => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { pend.get(d.id)(d); pend.delete(d.id); } else events.push(d.method); });
const send = (method, params = {}) => new Promise(r => { const i = ++id; pend.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });

for (const [o, w, h, nome] of [['v', 1080, 1920, 'vinheta-vertical-1080x1920'], ['h', 1920, 1080, 'vinheta-horizontal-1920x1080']]) {
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile: false });
  await send('Page.enable');
  events.length = 0;
  await send('Page.navigate', { url: 'file://' + path.join(dir, 'vinheta.html') + '?o=' + o });
  for (let i = 0; i < 100 && !events.includes('Page.loadEventFired'); i++) await sleep(100);
  await send('Runtime.evaluate', { expression: 'document.fonts.ready.then(()=>1)', awaitPromise: true });
  await sleep(400);
  const tmp = path.join(dir, '_frames'); rmSync(tmp, { recursive: true, force: true }); mkdirSync(tmp);
  for (let i = 0; i < FPS * DUR; i++) {
    await send('Runtime.evaluate', { expression: `setT(${i / FPS})` });
    const r = await send('Page.captureScreenshot', { format: 'jpeg', quality: 92 });
    writeFileSync(path.join(tmp, `f${String(i).padStart(4, '0')}.jpg`), Buffer.from(r.result.data, 'base64'));
  }
  mkdirSync(outDir, { recursive: true });
  const r = spawnSync('ffmpeg', ['-y', '-framerate', String(FPS), '-i', path.join(tmp, 'f%04d.jpg'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '16', path.join(outDir, nome + '.mp4')], { stdio: 'ignore' });
  console.log(nome, r.status === 0 ? 'ok' : 'erro ffmpeg');
  rmSync(tmp, { recursive: true, force: true });
}
ws.close(); chrome.kill();
await sleep(800);
try { rmSync(profile, { recursive: true, force: true }); } catch {}
process.exit(0);
