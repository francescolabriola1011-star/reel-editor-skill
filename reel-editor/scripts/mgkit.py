"""mgkit — motion graphics per reel verticali 1080x1920 @30fps.
Tutti i tempi sono in secondi ASSOLUTI sulla timeline di base.mp4.
Vedi references/visual.md per il catalogo e references/esempio_edit.py per un montaggio completo."""
import skia, math, random, os

W, H = 1080, 1920
FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'fonts', 'Poppins-')
TF = {k: skia.Typeface.MakeFromFile(FD + v + '.ttf') for k, v in
      {'bk': 'Black', 'bi': 'BlackItalic', 'xb': 'ExtraBold', 'b': 'Bold', 'm': 'Medium'}.items()}
NAVY, BLUE, YEL, RED, GRN, WHT, GOLD, GREY = 0x0A0F24, 0x1E90FF, 0xFFD60A, 0xFF3355, 0x1EE58B, 0xFFFFFF, 0xFFC53D, 0x6B7391
COLORS = dict(blue=BLUE, yel=YEL, red=RED, grn=GRN, gold=GOLD, wht=WHT)
# tema: (sfondo alto, sfondo basso, colore luce/accento, intensità luce)
THEMES = dict(blue=(0x0D1638, 0x04060E, BLUE, .32), red=(0x4A0716, 0x0C0205, RED, .42), green=(0x06281D, 0x030A08, GRN, .28),
              gold=(0x241A05, 0x070502, GOLD, .28), ocean=(0x0A2E66, 0x03102A, 0x39B8FF, .4), teal=(0x052A2E, 0x02090B, GRN, .25),
              purple=(0x230A26, 0x06030C, RED, .28), dark=(0x0D1638, 0x04060E, YEL, .16))


# ------------------------------------------------------------------ base
def C(h, a=1.0): return skia.Color((h >> 16) & 255, (h >> 8) & 255, h & 255, int(255 * max(0, min(1, a))))
def cl(x, a=0, b=1): return max(a, min(b, x))
def pr(t, t0, d): return cl((t - t0) / d)          # avanzamento 0..1 di un'animazione che parte a t0 e dura d
def oc(x): return 1 - (1 - x) ** 3                 # ease out cubic
def oe(x): return 1 if x >= 1 else 1 - 2 ** (-10 * x)   # ease out expo
def ob(x, s=1.9):                                  # ease out back (rimbalzo)
    x -= 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2
def lerp(a, b, x): return a + (b - a) * x


def P(color, a=1, stroke=0, blur=0):
    p = skia.Paint(AntiAlias=True, Color=C(color, a))
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(stroke)
        p.setStrokeCap(skia.Paint.kRound_Cap); p.setStrokeJoin(skia.Paint.kRound_Join)
    if blur: p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    return p


_fc = {}
def font(k, size):
    key = (k, round(size))
    if key not in _fc: _fc[key] = skia.Font(TF[k], round(size))
    return _fc[key]
def tw(s, k, size): return font(k, size).measureText(s)


def text(c, s, x, y, size, color=WHT, k='bk', a=1, sc=1, rot=0, align=.5, glow=None, maxw=None, shadow=True):
    if a <= 0.01 or sc <= 0 or not s: return
    if maxw:
        w0 = tw(s, k, size)
        if w0 > maxw: size = size * maxw / w0
    f = font(k, size); w = f.measureText(s)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(sc, sc)
    ox, oy = -w * align, size * 0.36
    if glow is not None: c.drawString(s, ox, oy, f, P(glow, a * 0.55, blur=size * 0.16))
    if shadow: c.drawString(s, ox + size * .035, oy + size * .06, f, P(0x000000, a * 0.5))
    c.drawString(s, ox, oy, f, P(color, a))
    c.restore()

def pop(c, g, t0, s, x, y, size, color=WHT, k='bk', d=.24, **kw):     # entra con rimbalzo
    if g < t0: return
    p = pr(g, t0, d); text(c, s, x, y, size, color, k, a=cl(p * 3), sc=lerp(.45, 1, ob(p)), **kw)
def slam(c, g, t0, s, x, y, size, color=WHT, k='bk', d=.2, **kw):     # arriva da grande e "sbatte"
    if g < t0: return
    p = pr(g, t0, d); text(c, s, x, y, size, color, k, a=cl(p * 4), sc=lerp(2.6, 1, oe(p)), **kw)
def rise(c, g, t0, s, x, y, size, color=WHT, k='bk', d=.25, **kw):     # sale dal basso
    if g < t0: return
    p = oe(pr(g, t0, d)); text(c, s, x, y + 90 * (1 - p), size, color, k, a=p, **kw)


def circ(c, x, y, r, color, a=1, stroke=0, blur=0):
    if r > 0 and a > 0: c.drawCircle(x, y, r, P(color, a, stroke, blur))
def rr(c, x, y, w, h, rad, color, a=1, stroke=0):
    c.drawRoundRect(skia.Rect.MakeXYWH(x, y, w, h), rad, rad, P(color, a, stroke))
def line(c, x1, y1, x2, y2, color, wd=6, a=1):
    c.drawLine(x1, y1, x2, y2, P(color, a, wd))
def arc(c, x, y, r, a0, sw, color, wd, a=1, blur=0):
    c.drawArc(skia.Rect.MakeLTRB(x - r, y - r, x + r, y + r), a0, sw, False, P(color, a, wd, blur))
def tri(c, x, y, ang, s, color, a=1):
    p = skia.Path(); p.moveTo(s, 0); p.lineTo(-s * .7, s * .75); p.lineTo(-s * .7, -s * .75); p.close()
    c.save(); c.translate(x, y); c.rotate(ang); c.drawPath(p, P(color, a)); c.restore()
def check(c, x, y, s, color, ok=True, a=1):
    if ok: line(c, x - s * .5, y, x - s * .12, y + s * .38, color, s * .22, a); line(c, x - s * .12, y + s * .38, x + s * .5, y - s * .35, color, s * .22, a)
    else: line(c, x - s * .4, y - s * .4, x + s * .4, y + s * .4, color, s * .22, a); line(c, x + s * .4, y - s * .4, x - s * .4, y + s * .4, color, s * .22, a)

