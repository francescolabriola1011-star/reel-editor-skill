"""Renderer 16:9 (1920x1080) del motore reel-editor per i video YouTube (8/10/2026).

  python3 render16.py <wd> check
  python3 render16.py <wd> sheet                  -> check_N.jpg, un fotogramma per inquadratura
  python3 render16.py <wd> test out.jpg 3.2 7.5
  python3 render16.py <wd> all [--shard 0/3]      -> render a blocchi; con --shard k/n fa un blocco ogni n

Differenze dal render.py dei reel:
- inquadrature orizzontali: 'head' (zoom sul volto), 'mg' (scena a tutto schermo),
  'split' (grafica su meta' schermo e Francesco in una scheda sull'altra meta');
- sottotitoli piccoli in basso, 2-3 parole, la parola detta in giallo di marca;
- un blocco si rifa' SOLO se cambia una inquadratura che lo tocca (testo della riga in edit.py),
  oppure se cambiano vis, kit, parole o base: su 8 minuti rifare tutto costa mezz'ora.
"""
import sys, os, ast, math, subprocess, time, hashlib, importlib.util, numpy as np, skia, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import jload, duration, FPS
import mg16 as M
import mgkit as K
W, H = M.W16, M.H16

wd = sys.argv[1]; mode = sys.argv[2]
sys.path.insert(0, wd)
lay = jload(os.path.join(wd, 'layout.json')); words = [w for w in jload(os.path.join(wd, 'words.json')) if w['w']]
base = os.path.join(wd, 'base.mp4'); DUR = duration(base); NF = int(round(DUR * FPS))
spec = importlib.util.spec_from_file_location('edit', os.path.join(wd, 'edit.py')); E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
SHOTS = sorted(E.SHOTS, key=lambda s: s['a'])
SUBS = getattr(E, 'SUBS', True); SUB_COLOR = getattr(E, 'SUB_COLOR', M.YELB)

problems = []
if SHOTS[0]['a'] > 0.001: problems.append(f"la prima inquadratura parte a {SHOTS[0]['a']}s"); SHOTS[0]['a'] = 0
for s, n in zip(SHOTS, SHOTS[1:]):
    if abs(s['b'] - n['a']) > 0.05: problems.append(f"buco/sovrapposizione tra {s['b']}s e {n['a']}s")
    s['b'] = n['a']
if SHOTS[-1]['b'] < DUR - 0.05: problems.append(f"l'ultima inquadratura finisce a {SHOTS[-1]['b']}s, il video dura {DUR:.2f}s (estesa)")
SHOTS[-1]['b'] = DUR + 1
GFX = ('mg', 'split')
HITS = sorted({h for s in SHOTS if s['kind'] in GFX for h in getattr(s['fn'], 'hits', []) if h})


