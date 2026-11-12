// Stress test for the screens: the opening sequence on many phones and languages, deliberate failures,
// and thousands of random map gestures. Any page error, raw error text or frozen screen fails the run.
// usage: node ci/stress/stress.cjs [baseUrl]   (serve the repo root first, e.g. python3 -m http.server 8766)
const { chromium } = require('playwright');
const BASE = process.argv[2] || 'http://localhost:8766';
const VIEWPORTS = [[360, 640], [390, 844], [412, 915], [480, 1040], [768, 1024], [1024, 768], [915, 412], [844, 390], [1280, 800]];
const results = { pass: 0, fail: 0, failures: [] };
const ok = (name, cond, info = '') => { if (cond) results.pass++; else { results.fail++; results.failures.push(name + (info ? ': ' + info : '')); } };

async function newPage(browser, vp, locale, block = []) {
  const ctx = await browser.newContext({ viewport: { width: vp[0], height: vp[1] }, locale, hasTouch: true });
  const page = await ctx.newPage(); const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (m) => { if (m.type() === 'error' && !/Failed to load resource|net::ERR_FAILED/.test(m.text())) errors.push(m.text()); });
  if (block.length) await page.route('**/*', (r) => (block.some((b) => r.request().url().includes(b)) ? r.abort() : r.continue()));
  return { ctx, page, errors };
}
async function waitMap(page, ms = 45000) {
  const t0 = Date.now();
  while (Date.now() - t0 < ms) {
    const s = await page.evaluate(() => ({ on: !!document.querySelector('#game-frame.on'), problem: !!document.querySelector('#problem.on') }));
    if (s.on || s.problem) return s;
    await page.waitForTimeout(300);
  }
  return { on: false, problem: false };
}

async function introRun(browser, vp, locale, skipAt) {
  const name = `intro ${vp.join('x')} ${locale} skip=${skipAt}`;
  const { ctx, page, errors } = await newPage(browser, vp, locale);
  await page.goto(BASE + '/app/start.html', { waitUntil: 'domcontentloaded' });
  if (skipAt) { await page.waitForTimeout(skipAt); await page.mouse.click(vp[0] / 2, vp[1] / 2); }
  else {
    await page.waitForTimeout(2300);
    const fit = await page.evaluate(() => { const e = document.querySelector('.studio .name'); if (!e) return 'gone'; const r = e.getBoundingClientRect(); return r.left >= 0 && r.right <= innerWidth; });
    ok(name + ' studio name fits', fit === true, String(fit));
    await page.waitForTimeout(1900);
    const fit2 = await page.evaluate(() => [...document.querySelectorAll('.game .ar, .game .en')].every((e) => { const r = e.getBoundingClientRect(); return r.left >= -1 && r.right <= innerWidth + 1; }));
    ok(name + ' game logo fits', fit2);
  }
  const s = await waitMap(page);
  ok(name + ' reaches the map', s.on, s.problem ? 'showed problem card' : 'timed out');
  const rtl = await page.evaluate(() => document.documentElement.dir);
  ok(name + ' direction', locale.startsWith('ar') ? rtl === 'rtl' : rtl === 'ltr');
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1);
  ok(name + ' no sideways overflow', !overflow);
  ok(name + ' no errors', errors.length === 0, errors.slice(0, 3).join(' | '));
  await ctx.close();
}

async function faultRun(browser, label, block, expect, locale = 'en-US') {
  const { ctx, page, errors } = await newPage(browser, [412, 915], locale, block);
  await page.goto(BASE + '/app/start.html', { waitUntil: 'domcontentloaded' }); await page.mouse.click(200, 400);
  const s = await waitMap(page, 60000);
  if (expect === 'problem') {
    ok(`fault ${label}: problem card shown`, s.problem);
    const txt = await page.evaluate(() => document.querySelector('#problem')?.innerText || '');
    ok(`fault ${label}: says what to do`, txt.length > 40 && !/undefined|null|error code|exception/i.test(txt), txt.slice(0, 80));
  } else ok(`fault ${label}: still reaches the map`, s.on);
  ok(`fault ${label}: no script errors`, errors.length === 0, errors.slice(0, 3).join(' | '));
  await ctx.close();
}