def person(c, x, y, s, color, a=1):
    if s <= 0 or a <= 0: return
    c.drawCircle(x, y - s * .42, s * .27, P(color, a))
    p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x - s * .42, y - s * .08, x + s * .42, y + s * .9), s * .36, s * .36))
    c.save(); c.clipRect(skia.Rect.MakeLTRB(x - s, y - s, x + s, y + s * .5), True); c.drawPath(p, P(color, a)); c.restore()

def gear(c, x, y, r, n, rot, color, a=1):
    if r <= 0: return
    p = skia.Path(); ri = r * .8
    for i in range(n):
        b = 2 * math.pi * i / n; st = 2 * math.pi / n
        for j, (rad, da) in enumerate([(ri, 0), (r, .12), (r, .38), (ri, .5)]):
            ang = b + st * da
            (p.moveTo if i == 0 and j == 0 else p.lineTo)(math.cos(ang) * rad, math.sin(ang) * rad)
    p.close(); p.addCircle(0, 0, r * .38); p.setFillType(skia.PathFillType.kEvenOdd)
    c.save(); c.translate(x, y); c.rotate(rot); c.drawPath(p, P(color, a)); c.restore()

def note(c, x, y, rot, sc, label, a=1):                # banconota
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(sc, sc)
    c.drawRoundRect(skia.Rect.MakeXYWH(-280, -134, 580, 300), 30, 30, P(0, .45 * a, blur=14))
    c.drawRoundRect(skia.Rect.MakeXYWH(-290, -150, 580, 300), 30, 30, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(-290, -150), (290, 150)], [C(0x2BF29B, a), C(0x0B9E63, a)])))
    c.drawRoundRect(skia.Rect.MakeXYWH(-268, -128, 536, 256), 18, 18, P(WHT, .55 * a, 5))
    circ(c, -200, 0, 46, WHT, .25 * a); circ(c, 200, 0, 46, WHT, .25 * a)
    text(c, label, 0, 0, 150, 0x06301F, 'bk', a=a, shadow=False, maxw=330); c.restore()

def ring(c, g, cx, cy, r, color, spd, wd=30, a=1):     # anello di frecce che gira
    rot = g * spd
    for k in range(3):
        a0 = rot + k * 120
        arc(c, cx, cy, r, a0, 88, color, wd, a)
        ae = math.radians(a0 + 96); tri(c, cx + math.cos(ae) * r, cy + math.sin(ae) * r, a0 + 96 + 90, wd * 1.5, color, a)

def pill(c, g, t0, s, x, y, color):                    # etichetta a pillola che entra con rimbalzo
    if g < t0: return
    p = pr(g, t0, .26); sc = lerp(.3, 1, ob(p)); size = 56; w = min(tw(s, 'bk', size) + 80, W - 60)
    x = cl(x, w / 2 + 24, W - w / 2 - 24)
    c.save(); c.translate(x, y); c.scale(sc, sc)
    c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2 + 6, -42, w, 104), 52, 52, P(0, .5, blur=10))
    rr(c, -w / 2, -52, w, 104, 52, color); text(c, s, 0, 0, size, NAVY, 'bk', shadow=False, maxw=w - 60); c.restore()


random.seed(7)
_PART = [(random.uniform(0, W), random.uniform(0, H), random.uniform(30, 110), random.uniform(2, 6)) for _ in range(34)]

def bg(c, g, top=0x0D1638, bot=0x04060E, acc=BLUE, ga=.3, grid=True):
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 0), (0, H)], [C(top), C(bot)])))
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=skia.GradientShader.MakeRadial((W / 2, H * .5), 950, [C(acc, ga), C(acc, 0)])))
    if grid:
        off = (g * 90) % 120; p = P(WHT, .05, 2)
        for i in range(-1, 18): c.drawLine(0, i * 120 + off, W, i * 120 + off, p)
        for i in range(0, 10): c.drawLine(i * 120, 0, i * 120, H, p)
    for (x, y, sp, sz) in _PART:
        c.drawCircle(x + math.sin(g * 1.5 + y) * 20, (y - g * sp * 1.6) % H, sz, P(acc, .35))

def vign(c):
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=skia.GradientShader.MakeRadial((W / 2, H / 2), 1150, [C(0, 0), C(0, 0), C(0, .55)], [0, .55, 1])))

def shake(c, g, cues, amp=24, d=.28):
    for tc in cues:
        if 0 <= g - tc < d:
            k = (1 - (g - tc) / d) ** 2 * amp
            c.translate(math.sin((g - tc) * 95) * k, math.cos((g - tc) * 81) * k)


# ------------------------------------------------------------------ titoli cinetici
# riga = (tempo, 'TESTO', stile)   stile: 'sm' piccola che sale | 'w' bianca | 'big' bianca grande | 'acc' accento corsivo con bagliore | 'huge' accento enorme (parole corte)
# colore forzato con suffisso: 'acc:yel', 'huge:red', 'w:grn' ... (blue, yel, red, grn, gold, wht)
STY = {'sm': (86, 'bk', 'rise'), 'w': (122, 'bk', 'slam'), 'big': (168, 'bk', 'slam'), 'acc': (134, 'bi', 'slam'), 'huge': (250, 'bi', 'slam')}

def _layout(lines, acc, top):
    out = []; y = top
    for ln in lines:
        t, txt = ln[0], ln[1]; st = ln[2] if len(ln) > 2 else 'w'
        name, _, cn = st.partition(':'); size, k, anim = STY[name]
        col = COLORS[cn] if cn else (acc if name in ('acc', 'huge') else WHT)
        w0 = tw(txt, k, size)
        if w0 > 1000: size = size * 1000 / w0
        y += size * .64
        out.append((t, txt, y, size, col, k, anim, name in ('acc', 'huge')))
        y += size * .64
    return out

def _draw_lines(c, g, L):
    for (t, txt, y, size, col, k, anim, glow) in L:
        if anim == 'rise': rise(c, g, t, txt, 540, y, size, col, k)
        else: slam(c, g, t, txt, 540, y, size, col, k, glow=col if glow else None)


