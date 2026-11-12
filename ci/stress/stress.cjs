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
  await page.goto(BASE + '/app/start.html');
  if (skipAt) { await page.waitForTimeout(skipAt); await page.mouse.click(vp[0] / 2, vp[1] / 2); }
  else {
    await page.waitForTimeout(2300);
    const fit = await page.evaluate(() => { const r = document.querySelector('.studio .name').getBoundingClientRect(); return r.left >= 0 && r.right <= innerWidth; });
    ok(name + ' studio name fits', fit);
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
  await page.goto(BASE + '/app/start.html'); await page.mouse.click(200, 400);
  const s = await waitMap(page, 60000);
  if (expect === 'problem') {
    ok(`fault ${label}: problem card shown`, s.problem);
    const txt = await page.evaluate(() => document.querySelector('#problem')?.innerText || '');
    ok(`fault ${label}: says what to do`, txt.length > 40 && !/undefined|null|error code|exception/i.test(txt), txt.slice(0, 80));
  } else ok(`fault ${label}: still reaches the map`, s.on);
  ok(`fault ${label}: no script errors`, errors.length === 0, errors.slice(0, 3).join(' | '));
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
  // C. thousands of random gestures on the map
  await mapFuzz(browser, Number(process.env.OPS || 3000));
  await browser.close();
  console.log(`\nSTRESS: ${results.pass} passed, ${results.fail} failed in ${Math.round((Date.now() - t0) / 1000)} s`);
  for (const f of results.failures) console.log('  FAIL ' + f);
  process.exit(results.fail ? 1 : 0);
})();
