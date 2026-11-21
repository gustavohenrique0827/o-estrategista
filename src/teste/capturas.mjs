// Abre uma pagina em um navegador de teste (celular ou computador), espera o 3D ligar e tira capturas em varias posicoes de rolagem.
// Uso: node src/teste/capturas.mjs <pasta-saida> <url> <posicoes,separadas,por,virgula> <modo: m|d> [largura] [altura]
//   m = celular (390x844, toque)   d = computador (largura x altura, padrao 1463x760)
// Sem dependencias: usa o Chrome (DevTools Protocol) do Mac.
import { spawn } from 'child_process';
import { mkdirSync, rmSync, writeFileSync, mkdtempSync } from 'fs';
import { tmpdir } from 'os';
import path from 'path';

const [OUT, URL_, POSSTR, MODO = 'd', WARG, HARG] = process.argv.slice(2);
const POS = POSSTR.split(',').map(Number);
const mobile = MODO === 'm';
const W = Number(WARG || (mobile ? 390 : 1463)), H = Number(HARG || (mobile ? 844 : 760));
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9400 + Math.floor(Math.random() * 400);
const sleep = ms => new Promise(r => setTimeout(r, ms));
mkdirSync(OUT, { recursive: true });
const profile = mkdtempSync(path.join(tmpdir(), 'cap-'));
const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`,
  '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--hide-scrollbars', 'about:blank'], { stdio: 'ignore' });
let targets;
for (let i = 0; i < 60; i++) { try { targets = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json(); if (targets.find(t => t.type === 'page')) break; } catch {} await sleep(200); }
const ws = new WebSocket(targets.find(t => t.type === 'page').webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener('open', r));
let id = 0; const pend = new Map(); const events = [];
ws.addEventListener('message', m => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { pend.get(d.id)(d); pend.delete(d.id); } else events.push(d.method); });
const send = (method, params = {}) => new Promise(r => { const i = ++id; pend.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });

await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: mobile ? 2 : 1, mobile });
if (mobile) await send('Emulation.setTouchEmulationEnabled', { enabled: true });
await send('Page.enable');
await send('Page.navigate', { url: URL_ });
for (let i = 0; i < 100 && !events.includes('Page.loadEventFired'); i++) await sleep(100);
await sleep(3500);
const nome = (URL_.split('/').pop() || 'pagina').replace(/[^a-z0-9]+/gi, '_');
for (const y of POS) {
  await send('Runtime.evaluate', { expression: `window.scrollTo(0,${y})` });
  await sleep(1200);
  const r = await send('Page.captureScreenshot', { format: 'png' });
  writeFileSync(path.join(OUT, `${nome}_${MODO}_${String(y).padStart(5, '0')}.png`), Buffer.from(r.result.data, 'base64'));
}
ws.close(); chrome.kill(); await sleep(800);
try { rmSync(profile, { recursive: true, force: true }); } catch {}
process.exit(0);
