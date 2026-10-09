"""Quando si tolgono tratti da un video gia' in regia, sposta parole ed edit.py (8/10/2026).

  python3 sposta_regia.py <wd> a1-b1 a2-b2 ... [--soglia 1.0]

I tagli sono in secondi della timeline VECCHIA (quella di words.json ed edit.py attuali).
- words.json: le parole che iniziano dentro un taglio si tolgono, le altre scalano indietro;
- edit.py: ogni numero decimale >= soglia viene trattato come un tempo e rimappato; un tempo
  dentro un taglio va all'inizio del taglio. Le durate brevi (sotto soglia) restano uguali.
Fa il backup di words.json ed edit.py con suffisso .prima_tagli.
"""
import sys, os, re, json, shutil

wd = sys.argv[1]; args = sys.argv[2:]; soglia = 1.0
if '--soglia' in args:
    k = args.index('--soglia'); soglia = float(args[k + 1]); args = args[:k] + args[k + 2:]
tagli = sorted(tuple(float(x) for x in r.split('-')) for r in args)

def mappa(t):
    tolto = 0.0
    for a, b in tagli:
        if t >= b: tolto += b - a
        elif t > a: return round(a - tolto, 2)
    return round(t - tolto, 2)

wp, ep = os.path.join(wd, 'words.json'), os.path.join(wd, 'edit.py')
for p in (wp, ep): shutil.copy(p, p + '.prima_tagli')
w = json.load(open(wp)); out = []
for x in w:
    if any(a <= x['s'] < b for a, b in tagli): continue
    x = dict(x); x['s'], x['e'] = mappa(x['s']), mappa(x['e']); out.append(x)
json.dump(out, open(wp, 'w'), ensure_ascii=False, indent=1)
src = open(ep).read()
nuovo = re.sub(r'(?<![\w.])(\d+\.\d+)(?![\w.])', lambda m: (f"{mappa(float(m.group(1))):.2f}" if float(m.group(1)) >= soglia else m.group(1)), src)
open(ep, 'w').write(nuovo)
print(f"OK: {len(w) - len(out)} parole tolte, {sum(b - a for a, b in tagli):.2f} s tolti, edit.py rimappato")
