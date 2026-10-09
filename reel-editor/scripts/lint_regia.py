#!/usr/bin/env python3
"""Lint della REGIA di un reel montato col motore reel-editor (8/10/2026).

Due regole di Francesco che dipendevano dalla disciplina di chi scrive edit.py, ora misurate:
  1. GRAFICHE NUOVE PER OGNI VIDEO (correzione 410): almeno 4 visual scritti apposta per
     QUESTO reel in reel-editor/scripts/vis_NNNN.py e usati davvero in SHOTS. Il catalogo
     di mgkit.py e' una base, non un menu.
  2. A SCHERMO SOLO NUMERI DETTI: niente v_people (mostra sempre una cifra che sale) e
     v_sliders solo con prefix=None (senza, stampa un numero illustrativo).

    python3 lint_regia.py <work_dir_re>            # es. ~/automazioni/editor-video/work/re-3267
    python3 lint_regia.py <work_dir_re> --min 4

Exit 0 passa, 1 boccia, 2 GATE NON ESEGUITO (edit.py mancante o illeggibile).
Legge il testo con ast: non importa edit.py e non esegue niente.
"""
import argparse, ast, os, re, sys

S = os.path.dirname(os.path.abspath(__file__))


def chiamate(nodo):
    for n in ast.walk(nodo):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
            yield n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wd")
    ap.add_argument("--min", type=int, default=4)
    a = ap.parse_args()
    wd = os.path.abspath(os.path.expanduser(a.wd))
    ep = os.path.join(wd, "edit.py")
    try:
        tree = ast.parse(open(ep).read())
    except Exception as e:
        print(f"GATE NON ESEGUITO: {ep} ({e})")
        return 2
    mod = [n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module
           and re.fullmatch(r"vis_\w+", n.module)]
    propri = set()
    for m in mod:
        vp = os.path.join(S, m + ".py")
        if not os.path.exists(vp):
            print(f"GATE NON ESEGUITO: edit.py importa {m} ma {vp} non esiste")
            return 2
        propri |= {n.name for n in ast.parse(open(vp).read()).body
                   if isinstance(n, ast.FunctionDef) and n.name.startswith(("v_", "p_"))}
    usati = {c.func.id for c in chiamate(tree)}
    nuovi = sorted(propri & usati)
    errori = []
    if len(nuovi) < a.min:
        errori.append(f"visual nuovi usati: {len(nuovi)} ({', '.join(nuovi) or 'nessuno'}), ne servono "
                      f"almeno {a.min} scritti apposta in scripts/vis_NNNN.py (correzione 410)")
    for c in chiamate(tree):
        if c.func.id == "v_people" and "v_people" not in propri:
            errori.append(f"riga {c.lineno}: v_people mostra una cifra che sale, a schermo solo numeri DETTI")
        if c.func.id == "v_sliders" and "v_sliders" not in propri:
            kw = {k.arg: k.value for k in c.keywords}
            if not (isinstance(kw.get("prefix"), ast.Constant) and kw["prefix"].value is None):
                errori.append(f"riga {c.lineno}: v_sliders senza prefix=None stampa un numero illustrativo")
    print(f"regia {ep}: {len(nuovi)} visual nuovi usati ({', '.join(nuovi)})")
    if errori:
        print("FALLITO:")
        for e in errori:
            print("  " + e)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