def scene(visual=None, lines=(), theme='blue', swap=None, top=350, accent=None):
    """Scena a tutto schermo: sfondo a tema + visual + titoli cinetici in alto.
    swap: tempo a cui le righe precedenti spariscono, entrano quelle con tempo >= swap e la camera stringe sul visual (stacco interno)."""
    th = THEMES[theme]; acc = COLORS.get(accent, th[2]) if accent else th[2]
    if theme == 'ocean': acc = COLORS.get(accent, YEL)
    lines = sorted(lines, key=lambda l: l[0])
    L1 = _layout([l for l in lines if swap is None or l[0] < swap], acc, top)
    L2 = _layout([l for l in lines if swap is not None and l[0] >= swap], acc, top)
    slams = [l[0] for l in L1 + L2 if l[6] == 'slam']
    hits = sorted(set(([swap] if swap else []) + list(getattr(visual, 'hits', []))))
    def draw(c, g):
        bg(c, g, th[0], th[1], th[2], th[3], grid=theme != 'teal')
        shake(c, g, slams + hits)
        if visual:
            c.save()
            if swap and g >= swap: c.translate(540, 1200); c.scale(1.22, 1.22); c.translate(-540, -1200)
            visual(c, g, acc); c.restore()
        _draw_lines(c, g, L2 if (swap and g >= swap) else L1)
    draw.hits = hits; draw.slams = slams
    return draw


def _v(fn, hits=()):
    fn.hits = list(hits); return fn


# ------------------------------------------------------------------ VISUAL (zona utile: y 800-1800, centro 540,1200)
def v_fish():
    """Banco di pesciolini che attraversa lo schermo (tema 'ocean')."""
    random.seed(3); F = [(random.uniform(330, 1700), random.uniform(380, 760), random.uniform(.9, 1.9), random.uniform(0, 1400)) for _ in range(22)]
    def d(c, g, acc):
        for i, (y, sp, sz, ph) in enumerate(F):
            x = (g * sp + ph) % (W + 300) - 150; yy = y + math.sin(g * 6 + i) * 16; wag = math.sin(g * 26 + i)
            col = [0x7FD4FF, WHT, 0x4AA8FF][i % 3]; a = .5 if yy < 1150 else .95
            c.save(); c.translate(x, yy); c.scale(sz, sz); c.drawOval(skia.Rect.MakeLTRB(-34, -15, 34, 15), P(col, a))
            p = skia.Path(); p.moveTo(-28, 0); p.lineTo(-58, -18 + wag * 6); p.lineTo(-58, 18 + wag * 6); p.close()
            c.drawPath(p, P(col, a)); c.drawCircle(20, -4, 3.5, P(NAVY, a)); c.restore()
    return _v(d)


def v_chart(t, dur=1.8, mode='slow', t_badge=None):
    """Grafico a linea che si disegna da t. mode: 'slow' cresce poi si appiattisce (rosso) | 'up' crescita che accelera (verde) | 'down' crollo (rosso). t_badge: freccia che compare."""
    x0, x1, yb, hh = 120, 960, 1600, 640
    f = {'slow': lambda u: (1 - math.exp(-5 * u)) / (1 - math.exp(-5)) * .92 - 1.5 * max(0, u - .62) ** 2,
         'up': lambda u: .08 + .9 * u ** 2.4, 'down': lambda u: .9 - .82 * u ** 1.8 + .05 * math.sin(u * 14)}[mode]
    c1, c2 = (BLUE, RED) if mode != 'up' else (BLUE, GRN)
    def d(c, g, acc):
        for i in range(5): line(c, x0, yb - i * hh / 4, x1, yb - i * hh / 4, WHT, 3, .12)
        p = pr(g, t, dur); n = 70; m = max(1, int(n * p))
        path = skia.Path(); fill = skia.Path(); fill.moveTo(x0, yb)
        for i in range(m + 1):
            u = i / n; x = x0 + (x1 - x0) * u; y = yb - hh * f(u)
            (path.moveTo if i == 0 else path.lineTo)(x, y); fill.lineTo(x, y)
        fill.lineTo(x, yb); fill.close()
        sh = skia.GradientShader.MakeLinear([(x0, 0), (x1, 0)], [C(c1), C(c1), C(c2)], [0, .5, .85])
        c.drawPath(fill, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, yb - hh), (0, yb)], [C(c1, .35), C(c1, 0)])))
        pg = P(c1, .6, 34, 18); pg.setShader(sh); c.drawPath(path, pg)
        pl = P(c1, 1, 16); pl.setShader(sh); c.drawPath(path, pl)
        circ(c, x, y, 34, WHT, .25, blur=10); circ(c, x, y, 20, WHT)
        if t_badge and g >= t_badge:
            q = ob(pr(g, t_badge, .25)); bx, by = 860, yb - hh * f(.9) + (140 if mode == 'up' else 120)
            circ(c, bx, by, 92 * q, c2); c.save(); c.translate(bx, by); c.scale(q, q)
            if mode == 'up': line(c, 0, 38, 0, -30, WHT, 20); tri(c, 0, -34, -90, 30, WHT)
            else: line(c, 0, -38, 0, 30, WHT, 20); tri(c, 0, 34, 90, 30, WHT)
            c.restore()
    return _v(d)


def v_donut(t, steps, unit='%'):
    """Ciambella percentuale. steps=[(tempo, valore), ...]: sale da 0 al primo valore entro il suo tempo, poi scatta ai successivi."""
    cx, cy, r = 540, 1150, 300
    def d(c, g, acc):
        t1, v1 = steps[0]; v = lerp(0, v1, oc(pr(g, t, max(.3, t1 - t)))); bump = 1
        for k, (ts, vs) in enumerate(steps):
            if g >= ts:
                if k > 0: v = lerp(steps[k - 1][1], vs, oe(pr(g, ts, .25)))
                bump = 1 + .18 * (1 - pr(g, ts, .25))
        for i in range(48):
            a = math.radians(i * 7.5 + g * 40); r1 = r + 85; r2 = r + (115 if i % 4 == 0 else 100)
            line(c, cx + math.cos(a) * r1, cy + math.sin(a) * r1, cx + math.cos(a) * r2, cy + math.sin(a) * r2, WHT, 4, .25)
        arc(c, cx, cy, r, 0, 360, WHT, 86, .1)
        arc(c, cx, cy, r, -90, 3.6 * v, acc, 86, .5, blur=22); arc(c, cx, cy, r, -90, 3.6 * v, acc, 86)
        text(c, f'{int(round(v))}{unit}', cx, cy, 200, WHT, 'bk', sc=bump, maxw=430)
    return _v(d, [s[0] for s in steps[1:]])


