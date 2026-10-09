"""Visual NUOVI scritti per il reel 3262 "i pesci piccoli" (8/10/2026).
Regola 410: nessuno ripete il riferimento di Francesco (pesci, linea, ciambella, banconote,
rete, contatore, orologio, mirino, loop, orbita, freccia, ingranaggi, radar, ricerca, bacino)
ne' vis_3263, 3264, 3265, 3266, 3267. Numeri a schermo solo quelli detti.
Zona utile y 800-1800, centro 540,1200. Tempi assoluti sulla timeline di base.mp4."""
import math, random, skia
from mgkit import *
from mgkit import _v


def v_zavorra(t, t_pesi):
    """'I pesci piccoli stanno rallentando la tua crescita': una freccia che sale, e i
    pesetti che le si appendono uno alla volta finche' si piega e si ferma."""
    def d(c, g, acc):
        n = sum(1 for i in range(4) if g >= t_pesi + i * .28); k = oe(pr(g, t, .5))
        tip_y = lerp(1700, 950, k) + n * 70; tip_x = 800
        pth = skia.Path(); pth.moveTo(160, 1720); pth.quadTo(520, 1600 + n * 20, tip_x, tip_y)
        c.drawPath(pth, P(GRN if n < 3 else RED, 1, 26)); tri(c, tip_x, tip_y, -40 + n * 14, 60, GRN if n < 3 else RED)
        for i in range(n):
            t0 = t_pesi + i * .28; q = oe(pr(g, t0, .2)); x = 330 + i * 130; y0 = 1640 - i * 60 + n * 14
            line(c, x, y0, x, y0 + 120 * q, WHT, 6)
            pw = skia.Path(); pw.moveTo(x - 46, y0 + 120 * q); pw.lineTo(x + 46, y0 + 120 * q); pw.lineTo(x + 62, y0 + 210 * q); pw.lineTo(x - 62, y0 + 210 * q); pw.close()
            c.drawPath(pw, P(0x8A93B8))
    return _v(d, [t_pesi + i * .28 for i in range(4)])


def v_bicchiere(steps):
    """'Composto al 70, 80% da clienti piccoli': un bicchiere che si riempie fino al livello
    detto, con la tacca e la cifra a fianco. steps=[(t, 70), (t, 80)]."""
    def d(c, g, acc):
        lv = 0; cur = None
        for i, (t0, v) in enumerate(steps):
            if g >= t0:
                prev = steps[i - 1][1] if i else 0; lv = lerp(prev, v, oe(pr(g, t0, .35))); cur = (t0, v)
        if not cur: lv = 55 * pr(g, steps[0][0] - .7, .7)
        x0, x1, yt, yb = 300, 660, 900, 1720
        pth = skia.Path(); pth.moveTo(x0 - 40, yt); pth.lineTo(x0, yb); pth.lineTo(x1, yb); pth.lineTo(x1 + 40, yt)
        yl = yb - (yb - yt) * lv / 100; wob = 8 * math.sin(g * 6)
        liq = skia.Path(); liq.moveTo(x0 - 40 * (yb - yl) / (yb - yt), yl + wob); liq.lineTo(x0, yb); liq.lineTo(x1, yb); liq.lineTo(x1 + 40 * (yb - yl) / (yb - yt), yl - wob); liq.close()
        c.drawPath(liq, P(acc, .85)); c.drawPath(pth, P(WHT, .9, 12))
        if cur:
            line(c, x1 + 60, yl, x1 + 150, yl, WHT, 6); slam(c, g, cur[0], f'{cur[1]}%', 880, yl, 150, acc, 'bk', glow=acc, d=.16, maxw=330)
    return _v(d, [s[0] for s in steps])


def v_spiccioli(steps):
    """'Una piccola provvigione da 50, 100 euro': un piatto grande e vuoto, e dentro cadono
    due spiccioli; la cifra piccola accanto a ogni moneta. steps=[(t, '50€'), (t, '100€')]."""
    def d(c, g, acc):
        p = oe(pr(g, steps[0][0] - .6, .4))
        c.drawOval(skia.Rect.MakeXYWH(120, 1380 + 300 * (1 - p), 840, 300), P(0x2A3566)); c.drawOval(skia.Rect.MakeXYWH(120, 1380 + 300 * (1 - p), 840, 300), P(WHT, .6, 8))
        c.drawOval(skia.Rect.MakeXYWH(230, 1430 + 300 * (1 - p), 620, 200), P(0x16204A))
        for i, (t0, lab) in enumerate(steps[:3]):
            if g < t0: continue
            q = pr(g, t0, .3); x = 420 + i * 230; y = lerp(850, 1520, oe(q)) - 40 * math.sin(q * math.pi) * (1 - q)
            circ(c, x, y, 62, GOLD); circ(c, x, y, 46, 0xB8860B, .9, 5); text(c, '€', x, y, 64, 0x7A5A00, 'bk', shadow=False)
            pop(c, g, t0 + .12, lab, x, 1180 - i * 130, 130, acc, 'bk', glow=acc)
    return _v(d, [s[0] for s in steps])