async function phoneSpeed(browser) {
  const ctx = await browser.newContext({ viewport: { width: 412, height: 915 }, deviceScaleFactor: 2.625 });
  const page = await ctx.newPage(); const cdp = await ctx.newCDPSession(page); await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
  const errors = []; page.on('pageerror', (e) => errors.push(e.message));
  await page.goto(BASE + '/app/world/index.html');
  await page.waitForFunction(() => window.worldReady === true, null, { timeout: 120000 });
  await page.waitForTimeout(4000);
  for (const z of [0.5, 0.9, 1.4, 2.5, 5]) {
    const ms = await page.evaluate((z) => { const v = window.world_().countries.find((c) => c.iso === 'JOR').label; window.mapView(v.x, v.y, z); const t = performance.now(); for (let i = 0; i < 10; i++) window.draw(); return (performance.now() - t) / 10; }, z);
    ok(`phone speed: map frame work at zoom ${z} (${ms.toFixed(1)} ms, budget 12)`, ms < 12);
    await page.waitForTimeout(1500);
  }
  ok('phone speed: no errors', errors.length === 0, errors.slice(0, 3).join(' | '));
  await ctx.close();
}


// two-finger zoom: the map must zoom around the fingers, stop at the edge, and never jump when a finger lifts
async function pinchCheck(browser) {
  const ctx = await browser.newContext({ viewport: { width: 412, height: 915 }, hasTouch: true, isMobile: true }); const p = await ctx.newPage();
  const errors = []; p.on('pageerror', (e) => errors.push(e.message));
  await p.goto(BASE + '/app/world/index.html'); await p.waitForFunction(() => window.worldReady === true, null, { timeout: 60000 });
  const cdp = await ctx.newCDPSession(p);
  const T = (type, pts) => cdp.send('Input.dispatchTouchEvent', { type, touchPoints: pts.map((q) => ({ x: q[0], y: q[1], id: q[2] })) });
  const V = () => p.evaluate(() => ({ x: view.x, y: view.y, z: view.z, top: (0 - view.y) * view.z + innerHeight / 2, bottom: (H - view.y) * view.z + innerHeight / 2, left: (0 - view.x) * view.z + innerWidth / 2, right: (W - view.x) * view.z + innerWidth / 2 }));
  let seed = 5; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  let worstJump = 0, edgeShown = 0;
  for (let n = 0; n < 60; n++) {
    await p.evaluate(([x, y, z]) => mapView(x, y, z), [1000 + rnd() * 6000, 600 + rnd() * 2600, 0.3 + rnd() * 3]); await p.waitForTimeout(100);
    const cx = 60 + rnd() * 290, cy = 100 + rnd() * 700, from = 20 + rnd() * 120, to = 5 + rnd() * 150;
    await T('touchStart', [[cx - from, cy, 0], [cx + from, cy, 1]]);
    for (let i = 1; i <= 12; i++) { const d = from + (to - from) * i / 12; await T('touchMove', [[cx - d, cy + i, 0], [cx + d, cy - i, 1]]); }
    await p.waitForTimeout(300); const before = await V();
    await T('touchEnd', [[cx + to, cy - 12, 1]]); await T('touchMove', [[cx + to, cy - 12, 1]]); await p.waitForTimeout(300);
    const after = await V(); await T('touchEnd', []); await p.waitForTimeout(500); const end = await V();
    worstJump = Math.max(worstJump, Math.hypot((after.x - before.x) * after.z, (after.y - before.y) * after.z));
    if (end.top > 1 || end.bottom < 914) edgeShown++;   // east and west wrap round: only north and south have an edge
  }
  ok(`two-finger zoom: no jump when a finger lifts (worst ${worstJump.toFixed(0)} px, limit 12)`, worstJump < 12);
  ok(`two-finger zoom: map edge never shows (${edgeShown} of 60)`, edgeShown === 0);
  ok('two-finger zoom: no errors', errors.length === 0, errors.slice(0, 3).join(' | '));
  await ctx.close();
}
// names must not blink on and off while the map is dragged
async function namesSteady(browser) {
  const { ctx, page } = await newPage(browser, [412, 915], 'en-US');
  await page.goto(BASE + '/app/world/index.html'); await page.waitForFunction(() => window.worldReady === true, null, { timeout: 60000 });
  for (const [x, y, z] of [[4500, 1600, 0.6], [4500, 1600, 1.1], [4400, 1500, 1.5], [4700, 1650, 2.5], [3000, 1200, 1.2], [6000, 1500, 0.8]]) {
    await page.evaluate(([x, y, z]) => mapView(x, y, z), [x, y, z]); await page.waitForTimeout(1200);
    const flips = await page.evaluate(([x0, y0, z]) => new Promise((res) => { let flips = 0, i = 0; const prev = new Map(), prevC = new Map(); const sw = innerWidth * MAPDPR, sh = innerHeight * MAPDPR;
      const f = () => { mapView(x0 + i * 4 / z, y0 + i * 2 / z, z);
        for (const [L, st] of labelState) { const was = prev.get(L); if (was !== undefined && was !== st.on && st.x > 0 && st.x < sw && st.y > 0 && st.y < sh) flips++; prev.set(L, st.on); }
        for (const [L, st] of countryState) { const was = prevC.get(L); if (was !== undefined && was !== st.on) flips++; prevC.set(L, st.on); }
        if (++i < 120) requestAnimationFrame(f); else res(flips); }; requestAnimationFrame(f); }), [x, y, z]);
    ok(`names steady while dragging at zoom ${z} (${flips} switched)`, flips <= 1);
  }
  await ctx.close();
}