def v_money(notes=()):
    """Pioggia di monete + banconote che sbattono a schermo. notes=[(tempo, '50€'), (tempo, '100€')] (max 3)."""
    random.seed(11); CO = [(random.uniform(40, 1040), random.uniform(0, 2100), random.uniform(500, 1100), random.uniform(20, 38)) for _ in range(18)]
    pos = [(470, 1060, -9), (610, 1290, 7), (480, 1520, -5)]
    def d(c, g, acc):
        for (x, y, sp, r) in CO:
            yy = (y + g * sp) % (H + 200) - 100
            circ(c, x, yy, r, GOLD, .85); circ(c, x, yy, r * .72, 0xB8860B, .9, 3); text(c, '€', x, yy, r * 1.1, 0x7A5A00, 'bk', shadow=False)
        for (tn, lab), (x, y, rot) in zip(notes, pos):
            if g >= tn: p = pr(g, tn, .2); note(c, x, y, rot, lerp(2.4, 1, oe(p)), lab, cl(p * 4))
    return _v(d, [n[0] for n in notes])


def v_network(t, n=5, symbol='€'):
    """Da una persona piccola partono linee verso n nodi grandi che compaiono in sequenza (referenze, contatti, opportunità)."""
    cx, cy = 540, 1640
    def d(c, g, acc):
        for i in range(n):
            a = -150 + 120 * i / max(1, n - 1); t0 = t + i * .11; p = oe(pr(g, t0, .3)); ar = math.radians(a)
            rad = 540 if i % 2 == 0 else 440; ex, ey = cx + math.cos(ar) * rad, cy + math.sin(ar) * rad
            if g > t0:
                pp = P(acc, .7, 7); pp.setPathEffect(skia.DashPathEffect.Make([22, 18], -g * 160)); c.drawLine(cx, cy, lerp(cx, ex, p), lerp(cy, ey, p), pp)
                q = ob(pr(g, t0 + .16, .25)) if g > t0 + .16 else 0
                circ(c, ex, ey, 96 * q, acc, .35, blur=20); circ(c, ex, ey, 78 * q, acc); text(c, symbol, ex, ey, 90, NAVY, 'bk', sc=q, shadow=False)
        circ(c, cx, cy, 70, 0x2A3358); circ(c, cx, cy, 70, GREY, 1, 6); person(c, cx, cy + 6, 62, 0xAEB6D6)
    return _v(d)


def v_counter(steps, coin_from=None, coin='€', bars=True):
    """Numero gigante che cambia a scatti. steps=[(tempo, '100'), (tempo, '200'), ...]. coin_from: prima del primo scatto gira una moneta. bars: barre che crescono dietro."""
    def d(c, g, acc):
        if bars:
            for i, (t0, _) in enumerate(steps[:3]):
                p = ob(pr(g, t0, .3), 1.2) if g >= t0 else 0; x = 150 + i * 280; hgt = lerp(230, 760, i / max(1, min(3, len(steps)) - 1)) if len(steps) > 1 else 500
                c.drawRoundRect(skia.Rect.MakeLTRB(x, 1790 - hgt * p, x + 220, 1820), 26, 26, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, 1790 - hgt), (0, 1820)], [C(acc, .7), C(acc, .1)])))
        if coin_from is not None and coin_from <= g < steps[0][0]:
            q = ob(pr(g, coin_from, .3)); fx = math.cos((g - coin_from) * 7)
            c.save(); c.translate(540, 1150); c.scale(q * (abs(fx) * .9 + .1), q)
            circ(c, 0, 0, 215, acc, .35, blur=30); circ(c, 0, 0, 190, acc); circ(c, 0, 0, 150, NAVY, .35, 10); text(c, coin, 0, 0, 230, NAVY, 'bk', shadow=False); c.restore()
        cur = None
        for s in steps:
            if g >= s[0]: cur = s
        if cur: slam(c, g, cur[0], cur[1], 540, 1150, 400, acc, 'bk', glow=acc, d=.16, maxw=980)
    return _v(d, [s[0] for s in steps])


def v_clock():
    """Orologio con lancette impazzite (tempo perso, urgenza, scadenze)."""
    cx, cy, r = 540, 1400, 300
    def d(c, g, acc):
        circ(c, cx, cy, r, 0x000000, .45); circ(c, cx, cy, r, WHT, 1, 22)
        for i in range(12):
            a = math.radians(i * 30); line(c, cx + math.cos(a) * (r - 58), cy + math.sin(a) * (r - 58), cx + math.cos(a) * (r - 28), cy + math.sin(a) * (r - 28), WHT, 12)
        a1 = math.radians(g * 1500); a2 = math.radians(g * 125)
        line(c, cx, cy, cx + math.cos(a2) * 140, cy + math.sin(a2) * 140, WHT, 24)
        for k in range(6):
            ak = a1 - k * .12; line(c, cx, cy, cx + math.cos(ak) * 225, cy + math.sin(ak) * 225, YEL, 16, .9 - k * .15)
        circ(c, cx, cy, 26, YEL)
    return _v(d)


def v_target(t_aim, t_lock, t_pulse=None):
    """Mirino che stringe (da t_aim) e aggancia (t_lock) un cerchio dorato in mezzo a tanti puntini grigi. t_pulse: onde dal bersaglio (usalo insieme a swap)."""
    random.seed(21); TD = [(random.uniform(40, 1040), random.uniform(820, 1800), random.uniform(13, 24), random.uniform(0, 6)) for _ in range(46)]
    cx, cy = 540, 1200
    def d(c, g, acc):
        for (x, y, r, ph) in TD:
            if (x - cx) ** 2 + (y - cy) ** 2 < 230 ** 2: continue
            circ(c, x + math.sin(g * 1.3 + ph) * 12, y + math.cos(g * 1.1 + ph) * 12, r, GREY, .55)
        if t_pulse and g >= t_pulse:
            for k in range(3):
                q = ((g - t_pulse) * 1.1 + k / 3) % 1; circ(c, cx, cy, 130 + 330 * q, acc, (1 - q) * .7, 8)
        circ(c, cx, cy, 150, acc, .4, blur=30); circ(c, cx, cy, 118, acc); person(c, cx, cy + 10, 104, NAVY)
        lp = oe(pr(g, t_aim, max(.2, t_lock - t_aim))); rad = lerp(820, 185, lp); locked = g >= t_lock
        col = GRN if locked else WHT; rot = g * 260 if not locked else 45 + 20 * (1 - oe(pr(g, t_lock, .3)))
        for k in range(4): arc(c, cx, cy, rad, rot + k * 90 + 20, 50, col, 16)
        for k in range(4):
            a = math.radians(k * 90); line(c, cx + math.cos(a) * (rad + 30), cy + math.sin(a) * (rad + 30), cx + math.cos(a) * (rad + 95), cy + math.sin(a) * (rad + 95), col, 10)
    return _v(d, [t_lock])


