// deterministic animation helpers: every frame is a pure function of t
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const seg = (t, a, b) => clamp((t - a) / (b - a));
const eOut = u => 1 - Math.pow(1 - u, 3);
const eIn = u => u * u * u;
const eBack = (u, s = 1.7) => { const c = s + 1; return 1 + c * Math.pow(u - 1, 3) + s * Math.pow(u - 1, 2); };
const lerp = (a, b, u) => a + (b - a) * u;
function rng(seed) { return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
// snow on a canvas
function makeSnow(canvas, n = 95, seed = 7) {
  const r = rng(seed), ctx = canvas.getContext('2d'); canvas.width = 1080; canvas.height = 1920;
  const f = Array.from({ length: n }, () => ({ x: r() * 1080, y: r() * 2000, s: 1.5 + r() * 5.5, v: 50 + r() * 110,
    a: 8 + r() * 26, w: 0.4 + r() * 1.2, p: r() * 6.28, o: 0.35 + r() * 0.55 }));
  return t => { ctx.clearRect(0, 0, 1080, 1920);
    for (const k of f) { const y = (k.y + k.v * t) % 2000 - 40, x = k.x + Math.sin(k.p + t * k.w) * k.a;
      ctx.globalAlpha = k.o; ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(x, y, k.s, 0, 6.2832); ctx.fill(); } };
}
// show/hide a sticker: pop in with overshoot at a, fly out at b
function popSticker(el, t, a, b, rot = 0) {
  const i = eBack(seg(t, a, a + 0.38), 2.2), o = eIn(seg(t, b, b + 0.28));
  const sc = i * (1 - 0.25 * o), wob = Math.sin((t - a) * 7) * 1.4 * Math.exp(-(t - a) * 1.6) * (t > a);
  el.style.opacity = t < a ? 0 : (1 - o);
  el.style.transform = `translate(-50%,-50%) translateX(${-700 * o}px) scale(${sc}) rotate(${rot + wob}deg)`;
}
