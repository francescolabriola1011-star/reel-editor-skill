"""Renderizza il montaggio descritto in <workdir>/edit.py.
  python3 render.py <workdir> check                 -> valida la timeline e segnala problemi di ritmo
  python3 render.py <workdir> sheet                 -> check_N.jpg: un fotogramma per ogni inquadratura (da guardare prima del render)
  python3 render.py <workdir> test out.jpg 3.2 7.5  -> fotogrammi a tempi precisi
  python3 render.py <workdir> all [--budget 230]    -> render a blocchi con ripresa: rilancia finché non stampa "OK render completo"
"""
import sys, os, subprocess, time, hashlib, importlib.util, shutil, numpy as np, skia
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import mgkit as K
from mgkit import cl, pr, oe, ob, P, WHT, BLUE

wd = sys.argv[1]; mode = sys.argv[2]
lay = jload(os.path.join(wd, 'layout.json')); words = [w for w in jload(os.path.join(wd, 'words.json')) if w['w']]
base = os.path.join(wd, 'base.mp4'); DUR = duration(base); NF = int(round(DUR * FPS))
spec = importlib.util.spec_from_file_location('edit', os.path.join(wd, 'edit.py')); E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
SHOTS = sorted(E.SHOTS, key=lambda s: s['a'])
SUBS = getattr(E, 'SUBS', True); SUB_COLOR = getattr(E, 'SUB_COLOR', BLUE); SUBS_ON_MG = getattr(E, 'SUBS_ON_MG', False); SUB_UPPER = getattr(E, 'SUB_UPPER', False)

# ---- normalizza la timeline
problems = []
if SHOTS[0]['a'] > 0.001: problems.append(f"la prima inquadratura parte a {SHOTS[0]['a']}s: deve partire da 0"); SHOTS[0]['a'] = 0
for s, n in zip(SHOTS, SHOTS[1:]):
    if abs(s['b'] - n['a']) > 0.05: problems.append(f"buco/sovrapposizione tra {s['b']}s e {n['a']}s")
    s['b'] = n['a']
if SHOTS[-1]['b'] < DUR - 0.05: problems.append(f"l'ultima inquadratura finisce a {SHOTS[-1]['b']}s ma il video dura {DUR:.2f}s (estesa)")
SHOTS[-1]['b'] = DUR + 1
HITS = sorted({h for s in SHOTS if s['kind'] == 'mg' for h in getattr(s['fn'], 'hits', []) if h})

def check():
    n = len(SHOTS); mgs = [s for s in SHOTS if s['kind'] == 'mg']; warn = list(problems)
    for s in SHOTS:
        d = min(s['b'], DUR) - s['a']
        if d < 0.6: warn.append(f"{s['a']:.2f}s: inquadratura di {d:.2f}s, troppo corta per essere letta")
        if s['kind'] == 'head' and d > 3.6: warn.append(f"{s['a']:.2f}s: parlato fisso per {d:.1f}s -> spezza con un cambio di zoom, un pannello o un b-roll")
        if s['kind'] == 'mg' and d > 4.2 and not getattr(s['fn'], 'hits', []): warn.append(f"{s['a']:.2f}s: b-roll di {d:.1f}s senza stacchi interni -> usa swap o dividi in due scene")
        if s['kind'] == 'head' and s.get('panel') and not lay.get('panel_ok', True): warn.append(f"{s['a']:.2f}s: pannello richiesto ma non c'è spazio sopra la testa")
        if s['kind'] == 'head' and s.get('panel') and s['zoom'] > 1.05: warn.append(f"{s['a']:.2f}s: i pannelli vanno usati solo con zoom 'wide'")
        if s['kind'] == 'mg':
            for t in getattr(s['fn'], 'slams', []):
                if not (s['a'] - .02 <= t < s['b'] - .15): warn.append(f"{s['a']:.2f}s: una riga di titolo a {t}s cade fuori dalla scena ({s['a']}-{min(s['b'], DUR):.2f})")
    run_mg = 0; prev = None
    for s in SHOTS:
        if s['kind'] == 'mg':
            run_mg += min(s['b'], DUR) - s['a']
            if run_mg > 9.5: warn.append(f"{s['a']:.2f}s: più di 9 secondi di fila senza vedere il volto"); run_mg = -99
        else: run_mg = 0
        if prev and prev['kind'] == 'head' and s['kind'] == 'head' and abs(prev['zoom'] - s['zoom']) < .1 and not s.get('panel') and not prev.get('panel'):
            warn.append(f"{s['a']:.2f}s: due inquadrature sul parlato consecutive con lo stesso zoom (lo stacco non si vede)")
        prev = s
    share = sum(min(s['b'], DUR) - s['a'] for s in mgs) / DUR
    print(f"{n} inquadrature in {DUR:.1f}s (una ogni {DUR / n:.1f}s) | b-roll: {len(mgs)} scene, {share * 100:.0f}% del tempo | stacchi interni: {len(HITS)}")
    if DUR / n > 2.6: warn.append("ritmo lento: punta a un'inquadratura ogni 2 secondi circa")
    if share < .35: warn.append("poco b-roll: punta al 45-60% del tempo")
    for w_ in warn: print('  ATTENZIONE:', w_)
    if not warn: print('  timeline OK')

