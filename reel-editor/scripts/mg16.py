"""mg16: il kit mgkit dei reel portato a 16:9 (1920x1080) per i video YouTube (8/10/2026).

Stesso stile dello standard motion dei reel (riferimento 3262): fondo scuro a gradiente che
cambia a ogni scena, titolo cinetico riga bianca + corsivo pesante, animazione che MOSTRA il
concetto. In orizzontale la scena si divide in due colonne: titoli da una parte, visual
dall'altra, e il lato si alterna. I visual di mgkit e dei vis_NNNN.py si disegnano nel loro
spazio verticale (zona utile y 700-1820) e qui vengono riportati dentro un riquadro.

PALETTE DI MARCA nel codice (regola del 7/10/2026): solo blu scuro, giallo, oro e bianco.
I colori rosso, verde e viola di mgkit vengono rimappati PRIMA che i vis_NNNN.py li importino:
  rosso  -> acciaio spento (cio' che perde, il problema)
  verde  -> giallo di marca (cio' che vince)
  viola, teal, ocean -> varianti di blu
Per questo edit.py deve importare mg16 PRIMA di qualsiasi vis_NNNN.
"""
import math, random, skia
import mgkit as K

W16, H16 = 1920, 1080
NAVYB, YELB, GOLDB, STEEL, BLUEB = 0x0B1A3A, 0xFFD21F, 0xD4A537, 0x7C88AE, 0x3A6BD8
# i default dei parametri (es. p_stat(color=GRN)) sono fissati alla definizione: si rimappano qui
_MAP = {K.YEL: YELB, K.GOLD: GOLDB, K.RED: STEEL, K.GRN: YELB, K.BLUE: BLUEB, 0x1EE58B: YELB}
for _f in list(vars(K).values()):
    if callable(_f) and getattr(_f, '__defaults__', None):
        _f.__defaults__ = tuple(_MAP.get(d, d) if isinstance(d, int) and not isinstance(d, bool) else d for d in _f.__defaults__)
K.YEL, K.GOLD, K.RED, K.GRN, K.BLUE, K.NAVY = YELB, GOLDB, STEEL, YELB, BLUEB, NAVYB
K.COLORS.update(blue=BLUEB, yel=YELB, red=GOLDB, grn=YELB, gold=GOLDB, wht=K.WHT, steel=STEEL)
# (alto, basso, accento, intensita' luce)
THEMES16 = dict(navy=(0x0B1A3A, 0x02050E, YELB, .30), deep=(0x13306E, 0x030816, YELB, .26),
                gold=(0x2E2208, 0x070502, GOLDB, .32), ink=(0x161C2A, 0x020306, GOLDB, .22),
                night=(0x0B1A3A, 0x000000, K.WHT, .12), steel=(0x1C2438, 0x05070C, YELB, .20))
ALIAS = dict(blue='deep', red='ink', purple='steel', green='navy', teal='deep', ocean='deep', dark='night')
K.THEMES.update({k: THEMES16[v] for k, v in ALIAS.items()})
K.THEMES.update(THEMES16)
from mgkit import *          # noqa: E402  (dopo la rimappa: i nomi esportati sono gia' di marca)
from mgkit import _v         # noqa: E402,F401
YEL, GOLD, RED, GRN, BLUE, NAVY = YELB, GOLDB, STEEL, YELB, BLUEB, NAVYB

def th16(name):
    return THEMES16.get(ALIAS.get(name, name), THEMES16['navy'])

random.seed(9)
_P16 = [(random.uniform(0, W16), random.uniform(0, H16), random.uniform(25, 90), random.uniform(2, 5)) for _ in range(40)]

def bg16(c, g, theme='navy', glow=(1380, 540), grid=True, tilt=0):
    top, bot, acc, ga = th16(theme)
    c.drawRect(skia.Rect(0, 0, W16, H16), skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 0), (W16 * .25 * tilt, H16)], [K.C(top), K.C(bot)])))
    c.drawRect(skia.Rect(0, 0, W16, H16), skia.Paint(Shader=skia.GradientShader.MakeRadial(glow, 900, [K.C(acc, ga), K.C(acc, 0)])))
    if grid:
        off = (g * 70) % 120; p = K.P(K.WHT, .045, 2)
        for i in range(-1, 11): c.drawLine(0, i * 120 + off, W16, i * 120 + off, p)
        for i in range(0, 17): c.drawLine(i * 120, 0, i * 120, H16, p)
    for (x, y, sp, sz) in _P16:
        c.drawCircle(x + math.sin(g * 1.4 + y) * 18, (y - g * sp * 1.4) % H16, sz, K.P(acc, .3))

def vign16(c):
    c.drawRect(skia.Rect(0, 0, W16, H16), skia.Paint(Shader=skia.GradientShader.MakeRadial((W16 / 2, H16 / 2), 1250, [K.C(0, 0), K.C(0, 0), K.C(0, .5)], [0, .6, 1])))

