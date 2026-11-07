// usage: node render.js page.html outDir seconds [fps] -> outDir/00000.jpg ... + outDir/sfx.json
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
const [, , html, outDir, dur, fps = '30'] = process.argv;
(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(html)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
  const n = Math.round(parseFloat(dur) * parseInt(fps));
  for (let i = 0; i < n; i++) {
    await p.evaluate(t => window.seek(t), i / parseInt(fps));
    await p.screenshot({ path: `${outDir}/${String(i).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 92 });
  }
  fs.writeFileSync(path.join(outDir, 'sfx.json'), JSON.stringify(await p.evaluate(() => window.SFX || [])));
  console.log('frames', n); await b.close();
})();