# ---- sottotitoli
groups = []; cur = []
for i, w in enumerate(words):
    cur.append(w); nxt = words[i + 1] if i + 1 < len(words) else None
    if (len(cur) >= 3 or sum(len(x['w']) for x in cur) >= 15 or w['w'][-1] in '.,?!:;' or nxt is None or nxt['s'] - w['e'] > .35):
        groups.append(cur); cur = []
GT = [(gp[0]['s'] - .03, min(gp[-1]['e'] + .3, groups[k + 1][0]['s'] - .03) if k + 1 < len(groups) else gp[-1]['e'] + .4) for k, gp in enumerate(groups)]

def draw_subs(c, g, y, size=62):
    for (a, b), gp in zip(GT, groups):
        if a <= g < b:
            f = K.font('b', size); txt = [(x['w'].upper() if SUB_UPPER else x['w']) for x in gp]; sp = size * .28
            tot = sum(f.measureText(t) for t in txt) + sp * (len(txt) - 1); sc = min(1, 960 / tot); x = -tot / 2
            c.save(); c.translate(540, y); c.scale(sc, sc)
            act = max((k for k, w in enumerate(gp) if w['s'] - .03 <= g), default=0)
            for k, t in enumerate(txt):
                c.drawString(t, x + 3, size * .36 + 5, f, P(0, .55, blur=7)); c.drawString(t, x, size * .36, f, P(0x000000, .9, 10))
                c.drawString(t, x, size * .36, f, P(SUB_COLOR if k == act else WHT)); x += f.measureText(t) + sp
            c.restore(); return

# ---- un fotogramma
PX, PW = 70, 940; PY, PH = lay.get('panel_y', 120), lay.get('panel_h', 490)
SAMP = skia.SamplingOptions(skia.FilterMode.kLinear)
_titles = {}
def render(c, g, img):
    sh = next((s for s in SHOTS if s['a'] <= g < s['b']), SHOTS[-1]); l = g - sh['a']; d = min(sh['b'], DUR) - sh['a']
    punch = .10 * (1 - oe(pr(l, 0, .22)))
    for tc in HITS:
        if 0 <= g - tc < .22: punch = max(punch, .08 * (1 - oe(pr(g, tc, .22))))
    c.save()
    if sh['kind'] == 'head':
        z0 = sh['zoom']; z = z0 * (1 + punch * .8) * (1 + .022 * l)
        cx = cl(lay['face_cx'], W / (2 * z), W - W / (2 * z)); cy = cl(lay['face_cy'] + .3 * lay['face_h'], H / (2 * z), H - H / (2 * z))
        if z0 < 1.05: cx, cy = W / 2, H / 2
        c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-cx, -cy); c.drawImage(img, 0, 0, SAMP); c.restore(); c.save()
        cx0 = cl(lay['face_cx'], W / (2 * z0), W - W / (2 * z0)) if z0 >= 1.05 else W / 2
        cy0 = cl(lay['face_cy'] + .3 * lay['face_h'], H / (2 * z0), H - H / (2 * z0)) if z0 >= 1.05 else H / 2
        sub_y = cl(H / 2 + (lay['chin_y'] - cy0) * z0 + .42 * lay['face_h'] * z0, 700, 1520)
        if sh.get('title'):
            L = _titles.setdefault(id(sh), K._layout(sorted(sh['title'], key=lambda x: x[0]), BLUE, 0))
            c.save(); c.translate(540, sub_y - 110); c.scale(.74, .74); c.translate(-540, 0)
            K.shake(c, g, [x[0] for x in L if x[6] == 'slam'], 14); K._draw_lines(c, g, L); c.restore()
        elif SUBS: draw_subs(c, g, sub_y)
        if sh.get('panel') and lay.get('panel_ok', True):
            q = ob(pr(l, .04, .32), 1.3) if l > .04 else 0; out = oe(pr(l, d - .14, .14))
            c.translate(0, -(PY + PH + 40) * (1 - q) - (PY + PH + 40) * out)
            c.drawRoundRect(skia.Rect.MakeXYWH(PX, PY + 14, PW, PH), 50, 50, P(BLUE, .55, blur=30))
            K.rr(c, PX, PY, PW, PH, 50, 0x0B1230, .96); K.rr(c, PX, PY, PW, PH, 50, BLUE, .9, 5)
            c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(PX, PY, PW, PH), 50, 50), True); c.translate(PX, PY); sh['panel'](c, g); c.restore()
    else:
        z = (1 + punch) * (1 + .03 * l / max(d, .1)); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
        c.save(); sh['fn'](c, g); c.restore(); c.restore(); c.save(); K.vign(c)
        if SUBS and SUBS_ON_MG: draw_subs(c, g, 1790, 50)
    c.restore()
    fa = .42 * (1 - pr(l, 0, .14)) if sh['a'] > 0 else 0
    for tc in HITS:
        if 0 <= g - tc < .12: fa = max(fa, .3 * (1 - pr(g, tc, .12)))
    if fa > 0: c.drawRect(skia.Rect(0, 0, W, H), P(WHT, fa))

