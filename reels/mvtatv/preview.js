// usage: node preview.js page.html out.jpg t1 t2 ... -> stills side by side (half size)
const { chromium } = require('playwright'); const path = require('path');
const [, , html, out, ...ts] = process.argv;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(html)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
  const shots = [];
  for (const t of ts) { await p.evaluate(t => window.seek(t), parseFloat(t)); shots.push((await p.screenshot({ type: 'png' })).toString('base64')); }
  const q = await b.newPage({ viewport: { width: 545 * ts.length, height: 960 } });
  await q.setContent(`<body style="margin:0;background:#444;display:flex;gap:5px">${shots.map(s => `<img src="data:image/png;base64,${s}" style="width:540px;height:960px">`).join('')}</body>`);
  await q.screenshot({ path: out, type: 'jpeg', quality: 85 }); await b.close();
})();
