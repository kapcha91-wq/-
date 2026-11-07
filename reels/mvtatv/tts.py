# usage: tts.py lines.json outdir  -> wav per key (normalized to -3 dBFS peak) + durs.json
import json, sys, wave, numpy as np
from piper import PiperVoice, SynthesisConfig
v = PiperVoice.load(sys.argv[3] if len(sys.argv) > 3 else "../tts/ru-irinia-medium.onnx")
cfg = SynthesisConfig(length_scale=0.88)
out = sys.argv[2]; durs = {}
for k, s in json.load(open(sys.argv[1])).items():
    chunks = list(v.synthesize(s, syn_config=cfg))
    sr = chunks[0].sample_rate
    x = np.concatenate([c.audio_float_array for c in chunks]).astype(np.float32)
    # trim leading/trailing silence
    nz = np.where(np.abs(x) > 0.01)[0]; x = x[max(nz[0]-200,0):nz[-1]+800]
    x = x / (np.abs(x).max() + 1e-9) * 0.7
    with wave.open(f"{out}/{k}.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((x * 32767).astype(np.int16).tobytes())
    durs[k] = round(len(x) / sr, 3)
json.dump(durs, open(f"{out}/durs.json", "w"), indent=1); print(durs)
