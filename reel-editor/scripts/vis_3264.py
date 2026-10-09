"""Visual NUOVI scritti per il reel 3264 "fare marketing costa troppo" (8/10/2026).
Regola 410: ogni video le sue grafiche; nessuna ripete vis_3263, 3265, 3266, 3267.
I numeri a schermo sono SOLO quelli detti da Francesco (li passa la regia).
Zona utile y 800-1800, centro 540,1200. Tempi assoluti sulla timeline di base.mp4."""
import math, random, skia
from mgkit import *
from mgkit import _v


def v_cartellino(t, testo='€', t_q=None, poi=None):
    """'Fare marketing costa troppo' / 'il costo fosse di mille euro': un cartellino del
    prezzo appeso che dondola, con la cifra o il simbolo; t_q fa comparire il punto di domanda."""
    def d(c, g, acc):
        p = ob(pr(g, t, .4)) if g >= t else 0; sw = 9 * math.sin((g - t) * 3.2) * math.exp(-(g - t) * .5)
        c.save(); c.translate(540, 820); c.rotate(sw); c.scale(p, p)
        line(c, 0, 0, 0, 150, WHT, 6)
        pth = skia.Path(); pth.moveTo(0, 130); pth.lineTo(260, 300); pth.lineTo(260, 760); pth.lineTo(-260, 760); pth.lineTo(-260, 300); pth.close()
        c.drawPath(pth, P(acc, .4, blur=30)); c.drawPath(pth, P(0xF4F1E8)); circ(c, 0, 240, 34, NAVY)
        tx = poi[1] if (poi and g >= poi[0]) else testo           # poi=(t, 'MILLE'): la cifra entra quando e' detta
        text(c, tx, 0, 520, 230, NAVY, 'bk', shadow=False, maxw=440, sc=lerp(1.5, 1, oe(pr(g, poi[0], .2))) if (poi and g >= poi[0]) else 1)
        c.restore()
        if t_q and g >= t_q: pop(c, g, t_q, '?', 880, 1000, 320, RED, 'bk', glow=RED, rot=14)
    return _v(d, ([t_q] if t_q else []) + ([poi[0]] if poi else []))


def v_portafoglio(steps, unita='EURO'):
    """'Ti lascia di commissione 500, 600 euro': un portafoglio che si apre e la cifra che
    sbatte sopra a ogni numero detto. steps=[(t, '500'), (t, '600')]."""
    def d(c, g, acc):
        t0 = steps[0][0] - .5; p = ob(pr(g, t0, .35)) if g >= t0 else 0; cx, cy = 540, 1500
        c.save(); c.translate(cx, cy); c.scale(p, p)
        n = sum(1 for s in steps if g >= s[0])
        for i in range(n + 1):                                          # banconote che spuntano
            q = oe(pr(g, (steps[i - 1][0] if i else t0), .3)); rr(c, -230 + i * 40, -150 - 150 * q - i * 26, 380, 200, 20, 0x2BF29B if i else 0x1EBD7C)
        rr(c, -330, -110, 660, 380, 50, 0x6B4A2B); rr(c, -330, -110, 660, 380, 50, 0x3F2A16, 1, 10)
        rr(c, 150, 20, 220, 120, 40, 0x8A6238); circ(c, 210, 80, 26, GOLD)
        c.restore()
        cur = None
        for s in steps:
            if g >= s[0]: cur = s
        if cur:
            slam(c, g, cur[0], cur[1], 540, 960, 300, acc, 'bk', glow=acc, d=.16, maxw=900)
    return _v(d, [s[0] for s in steps])


def v_torre(steps):
    """'Un gestito medio di 100, 150 mila euro': una torre di blocchi che sale a ogni cifra,
    con la cifra in cima. steps=[(t, '100', 4), (t, '150', 6)] (terzo = blocchi)."""
    def d(c, g, acc):
        n = 0; cur = None
        for s in steps:
            if g >= s[0]: n, cur = s[2], s
        for i in range(n):
            ts = max(s[0] for s in steps if s[2] > i and g >= s[0]) if cur else 0
            q = oe(pr(g, ts + (i % 3) * .04, .22)); y = 1760 - i * 105
            c.drawRoundRect(skia.Rect.MakeXYWH(340, lerp(y - 400, y, q), 400, 92, ), 16, 16,
                            skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(340, y), (740, y + 92)], [C(acc, q), C(0x8A6300, q)])))
        if cur:
            ytop = 1760 - n * 105 - 110
            slam(c, g, cur[0], cur[1], 540, max(930, ytop), 260, WHT, 'bk', glow=acc, d=.16)
    return _v(d, [s[0] for s in steps])


