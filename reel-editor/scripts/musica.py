"""[versione Clienti10X: SOLO la base, senza effetti sintetici]
Genera la base musicale incalzante + effetti sonori sincronizzati sui tagli.
  python3 music.py <workdir>
Legge da edit.py (facoltativi): BPM=128, DROPS=[33.7, 67.5] (momenti in cui la musica "riparte" dopo due battute di attesa: mettili sui passaggi chiave), SFX=True.
Produce music.wav"""
import sys, os, wave, importlib.util, numpy as np, scipy.signal as sg
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
wd = sys.argv[1]
spec = importlib.util.spec_from_file_location('edit', os.path.join(wd, 'edit.py')); E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
DURV = duration(os.path.join(wd, 'base.mp4')); sr = 48000; DUR = DURV + .15; N = int(sr * DUR)
bpm = getattr(E, 'BPM', 128); B = 60 / bpm; S = B / 4; BAR = 4 * B
SHOTS = sorted(E.SHOTS, key=lambda s: s['a']); HITS = sorted({h for s in SHOTS if s['kind'] == 'mg' for h in getattr(s['fn'], 'hits', []) if h})
drops = getattr(E, 'DROPS', None)
if drops is None: drops = [DURV * .45, DURV * .86] if DURV > 35 else ([DURV * .6] if DURV > 15 else [])
dbars = sorted({max(3, int(round(t / BAR))) for t in drops if t < DURV - 2})
breaks = {b - k for b in dbars for k in (1, 2)}
rng = np.random.default_rng(1)
def buf(): return np.zeros(N)
def add(b, t, x, g=1.0):
    i = int(t * sr)
    if i >= N or i < 0: return
    n = min(len(x), N - i); b[i:i + n] += x[:n] * g
def env(n, a, d):
    t = np.arange(n) / sr; return np.minimum(t / a, 1) * np.exp(-t / d)
