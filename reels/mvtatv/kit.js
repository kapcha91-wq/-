// scene kit: background + badge + header + cards + call-to-action; every element is driven by seek(t)
const $ = id => document.getElementById(id);
function el(tag, cls, html, parent = document.body) { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; parent.appendChild(e); return e; }
function base(seed = 7, opts = {}) {
  el('div', null, null).id = 'bg';
  const c = el('canvas'); c.id = 'snow'; const snow = makeSnow(c, opts.flakes ?? 95, seed);
  const badge = el('div', 'abs badge', '@mvtatv · <b>доставка по всей России</b> 🚚');
  if (opts.badgeDark) { badge.style.background = 'rgba(13,33,96,.85)'; badge.style.borderColor = 'transparent'; }
  return t => { snow(t); badge.style.opacity = eOut(seg(t, 0, 0.3)); };
}
function header({ l1, l2, sub, s1 = 96, s2 = 112, top = 292, subTop, dark = false }) {
  const a = el('div', 'k-title k-l1', l1); a.style.top = top + 'px'; a.style.fontSize = s1 + 'px';
  let y = top + s1 * 1.08, b = null, c = null;
  if (l2) { b = el('div', 'k-title k-l2', l2); b.style.top = y + 'px'; b.style.fontSize = s2 + 'px'; y += s2 * 1.25; }
  else y += s1 * 0.25;
  if (sub) { c = el('div', 'k-sub', sub); c.style.top = (subTop ?? y + 4) + 'px'; }
  if (dark) { a.style.color = '#0d2160'; a.style.textShadow = '0 6px 0 rgba(255,255,255,.6)'; if (b) { b.style.color = '#fff'; b.style.textShadow = '0 8px 0 #0d2160'; } if (c) c.style.color = '#0d2160'; }
  return t => {
    a.style.transform = `translateX(-50%) scale(${eBack(seg(t, 0, 0.35), 2.2)})`;
    if (b) b.style.transform = `translateX(-50%) scale(${eBack(seg(t, 0.15, 0.5), 2.6) * (1 + 0.04 * Math.sin(t * 12.57) * (t > 0.6))}) rotate(${-2 + Math.sin(t * 3) * 1.2}deg)`;
    if (c) { const s = eOut(seg(t, 0.3, 0.65)); c.style.opacity = s; c.style.transform = `translateX(-50%) translateY(${(1 - s) * 30}px)`; }
  };
}
// photo card centred at (x, y); returns the element (use .img, .w)
function card(key, x, y, w, h, { num, chip = true, parent = document.body, img } = {}) {
  const d = el('div', 'k-card', null, parent);
  Object.assign(d.style, { left: x - w / 2 + 'px', top: y - h / 2 + 'px', width: w + 'px', height: h + 'px' });
  d.w = el('div', 'w', null, d); d.img = el('img', null, null, d.w); d.img.src = img || PRODUCTS[key].img;
  if (chip && key) d.chip = el('div', 'k-chip', PRODUCTS[key].label, d.w);
  if (num != null) d.num = el('div', 'k-num', String(num), d);
  return d;
}
function cta(html, y = 1060, extra = {}) {
  const s = el('div', 'sticker k-cta', html); s.style.top = y + 'px'; Object.assign(s.style, extra); return s;
}
function dim(parent = document.body) { return el('div', 'k-dim', null, parent); }