def check():
    n = len(SHOTS); warn = list(problems); g_ = [s for s in SHOTS if s['kind'] in GFX]
    for s in SHOTS:
        d = min(s['b'], DUR) - s['a']
        if d < 0.7: warn.append(f"{s['a']:.2f}s: inquadratura di {d:.2f}s, troppo corta")
        if s['kind'] == 'head' and d > 7.5: warn.append(f"{s['a']:.2f}s: parlato fisso per {d:.1f}s -> spezza")
        if s['kind'] in GFX and d > 6.5 and not getattr(s['fn'], 'hits', []): warn.append(f"{s['a']:.2f}s: grafica di {d:.1f}s senza stacchi interni")
        if s['kind'] == 'head' and s.get('panel') and s['zoom'] > 1.05: warn.append(f"{s['a']:.2f}s: pannello su inquadratura stretta")
        for t in getattr(s.get('fn'), 'slams', []) if s['kind'] in GFX else []:
            if not (s['a'] - .02 <= t < min(s['b'], DUR) - .15): warn.append(f"{s['a']:.2f}s: titolo a {t}s fuori dalla scena")
    run_mg = 0; prev = None
    for s in SHOTS:
        if s['kind'] == 'mg':
            run_mg += min(s['b'], DUR) - s['a']
            if run_mg > 12: warn.append(f"{s['a']:.2f}s: oltre 12 s senza vedere Francesco"); run_mg = -99
        else: run_mg = 0
        if prev and prev['kind'] == 'head' and s['kind'] == 'head' and abs(prev['zoom'] - s['zoom']) < .1 and not s.get('panel') and not prev.get('panel'):
            warn.append(f"{s['a']:.2f}s: due inquadrature sul parlato con lo stesso zoom")
        if prev and prev['kind'] in GFX and s['kind'] in GFX and getattr(prev['fn'], 'side', 0) == getattr(s['fn'], 'side', 1) and s['kind'] == 'mg' and prev['kind'] == 'mg':
            warn.append(f"{s['a']:.2f}s: due scene di fila con la grafica dallo stesso lato")
        prev = s
    share = sum(min(s['b'], DUR) - s['a'] for s in g_) / DUR
    mgs = sum(min(s['b'], DUR) - s['a'] for s in SHOTS if s['kind'] == 'mg') / DUR
    print(f"{n} inquadrature in {DUR:.1f}s (una ogni {DUR / n:.1f}s) | grafica: {len(g_)} ({share * 100:.0f}% del tempo, di cui pieno schermo {mgs * 100:.0f}%) | stacchi interni {len(HITS)}")
    if DUR / n > 4.5: warn.append("ritmo lento: punta a un'inquadratura ogni 3-4 secondi")
    if share < .38: warn.append("poca grafica: punta al 40-55% del tempo")
    for w_ in warn: print('  ATTENZIONE:', w_)
    if not warn: print('  timeline OK')


# ---- sottotitoli: 2-3 parole, la parola detta in giallo
groups = []; cur = []
for i, w in enumerate(words):
    cur.append(w); nxt = words[i + 1] if i + 1 < len(words) else None
    if (len(cur) >= 3 or sum(len(x['w']) for x in cur) >= 16 or w['w'][-1] in '.,?!:;' or nxt is None or nxt['s'] - w['e'] > .35):
        groups.append(cur); cur = []
GT = [(gp[0]['s'] - .03, min(gp[-1]['e'] + .3, groups[k + 1][0]['s'] - .03) if k + 1 < len(groups) else gp[-1]['e'] + .4) for k, gp in enumerate(groups)]

def fine_shot(g):
    sh = next((s for s in SHOTS if s['a'] <= g < s['b']), SHOTS[-1]); return sh['b']

def draw_subs(c, g, x0, y, size=50, maxw=1100):
    for (a, b), gp in zip(GT, groups):
        if a <= g < b:
            # 9/10: le parole dette DOPO lo stacco non si anticipano nel sottotitolo (sbilanciato + titolo SBILANCIATO)
            fb = fine_shot(g); gp = [x for x in gp if x['s'] < fb - .02] or gp
            f = K.font('bk', size); txt = [x['w'] for x in gp]; sp = size * .3
            tot = sum(f.measureText(t) for t in txt) + sp * (len(txt) - 1); sc = min(1, maxw / tot); x = -tot / 2
            q = K.ob(K.pr(g, a, .16), 1.4); c.save(); c.translate(x0, y); c.scale(sc * (.85 + .15 * q), sc * (.85 + .15 * q))
            act = max((k for k, w in enumerate(gp) if w['s'] - .03 <= g), default=0)
            for k, t in enumerate(txt):
                c.drawString(t, x + 3, size * .36 + 4, f, K.P(0, .6, blur=6)); c.drawString(t, x, size * .36, f, K.P(0, .95, 9))
                c.drawString(t, x, size * .36, f, K.P(SUB_COLOR if k == act else K.WHT)); x += f.measureText(t) + sp
            c.restore(); return


SAMP = skia.SamplingOptions(skia.CubicResampler.Mitchell())   # 8/10: bicubico, il lineare impastava il volto negli zoom
PX, PY, PS = 1110, 100, .8            # pannello a destra del volto, scala dei pannelli 940x490
_titles = {}
FX, FY, FH = lay['face_cx'], lay['face_cy'], lay['face_h']