def v_corona(t):
    """'Ti aspetti che da questi arrivino referenze patrimonializzate': tre clienti piccoli in
    basso che indicano in alto una figura con la corona, lontana, con il punto di domanda."""
    def d(c, g, acc):
        for i in range(3):
            q = ob(pr(g, t + i * .1, .25)) if g >= t + i * .1 else 0; x = 250 + i * 290
            person(c, x, 1640, 130 * q, 0x8A93B8)
            pp = P(0x8A93B8, .6 * q, 5); pp.setPathEffect(skia.DashPathEffect.Make([16, 16], -g * 90)); c.drawLine(x, 1500, 540, 1220, pp)
        q = ob(pr(g, t + .45, .3)) if g >= t + .45 else 0; y = 1080 + 14 * math.sin(g * 3)
        circ(c, 540, y, 150 * q, acc, .25, blur=24); person(c, 540, y + 20, 190 * q, acc)
        cr = skia.Path(); cr.moveTo(450, y - 110); cr.lineTo(450, y - 190); cr.lineTo(495, y - 150); cr.lineTo(540, y - 205); cr.lineTo(585, y - 150); cr.lineTo(630, y - 190); cr.lineTo(630, y - 110); cr.close()
        c.save(); c.translate(540, y - 150); c.scale(q, q); c.translate(-540, -(y - 150)); c.drawPath(cr, P(YEL)); c.restore()
        if g >= t + .8: pop(c, g, t + .8, '?', 800, 1000, 260, WHT, 'bk', rot=12)
    return _v(d)


def v_termometro(steps):
    """'Un gestito da 100, 200, 500 mila euro': una colonna graduata che sale a scatti fino
    alla tacca della cifra detta. steps=[(t, '100', .25), (t, '200', .5), (t, '500', 1)]."""
    def d(c, g, acc):
        lv = 0; cur = None
        for i, (t0, lab, v) in enumerate(steps):
            if g >= t0: prev = steps[i - 1][2] if i else 0; lv = lerp(prev, v, oe(pr(g, t0, .25))); cur = (t0, lab)
        x, yb, yt = 300, 1720, 880
        rr(c, x - 60, yt - 40, 120, yb - yt + 80, 60, 0x16204A); rr(c, x - 60, yt - 40, 120, yb - yt + 80, 60, WHT, .7, 8)
        h = (yb - yt) * lv; rr(c, x - 38, yb - h, 76, h + 20, 38, acc)
        circ(c, x, yb + 60, 90, acc); circ(c, x, yb + 60, 90, WHT, .7, 8)
        for (t0, lab, v) in steps:
            y = yb - (yb - yt) * v; on = g >= t0
            line(c, x + 80, y, x + 150, y, WHT if on else GREY, 6); text(c, lab, x + 180, y, 70, WHT if on else GREY, 'bk', align=0, shadow=False)
        if cur: slam(c, g, cur[0], cur[1], 820, 1250, 280, acc, 'bk', glow=acc, d=.16, maxw=380)
    return _v(d, [s[0] for s in steps])


def v_pagine(t):
    """'Stai perdendo solo tempo': un calendario a blocco da cui le pagine si staccano e
    volano via una dopo l'altra."""
    def d(c, g, acc):
        p = ob(pr(g, t, .35)) if g >= t else 0; cx, cy = 540, 1320
        c.save(); c.translate(cx, cy); c.scale(p, p)
        rr(c, -250, -260, 500, 560, 36, 0xF4F1E8); rr(c, -250, -260, 500, 130, 36, RED)
        for i in range(2): circ(c, -120 + i * 240, -260, 26, 0x8A93B8)
        day = 1 + int((g - t) * 3.2); text(c, str(day % 31 or 31), 0, 90, 260, NAVY, 'bk', shadow=False)
        c.restore()
        for i in range(4):
            k = ((g - t) * .8 + i / 4) % 1
            if g < t + .2: continue
            x = cx + 150 + 520 * k; y = cy - 100 - 420 * k + 60 * math.sin(k * 9 + i)
            c.save(); c.translate(x, y); c.rotate(360 * k + i * 40); rr(c, -90, -110, 180, 220, 14, 0xF4F1E8, 1 - k); rr(c, -90, -110, 180, 50, 14, RED, 1 - k); c.restore()
    return _v(d)


