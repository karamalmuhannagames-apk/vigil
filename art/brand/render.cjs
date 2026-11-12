const { chromium } = require('playwright');
(async () => {
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1700, height: 5000 } });
await p.goto('file://' + process.cwd() + '/brand.html'); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
for (const id of process.argv.slice(2).length ? process.argv.slice(2) : ['studio', 'game', 'iconFull', 'iconFg', 'iconMono']) {
  await p.locator('#' + id).screenshot({ path: `out_${id}.png`, omitBackground: true });
}
await b.close();
})();