def card(c, img, rect, g, l, zoom=1.28):
    x, y, w, h = rect
    q = K.oe(K.pr(l, 0, .3)); y += 40 * (1 - q)
    c.drawRoundRect(skia.Rect.MakeXYWH(x + 8, y + 18, w, h), 40, 40, K.P(0, .55, blur=24))
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), 40, 40), True)
    z = zoom * (1 + .015 * l)
    c.translate(x + w / 2, y + h * .34); c.scale(z, z); c.translate(-FX, -FY); c.drawImage(img, 0, 0, SAMP); c.restore()
    c.drawRoundRect(skia.Rect.MakeXYWH(x, y, w, h), 40, 40, K.P(M.YELB, .85, 4))

def render(c, g, img):
    sh = next((s for s in SHOTS if s['a'] <= g < s['b']), SHOTS[-1]); l = g - sh['a']; d = min(sh['b'], DUR) - sh['a']
    punch = .06 * (1 - K.oe(K.pr(l, 0, .22))) if sh['kind'] != 'head' else 0
    for tc in HITS:
        if 0 <= g - tc < .22: punch = max(punch, .05 * (1 - K.oe(K.pr(g, tc, .22))))
    c.save()
    if sh['kind'] == 'head':
        z0 = sh['zoom']; z = z0 * (1 + .018 * l)
        tx = K.cl(FX, W / (2 * z), W - W / (2 * z)); ty = K.cl(FY + .55 * FH, H / (2 * z), H - H / (2 * z))
        if z0 < 1.05: tx, ty = W / 2, H / 2
        c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-tx, -ty); c.drawImage(img, 0, 0, SAMP); c.restore(); c.save()
        if sh.get('title'):
            L = _titles.setdefault(id(sh), M.layout16(sorted(sh['title'], key=lambda x: x[0]), M.YELB, 640, 470, .95))
            c.drawRect(skia.Rect(1000, 0, W, H), skia.Paint(Shader=skia.GradientShader.MakeLinear([(1000, 0), (1500, 0)], [K.C(0, 0), K.C(0, .7)])))
            K.shake(c, g, [x[0] for x in L if x[6] == 'slam'], 10); M.draw16(c, g, L, 1500)
        elif SUBS and not sh.get('panel'): draw_subs(c, g, W / 2, H - 112)   # 9/10: con titolo grande o pannello niente sottotitoli (testo doppio)
        if sh.get('panel'):
            q = K.ob(K.pr(l, .04, .32), 1.3) if l > .04 else 0; out = K.oe(K.pr(l, d - .14, .14))
            pw, ph = 940 * PS, 490 * PS
            c.translate((pw + 140) * (1 - q) + (pw + 140) * out, 0)
            c.drawRoundRect(skia.Rect.MakeXYWH(PX, PY + 14, pw, ph), 40, 40, K.P(M.YELB, .35, blur=30))
            K.rr(c, PX, PY, pw, ph, 40, 0x0B1A3A, .95); K.rr(c, PX, PY, pw, ph, 40, M.YELB, .9, 4)
            c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(PX, PY, pw, ph), 40, 40), True)
            c.translate(PX, PY); c.scale(PS, PS); sh['panel'](c, g); c.restore()
    elif sh['kind'] == 'split':
        z = 1 + punch * .5; c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
        sh['fn'](c, g)
        r = (1010, 70, 850, 940) if sh['side'] == 'L' else (60, 70, 850, 940)
        card(c, img, r, g, l)
        # 9/10: niente sottotitoli nello schermo diviso, il titolo dice gia' le parole chiave (testo doppio a schermo)
        c.restore(); c.save()
    else:
        z = (1 + punch) * (1 + .025 * l / max(d, .1)); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
        c.save(); sh['fn'](c, g); c.restore(); c.restore(); c.save(); M.vign16(c)
    c.restore()
    fa = .28 * (1 - K.pr(l, 0, .12)) if sh['a'] > 0 and sh['kind'] in GFX else 0
    for tc in HITS:
        if 0 <= g - tc < .1: fa = max(fa, .18 * (1 - K.pr(g, tc, .1)))
    if fa > 0: c.drawRect(skia.Rect(0, 0, W, H), K.P(K.WHT, fa))
    if STICKERS: sticker(c, g)


