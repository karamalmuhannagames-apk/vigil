// Phone-speed performance test for the map: CPU slowed like a mid-range phone, real phone screen density.
// Measures time to first full map, frame times while dragging and zooming, and blank (unpainted) land while moving.
// usage: node ci/stress/perf.cjs [cpuSlowdown=4]
const { chromium } = require('playwright');
const SLOW = Number(process.argv[2] || 4);
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 412, height: 915 }, deviceScaleFactor: 2.625, hasTouch: true });
  const p = await ctx.newPage();
  const cdp = await ctx.newCDPSession(p); await cdp.send('Emulation.setCPUThrottlingRate', { rate: SLOW });
  const errors = []; p.on('pageerror', (e) => errors.push(e.message));
  const t0 = Date.now();
  await p.goto('http://localhost:8766/app/world/index.html?me=JOR');
  await p.waitForFunction(() => window.worldReady === true, null, { timeout: 120000 });
  await p.waitForFunction(() => window.tilesPending && window.tilesPending() === 0, null, { timeout: 120000 }).catch(() => {});
  const ready = (Date.now() - t0) / 1000;
  // frame timer inside the page
  await p.evaluate(() => { window.__fr = []; let last = performance.now(); const f = (t) => { window.__fr.push(t - last); last = t; requestAnimationFrame(f); }; requestAnimationFrame(f); });
  const measure = async (label, action) => {
    await p.evaluate(() => { window.__fr.length = 0; });
    await action();
    const fr = await p.evaluate(() => window.__fr.slice());
    fr.sort((a, z) => a - z);
    const avg = fr.reduce((a, v) => a + v, 0) / Math.max(1, fr.length), p95 = fr[Math.floor(fr.length * 0.95)] || 0, worst = fr[fr.length - 1] || 0;
    const blank = await p.evaluate(() => { const c = document.querySelector('canvas'); const g = c.getContext('2d'); let n = 0, tot = 0;
      for (let i = 0; i < 400; i++) { const x = Math.floor(Math.random() * c.width), y = Math.floor(Math.random() * c.height); const d = g.getImageData(x, y, 1, 1).data; tot++; if (d[3] === 0) n++; } return n / tot; });
    console.log(`${label.padEnd(22)} fps ${(1000 / avg).toFixed(0).padStart(3)}  p95 ${p95.toFixed(0).padStart(4)} ms  worst ${worst.toFixed(0).padStart(5)} ms`);
    return { avg, p95, worst };
  };
  const drag = async () => { for (let r = 0; r < 4; r++) { await p.mouse.move(200, 450); await p.mouse.down(); for (let i = 0; i < 30; i++) await p.mouse.move(200 - i * 8 + r * 2, 450 - i * 4, { steps: 1 }); await p.mouse.up(); await p.waitForTimeout(300); } };
  const zoom = async () => { for (let i = 0; i < 12; i++) { await p.mouse.move(206, 450); await p.mouse.wheel(0, i < 6 ? -120 : 120); await p.waitForTimeout(80); } await p.waitForTimeout(600); };
  const far = async () => { for (let i = 0; i < 25; i++) { await p.mouse.move(200, 450); await p.mouse.down(); await p.mouse.move(380, 300, { steps: 6 }); await p.mouse.up(); } await p.waitForTimeout(800); };
  const r1 = await measure('drag (short)', drag);
  const r2 = await measure('zoom in and out', zoom);
  const r3 = await measure('drag far (new land)', far);
  const mem = await p.evaluate(() => performance.memory ? Math.round(performance.memory.usedJSHeapSize / 1e6) : -1);
  console.log(`first full map ${ready.toFixed(1)} s, JS memory ${mem} MB, errors ${errors.length}`);
  await p.screenshot({ path: process.env.SHOT || '/tmp/perf.png' });
  await b.close();
})();
