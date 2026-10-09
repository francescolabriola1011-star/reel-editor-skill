"""Trascrive con timestamp per parola. Uso: python3 transcribe.py <workdir>
Produce: words_raw.json (parole con indice, inizio, fine), vad.json (intervalli di parlato) e stampa la trascrizione indicizzata."""
import sys, os, wave, numpy as np, sherpa_onnx
from common import *

wd = sys.argv[1]
w = wave.open(os.path.join(wd, 'a16k.wav')); s = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
SR = 16000
cfg = sherpa_onnx.VadModelConfig(); cfg.silero_vad.model = VAD; cfg.silero_vad.min_silence_duration = 0.12
cfg.silero_vad.min_speech_duration = 0.08; cfg.silero_vad.threshold = 0.5; cfg.sample_rate = SR
vad = sherpa_onnx.VoiceActivityDetector(cfg, buffer_size_in_seconds=600)
ws = cfg.silero_vad.window_size; sp = []
def drain():
    while not vad.empty():
        g = vad.front; sp.append([g.start / SR, (g.start + len(g.samples)) / SR]); vad.pop()
for i in range(0, len(s) - ws + 1, ws):
    vad.accept_waveform(s[i:i + ws]); drain()
vad.flush(); drain()
if not sp: raise SystemExit('ERRORE: nessun parlato rilevato.')
jsave(os.path.join(wd, 'vad.json'), [[round(a, 3), round(b, 3)] for a, b in sp])

# blocchi <= 18 s tagliati nei silenzi
chunks = []; st = max(0, sp[0][0] - .3); last = sp[0][1]
for a, b in sp[1:]:
    if b - st > 18: chunks.append((st, (last + a) / 2)); st = (last + a) / 2
    last = b
chunks.append((st, min(len(s) / SR, last + .4)))
rec = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=ASR + '/encoder.int8.onnx', decoder=ASR + '/decoder.int8.onnx',
        joiner=ASR + '/joiner.int8.onnx', tokens=ASR + '/tokens.txt', model_type='nemo_transducer', num_threads=2)
words = []
for a, b in chunks:
    x = s[int(a * SR):int(b * SR)]
    if len(x) < SR * .2: continue
    stt = rec.create_stream(); stt.accept_waveform(SR, x); rec.decode_stream(stt); r = stt.result
    cur = ''; ct = 0
    for tok, ts in zip(r.tokens, r.timestamps):
        if tok.startswith(' ') or not cur:
            if cur.strip(): words.append([cur.strip(), a + ct])
            cur = tok; ct = ts
        else: cur += tok
    if cur.strip(): words.append([cur.strip(), a + ct])
out = []
for i, (t, st) in enumerate(words):
    st = max(0, st - 0.04)
    nxt = words[i + 1][1] - 0.04 if i + 1 < len(words) else 1e9
    seg_end = next((b for a, b in sp if a - .1 <= st < b + .05), st + .6)
    e = min(nxt, max(st + .12, min(seg_end, st + .09 * len(t) + .3)))
    out.append(dict(i=i, w=t, s=round(st, 3), e=round(e, 3)))
jsave(os.path.join(wd, 'words_raw.json'), out)
import words as W_; W_.show(out)
print(f"\nOK transcribe: {len(out)} parole. Correggi gli errori con: python3 words.py <workdir> fix N=parola ...")