def v_spin(speed=300):
    """Doppio anello di frecce che gira (ciclo, loop, ripetizione). Solo decorativo, per scene-titolo."""
    def d(c, g, acc):
        ring(c, g, 540, 1340, 310, acc, speed, 40); ring(c, g, 540, 1340, 190, WHT, -speed * 1.4, 20, .5)
    return _v(d)


def v_loop(pills, center='LOOP'):
    """Anello che gira con etichette che compaiono lungo il giro. pills=[(tempo, 'TESTO'), ...] da 2 a 4."""
    cx, cy, r = 540, 1180, 340
    pos = [(cx, cy - r), (cx + 250, cy + r * .55), (cx - 250, cy + r * .92), (cx, cy + r * 1.45)]; cols = [WHT, YEL, RED, WHT]
    def d(c, g, acc):
        arc(c, cx, cy, r, 0, 360, WHT, 30, .08); ring(c, g, cx, cy, r, acc, 150, 30)
        a = math.radians(g * 330)
        for k in range(8): circ(c, cx + math.cos(a - k * .09) * r, cy + math.sin(a - k * .09) * r, 26 - k * 2.5, WHT, .9 - k * .11)
        text(c, center, cx, cy, 110, WHT, 'bi', a=.25 + .15 * math.sin(g * 9), maxw=460)
        for (tp, lab), (x, y), col in zip(pills, pos, cols): pill(c, g, tp, lab, x, y, col)
    return _v(d, [p[0] for p in pills])


def v_orbit(center=(), n=6, speed=260):
    """Anello veloce con persone che ci girano sopra e testo al centro. center=[(tempo, 'RIGA 1'), (tempo, 'RIGA 2')] (max 2)."""
    cx, cy, r = 540, 1240, 400
    def d(c, g, acc):
        ring(c, g, cx, cy, r, acc, speed * 2, 36)
        for k in range(n):
            a = math.radians(g * speed + k * 360 / n); x, y = cx + math.cos(a) * r, cy + math.sin(a) * r
            circ(c, x, y, 54, 0x14060C); circ(c, x, y, 54, WHT, 1, 6); person(c, x, y + 5, 48, WHT)
        for i, (tc, txt) in enumerate(center[:2]):
            slam(c, g, tc, txt, cx, cy - 60 + i * 115 if len(center) > 1 else cy, 76 if (i == 0 and len(center) > 1) else 124, WHT, 'bk', maxw=600)
    return _v(d, [x[0] for x in center])


def v_escape(t):
    """Una freccia verde sfonda il cerchio rosso e scappa in alto a destra a t (via d'uscita, soluzione, svolta)."""
    cx, cy, r = 400, 1400, 270
    def d(c, g, acc):
        for k in range(5): arc(c, cx, cy, r, g * 120 + k * 72 + 30, 44, RED, 32, .55)
        if g >= t:
            p = oe(pr(g, t, .4)); ex, ey = 900, 840; x2, y2 = lerp(cx, ex, p), lerp(cy, ey, p)
            line(c, cx, cy, x2, y2, GRN, 70, .35); c.drawLine(cx, cy, x2, y2, P(GRN, .5, 60, 22)); line(c, cx, cy, x2, y2, GRN, 38)
            tri(c, x2, y2, math.degrees(math.atan2(ey - cy, ex - cx)), 80, GRN)
        circ(c, cx, cy, 60, WHT); person(c, cx, cy + 5, 52, NAVY)
    return _v(d, [t])


def v_gears(t):
    """Ingranaggi che girano + pipeline con impulsi (automazione, sistema, processo)."""
    def d(c, g, acc):
        q = ob(pr(g, t, .35), 1.3)
        gear(c, 350, 1260, 215 * q, 12, g * 110, acc); gear(c, 668, 1450, 135 * q, 8, -g * 165 + 12, GRN); gear(c, 760, 1150, 100 * q, 7, g * 190, WHT, .85)
        y = 1720; xs = [150, 410, 670, 930]
        pp = P(WHT, .4, 8); pp.setPathEffect(skia.DashPathEffect.Make([24, 20], -g * 300)); c.drawLine(xs[0], y, xs[-1], y, pp)
        for i, x in enumerate(xs):
            on = (int(g * 7) % 4) == i
            if on: circ(c, x, y, 76, acc, .4, blur=16)
            circ(c, x, y, 50, acc if on else 0x1A2450); circ(c, x, y, 50, WHT, .9, 6)
    return _v(d)


