"""Mostra o corregge la trascrizione.
  python3 words.py <workdir> show            -> stampa parole con indice e pause
  python3 words.py <workdir> times           -> ogni parola col suo tempo di inizio (serve per sincronizzare titoli e tagli)
  python3 words.py <workdir> raw             -> trascrizione ORIGINALE (indici da usare in cut.py --drop), anche dopo un taglio
  python3 words.py <workdir> fix 12=provvigione 40="cento mila" 57=   (vuoto = elimina la parola dai sottotitoli)
Lavora su words.json se esiste (dopo il taglio), altrimenti su words_raw.json."""
import sys, os
from common import *

def show(ws):
    line = []; 
    for k, x in enumerate(ws):
        if k and x['s'] - ws[k - 1]['e'] >= 0.45:
            line.append(f"\n   [pausa {x['s'] - ws[k - 1]['e']:.1f}s]\n")
        if not line or line[-1].endswith('\n'): line.append(f"({x['s']:.2f}s) ")
        line.append(f"{x['i']}:{x['w']} ")
        if x['w'][-1:] in '.?!': line.append('\n')
    print(''.join(line))

def times(ws):
    for k in range(0, len(ws), 7): print('  '.join(f"{x['s']:.2f} {x['w']}" for x in ws[k:k + 7]))

if __name__ == '__main__':
    wd, cmd = sys.argv[1], sys.argv[2]
    p = os.path.join(wd, 'words.json')
    if not os.path.exists(p) or cmd == 'raw': p = os.path.join(wd, 'words_raw.json')
    ws = jload(p)
    if cmd == 'fix':
        for a in sys.argv[3:]:
            i, _, t = a.partition('='); ws[int(i)]['w'] = t.strip()
        jsave(p, ws); print('OK fix su', os.path.basename(p))
    (times if cmd == 'times' else show)([x for x in ws if x['w']])