def frames(t0, n):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{t0:.4f}', '-i', base, '-frames:v', str(n), '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'], stdout=subprocess.PIPE, bufsize=W * H * 8)
    last = None
    for _ in range(n):
        b = p.stdout.read(W * H * 4)
        if len(b) < W * H * 4:
            if last is None: break
        else: last = np.frombuffer(b, np.uint8).reshape(H, W, 4)
        yield last
    p.stdout.close(); p.wait()
surf = skia.Surface(W, H); cv = surf.getCanvas()
def draw(g, arr):
    render(cv, g, skia.Image.fromarray(arr, colorType=skia.kRGBA_8888_ColorType)); return surf.toarray(colorType=skia.kRGBA_8888_ColorType)

def sheet(ts, out, cols=8):
    from PIL import Image, ImageDraw
    rows = (len(ts) + cols - 1) // cols; im = Image.new('RGB', (cols * 216, rows * 384)); dr = ImageDraw.Draw(im)
    for i, t in enumerate(ts):
        t = min(max(0, t), DUR - .05); arr = next(frames(t, 1)); o = draw(round(t * FPS) / FPS, arr)
        im.paste(Image.fromarray(o[:, :, :3]).resize((216, 384)), ((i % cols) * 216, (i // cols) * 384))
        dr.rectangle([(i % cols) * 216, (i // cols) * 384, (i % cols) * 216 + 62, (i // cols) * 384 + 16], fill=(0, 0, 0)); dr.text(((i % cols) * 216 + 3, (i // cols) * 384 + 2), f'{t:.2f}s', fill=(255, 255, 0))
    im.save(out, quality=86)

if mode == 'check': check()
elif mode == 'test': sheet([float(x) for x in sys.argv[4:]], sys.argv[3]); print('OK', sys.argv[3])
elif mode == 'sheet':
    check(); ts = []
    for s in SHOTS:
        b = min(s['b'], DUR)
        ts.append(b - .12 if s['kind'] == 'mg' else (s['a'] + b) / 2)
        if s['kind'] == 'mg':
            for h in getattr(s['fn'], 'hits', []):
                if s['a'] + .4 < h < b - .4 and h - .1 not in ts: ts.append(h - .1)
    ts.sort()
    for k in range(0, len(ts), 24): sheet(ts[k:k + 24], os.path.join(wd, f'check_{k // 24 + 1}.jpg')); print('OK', os.path.join(wd, f'check_{k // 24 + 1}.jpg'))
elif mode == 'all':
    budget = float(sys.argv[sys.argv.index('--budget') + 1]) if '--budget' in sys.argv else 230
    T0 = time.time(); pd = os.path.join(wd, 'parts'); CH = 120
    hsh = hashlib.md5(open(os.path.join(wd, 'edit.py'), 'rb').read() + open(os.path.join(wd, 'words.json'), 'rb').read() + open(os.path.join(wd, 'layout.json'), 'rb').read() + str(os.path.getmtime(base)).encode()).hexdigest()
    if os.path.exists(pd) and (not os.path.exists(pd + '/_hash') or open(pd + '/_hash').read() != hsh): shutil.rmtree(pd)
    os.makedirs(pd, exist_ok=True); open(pd + '/_hash', 'w').write(hsh)
    chunks = [(a, min(a + CH, NF)) for a in range(0, NF, CH)]; per = None; done = 0
    for f0, f1 in chunks:
        out = os.path.join(pd, f'part_{f0:06d}.mp4')
        if os.path.exists(out): done += 1; continue
        if per and time.time() - T0 + per > budget:
            print(f'CONTINUA: {done}/{len(chunks)} blocchi fatti. Rilancia lo stesso comando.'); sys.exit(0)
        t1 = time.time(); tmp = out + '.tmp.mp4'
        enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-g', str(FPS), tmp], stdin=subprocess.PIPE)
        i = f0
        for arr in frames(f0 / FPS, f1 - f0):
            enc.stdin.write(draw(i / FPS, arr).tobytes()); i += 1
        enc.stdin.close(); enc.wait(); os.rename(tmp, out); done += 1; per = time.time() - t1
    print(f'OK render completo: {done} blocchi in {pd}')