def v_dieci_anni(t, dur, steps):
    """'Nei prossimi dieci anni ti ha messo in tasca 5, 6 mila euro': una linea del tempo con
    dieci tacche che si accendono, le monete che si impilano sopra e la cifra che scatta."""
    def d(c, g, acc):
        k = pr(g, t, dur); n = int(k * 10 + .001)
        line(c, 90, 1600, 990, 1600, 0x5F6B8A, 8); line(c, 90, 1600, lerp(90, 990, k), 1600, acc, 8)
        for i in range(10):
            x = 135 + i * 90; on = i < n
            circ(c, x, 1600, 22, acc if on else 0x2A3566); text(c, str(i + 1), x, 1670, 40, WHT if on else GREY, 'b', shadow=False)
            if on:
                for j in range(1 + i // 2):
                    circ(c, x, 1540 - j * 34, 30, GOLD); circ(c, x, 1540 - j * 34, 22, 0xB8860B, .9, 4)
        cur = None
        for s in steps:
            if g >= s[0]: cur = s
        if cur: slam(c, g, cur[0], cur[1], 540, 1050, 300, acc, 'bk', glow=acc, d=.16)
    return _v(d, [s[0] for s in steps])


def v_secchio(t, steps):
    """'Stai perdendo potenzialmente 4, 5 mila euro': un secchio bucato da cui le monete
    scappano di sotto, e la cifra persa che scatta in rosso."""
    random.seed(6); CO = [(random.uniform(-90, 90), random.uniform(0, 1), random.uniform(.9, 1.5)) for _ in range(12)]
    def d(c, g, acc):
        p = ob(pr(g, t, .35)) if g >= t else 0; cx = 300
        c.save(); c.translate(cx, 1250); c.scale(p, p)
        pth = skia.Path(); pth.moveTo(-200, -160); pth.lineTo(200, -160); pth.lineTo(150, 200); pth.lineTo(-150, 200); pth.close()
        c.drawPath(pth, P(0x8A93B8)); c.drawPath(pth, P(WHT, .5, 8)); arc(c, 0, -160, 190, 180, 180, WHT, 10, .7)
        circ(c, 60, 200, 40, 0x0A0F24)
        c.restore()
        if g >= t + .3:
            for (dx, ph, sp) in CO:
                k = ((g - t) * sp + ph) % 1; x = cx + 60 + dx * k * 1.6; y = 1450 + 330 * k * k
                circ(c, x, y, 28, GOLD, 1 - k * .7); text(c, '€', x, y, 30, 0x7A5A00, 'bk', a=1 - k * .7, shadow=False)
        cur = None
        for s in steps:
            if g >= s[0]: cur = s
        if cur: slam(c, g, cur[0], cur[1], 760, 1180, 330, RED, 'bk', glow=RED, d=.16, maxw=520)
    return _v(d, [s[0] for s in steps])


def v_giorni(t, n=7):
    """'Un piccolo budget giornaliero': una settimana di caselle, in ognuna cade una moneta
    piccola, un giorno dopo l'altro."""
    G = ['L', 'M', 'M', 'G', 'V', 'S', 'D']
    def d(c, g, acc):
        for i in range(n):
            x = 110 + i * 143; t0 = t + i * .18; q = ob(pr(g, t0, .22)) if g >= t0 else 0
            rr(c, x - 62, 1180, 124, 300, 24, 0x16204A, q); rr(c, x - 62, 1180, 124, 300, 24, acc, .6 * q, 4)
            text(c, G[i], x, 1240, 50, WHT, 'bk', a=q, shadow=False)
            tc = t0 + .25
            if g >= tc:
                k = oe(pr(g, tc, .3)); y = lerp(900, 1390, k)
                circ(c, x, y, 40, GOLD); circ(c, x, y, 30, 0xB8860B, .9, 4); text(c, '€', x, y, 40, 0x7A5A00, 'bk', shadow=False)
    return _v(d)


def v_rewind(t):
    """'Tutto rimarra' come prima': il simbolo del riavvolgi che lampeggia sopra un
    calendario che torna sempre allo stesso giorno."""
    def d(c, g, acc):
        p = ob(pr(g, t, .35)) if g >= t else 0; cx, cy = 540, 1280
        a = (g - t) * -260; c.save(); c.translate(cx, cy); c.scale(p, p)
        arc(c, 0, 0, 300, a, 290, acc, 30); tri(c, math.cos(math.radians(a)) * 300, math.sin(math.radians(a)) * 300, a - 90, 60, acc)
        b = .6 + .4 * abs(math.sin(g * 6))
        tri(c, -30, 0, 180, 90, WHT, b); tri(c, 110, 0, 180, 90, WHT, b)
        c.restore()
    return _v(d)


def v_candela(t, dur=2.4):
    """'Dal passaparola, fin quando funzionera'': una candela che si consuma, la fiamma che
    tremola e si abbassa."""
    def d(c, g, acc):
        p = oe(pr(g, t, .3)); k = pr(g, t + .2, dur); h = lerp(520, 150, k); cx = 540; base = 1700
        rr(c, cx - 190, base, 380, 50, 25, 0x8A93B8, p)
        rr(c, cx - 90, base - h * p, 180, h * p, 26, 0xF4F1E8); rr(c, cx - 90, base - h * p, 60, h * p, 26, 0xD9D4C4, .8)
        fy = base - h * p - 30; s = (1 - .55 * k) * (1 + .12 * math.sin(g * 21))
        line(c, cx, base - h * p, cx, fy + 10, NAVY, 8)
        fl = skia.Path(); fl.moveTo(cx, fy - 190 * s); fl.quadTo(cx + 90 * s, fy - 60 * s, cx, fy); fl.quadTo(cx - 90 * s, fy - 60 * s, cx, fy - 190 * s)
        c.drawPath(fl, P(0xFF9F43, .5 * p, blur=30)); c.drawPath(fl, P(0xFF9F43, p)); circ(c, cx, fy - 50 * s, 30 * s, YEL, p)
        for i in range(3): circ(c, cx - 110 - i * 14, base - 60 - i * 70 * k, 16 * k, 0xF4F1E8)        # gocce di cera
    return _v(d)


def v_cruscotto(t, t_lock):
    """'Sai esattamente quanto ti serve investire': un cruscotto con la lancetta che oscilla
    e poi si ferma netta sul punto; la spia diventa verde."""
    def d(c, g, acc):
        p = ob(pr(g, t, .35)) if g >= t else 0; cx, cy = 540, 1420; lock = g >= t_lock
        c.save(); c.translate(cx, cy); c.scale(p, p)
        arc(c, 0, 0, 360, 180, 180, 0x2A3566, 60)
        for i in range(13):
            a = math.radians(180 + i * 15); line(c, math.cos(a) * 300, math.sin(a) * 300, math.cos(a) * 250, math.sin(a) * 250, WHT, 8, .7)
        ang = 250 if lock else 270 + 70 * math.sin((g - t) * 7)
        if lock: ang = lerp(270 + 70 * math.sin((t_lock - t) * 7), 250, oe(pr(g, t_lock, .2)))
        arc(c, 0, 0, 360, 180, ang - 180, GRN if lock else acc, 60)
        a = math.radians(ang); line(c, 0, 0, math.cos(a) * 280, math.sin(a) * 280, WHT, 18); circ(c, 0, 0, 44, WHT)
        circ(c, 0, 190, 46, GRN if lock else 0x5F6B8A);
        if lock: check(c, 0, 190, 44 * ob(pr(g, t_lock, .25)), NAVY)
        c.restore()
    return _v(d, [t_lock])


def v_albero(t, dur=2.0, n=9):
    """'Quanto ti porta in tutto il suo ciclo di vita': un albero che cresce dal seme, e sui
    rami maturano le monete una dopo l'altra."""
    random.seed(12); FR = [(random.uniform(-250, 250), random.uniform(-520, -260)) for _ in range(n)]
    def d(c, g, acc):
        k = oe(pr(g, t, dur * .5)); cx, base = 540, 1740
        rr(c, cx - 26, base - 430 * k, 52, 430 * k, 20, 0x8A6238)
        for (a, l) in [(-40, 200), (35, 220), (-20, 150)]:
            ar = math.radians(a - 90); y0 = base - 300 * k
            if k > .6: line(c, cx, y0, cx + math.cos(ar) * l * (k - .6) * 2.5, y0 + math.sin(ar) * l * (k - .6) * 2.5, 0x8A6238, 22)
        q = oe(pr(g, t + dur * .35, .5)); circ(c, cx, base - 520, 300 * q, GRN, .9); circ(c, cx - 150, base - 420, 190 * q, 0x17C97A, .9); circ(c, cx + 160, base - 430, 200 * q, 0x17C97A, .9)
        for i, (dx, dy) in enumerate(FR):
            t0 = t + dur * .5 + i * (dur * .5 / n)
            if g < t0: continue
            s = ob(pr(g, t0, .22)); x, y = cx + dx, base + dy
            circ(c, x, y, 42 * s, GOLD); circ(c, x, y, 30 * s, 0xB8860B, .9, 4); text(c, '€', x, y, 42, 0x7A5A00, 'bk', sc=s, shadow=False)
        rr(c, cx - 300, base, 600, 26, 13, 0x5F6B8A)
    return _v(d)


def v_folla(t, rows=4, cols=7):
    """'Quanti clienti puoi riuscire a ottenere': una folla che si riempie a onda, riga per
    riga, senza cifre a schermo."""
    def d(c, g, acc):
        for r in range(rows):
            for col in range(cols):
                i = r * cols + col; t0 = t + i * .045
                if g < t0: continue
                q = ob(pr(g, t0, .22)); x = 120 + col * 140; y = 1040 + r * 200 + 12 * math.sin(g * 4 + col * .8)
                person(c, x, y, 110 * q, [GRN, YEL, WHT][(r + col) % 3])
    return _v(d)