def v_radar(t, t_pin=None):
    """Radar su mappa: il fascio gira e accende le persone trovate. t_pin: cade un segnaposto giallo al centro (usalo con swap)."""
    random.seed(5); RP = [(random.uniform(0, 360), random.uniform(130, 640)) for _ in range(22)]
    cx, cy = 540, 1220
    def d(c, g, acc):
        c.save(); c.translate(cx, cy); c.rotate(24)
        for i in range(-9, 10):
            line(c, i * 150, -1400, i * 150, 1400, WHT, 10 if i % 3 == 0 else 4, .07); line(c, -1400, i * 150, 1400, i * 150, WHT, 10 if i % 3 == 0 else 4, .07)
        c.restore()
        for r in (160, 320, 480, 640): circ(c, cx, cy, r, acc, .3, 4)
        sw = ((g - t) * 300) % 360
        for k in range(26): c.drawArc(skia.Rect.MakeLTRB(cx - 640, cy - 640, cx + 640, cy + 640), sw - k * 2.6 - 2.6, 3, True, P(acc, .32 * (1 - k / 26)))
        a = math.radians(sw); line(c, cx, cy, cx + math.cos(a) * 640, cy + math.sin(a) * 640, acc, 6)
        for (an, rad) in RP:
            age = ((sw - an) % 360) / 300; x, y = cx + math.cos(math.radians(an)) * rad, cy + math.sin(math.radians(an)) * rad
            if g - t < age: continue
            br = max(0, 1 - age * 1.1); circ(c, x, y, 20 + 60 * (1 - br), acc, br * .7, 5); circ(c, x, y, 20, WHT if br > 0 else acc, .35 + .65 * br)
        if t_pin and g >= t_pin:
            p = pr(g, t_pin, .4); dy = -600 * (1 - ob(p, 1.1)) if p < 1 else 0
            circ(c, cx, cy, 80 * p, YEL, .3 * p, blur=18)
            pth = skia.Path(); pth.moveTo(cx, cy + dy); pth.cubicTo(cx - 120, cy - 130 + dy, cx - 95, cy - 280 + dy, cx, cy - 280 + dy); pth.cubicTo(cx + 95, cy - 280 + dy, cx + 120, cy - 130 + dy, cx, cy + dy)
            c.drawPath(pth, P(YEL)); circ(c, cx, cy - 185 + dy, 36, NAVY)
        else: circ(c, cx, cy, 26, WHT)
    return _v(d, [t_pin] if t_pin else [])


def v_search(t, query, t_type, type_dur=1.5, t_results=None, top='Il risultato giusto', badge='TU'):
    """Barra di ricerca in cui si digita `query` (da t_type per type_dur secondi), poi salgono 3 risultati col primo evidenziato. Usa al massimo 2 righe di titolo."""
    def d(c, g, acc):
        p = ob(pr(g, t, .3), 1.2)
        c.save(); c.translate(540, 835); c.scale(p, p); c.translate(-540, -835)
        c.drawRoundRect(skia.Rect.MakeXYWH(78, 774, 940, 150), 75, 75, P(acc, .6, blur=26)); rr(c, 70, 760, 940, 150, 75, WHT)
        circ(c, 160, 830, 28, acc, 1, 10); line(c, 181, 851, 204, 874, acc, 12)
        n = int(len(query) * pr(g, t_type, type_dur)); f = font('m', 64)
        if f.measureText(query) > 700: f = font('m', 64 * 700 / f.measureText(query))
        c.drawString(query[:n], 240, 853, f, P(NAVY))
        if int(g * 5) % 2 == 0 or n < len(query): rr(c, 246 + f.measureText(query[:n]), 797, 6, 70, 3, acc)
        c.restore()
        if t_results is None: return
        for i in range(3):
            t0 = t_results + i * .13
            if g < t0: continue
            q = oe(pr(g, t0, .3)); y = 990 + i * 215 + 140 * (1 - q); first = i == 0
            rr(c, 70, y, 940, 185, 36, 0x16204A, q)
            if first:
                pulse = .5 + .5 * math.sin(g * 14); rr(c, 70, y, 940, 185, 36, acc, q, 8); c.drawRoundRect(skia.Rect.MakeXYWH(70, y, 940, 185), 36, 36, P(acc, .35 * pulse * q, 22, 14))
                circ(c, 165, y + 92, 58, acc, q); text(c, badge, 165, y + 92, 52, WHT, 'bk', a=q, shadow=False, maxw=96)
                text(c, top, 250, y + 66, 54, WHT, 'b', a=q, align=0, shadow=False, maxw=720)
                for k in range(5): circ(c, 268 + k * 46, y + 130, 15, YEL, q)
            else:
                circ(c, 165, y + 92, 58, 0x2A3566, q); person(c, 165, y + 97, 50, GREY, q)
                rr(c, 250, y + 46, 520 - i * 80, 30, 15, GREY, .6 * q); rr(c, 250, y + 108, 340, 24, 12, GREY, .35 * q)
    return _v(d, [t_results] if t_results else [])


def v_basin(t, dur=1.7, label='TU', inside=BLUE):
    """Un piccolo cerchio tratteggiato (il tuo giro) e fuori decine di puntini che si accendono uno dopo l'altro da t (mercato fuori dalla cerchia, nuovi contatti)."""
    random.seed(42); OD = []
    while len(OD) < 54:
        x, y = random.uniform(50, 1030), random.uniform(880, 1840)
        if (x - 290) ** 2 + (y - 1360) ** 2 > 260 ** 2: OD.append((x, y))
    OD.sort(key=lambda p: (p[0] - 290) ** 2 + (p[1] - 1360) ** 2); cx, cy = 290, 1360
    def d(c, g, acc):
        pp = P(inside, 1, 8); pp.setPathEffect(skia.DashPathEffect.Make([26, 18], g * 60)); c.drawCircle(cx, cy, 200, pp); circ(c, cx, cy, 200, inside, .12)
        for i in range(6): circ(c, cx + math.cos(i * 1.05) * 110, cy + math.sin(i * 1.05) * 110, 20, inside, .9)
        n = int(len(OD) * pr(g, t, dur))
        for i, (x, y) in enumerate(OD):
            if i < n:
                q = ob(pr(g, t + dur * i / len(OD), .22)); line(c, cx, cy, x, y, acc, 3, .22); circ(c, x, y, 38 * q, acc, .3, blur=12); circ(c, x, y, 22 * q, acc)
            else: circ(c, x, y, 14, GREY, .4)
        circ(c, cx, cy, 52, WHT); text(c, label, cx, cy, 44, NAVY, 'bk', shadow=False, maxw=90)
    return _v(d)


