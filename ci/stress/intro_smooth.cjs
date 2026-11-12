// Checks the opening is smooth at phone speed: samples the logos' opacity ~30 times a second while the map loads
// behind it, and fails on any jump (a sudden step instead of a fade).
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  const ctx = await b.newContext({ viewport: { width: 412, height: 915 }, deviceScaleFactor: 2.625 });
  const p = await ctx.newPage(); const cdp = await ctx.newCDPSession(p); await cdp.send('Emulation.setCPUThrottlingRate', { rate: Number(process.argv[2] || 4) });
  await p.goto('http://localhost:8766/app/start.html');
  const samples = [];
  const t0 = Date.now();
  while (Date.now() - t0 < 7200) {
    const v = await p.evaluate(() => { const g = (sel) => { const e = document.querySelector(sel); return e ? +getComputedStyle(e).opacity : -1; }; return [performance.now(), g('.studio'), g('.glow'), g('.game')]; });
    samples.push(v); await p.waitForTimeout(25);
  }
  let worst = { studio: 0, glow: 0, game: 0 }, maxv = { studio: 0, game: 0 };
  for (let i = 1; i < samples.length; i++) {
    const dt = (samples[i][0] - samples[i - 1][0]) / 1000; if (dt <= 0) continue;
    ['studio', 'glow', 'game'].forEach((k, j) => { const d = Math.abs(samples[i][j + 1] - samples[i - 1][j + 1]); if (samples[i][j + 1] >= 0 && samples[i - 1][j + 1] >= 0) worst[k] = Math.max(worst[k], d); });
    maxv.studio = Math.max(maxv.studio, samples[i][1]); maxv.game = Math.max(maxv.game, samples[i][3]);
  }
  const gaps = samples.slice(1).map((s, i) => s[0] - samples[i][0]).sort((a, z) => z - a);
  console.log('samples', samples.length, 'longest sampling gap', gaps[0].toFixed(0), 'ms');
  console.log('largest single step in opacity:', JSON.stringify(Object.fromEntries(Object.entries(worst).map(([k, v]) => [k, +v.toFixed(2)]))), 'peaks', JSON.stringify(maxv));
  // print the studio curve coarsely
  console.log('studio curve:', samples.filter((_, i) => i % 6 === 0).map((s) => s[1].toFixed(2)).join(' '));
  await b.close();
})();