STICKERS = sorted(getattr(E, 'STICKERS', []))
YTRED = 0xFF0033   # il rosso e' quello di YouTube: lo sticker deve essere riconoscibile (richiesta di Francesco 8/10/2026)

def sticker(c, g):
    """Sticker YouTube quando Francesco dice di iscriversi: entra la scheda del canale, il
    cursore clicca ISCRIVITI (diventa ISCRITTO), poi la campanella oscilla. Dura 3,4 s."""
    for t0 in STICKERS:
        l = g - t0
        if not (0 <= l < 3.4): continue
        q = K.ob(K.pr(l, 0, .35), 1.3) * (1 - K.oe(K.pr(l, 3.1, .3)))
        x, y, w, h = 1170, 760, 690, 150
        c.save(); c.translate(x + w / 2, y + h / 2); c.scale(q, q); c.translate(-(x + w / 2), -(y + h / 2))
        c.drawRoundRect(skia.Rect.MakeXYWH(x + 6, y + 12, w, h), 75, 75, K.P(0, .5, blur=18))
        K.rr(c, x, y, w, h, 75, K.WHT)
        K.circ(c, x + 75, y + 75, 52, 0x0B1A3A); K.text(c, 'AE', x + 75, y + 75, 46, M.YELB, 'bk', shadow=False)
        K.text(c, 'AI Elite Advisory', x + 145, y + 58, 38, 0x0B1A3A, 'bk', align=0, shadow=False, maxw=240)
        K.text(c, 'consulenti finanziari', x + 145, y + 100, 28, 0x6B7391, 'm', align=0, shadow=False, maxw=240)
        sub = l >= 1.0; b = 1 + .12 * (1 - K.pr(l, 1.0, .2)) if sub else 1
        c.save(); c.translate(x + 500, y + 75); c.scale(b, b)
        K.rr(c, -105, -38, 210, 76, 38, 0xD9DCE3 if sub else YTRED)
        K.text(c, 'ISCRITTO' if sub else 'ISCRIVITI', 0, 0, 30, 0x30333B if sub else K.WHT, 'bk', shadow=False, maxw=180)
        c.restore()
        # campanella
        sw = 18 * math.sin((l - 1.5) * 28) * (1 - K.pr(l, 1.5, .9)) if l >= 1.5 else 0
        c.save(); c.translate(x + 640, y + 72); c.rotate(sw)
        on = l >= 1.5; col = 0x0B1A3A if on else 0x9AA0AE
        pth = skia.Path(); pth.moveTo(-26, 18); pth.cubicTo(-26, -30, -14, -36, 0, -36); pth.cubicTo(14, -36, 26, -30, 26, 18); pth.close()
        c.drawPath(pth, K.P(col)); K.rr(c, -32, 14, 64, 10, 5, col); K.circ(c, 0, 30, 8, col)
        c.restore()
        if on and l < 2.4:
            for k in (1, -1):
                a_ = 1 - K.pr(l, 1.5, .9); K.arc(c, x + 640, y + 72, 46, -60 if k > 0 else 200, 40, M.YELB, 5, a_)
        # cursore che arriva e clicca a 1,0 s
        mx = K.lerp(x + 760, x + 520, K.oe(K.pr(l, .3, .65))); my = K.lerp(y + 230, y + 95, K.oe(K.pr(l, .3, .65)))
        cur = skia.Path(); cur.moveTo(0, 0); cur.lineTo(0, 46); cur.lineTo(12, 36); cur.lineTo(21, 56); cur.lineTo(29, 52); cur.lineTo(20, 33); cur.lineTo(36, 33); cur.close()
        c.save(); c.translate(mx, my); c.drawPath(cur, K.P(0)); c.drawPath(cur, K.P(K.WHT, 1, 3)); c.restore()
        if 1.0 <= l < 1.4: K.circ(c, x + 520, y + 95, 20 + 60 * K.pr(l, 1.0, .4), YTRED, .5 * (1 - K.pr(l, 1.0, .4)), 5)
        c.restore()


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

