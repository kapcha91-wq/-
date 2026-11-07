# usage: mix.py sfx.json vo_schedule.json out.wav  -- sfx + voice, sfx ducked under the voice
import json, sys, wave, subprocess, numpy as np
from sfx_lib import LIB, SR
events = json.load(open(sys.argv[1])); sch = json.load(open(sys.argv[2])); out = sys.argv[3]
n = int(sch['dur'] * SR); fx = np.zeros(n); vo = np.zeros(n)
for e in events:
    s = LIB[e['k']] * e.get('g', 1); i = int(e['t'] * SR); m = min(len(s), n - i)
    if m > 0: fx[i:i + m] += s[:m]
for k, t0 in sch['vo'].items():
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'vo/{k}.wav', '-ar', str(SR), '-ac', '1', '-f', 's16le', '-'], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16) / 32768.0; i = int(t0 * SR); m = min(len(x), n - i); vo[i:i + m] += x[:m]
# duck sfx to 40% where the voice speaks (smoothed envelope)
act = (np.abs(vo) > 0.02).astype(float); k = int(0.12 * SR)
act = np.convolve(act, np.ones(k) / k, 'same'); act = np.clip(act * 4, 0, 1)
mix = vo * 1.0 + fx * 0.55 * (1 - 0.6 * act)
mix = np.tanh(mix * 1.1) / np.tanh(1.1) * 0.89
st = np.stack([mix, mix], 1)
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
print(out, 'peak', round(float(np.abs(mix).max()), 3))