def v_scala(t, t_no):
    """'Diventa molto complesso andare a prendere i clienti piu' patrimonializzati': una scala
    con i pioli in alto mancanti, il cliente d'oro in cima che non si raggiunge."""
    def d(c, g, acc):
        p = oe(pr(g, t, .4)); x0, x1, yb, yt = 380, 700, 1760, 980
        line(c, x0, yb, x0, lerp(yb, yt, p), 0x8A6238, 22); line(c, x1, yb, x1, lerp(yb, yt, p), 0x8A6238, 22)
        for i in range(8):
            y = yb - 60 - i * 92; miss = i >= 5
            if y < lerp(yb, yt, p): continue
            if miss:
                a = cl(1 - (g - t_no - (i - 5) * .12) * 3) if g >= t_no else 1
                line(c, x0, y, x1, y + (1 - a) * 200, 0x8A6238, 18, a)
            else: line(c, x0, y, x1, y, 0x8A6238, 18)
        q = ob(pr(g, t + .4, .3)) if g >= t + .4 else 0
        circ(c, 540, 900, 110 * q, GOLD, .3, blur=24); person(c, 540, 910, 150 * q, GOLD)
        person(c, 540, 1500 - 130 * oe(pr(g, t + .5, .8)), 120, WHT)
    return _v(d, [t_no])


def v_criceto(pills):
    """'Continui in un circolo vizioso': una ruota da criceto che gira con una persona che
    corre dentro e resta ferma; le etichette entrano quando vengono dette. pills=[(t, 'TESTO')]."""
    def d(c, g, acc):
        cx, cy, R = 540, 1330, 330; rot = g * 150
        circ(c, cx, cy, R, WHT, .9, 18)
        for k in range(12):
            a = math.radians(rot + k * 30); line(c, cx + math.cos(a) * (R - 40), cy + math.sin(a) * (R - 40), cx + math.cos(a) * R, cy + math.sin(a) * R, WHT, 10, .8)
        line(c, cx, cy, cx - 200, 1760, 0x8A93B8, 18); line(c, cx, cy, cx + 200, 1760, 0x8A93B8, 18); circ(c, cx, cy, 26, WHT)
        b = 12 * math.sin(g * 18)
        person(c, cx, cy + 150 + b * .3, 150, acc)
        line(c, cx - 30, cy + 250, cx - 30 - b * 3, cy + 300, acc, 16); line(c, cx + 30, cy + 250, cx + 30 + b * 3, cy + 300, acc, 16)
        pos = [(300, 900), (790, 1000), (540, 1740)]; cols = [WHT, YEL, RED]
        for i, (tp, txt) in enumerate(pills[:3]): pill(c, g, tp, txt, pos[i][0], pos[i][1], cols[i])
    return _v(d, [p[0] for p in pills])


def v_porta(t, t_open):
    """'L'unico modo per uscirne': una porta chiusa nel buio che si apre e lascia uscire la
    luce, con la persona che la attraversa."""
    def d(c, g, acc):
        p = oe(pr(g, t, .35)); o = oe(pr(g, t_open, .5)) if g >= t_open else 0; x, y, w, h = 360, 900, 360, 800
        if o:
            ray = skia.Path(); ray.moveTo(x, y); ray.lineTo(x + w, y); ray.lineTo(x + w + 260 * o, 1800); ray.lineTo(x - 260 * o, 1800); ray.close()
            c.drawPath(ray, P(acc, .28 * o, blur=20)); rr(c, x, y, w, h, 8, acc, .9 * o)
        rr(c, x - 24, y - 24, w + 48, h + 24, 12, 0x5F6B8A, p, 24)
        c.save(); c.translate(x, 0); c.scale(max(.06, 1 - o * .9), 1); rr(c, 0, y, w, h, 8, 0x3B2A1A, p); rr(c, 30, y + 40, w - 60, h * .4, 8, 0x5A4028, p); circ(c, w - 50, y + h / 2, 22, GOLD, p); c.restore()
        if o > .4: person(c, x + w / 2, lerp(1640, 1500, o), 140 * o, NAVY)
    return _v(d, [t_open])


