"""Synthesize the ATV promo's music bed and engine sound with numpy only.

Writes 44.1 kHz mono WAVs:
  music.wav  - 13 s beat in D minor, 109.09 BPM, grid starting at 0.2 s so bars land on the cuts
  engine.wav - single-cylinder 4-stroke: starter crank, catch, revs on the cuts, idle under the end card

Everything is deterministic (fixed seed) so the film renders the same every time.
Run: python3 synth.py <out_dir>
"""
import sys
import wave

import numpy as np

SR = 44100
DUR = 13.0
N = int(SR * DUR)
rng = np.random.default_rng(7)
t_all = np.arange(N) / SR


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    data = (x * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())


def place(buf, sig, at):
    i = int(at * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i]


def one_pole_lp(x, cutoff):
    """Cheap low-pass: repeated moving average approximating a gentle filter."""
    k = max(1, int(SR / (cutoff * 2.2)))
    ker = np.ones(k) / k
    y = np.convolve(x, ker, mode="same")
    return np.convolve(y, ker, mode="same")


def highpass(x, cutoff):
    return x - one_pole_lp(x, cutoff)


# ---------------------------------------------------------------- drums
def kick():
    d = 0.42
    t = np.arange(int(SR * d)) / SR
    f = 46 + 110 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t / 0.16)
    click = rng.standard_normal(len(t)) * np.exp(-t / 0.004) * 0.35
    return np.tanh(1.6 * (body + click)) * 0.9


def clap():
    d = 0.3
    t = np.arange(int(SR * d)) / SR
    n = highpass(rng.standard_normal(len(t)), 900)
    env = np.exp(-t / 0.09)
    # three quick hand hits before the tail
    for off in (0.0, 0.011, 0.022):
        env += 0.6 * np.exp(-np.clip(t - off, 0, None) / 0.006) * (t >= off)
    return n * env * 0.35


def hat(open_=False):
    d = 0.18 if open_ else 0.05
    t = np.arange(int(SR * d)) / SR
    n = highpass(highpass(rng.standard_normal(len(t)), 6000), 6000)
    return n * np.exp(-t / (0.06 if open_ else 0.014)) * 0.22


# ---------------------------------------------------------------- tonal
def saw_additive(freq, dur, harmonics=14, detune=0.0):
    t = np.arange(int(SR * dur)) / SR
    out = np.zeros_like(t)
    for k in range(1, harmonics + 1):
        if freq * k > SR / 2 - 1000:
            break
        out += np.sin(2 * np.pi * freq * k * (1 + detune) * t) / k
    return out * (2 / np.pi)


def note_hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def bass_note(midi, dur):
    s = saw_additive(note_hz(midi), dur, harmonics=10)
    s += 0.6 * np.sin(2 * np.pi * note_hz(midi - 12) * np.arange(len(s)) / SR)
    t = np.arange(len(s)) / SR
    env = np.minimum(1, t / 0.004) * np.exp(-t / (dur * 0.9))
    return np.tanh(1.8 * s * env) * 0.42


def pad_chord(midis, dur):
    t = np.arange(int(SR * dur)) / SR
    out = np.zeros_like(t)
    for m in midis:
        for det in (-0.004, 0.004):
            out += saw_additive(note_hz(m), dur, harmonics=6, detune=det)
    env = np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 0.4)
    return out * env * 0.05


def music():
    buf = np.zeros(N)
    beat = 0.55  # 109.09 BPM: four beats = 2.2 s = one shot
    t0 = 0.2
    sixteenth = beat / 4
    drop = 6.8
    end = 12.6
    k, c, h, ho = kick(), clap(), hat(), hat(True)
    # D minor riff in eighths, one bar per shot: D D F D | G F D C
    riff = [38, 38, 41, 38, 43, 41, 38, 36]
    n_beats = int((end - t0) / beat) + 1
    for b in range(n_beats):
        tb = t0 + b * beat
        if tb >= end:
            break
        built = tb >= drop - 1e-6
        # kick: half-time before the drop, four on the floor after
        if built or b % 2 == 0:
            place(buf, k, tb)
        # clap on 2 and 4 after the drop, only on 4 before it
        if (built and b % 2 == 1) or (not built and b % 4 == 3):
            place(buf, c, tb)
        # hats: eighths before, sixteenths after, open hat on the off-beat
        steps = 4 if built else 2
        for s in range(steps):
            th = tb + s * (beat / steps)
            place(buf, ho if (built and s == 2) else h, th)
        # bass: eighth notes from the riff
        for e in range(2):
            m = riff[(b * 2 + e) % len(riff)]
            place(buf, bass_note(m, beat / 2 * 0.95), tb + e * beat / 2)
    # pad: D minor, then B-flat, under the drop
    place(buf, pad_chord([62, 65, 69], 2.2), drop)
    place(buf, pad_chord([58, 62, 65], 2.2), drop + 2.2)
    place(buf, pad_chord([62, 65, 69], end - drop - 4.4), drop + 4.4)
    # short gap before the drop so it lands
    gap = (t_all > drop - 0.14) & (t_all < drop)
    buf[gap] *= 0.15
    # fade out
    fade = np.clip((DUR - 0.05 - t_all) / 0.6, 0, 1)
    buf *= fade
    # gentle glue
    buf = np.tanh(1.3 * buf) / np.tanh(1.3)
    return buf / (np.max(np.abs(buf)) + 1e-9) * 0.85


