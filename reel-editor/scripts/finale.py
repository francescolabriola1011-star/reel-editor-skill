"""FINALE Clienti10X del motore reel-editor (8/10/2026): effetti VERI + mix + consegna.

  python3 finale.py <workdir> <output.mp4> [--music-vol 0.21]

1. legge edit.py e piazza gli effetti sonori sugli stacchi (whoosh sulle scene, pop sui
   pannelli, clic sugli scatti interni, colpo sulle ripartenze, campana in apertura,
   sigillo in chiusura), scelti da scripts/suoni_rif.py: SOLO campioni veri dei reel di
   riferimento, alla POTENZA di casa. Scrive suoni_usati.json per collaudo_suoni.py.
2. unisce i blocchi renderizzati, voce normalizzata, musica (musica.py) che si abbassa
   sotto la voce, effetti NON abbassati sopra la musica e sotto la voce.
"""
import sys, os, glob, json, wave, argparse, importlib.util, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
ROOT = os.path.expanduser('~/automazioni/editor-video')
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import suoni_rif

ap = argparse.ArgumentParser(); ap.add_argument('wd'); ap.add_argument('out'); ap.add_argument('--music-vol', type=float, default=.21)
a = ap.parse_args(); wd = a.wd
spec = importlib.util.spec_from_file_location('edit', os.path.join(wd, 'edit.py')); E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
base = os.path.join(wd, 'base.mp4'); DUR = duration(base)
SHOTS = sorted(E.SHOTS, key=lambda s: s['a'])
HITS = sorted({h for s in SHOTS if s['kind'] == 'mg' for h in getattr(s['fn'], 'hits', []) if h})
DROPS = getattr(E, 'DROPS', None) or []

ev = [(0.02, 'pop_scintilla', .25)]
for s in SHOTS:
    if s['a'] <= 0.05 or s['a'] > DUR - .2: continue
    if s['kind'] == 'mg': ev.append((s['a'], 'whoosh', .22))
    elif s.get('panel'): ev.append((s['a'] + .05, 'pop', .2))
for h in HITS:
    if h < DUR - .2: ev.append((h, 'pop_clic', .2))
for d in DROPS:
    if d < DUR - 1: ev.append((d, 'pop_boom', .22))
ev.append((max(0, DUR - .45), 'sigillo', .2))
# niente due effetti a meno di 0,18 s: si tiene il primo (il resto e' rumore, non ritmo)
ev.sort(); tenuti = []
for t, n, g in ev:
    if not tenuti or t - tenuti[-1][0] >= .18: tenuti.append((t, n, g))
suoni = suoni_rif.risolvi(tenuti, seme=os.path.basename(os.path.normpath(wd)))
# sticker YouTube (8/10/2026): clic sul pulsante e campanella vera, campioni dei reel di riferimento
for _t in getattr(E, 'STICKERS', []):
    if _t < DUR - 2: suoni += [(round(_t + .98, 3), 'rif_clic_b', .25), (round(_t + 1.48, 3), 'rif_campana_a', .4)]
suoni.sort()

sr = 48000; N = int((DUR + .5) * sr); fx = np.zeros(N)
def rd(p):
    with wave.open(p) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        if w.getnchannels() > 1: x = x.reshape(-1, w.getnchannels()).mean(1)
        return x
for t, nome, g in suoni:
    x = rd(os.path.join(ROOT, 'assets', nome + '.wav')) * g; i = int(t * sr); n = min(len(x), N - i)
    if n > 0: fx[i:i + n] += x[:n]
fxp = os.path.join(wd, 'sfx.wav')
with wave.open(fxp, 'w') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(fx, -1, 1) * 32767).astype(np.int16).tobytes())
jsave(os.path.join(wd, 'suoni_usati.json'), {'pop': True, 'motore': 'reel-editor', 'suoni': [{'t': t, 'nome': n, 'g': g} for t, n, g in suoni]})

parts = sorted(p for p in glob.glob(os.path.join(wd, 'parts', 'part_*.mp4')) if not p.endswith('.tmp.mp4'))
if not parts: raise SystemExit('ERRORE: nessun blocco renderizzato. Lancia prima render.py <workdir> all')
with open(os.path.join(wd, '_list.txt'), 'w') as f: f.write(''.join(f"file '{os.path.abspath(p)}'\n" for p in parts))
vid = os.path.join(wd, '_video.mp4'); run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', os.path.join(wd, '_list.txt'), '-c', 'copy', vid])
mus = os.path.join(wd, 'music.wav')
fc = ("[1:a]aresample=48000,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,pan=stereo|c0=c0|c1=c0,asplit=2[v1][v2];"
      f"[2:a]aresample=48000,volume={a.music_vol}[m];[m][v1]sidechaincompress=threshold=0.04:ratio=2.5:attack=15:release=400[md];"
      "[3:a]aresample=48000,pan=stereo|c0=c0|c1=c0[fx];"
      "[v2][md][fx]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95:level=0,afade=t=out:st={fs:.3f}:d=0.2[a]")
# CODA (regola di casa, 8/10/2026 dal 3266): il video chiude entro 0,45 s dall'ultima parola
_ws = [w for w in jload(os.path.join(wd, 'words.json')) if w['w']]
TEND = min(DUR, _ws[-1]['e'] + .45) if _ws else DUR
fc = fc.replace('{fs:.3f}', f'{TEND - .2:.3f}')
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
run(['ffmpeg', '-y', '-v', 'error', '-i', vid, '-i', base, '-i', mus, '-i', fxp, '-filter_complex', fc, '-map', '0:v', '-map', '[a]',
     '-t', f'{TEND:.3f}', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-shortest', a.out])
os.remove(vid); os.remove(os.path.join(wd, '_list.txt'))
print(f"OK {a.out}: {duration(a.out):.1f}s | effetti veri: {len(suoni)} ({len({n for _, n, _ in suoni})} campioni diversi)")