def v_people(t, dur=1.6, total=24, prefix='+'):
    """Contatore che sale da 0 a `total` mentre compaiono le icone delle persone (clienti, iscritti, lead)."""
    cols = 8; rows = (total + cols - 1) // cols
    def d(c, g, acc):
        n = int(total * oc(pr(g, t, dur))); b = 1 + .1 * (1 - ((g * 12) % 1)) if 0 < n < total else 1
        if g >= t - .05: text(c, f'{prefix}{n}', 540, 1030, 290, acc, 'bk', sc=b, glow=acc, a=pr(g, t - .05, .1))
        for i in range(n):
            t0 = t + dur * (1 - (1 - (i + 1) / total) ** (1 / 3)); q = ob(pr(g, t0 - .05, .2))
            person(c, 150 + (i % cols) * 111, 1340 + (i // cols) * min(160, 480 / rows), 92 * q, [acc, WHT, YEL][i % 3])
    return _v(d)


def v_sliders(t, label='RISULTATO', prefix='+'):
    """Finestra di un'app con 3 cursori che si muovono e un numero che cambia (simulatore, calcolatore, tool, dashboard). Max 2 righe di titolo."""
    def d(c, g, acc):
        q = oe(pr(g, t, .35)); c.save(); c.translate(0, 900 * (1 - q))
        c.drawRoundRect(skia.Rect.MakeXYWH(80, 760, 920, 920), 48, 48, P(acc, .45, blur=30)); rr(c, 80, 760, 920, 920, 48, 0x121A3F); rr(c, 80, 760, 920, 920, 48, acc, .8, 5)
        for i, col in enumerate([RED, YEL, GRN]): circ(c, 140 + i * 46, 820, 14, col)
        ks = []
        for i in range(3):
            y = 970 + i * 170; k = .5 + .38 * math.sin(g * 4.2 + i * 2.1); ks.append(k)
            rr(c, 140, y - 62, 240 - i * 30, 26, 13, GREY, .7); rr(c, 140, y - 9, 800, 18, 9, 0x2A3566); rr(c, 140, y - 9, 800 * k, 18, 9, acc)
            circ(c, 140 + 800 * k, y, 44, acc, .4, blur=10); circ(c, 140 + 800 * k, y, 30, WHT)
        rr(c, 140, 1450, 800, 180, 30, 0x0A1030); text(c, label, 180, 1540, 46, GREY, 'b', align=0, shadow=False, maxw=440)
        # Clienti10X 8/10/2026: prefix=None -> niente cifra illustrativa (a schermo solo numeri DETTI)
        val = '?' if prefix is None else f'{prefix}{int(8 + 40 * sum(ks) / 3)}'
        text(c, val, 900, 1540, 120 * (1 + .06 * math.sin(g * 6)) if prefix is None else 120, GRN, 'bk', align=1, shadow=False); c.restore()
    return _v(d)


def v_bars(t, t_line=None, n=6, down=False):
    """Istogramma che cresce barra dopo barra da t (ultima barra verde); t_line: freccia di tendenza che lo attraversa. down=True: barre che calano (rosso)."""
    hs = [150 + (830 - 150) * (i / (n - 1)) ** 1.5 for i in range(n)]
    if down: hs = hs[::-1]
    yb = 1740; step = 850 / n; bw = step * .73
    def d(c, g, acc):
        line(c, 100, yb + 12, 990, yb + 12, WHT, 6, .4); pts = []
        for i, hgt in enumerate(hs):
            t0 = t + i * .1; q = ob(pr(g, t0, .4), 1.2) if g >= t0 else 0; x = 125 + i * step
            col = (RED if down else GRN) if i == n - 1 else BLUE
            c.drawRoundRect(skia.Rect.MakeLTRB(x, yb - hgt * q, x + bw, yb), 20, 20, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, yb - hgt), (0, yb)], [C(col), C(col, .35)])))
            pts.append((x + bw / 2, yb - hgt - 70))
        if t_line and g > t_line:
            p = oc(pr(g, t_line, .6)); path = skia.Path(); path.moveTo(*pts[0])
            for pt in pts[1:]: path.lineTo(*pt)
            pp = P(YEL, 1, 14); pp.setPathEffect(skia.TrimPathEffect.Make(0, min(.999, max(.001, p)))); c.drawPath(path, pp)
            m = skia.PathMeasure(path, False); pos, tan = m.getPosTan(m.getLength() * p); tri(c, pos.x(), pos.y(), math.degrees(math.atan2(tan.y(), tan.x())), 44, YEL)
    return _v(d)


def v_list(items):
    """Elenco puntato animato: ogni riga entra di lato col suo segno. items=[(tempo, 'Testo breve', True/False), ...] (max 5; True = spunta verde, False = croce rossa)."""
    def d(c, g, acc):
        for i, (ti, txt, ok) in enumerate(items[:5]):
            if g < ti: continue
            q = oe(pr(g, ti, .3)); y = 860 + i * 185; x = 70 + 500 * (1 - q); col = GRN if ok else RED
            rr(c, x, y, 940, 150, 40, 0x16204A, q); rr(c, x, y, 940, 150, 40, col, .8 * q, 5)
            b = ob(pr(g, ti + .1, .25)) if g > ti + .1 else 0
            circ(c, x + 95, y + 75, 50 * b, col); check(c, x + 95, y + 75, 46 * b, NAVY, ok)
            text(c, txt, x + 180, y + 75, 60, WHT, 'b', a=q, align=0, shadow=False, maxw=720)
    return _v(d, [i[0] for i in items])


def v_versus(t, left, right, t_win=None):
    """Confronto a due colonne: `left` (rosso, perdente) contro `right` (verde, vincente). left/right = ('ETICHETTA', altezza_barra 0..1). t_win: la destra si illumina."""
    yb = 1580
    def d(c, g, acc):
        for i, ((lab, val), col) in enumerate(((left, RED), (right, GRN))):
            t0 = t + i * .18; q = ob(pr(g, t0, .4), 1.2) if g >= t0 else 0; x = 110 + i * 520; hgt = 120 + 600 * val
            if i == 1 and t_win and g >= t_win: c.drawRoundRect(skia.Rect.MakeLTRB(x - 10, yb - hgt, x + 350, yb + 10), 30, 30, P(col, .5, blur=30))
            c.drawRoundRect(skia.Rect.MakeLTRB(x, yb - hgt * q, x + 340, yb), 30, 30, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, yb - hgt), (0, yb)], [C(col), C(col, .4)])))
            text(c, lab, x + 170, yb + 80, 58, WHT, 'bk', a=cl(q), maxw=360)
        pop(c, g, t + .3, 'VS', 540, yb - 90, 84, WHT, 'bi')
    return _v(d, [t_win] if t_win else [])