# ---------------------------------------------------------------- engine
def interp_rpm(keys):
    ts, vs = zip(*keys)
    return np.interp(t_all, ts, vs)


def engine():
    # (time s, rpm). Revs line up with the cuts: 0.9 headlights, 2.2 whip, 4.55 cut, 6.8 reveal.
    keys = [
        (0.00, 0), (0.34, 0), (0.36, 2400), (0.60, 1600), (0.80, 1700), (1.05, 5600),
        (1.40, 2000), (1.95, 1500), (2.12, 5000), (2.45, 2600), (2.95, 1500),
        (4.40, 1450), (4.55, 5300), (4.95, 2000), (6.30, 1500), (6.55, 3000),
        (6.85, 7200), (7.60, 6600), (8.40, 2300), (9.40, 1500), (13.0, 1300),
    ]
    rpm = interp_rpm(keys)
    fire = rpm / 120.0  # single cylinder, 4-stroke: one firing every two revolutions
    phase = np.cumsum(fire) / SR
    fires = np.nonzero(np.diff(np.floor(phase)) > 0)[0] + 1

    # Exhaust impulse response: a few damped resonances plus a noise burst.
    ir_t = np.arange(int(SR * 0.09)) / SR
    ir = (
        np.sin(2 * np.pi * 85 * ir_t) * np.exp(-ir_t / 0.022)
        + 0.7 * np.sin(2 * np.pi * 170 * ir_t) * np.exp(-ir_t / 0.012)
        + 0.15 * np.sin(2 * np.pi * 410 * ir_t) * np.exp(-ir_t / 0.006)
        + 0.5 * rng.standard_normal(len(ir_t)) * np.exp(-ir_t / 0.008)
    )
    pulses = np.zeros(N)
    # Slight cycle-to-cycle variation, as in a real single.
    pulses[fires] = 1.0 + 0.18 * rng.standard_normal(len(fires))
    body = np.fft.irfft(np.fft.rfft(pulses, 2 * N) * np.fft.rfft(ir, 2 * N))[:N]

    load = np.clip((rpm - 1300) / 5900, 0, 1)
    intake = one_pole_lp(rng.standard_normal(N), 1800) * (0.05 + 0.25 * load)
    mech = highpass(rng.standard_normal(N), 2500) * 0.02 * (rpm > 0)
    # Pitched roar that follows the revs: firing-rate harmonics, louder under load.
    fphase = 2 * np.pi * np.cumsum(fire) / SR
    roar = np.zeros(N)
    for k, w in ((2, 1.0), (3, 0.7), (4, 0.55), (6, 0.35), (8, 0.22)):
        roar += w * np.sin(k * fphase)
    roar *= (0.08 + 0.55 * load) * (rpm > 0)
    x = body * (0.45 + 0.5 * load) + roar + intake + mech
    x = np.tanh(2.0 * x)

    # Starter motor: whine plus compression thumps before the engine catches.
    st = (t_all < 0.36).astype(float)
    whine = np.sin(2 * np.pi * (220 + 40 * t_all) * t_all) * 0.12
    thump_rate = 7.0
    thumps = np.maximum(0, np.sin(2 * np.pi * thump_rate * t_all)) ** 8 * np.sin(2 * np.pi * 70 * t_all)
    x += st * (whine + 0.5 * thumps)

    fade = np.clip((DUR - 0.05 - t_all) / 0.8, 0, 1)
    x *= fade
    return x / (np.max(np.abs(x)) + 1e-9) * 0.9


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    write_wav(f"{out}/music.wav", music())
    write_wav(f"{out}/engine.wav", engine())
    print("wrote", out)
