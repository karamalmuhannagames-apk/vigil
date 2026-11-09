// Plays the whole first battle in a real browser and saves screenshots.
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_PATH || 'playwright');
const out = process.argv[2] || '/tmp/shots', lang = process.argv[3] || 'en', why = process.argv[4] || 'road';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
const errors = [];
p.on('pageerror', (e) => errors.push(String(e)));
p.on('console', (m) => { if (m.type() === 'error' && !m.text().includes('404')) errors.push(m.text()); });
await p.goto('http://localhost:8765/app/index.html');
await p.waitForTimeout(1600);
if (lang === 'ar') { await p.click('#langBtn'); await p.waitForTimeout(200); }
await p.screenshot({ path: `${out}/1-intro-${lang}.png` });
await p.click('[data-act=start]'); await p.waitForTimeout(700);
const pos = await p.evaluate(() => { const v = window.__vigil; return v.R.toScreen(v.game.objective[0], v.game.objective[1]); });
await p.mouse.click(pos[0], pos[1]); await p.waitForTimeout(300);
await p.screenshot({ path: `${out}/2-why-${lang}.png` });
await p.click(`[data-act=why][data-v=${why}]`); await p.waitForTimeout(200);
await p.screenshot({ path: `${out}/3-limits-${lang}.png` });
await p.click('[data-act=send]');
await p.waitForSelector('[data-act=approve]', { timeout: 60000 }); await p.waitForTimeout(1500);
await p.screenshot({ path: `${out}/4-briefing-${lang}.png` });
const plan = await p.evaluate(() => window.__vigil.ui.briefing.planId);
await p.click('[data-act=approve]');
await p.click('#speed button[data-s="4"]');
await p.waitForTimeout(9000);
await p.screenshot({ path: `${out}/5-run-${lang}.png` });
const chip = await p.$('#battleChip:not([hidden])');
if (chip) { await chip.click(); await p.waitForTimeout(400); await p.screenshot({ path: `${out}/6-battle-${lang}.png` }); await p.click('[data-act=close]').catch(() => {}); }
// fast-forward the rest without waiting on the clock
await p.evaluate(() => { window.__vigil.ui.speed = 60; });
await p.waitForSelector('#report:not([hidden])', { timeout: 120000 }); await p.waitForTimeout(800);
await p.screenshot({ path: `${out}/7-report-${lang}.png`, fullPage: false });
const res = await p.evaluate(() => ({ r: window.__vigil.game.result, tick: window.__vigil.game.tick }));
console.log(JSON.stringify({ lang, plan, res, errors }));
await b.close();
process.exit(errors.length ? 1 : 0);