def v_comment(keyword, t_type, t_send, note_line=None):
    """Chiusura con invito al commento: nel campo commento si digita `keyword`, a t_send parte l'aeroplanino. note_line=(tempo, 'TE LO MANDO IN PRIVATO'). Frecce verso il basso."""
    def d(c, g, acc):
        c.drawRoundRect(skia.Rect.MakeXYWH(66, 754, 960, 180), 90, 90, P(acc, .6, blur=26)); rr(c, 60, 740, 960, 180, 90, WHT)
        circ(c, 150, 830, 56, 0xD5DBF0); person(c, 150, 835, 50, GREY)
        n = int(len(keyword) * pr(g, t_type, .5) + .001); f = font('bk', 80)
        if f.measureText(keyword) > 600: f = font('bk', 80 * 600 / f.measureText(keyword))
        c.drawString(keyword[:n], 235, 859, f, P(NAVY))
        if n < len(keyword): rr(c, 240 + f.measureText(keyword[:n]), 788, 7, 84, 3, acc)
        b = 1 + .25 * (1 - pr(g, t_send, .25)) if g >= t_send else 1
        circ(c, 930, 830, 62 * b, acc); fl = pr(g, t_send + .05, .7); e = oc(fl) if fl > 0 else 0
        px, py = lerp(930, 1250, e), lerp(830, 340, e)
        if fl > 0: line(c, 930, 830, px, py, WHT, 10, .5 * (1 - fl))
        pl = skia.Path(); pl.moveTo(34, 0); pl.lineTo(-26, -26); pl.lineTo(-12, 0); pl.lineTo(-26, 26); pl.close()
        c.save(); c.translate(px, py); c.rotate(-55 if fl > 0 else 0); c.scale(1 + fl, 1 + fl); c.drawPath(pl, P(WHT)); c.restore()
        if note_line: slam(c, g, note_line[0], note_line[1], 540, 1120, 98, GRN, 'bi', glow=GRN, maxw=1000)
        for k in range(3):
            y = 1360 + k * 150 + 34 * math.sin(g * 11 - k * .7); pth = skia.Path(); pth.moveTo(450, y - 40); pth.lineTo(540, y + 40); pth.lineTo(630, y - 40)
            c.drawPath(pth, P(YEL, .4 + .3 * k, 34))
    return _v(d, [t_send])


# ------------------------------------------------------------------ PANNELLI (scheda 940x490 sopra la testa, coordinate locali)
def p_people(t, title, n=30):
    """Griglia di omini che compare a onda + titolo. title=(tempo, 'TESTO')."""
    def d(c, g):
        slam(c, g, title[0], title[1], 470, 85, 80, YEL, 'bi', maxw=860)
        for i in range(n):
            t0 = t + (i % 10) * .04 + (i // 10) * .1; q = ob(pr(g, t0, .2)) if g >= t0 else 0
            person(c, 92 + (i % 10) * 84, 215 + (i // 10) * 100, 56 * q, [0x8FA0D8, 0x6B7391, 0xAEB6D6][i % 3])
    return d

def p_pulse(t, title, color=GRN):
    """Cerchi che si espandono + puntini + titolo grande al centro (novità, espansione, apertura). title=(tempo, 'TESTO')."""
    def d(c, g):
        for k in range(4):
            q = ((g - t) * .9 + k / 4) % 1; circ(c, 470, 300, 40 + 420 * q, color, (1 - q) * .8, 8)
        for i in range(14):
            t0 = t + .25 + i * .05; q = ob(pr(g, t0, .2)) if g >= t0 else 0; a = i * 2.4; rad = 90 + i * 22
            circ(c, 470 + math.cos(a) * rad * 1.4, 300 + math.sin(a) * rad * .5, 16 * q, color)
        slam(c, g, title[0], title[1], 470, 245, 112, WHT, 'bk', glow=color, maxw=880)
    return d

def p_strike(t, title, t_strike):
    """Parola che viene sbarrata in rosso (cosa da abbandonare) con fumetti sotto. title=(tempo, 'TESTO')."""
    def d(c, g):
        for i in range(3):
            t0 = t + i * .1; q = ob(pr(g, t0, .22)) if g >= t0 else 0; x = 200 + i * 270; col = [BLUE, WHT, BLUE][i]
            c.save(); c.translate(x, 345); c.scale(q, q); rr(c, -95, -62, 190, 110, 40, col); tri(c, -40, 62, 90, 26, col)
            for k in range(3): circ(c, -42 + k * 42, -8, 11, NAVY)
            c.restore()
            if i < 2 and g > t0 + .1: tri(c, x + 135, 340, 0, 24, GREY, q)
        slam(c, g, title[0], title[1], 470, 120, 110, WHT, 'bk', maxw=880)
        if g >= t_strike: line(c, 40, 132, 40 + 860 * oe(pr(g, t_strike, .2)), 108, RED, 22)
    return d

def p_text(lines, color=YEL):
    """Solo testo: lines=[(tempo, 'RIGA GRANDE'), (tempo, 'riga sotto')] (max 3 righe)."""
    def d(c, g):
        n = len(lines)
        for i, (tl, txt) in enumerate(lines[:3]):
            y = 245 + (i - (n - 1) / 2) * 135
            slam(c, g, tl, txt, 470, y, 104 if i == 0 else 84, color if i == 0 else WHT, 'bi' if i == 0 else 'bk', maxw=860)
    return d

def p_stat(t, value, label, color=GRN):
    """Numero grande + etichetta. value='+37%'  label='TASSO DI CHIUSURA'."""
    def d(c, g):
        slam(c, g, t, value, 470, 200, 210, color, 'bk', glow=color, maxw=860); pop(c, g, t + .25, label, 470, 385, 64, WHT, 'bk', maxw=860)
    return d


# ------------------------------------------------------------------ TIMELINE
ZOOM = dict(wide=1.0, mid=1.22, tight=1.42)

def head(a, b, zoom='wide', panel=None, title=None):
    """Inquadratura sul parlato da a a b. zoom: 'wide' | 'mid' | 'tight' (o numero). panel: pannello sopra la testa (solo con 'wide').
    title: righe di titolo cinetico sovrapposte al busto al posto dei sottotitoli (es. per l'hook)."""
    return dict(a=a, b=b, kind='head', zoom=ZOOM.get(zoom, zoom), panel=panel, title=title)

def mg(a, b, sc):
    """B-roll in motion graphics a tutto schermo da a a b. sc = scene(...) oppure una funzione f(c, g) che disegna l'intero fotogramma."""
    return dict(a=a, b=b, kind='mg', fn=sc)