# ---------------------------------------------------------------- titoli in colonna
STY16 = {'sm': (66, 'bk', 'rise'), 'w': (100, 'bk', 'slam'), 'big': (134, 'bk', 'slam'), 'acc': (110, 'bi', 'slam'), 'huge': (190, 'bi', 'slam')}

def layout16(lines, acc, colw=760, cy=540, scale=1.0):
    out = []
    for ln in lines:
        t, txt = ln[0], ln[1]; st = ln[2] if len(ln) > 2 else 'w'
        name, _, cn = st.partition(':'); size, k, anim = STY16[name]; size *= scale
        col = K.COLORS[cn] if cn else (acc if name in ('acc', 'huge') else K.WHT)
        w0 = K.tw(txt, k, size)
        if w0 > colw: size = size * colw / w0
        out.append([t, txt, 0, size, col, k, anim, name in ('acc', 'huge')])
    tot = sum(o[3] * 1.28 for o in out); y = cy - tot / 2
    for o in out:
        y += o[3] * .64; o[2] = y; y += o[3] * .64
    return [tuple(o) for o in out]

def draw16(c, g, L, x):
    for (t, txt, y, size, col, k, anim, glow) in L:
        if anim == 'rise': K.rise(c, g, t, txt, x, y, size, col, k)
        else: K.slam(c, g, t, txt, x, y, size, col, k, glow=col if glow else None)

def place_visual(c, g, visual, acc, cx, cy, size, zoom=1.0):
    """Disegna un visual dello spazio verticale (zona y 700-1820, centro 540,1260) dentro un
    riquadro quadrato di lato `size` centrato in (cx, cy)."""
    s = size / 1120 * zoom
    c.save(); c.clipRect(skia.Rect.MakeXYWH(cx - size * .62, cy - size * .56, size * 1.24, size * 1.12))
    c.translate(cx, cy); c.scale(s, s); c.translate(-540, -1260); visual(c, g, acc); c.restore()

_side = {'n': 0}
def scene16(visual=None, lines=(), theme='navy', swap=None, side=None, accent=None, vsize=1000):
    """Scena a tutto schermo 16:9. side='R' visual a destra e titoli a sinistra, 'L' il
    contrario, 'T' solo titoli al centro (scena-parola). Senza side il lato si alterna da solo."""
    if side is None:
        side = 'R' if _side['n'] % 2 == 0 else 'L'
    _side['n'] += 1
    if visual is None: side = 'T'
    top, bot, acc0, ga = th16(theme); acc = K.COLORS.get(accent, acc0) if accent else acc0
    lines = sorted(lines, key=lambda l: l[0])
    if side == 'T': tx, colw, vx = W16 / 2, 1500, None
    elif side == 'R': tx, colw, vx = 500, 780, 1400
    else: tx, colw, vx = 1420, 780, 520
    sc = 1.35 if side == 'T' else 1.0
    L1 = layout16([l for l in lines if swap is None or l[0] < swap], acc, colw, 540, sc)
    L2 = layout16([l for l in lines if swap is not None and l[0] >= swap], acc, colw, 540, sc)
    slams = [l[0] for l in L1 + L2 if l[6] == 'slam']
    hits = sorted(set(([swap] if swap else []) + list(getattr(visual, 'hits', []))))
    tilt = (_side['n'] % 3) - 1
    def draw(c, g):
        bg16(c, g, theme, (vx or W16 / 2, 540), grid=True, tilt=tilt)
        K.shake(c, g, slams + hits, 14)
        if visual:
            place_visual(c, g, visual, acc, vx, 540, vsize, 1.18 if (swap and g >= swap) else 1.0)
        draw16(c, g, L2 if (swap and g >= swap) else L1, tx)
    draw.hits = hits; draw.slams = slams; draw.side = side
    return draw

def split16(a, b, visual, lines=(), theme='navy', side='L', accent=None):
    """Schermo diviso: grafica su meta' schermo e Francesco in una scheda arrotondata
    sull'altra meta'. side = lato della GRAFICA."""
    top, bot, acc0, ga = th16(theme); acc = K.COLORS.get(accent, acc0) if accent else acc0
    lines = sorted(lines, key=lambda l: l[0])
    gx = 500 if side == 'L' else 1420
    L = layout16(lines, acc, 820, 190 if visual else 540, .9 if visual else 1.15)
    hits = sorted(set(getattr(visual, 'hits', []))) if visual else []
    def draw(c, g):
        bg16(c, g, theme, (gx, 620), grid=True)
        if visual: place_visual(c, g, visual, acc, gx, 660, 880)
        draw16(c, g, L, gx)
    draw.hits = hits; draw.slams = [l[0] for l in L if l[6] == 'slam']
    return dict(a=a, b=b, kind='split', fn=draw, side=side)

ZOOM16 = dict(wide=1.0, mid=1.18, tight=1.35)   # 8/10: oltre 1,35 una sorgente 1080p si sgrana (correzione 428)
def head16(a, b, zoom='wide', panel=None, title=None):
    return dict(a=a, b=b, kind='head', zoom=ZOOM16.get(zoom, zoom), panel=panel, title=title)
def mg16(a, b, sc):
    return dict(a=a, b=b, kind='mg', fn=sc)