def v_calamita(t):
    """'Intercettare le persone nella tua area': una calamita che entra e attira verso di se'
    le persone sparse, che le volano incontro."""
    random.seed(21); PP = [(random.uniform(120, 960), random.uniform(1250, 1780)) for _ in range(12)]
    def d(c, g, acc):
        p = ob(pr(g, t, .35)) if g >= t else 0; cx, cy = 540, 980
        for i, (x, y) in enumerate(PP):
            k = oe(pr(g, t + .4 + i * .08, .7)) if g >= t + .4 + i * .08 else 0
            xx, yy = lerp(x, cx + (i % 5 - 2) * 70, k), lerp(y, cy + 250 + (i // 5) * 80, k)
            person(c, xx, yy, 86, YEL if k > .5 else 0x8A93B8)
        c.save(); c.translate(cx, cy); c.scale(p, p); c.rotate(4 * math.sin(g * 8))
        arc(c, 0, 0, 150, 180, 180, RED, 90); rr(c, -195, 0, 90, 150, 6, RED); rr(c, 105, 0, 90, 150, 6, RED); rr(c, -195, 110, 90, 60, 6, WHT); rr(c, 105, 110, 90, 60, 6, WHT)
        c.restore()
        for k in range(3):
            q = ((g - t) * 1.3 + k / 3) % 1
            if g >= t + .3: arc(c, cx, cy + 190, 120 + 260 * q, 30, 120, WHT, 8, (1 - q) * .6)
    return _v(d)


def v_fumetti(t, t_ok):
    """'Hanno un problema e stanno ricercando la soluzione': persone con il fumetto del punto
    di domanda, che a t_ok diventa una lampadina accesa."""
    def d(c, g, acc):
        for i in range(3):
            x = 220 + i * 320; t0 = t + i * .18
            if g < t0: continue
            q = ob(pr(g, t0, .25)); person(c, x, 1600, 170 * q, WHT)
            ok = g >= t_ok + i * .12; col = YEL if ok else 0xF4F6FF
            c.save(); c.translate(x, 1230 + 10 * math.sin(g * 4 + i)); c.scale(q, q)
            rr(c, -110, -110, 220, 190, 60, col); tri(c, -30, 100, 90, 40, col)
            text(c, '!' if ok else '?', 0, -18, 150, NAVY, 'bk', shadow=False, sc=lerp(1.6, 1, oe(pr(g, t_ok + i * .12, .2))) if ok else 1)
            c.restore()
    return _v(d, [t_ok])


def v_ponte(t, dur=1.6):
    """'Persone che non sono nel tuo bacino e che non avresti mai incontrato': due sponde
    separate, e un ponte che si costruisce asse dopo asse fino a unirle."""
    def d(c, g, acc):
        rr(c, 0, 1500, 260, 320, 20, 0x16204A); rr(c, 820, 1500, 260, 320, 20, 0x16204A)
        for i in range(8): line(c, 280 + i * 70, 1700 + 14 * math.sin(g * 3 + i), 320 + i * 70, 1700 + 14 * math.sin(g * 3 + i + 1), 0x39B8FF, 8, .5)
        circ(c, 130, 1400, 62, acc); text(c, 'TU', 130, 1400, 46, NAVY, 'bk', shadow=False)
        for i in range(3): person(c, 880 + (i - 1) * 75, 1420 - (i % 2) * 50, 95, YEL)
        k = pr(g, t, dur); n = int(k * 9)
        for i in range(n):
            q = oe(pr(g, t + i * dur / 9, .2)); x = 260 + i * 62
            rr(c, x, lerp(1300, 1490, q), 56, 26, 8, 0xC9A66B)
        if n: arc(c, 540, 1500, 290, 180, 180 * n / 9, WHT, 8, .8)
    return _v(d, [t + dur])


def v_scalinata(t, n=6):
    """'Quanti clienti in piu' puoi ottenere': gradini che compaiono uno dopo l'altro, e su
    ogni gradino una persona in piu', senza cifre."""
    def d(c, g, acc):
        for i in range(n):
            t0 = t + i * .2
            if g < t0: continue
            q = ob(pr(g, t0, .25), 1.2); x = 110 + i * 150; h = 110 + i * 105
            c.drawRoundRect(skia.Rect.MakeLTRB(x, 1780 - h * q, x + 130, 1800), 16, 16,
                            skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, 1780 - h), (0, 1800)], [C(acc, .9), C(acc, .15)])))
            person(c, x + 65, 1780 - h * q - 70, 100 * q, WHT if i < n - 1 else YEL)
    return _v(d, [t + (n - 1) * .2])