// menus: every screen in both languages, choosing countries, the back button, every setting, switching language
async function menuFlow(browser, locale) {
  const { ctx, page, errors } = await newPage(browser, [412, 915], locale);
  await page.goto(BASE + '/app/start.html', { waitUntil: 'domcontentloaded' }); await page.waitForTimeout(1000); await page.mouse.click(200, 400);
  await page.waitForSelector('#menu.on', { timeout: 90000 }); await page.waitForTimeout(800);
  const L = locale.slice(0, 2);
  const overflow = () => page.evaluate(() => [...document.querySelectorAll('#menu .scr.on *')].some((e) => { const r = e.getBoundingClientRect(); return r.width && (r.right > innerWidth + 1 || r.left < -1) && getComputedStyle(e).overflowX !== 'auto' && !e.closest('.chips'); }));
  for (const scr of ['servers', 'settings', 'help']) {
    await page.click(`#m-home [data-go=${scr}]`); await page.waitForTimeout(200);
    ok(`menu ${L}: ${scr} opens`, await page.evaluate((s) => document.querySelector('#m-' + s).classList.contains('on'), scr));
    ok(`menu ${L}: ${scr} fits the screen`, !(await overflow()));
    ok(`menu ${L}: back from ${scr}`, await page.evaluate(() => window.gameBack()) && await page.evaluate(() => document.querySelector('#m-home').classList.contains('on')));
  }
  ok(`menu ${L}: back on home leaves the app`, (await page.evaluate(() => window.gameBack())) === false);
  await page.click('#m-home [data-soon]'); await page.waitForTimeout(100);
  ok(`menu ${L}: coming-soon notice`, await page.evaluate(() => document.querySelector('#toast').classList.contains('on')));
  // countries: search, regions, pick and start several times
  let seed = 11; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  for (let n = 0; n < 6; n++) {
    await page.click('.btn-play'); await page.click('[data-join]'); await page.waitForTimeout(300);
    const regs = await page.$$eval('[data-reg]', (b) => b.map((x) => x.dataset.reg)); await page.click(`[data-reg=${regs[Math.floor(rnd() * regs.length)]}]`);
    const isos = await page.$$eval('#clist [data-iso]', (b) => b.map((x) => x.dataset.iso));
    ok(`menu ${L}: countries listed (${isos.length})`, isos.length > 0);
    const iso = isos[Math.floor(rnd() * isos.length)];
    await page.click(`[data-iso=${iso}]`); await page.waitForTimeout(600);
    ok(`menu ${L}: command button for ${iso}`, await page.evaluate(() => document.querySelector('#cgo').classList.contains('on')));
    await page.click('#cgoBtn'); await page.waitForTimeout(900);
    const st = await page.evaluate(() => ({ hud: document.querySelector('#hudbar').classList.contains('on'), menu: document.querySelector('#menu').classList.contains('on'), me: document.getElementById('game-frame').contentWindow.eval('ME') }));
    ok(`menu ${L}: battle starts as ${iso}`, st.hud && !st.menu && st.me === iso, JSON.stringify(st));
    ok(`menu ${L}: back in battle opens the menu`, await page.evaluate(() => window.gameBack()) && await page.evaluate(() => document.querySelector('#menu').classList.contains('on')));
  }
  await page.fill('#cq', 'zzzz').catch(() => {});
  // search that finds nothing says so
  await page.click('.btn-play'); await page.click('[data-join]'); await page.fill('#cq', 'zzzzqq'); await page.waitForTimeout(200);
  ok(`menu ${L}: empty search explained`, await page.evaluate(() => !!document.querySelector('#clist .empty')));
  await page.evaluate(() => { window.gameBack(); window.gameBack(); });
  // settings: every option
  await page.click('#m-home [data-go=settings]');
  for (const key of ['quality', 'glide']) for (const v of await page.$$eval(`.seg[data-key=${key}] button`, (b) => b.map((x) => x.dataset.val))) {
    await page.click(`.seg[data-key=${key}] [data-val=${v}]`); await page.waitForTimeout(250);
  }
  await page.evaluate(() => { const r = document.querySelector('.rng[data-key=music]'); r.value = 20; r.dispatchEvent(new Event('input', { bubbles: true })); });
  const saved = await page.evaluate(() => ({ q: localStorage.getItem('cmd.quality'), g: localStorage.getItem('cmd.glide'), m: localStorage.getItem('cmd.music') }));
  ok(`menu ${L}: settings saved`, saved.q === 'sharp' && saved.g === 'quick' && saved.m === '20', JSON.stringify(saved));
  // language switch: the app reopens straight to the menu in the other language
  const other = L === 'ar' ? 'en' : 'ar';
  await page.click(`.seg[data-key=lang] [data-val=${other}]`);
  await page.waitForSelector('#menu.on', { timeout: 90000 });
  ok(`menu ${L}: language switched to ${other}`, await page.evaluate(() => document.documentElement.lang) === other);
  ok(`menu ${L}: no intro after a language switch`, !(await page.evaluate(() => !!document.querySelector('#intro.play'))));
  ok(`menu ${L}: no errors`, errors.length === 0, errors.slice(0, 3).join(' | '));
  await ctx.close();
}

