# synthesized sound effects (no downloads): every sound is built from sines and filtered noise
import numpy as np
SR = 44100
rng = np.random.default_rng(5)
def _t(d): return np.arange(int(d * SR)) / SR
def _env(d, tau): return np.exp(-_t(d) / tau)
def _lp(x, a):  # one-pole low-pass, a may be an array (0..1)
    y = np.zeros_like(x); s = 0.0; a = np.broadcast_to(a, x.shape)
    for i in range(len(x)): s += a[i] * (x[i] - s); y[i] = s
    return y
def tick():
    t = _t(0.028); return (0.55 * np.sin(2 * np.pi * 2300 * t) + 0.45 * rng.uniform(-1, 1, len(t))) * _env(0.028, 0.006)
def thunk():
    t = _t(0.2); f = 170 * np.exp(-t * 9) + 70
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(0.2, 0.06)
    click = rng.uniform(-1, 1, len(t)) * _env(0.2, 0.004)
    return 0.9 * body + 0.35 * click
def pop():
    t = _t(0.09); f = 950 * np.exp(-t * 28) + 260
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(0.09, 0.03) * np.minimum(1, t * 900)
def whoosh(d=0.42):
    t = _t(d); n = rng.uniform(-1, 1, len(t)); u = t / d
    a = 0.02 + 0.25 * np.sin(np.pi * u) ** 2
    x = _lp(n, a) - _lp(_lp(n, a), 0.02)
    return x * np.sin(np.pi * u) ** 1.5 * 3.0
def swish(): return whoosh(0.24)
def bell(f, d=1.0):
    t = _t(d); x = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t * k) for m, a, k in [(1, 1, 3.5), (2.76, .45, 6), (5.4, .22, 10), (8.9, .1, 16)])
    return x * np.minimum(1, t * 400) * 0.55
def ding(): return bell(1318.5, 1.1)
def chime():
    out = np.zeros(int(1.4 * SR))
    for i, f in enumerate([1046.5, 1318.5, 1568.0, 2093.0]):
        b = bell(f, 1.1) * 0.7; s = int(i * 0.085 * SR); out[s:s + len(b)] += b
    return out
LIB = {k: v() for k, v in dict(tick=tick, thunk=thunk, pop=pop, whoosh=whoosh, swish=swish, ding=ding, chime=chime).items()}