def saw(f, n, det=0.0): return 2 * ((f * (1 + det) * np.arange(n) / sr) % 1) - 1
def lp(x, fc, o=2): return sg.sosfilt(sg.butter(o, fc, 'low', fs=sr, output='sos'), x)
def hp(x, fc, o=2): return sg.sosfilt(sg.butter(o, fc, 'high', fs=sr, output='sos'), x)
def bp(x, f1, f2): return sg.sosfilt(sg.butter(2, [f1, f2], 'band', fs=sr, output='sos'), x)
n = int(.35 * sr); t = np.arange(n) / sr
kick = np.sin(2 * np.pi * (48 * t + (170 - 48) * 0.045 * (1 - np.exp(-t / 0.045)))) * np.exp(-t / 0.16); kick[:200] += rng.standard_normal(200) * np.linspace(.5, 0, 200)
n = int(.22 * sr); clap = bp(rng.standard_normal(n), 900, 5000) * env(n, .002, .07); clap += np.roll(clap, 480) * .6
n = int(.06 * sr); hat = hp(rng.standard_normal(n), 7500) * env(n, .001, .018)
n = int(.14 * sr); ohat = hp(rng.standard_normal(n), 6500) * env(n, .002, .06)
chords = [(45, [57, 60, 64]), (41, [57, 60, 65]), (48, [55, 60, 64]), (43, [55, 59, 62])]   # Am F C G
mf = lambda m: 440 * 2 ** ((m - 69) / 12)
Kk, Cl, Hh, Bs, Ar, Pd, FX = buf(), buf(), buf(), buf(), buf(), buf(), buf()
for bar in range(int(DUR / BAR) + 1):
    t0 = bar * BAR; root, tri = chords[(bar // 2) % 4]; brk = bar in breaks
    for b in range(4):
        tb = t0 + b * B
        if not brk: add(Kk, tb, kick)
        if b in (1, 3) and not brk: add(Cl, tb, clap)
        if brk and bar + 1 in dbars:
            for k in range(4 if b < 2 else 8): add(Cl, tb + k * B / (4 if b < 2 else 8), clap, .35 + .5 * (b / 4))
        add(Hh, tb + B / 2, ohat, .8 if not brk else .4)
        for k in range(4): add(Hh, tb + k * S, hat, [.5, .25, .0, .3][k])
        for k in (1, 2, 3):
            n = int(S * sr * .95); f = mf(root - 12)
            add(Bs, tb + k * S, (saw(f, n) + .6 * np.sign(np.sin(2 * np.pi * f * np.arange(n) / sr))) * env(n, .004, .09), .9 if not brk else .5)
        seq = [tri[0], tri[1], tri[2], tri[1] + 12, tri[2], tri[0] + 12, tri[1], tri[2] + 12]
        for k in range(4):
            m = seq[(b * 4 + k) % 8] + (12 if (bar % 4) >= 2 else 0); n = int(.32 * sr)
            add(Ar, tb + k * S, (saw(mf(m), n, .004) + saw(mf(m), n, -.004)) * env(n, .003, .07), .55 if (b * 4 + k) % 4 else .8)
    n = int(BAR * sr); x = sum(saw(mf(m), n, d) for m in tri for d in (.003, -.003)); x *= np.minimum(np.arange(n) / (0.05 * sr), 1) * np.minimum((n - np.arange(n)) / (0.1 * sr), 1)
    add(Pd, t0, x, .5)
Bs = lp(Bs, 420, 4); Ar = hp(lp(Ar, 4200), 300); Pd = hp(lp(Pd, 1800), 250)
tt = np.arange(N) / sr; ph = (tt % B) / B; pump = .25 + .75 * np.clip(ph / .55, 0, 1) ** 1.5
inbrk = np.isin((tt // BAR).astype(int), list(breaks)) if breaks else np.zeros(N, bool); pump = np.where(inbrk, 1.0, pump)
Bs *= pump; Pd *= pump; Ar *= (.5 + .5 * pump) * np.where(inbrk, 1.5, 1.0)
def riser(tend, d):
    n = int(d * sr); x = rng.standard_normal(n); k = np.linspace(0, 1, n); y = np.zeros(n)
    for i, (f1, f2) in enumerate([(300, 900), (900, 2500), (2500, 7000), (7000, 14000)]): y += bp(x, f1, f2) * np.clip(1 - abs(k * 3.3 - i), 0, 1)
    add(FX, tend - d, y * k ** 2, .5); tq = np.arange(n) / sr; add(FX, tend - d, np.sin(2 * np.pi * (200 * tq + (900 / d) * tq * tq / 2)) * k ** 2, .12)
def impact(t, g=1.0):
    n = int(.9 * sr); tq = np.arange(n) / sr
    add(FX, t, np.sin(2 * np.pi * (38 * tq + (120 - 38) * .08 * (1 - np.exp(-tq / .08)))) * np.exp(-tq / .3) + lp(rng.standard_normal(n), 2500) * np.exp(-tq / .12) * .5, g)
def whoosh(t, g=1.0, d=.3):
    n = int(d * sr); k = np.linspace(0, 1, n); x = rng.standard_normal(n)
    add(FX, t - d * .75, (bp(x, 500, 3000) * (1 - k) + bp(x, 3000, 11000) * k) * np.sin(np.pi * k ** 1.6) ** 2, g)
# 8/10/2026: effetti sintetici tolti, li mette sonoro.py coi campioni veri
endt = DURV - .28; fade = np.clip((endt - tt) / .03, 0, 1)
mus = (Kk * .95 + Cl * .5 + Hh * .22 + Bs * .42 + Ar * .16 + Pd * .05) * fade
mix = np.tanh((mus + FX * .5) * 1.3) / 1.3
d = int(.012 * sr); wide = (Ar * .16 + Hh * .22) * fade * .35
st = np.stack([mix + wide, mix - np.concatenate([np.zeros(d), wide[:-d]])], 1); st /= np.abs(st).max() / 0.9
w = wave.open(os.path.join(wd, 'music.wav'), 'w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((st * 32767).astype(np.int16).tobytes()); w.close()
print(f"OK music.wav: {bpm} bpm, ripartenze a {[round(b * BAR, 1) for b in dbars]}s, {len(SHOTS) - 1} tagli + {len(HITS)} colpi sonorizzati")