async function mapFuzz(browser, ops) {
  const { ctx, page, errors } = await newPage(browser, [412, 915], 'en-US');
  await page.goto(BASE + '/app/world/index.html');
  await page.waitForFunction(() => window.worldReady === true || window.world_ && window.world_(), null, { timeout: 30000 });
  let seed = 99; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  let bad = 0;
  for (let i = 0; i < ops; i++) {
    const kind = rnd();
    const x = 20 + rnd() * 370, y = 20 + rnd() * 870;
    if (kind < 0.45) { await page.mouse.move(x, y); await page.mouse.down(); const n = 2 + Math.floor(rnd() * 6); for (let k = 0; k < n; k++) await page.mouse.move(x + (rnd() - 0.5) * 300, y + (rnd() - 0.5) * 300, { steps: 2 }); await page.mouse.up(); }
    else if (kind < 0.85) { await page.mouse.move(x, y); await page.mouse.wheel(0, (rnd() - 0.5) * (rnd() < 0.1 ? 4000 : 600)); }
    else { await page.mouse.click(x, y); }
    if (i % 50 === 0) {
      await page.waitForTimeout(40);
      const v = await page.evaluate(() => { const c = document.querySelector('canvas'); return c ? 1 : 0; });
      if (!v) bad++;
    }
  }
  await page.waitForTimeout(800);
  const frame = await page.evaluate(() => new Promise((res) => { let n = 0, t0 = performance.now(), worst = 0, last = t0; const f = (t) => { worst = Math.max(worst, t - last); last = t; if (++n < 60) requestAnimationFrame(f); else res({ avg: (t - t0) / n, worst }); }; requestAnimationFrame(f); }));
  ok(`map fuzz ${ops} gestures: no errors`, errors.length === 0, errors.slice(0, 3).join(' | '));
  ok(`map fuzz: canvas alive`, bad === 0);
  ok(`map fuzz: smooth after fuzz (avg ${frame.avg.toFixed(1)} ms/frame)`, frame.avg < 40);
  await ctx.close();
}

(async () => {
  const browser = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  const t0 = Date.now();
  // A. intro on every screen, both languages, watched and skipped
  const jobs = [];
  for (const vp of VIEWPORTS) for (const loc of ['en-US', 'ar-JO']) for (const skip of [0, 800 + Math.floor(Math.random() * 4000)]) jobs.push([vp, loc, skip]);
  for (let i = 0; i < jobs.length; i += 4) await Promise.all(jobs.slice(i, i + 4).map((j) => introRun(browser, ...j)));
  // B. deliberate failures
  await faultRun(browser, 'map data missing', ['world.json'], 'problem');
  await faultRun(browser, 'map data missing (Arabic)', ['world.json'], 'problem', 'ar-JO');
  await faultRun(browser, 'sounds missing', ['.ogg'], 'map');
  await faultRun(browser, 'loading photos missing', ['img/loading'], 'map');
  await faultRun(browser, 'tile list missing', ['tiles.json'], 'map');
  await faultRun(browser, 'fonts missing', ['.ttf'], 'map');
  // C. phone speed
  await phoneSpeed(browser);
  await menuFlow(browser, 'ar-JO');
  await menuFlow(browser, 'en-US');
  await pinchCheck(browser);
  await namesSteady(browser);
  // D. thousands of random gestures on the map
  await mapFuzz(browser, Number(process.env.OPS || 3000));
  await browser.close();
  console.log(`\nSTRESS: ${results.pass} passed, ${results.fail} failed in ${Math.round((Date.now() - t0) / 1000)} s`);
  for (const f of results.failures) console.log('  FAIL ' + f);
  process.exit(results.fail ? 1 : 0);
})();
