"""Taglia silenzi ed errori, oppure prepara il video senza tagli.
  python3 cut.py <workdir> --none                         -> nessun taglio (video già tagliato)
  python3 cut.py <workdir> [--drop "12-18,40-44"] [--keep-silence] [--max-pause 0.30] [--pad 0.07]
--drop: intervalli di INDICI di parole (inclusi) da eliminare: false partenze, frasi ripetute, errori.
--keep-silence: elimina solo gli errori, lascia le pause.
Produce: base.mp4 (video su cui si monta) e words.json (tempi riallineati)."""
import sys, os, wave, argparse, numpy as np, shutil
from common import *

ap = argparse.ArgumentParser(); ap.add_argument('wd'); ap.add_argument('--none', action='store_true'); ap.add_argument('--drop', default='')
ap.add_argument('--keep-silence', action='store_true'); ap.add_argument('--max-pause', type=float, default=.30); ap.add_argument('--pad', type=float, default=.07)
a = ap.parse_args(); wd = a.wd
words = jload(os.path.join(wd, 'words_raw.json')); vad = jload(os.path.join(wd, 'vad.json'))
norm = os.path.join(wd, 'norm.mp4'); base = os.path.join(wd, 'base.mp4'); dur = duration(norm)
if a.none:
    shutil.copy(norm, base); jsave(os.path.join(wd, 'words.json'), words)
    print(f'OK nessun taglio: base.mp4 = {dur:.1f}s'); sys.exit()

drop = set()
for r in filter(None, a.drop.replace(' ', '').split(',')):
    x, _, y = r.partition('-'); drop.update(range(int(x), int(y or x) + 1))
q = lambda t: round(t * FPS) / FPS
# 1) intervalli da tenere
if a.keep_silence: keep = [[0.0, dur]]
else:
    keep = []
    for s, e in vad:
        s, e = max(0, s - a.pad), min(dur, e + a.pad)
        if keep and s - keep[-1][1] <= a.max_pause - 2 * a.pad: keep[-1][1] = e
        else: keep.append([s, e])
    keep[0][0] = max(0, keep[0][0] - .12); keep[-1][1] = min(dur, keep[-1][1] + .3)
# 2) togli gli errori (da inizio prima parola scartata a inizio prossima parola tenuta), agganciando ai silenzi vicini
def snap(t):
    best = None
    for k in range(len(vad) - 1):
        g0, g1 = vad[k][1], vad[k + 1][0]
        if g1 - g0 >= .08 and g0 - .25 <= t <= g1 + .25:
            m = (g0 + g1) / 2
            if best is None or abs(m - t) < abs(best - t): best = m
    return best if best is not None else t - .05
cuts = []; i = 0
while i < len(words):
    if i in drop:
        j = i
        while j + 1 < len(words) and j + 1 in drop: j += 1
        cs = snap(words[i]['s']) if i > 0 else 0.0
        ce = snap(words[j + 1]['s']) if j + 1 < len(words) else dur
        cuts.append((cs, ce)); i = j + 1
    else: i += 1
for cs, ce in cuts:
    nk = []
    for s, e in keep:
        if e <= cs or s >= ce: nk.append([s, e])
        else:
            if s < cs: nk.append([s, cs])
            if e > ce: nk.append([ce, e])
    keep = nk
keep = [[q(s), q(e)] for s, e in keep if q(e) - q(s) >= 3 / FPS]
m = []
for s, e in keep:
    if m and s <= m[-1][1]: m[-1][1] = max(m[-1][1], e)
    else: m.append([s, e])
keep = m
# 3) audio: taglio esatto al campione con micro dissolvenze
run(['ffmpeg', '-y', '-v', 'error', '-i', norm, '-ac', '1', '-ar', '48000', os.path.join(wd, '_a48.wav')])
w = wave.open(os.path.join(wd, '_a48.wav')); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32); SR = 48000
parts = []; f = int(.006 * SR)
for s, e in keep:
    seg = x[int(round(s * SR)):int(round(e * SR))].copy(); n = int(round((e - s) * SR))
    if len(seg) < n: seg = np.concatenate([seg, np.zeros(n - len(seg), np.float32)])
    seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f); parts.append(seg)
y = np.concatenate(parts).astype(np.int16)
wo = wave.open(os.path.join(wd, '_cut.wav'), 'w'); wo.setnchannels(1); wo.setsampwidth(2); wo.setframerate(SR); wo.writeframes(y.tobytes()); wo.close()
# 4) video
expr = '+'.join(f'gte(t,{s - .001:.4f})*lt(t,{e - .001:.4f})' for s, e in keep)
with open(os.path.join(wd, '_sel.txt'), 'w') as fh: fh.write(f"[0:v]select='{expr}',setpts=N/{FPS}/TB[v]")
run(['ffmpeg', '-y', '-v', 'error', '-i', norm, '-i', os.path.join(wd, '_cut.wav'), '-filter_complex_script', os.path.join(wd, '_sel.txt'),
     '-map', '[v]', '-map', '1:a', '-r', str(FPS), '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '14', '-c:a', 'aac', '-b:a', '192k', '-shortest', base])
# 5) riallinea le parole
def remap(t):
    acc = 0
    for s, e in keep:
        if t < s: return acc
        if t <= e: return acc + (t - s)
        acc += e - s
    return acc
out = []
for wd_ in words:
    if wd_['i'] in drop: continue
    mid = (wd_['s'] + min(wd_['e'], wd_['s'] + .2)) / 2
    if not any(s - .15 <= mid <= e + .15 for s, e in keep): continue
    ns, ne = remap(wd_['s']), remap(wd_['e'])
    out.append(dict(i=len(out), w=wd_['w'], s=round(ns, 3), e=round(max(ne, ns + .1), 3)))
jsave(os.path.join(wd, 'words.json'), out)
nd = duration(base); lay = jload(os.path.join(wd, 'layout.json')); lay['duration'] = round(nd, 3); jsave(os.path.join(wd, 'layout.json'), lay)
for t in ('_a48.wav', '_cut.wav', '_sel.txt'): os.remove(os.path.join(wd, t))
print(f'OK taglio: {dur:.1f}s -> {nd:.1f}s ({len(keep)} spezzoni, {len(drop)} parole scartate, {dur - nd:.1f}s rimossi)')
print('Gli indici delle parole sono stati rinumerati: rileggi con  python3 words.py <workdir> show')