def sheet(ts, out, cols=4):
    from PIL import Image, ImageDraw
    tw_, th_ = 480, 270; rows = (len(ts) + cols - 1) // cols; im = Image.new('RGB', (cols * tw_, rows * th_)); dr = ImageDraw.Draw(im)
    for i, t in enumerate(ts):
        t = min(max(0, t), DUR - .05); arr = next(frames(t, 1)); o = draw(round(t * FPS) / FPS, arr)
        x, y = (i % cols) * tw_, (i // cols) * th_
        im.paste(Image.fromarray(o[:, :, :3]).resize((tw_, th_)), (x, y)); dr.rectangle([x, y, x + 70, y + 16], fill=(0, 0, 0)); dr.text((x + 3, y + 2), f'{t:.2f}s', fill=(255, 255, 0))
    im.save(out, quality=86)


def firma_blocchi():
    """Per ogni blocco: il testo delle righe di SHOTS che lo toccano + firma globale."""
    src = open(os.path.join(wd, 'edit.py')).read(); tree = ast.parse(src); segs = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(getattr(t, 'id', '') == 'SHOTS' for t in node.targets) and isinstance(node.value, ast.List):
            for el in node.value.elts:
                try: a, b = [ast.literal_eval(x) for x in el.args[:2]]
                except Exception: a, b = 0, 1e9
                segs.append((a, b, ast.get_source_segment(src, el)))
    rest = src
    for _, _, s in segs: rest = rest.replace(s, '')
    glob_h = hashlib.md5(rest.encode() + open(os.path.join(wd, 'words.json'), 'rb').read() + open(os.path.join(wd, 'layout.json'), 'rb').read()
                         + str(os.path.getmtime(base)).encode())
    here = os.path.dirname(os.path.abspath(__file__))
    for f in sorted(glob.glob(os.path.join(here, 'vis_*.py'))) + [os.path.join(here, 'mg16.py'), os.path.join(here, 'mgkit.py'), os.path.abspath(__file__)]:
        if os.path.basename(f).startswith('vis_') and os.path.basename(f)[4:-3] not in src: continue
        glob_h.update(open(f, 'rb').read())
    gh = glob_h.hexdigest()
    def sig(f0, f1):
        a0, a1 = f0 / FPS - 1, f1 / FPS + 1
        return hashlib.md5((gh + ''.join(s for a, b, s in segs if a < a1 and b > a0)).encode()).hexdigest()
    return sig


def esporta_ass():
    """subs.ass con TUTTO il testo bruciato (8/10/2026): sottotitoli dai gruppi di parole e, da
    edit.py, ogni tupla (tempo, 'TESTO', ...) di titoli, pannelli ed elenchi, piu' le stringhe di
    p_stat. Serve a collaudo_testo.py, che senza questo file non girava sui video 16:9."""
    def ts(t):
        t = max(0, t); return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"
    def visibile(a):          # i sottotitoli si disegnano solo sul parlato senza titolo e negli schermi divisi
        sh = next((x for x in SHOTS if x['a'] <= a < x['b']), SHOTS[-1])
        return sh['kind'] == 'head' and not sh.get('title') and not sh.get('panel')
    ev = [(a, b, ' '.join(x['w'] for x in gp if x['s'] < fine_shot(a + .05) - .02) or ' '.join(x['w'] for x in gp)) for (a, b), gp in zip(GT, groups) if visibile(a + .05)]
    tree = ast.parse(open(os.path.join(wd, 'edit.py')).read())
    for n in ast.walk(tree):
        if isinstance(n, ast.Tuple) and len(n.elts) >= 2 and isinstance(n.elts[0], ast.Constant) and isinstance(n.elts[0].value, (int, float)) \
                and isinstance(n.elts[1], ast.Constant) and isinstance(n.elts[1].value, str) and n.elts[1].value.strip():
            t = float(n.elts[0].value); ev.append((t, t + 1.5, n.elts[1].value))
        if isinstance(n, ast.Call) and getattr(n.func, 'id', '') == 'p_stat' and len(n.args) >= 3:
            t = float(n.args[0].value); ev += [(t, t + 1.5, a.value) for a in n.args[1:3] if isinstance(a, ast.Constant)]
    ev.sort()
    with open(os.path.join(wd, 'subs.ass'), 'w', encoding='utf-8') as f:
        f.write('[Script Info]\nScriptType: v4.00+\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n')
        for a, b, txt in ev: f.write(f"Dialogue: 0,{ts(a)},{ts(b)},Default,,0,0,0,,{txt}\n")
    print('OK subs.ass:', len(ev), 'righe')


if mode == 'check': check()
elif mode == 'ass': esporta_ass()
elif mode == 'test': sheet([float(x) for x in sys.argv[4:]], sys.argv[3]); print('OK', sys.argv[3])
elif mode == 'sheet':
    check(); ts = []
    for s in SHOTS:
        b = min(s['b'], DUR)
        ts.append(b - .15 if s['kind'] in GFX else (s['a'] + b) / 2)
    ts.sort(); rng = sys.argv[3] if len(sys.argv) > 3 else None
    if rng: lo, hi = map(float, rng.split('-')); ts = [t for t in ts if lo <= t <= hi]
    for k in range(0, len(ts), 20): sheet(ts[k:k + 20], os.path.join(wd, f'check_{k // 20 + 1}.jpg')); print('OK', os.path.join(wd, f'check_{k // 20 + 1}.jpg'))
elif mode == 'solo_pannelli':
    # 9/10: dopo una modifica al motore che tocca SOLO le inquadrature con pannello, si rifanno
    # solo quei blocchi; gli altri tengono il video e prendono la firma nuova.
    pd = os.path.join(wd, 'parts'); CH = 120; sig = firma_blocchi(); rifare = 0
    for a in range(0, NF, CH):
        f1 = min(a + CH, NF); out = os.path.join(pd, f'part_{a:06d}.mp4')
        tocca = any(x['kind'] == 'head' and x.get('panel') and x['a'] < f1 / FPS and x['b'] > a / FPS for x in SHOTS)
        if tocca or not os.path.exists(out):
            for f in (out, out + '.sig'):
                if os.path.exists(f): os.remove(f)
            rifare += 1
        else: open(out + '.sig', 'w').write(sig(a, f1))
    print(f'OK: {rifare} blocchi da rifare (pannelli), gli altri confermati')
elif mode == 'all':
    shard = sys.argv[sys.argv.index('--shard') + 1] if '--shard' in sys.argv else '0/1'; sk, sn = map(int, shard.split('/'))
    pd = os.path.join(wd, 'parts'); os.makedirs(pd, exist_ok=True); CH = 120; sig = firma_blocchi()
    chunks = [(a, min(a + CH, NF)) for a in range(0, NF, CH)]
    keep = set()
    for f0, f1 in chunks:
        keep.add(f'part_{f0:06d}.mp4')
    for p in glob.glob(os.path.join(pd, 'part_*.mp4')):
        if os.path.basename(p) not in keep: os.remove(p)
    done = redo = 0; T0 = time.time()
    for idx, (f0, f1) in enumerate(chunks):
        out = os.path.join(pd, f'part_{f0:06d}.mp4'); sg_ = sig(f0, f1); sp = out + '.sig'
        if os.path.exists(out) and os.path.exists(sp) and open(sp).read() == sg_: done += 1; continue
        if idx % sn != sk: continue
        tmp = out + '.tmp.mp4'
        enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'fast', '-crf', '15', '-pix_fmt', 'yuv420p', '-g', str(FPS), tmp], stdin=subprocess.PIPE)
        i = f0
        for arr in frames(f0 / FPS, f1 - f0):
            enc.stdin.write(draw(i / FPS, arr).tobytes()); i += 1
        enc.stdin.close(); enc.wait(); os.rename(tmp, out); open(sp, 'w').write(sg_); redo += 1
        if redo % 10 == 0: print(f'  shard {shard}: {redo} blocchi rifatti, {time.time() - T0:.0f}s', flush=True)
    print(f'OK render shard {shard}: {redo} rifatti, {done} gia buoni, {len(chunks)} blocchi totali')
