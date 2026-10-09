"""Visual NUOVI scritti per il reel 3263 (8/10/2026).

Regola di Francesco dell'8/10: ogni video ha grafiche nuove fatte apposta per le sue frasi,
non sempre il catalogo. Questi nascono dalle frasi del 3263; un video dopo puo' riusarli solo
in un punto narrativo diverso, e intanto ne scrive di suoi.
Zona utile y 800-1800, centro 540,1200. Tempi assoluti sulla timeline di base.mp4.
"""
import math, random, skia
from mgkit import *
from mgkit import _v


def v_fila(steps, n=10):
    """'Composto al 70, 80% di clienti piccoli': dieci clienti in fila, si colorano di rosso
    uno alla volta fino alla quota detta; la percentuale sbatte sopra. steps=[(t, 7), (t, 8)]."""
    def d(c, g, acc):
        k = 0
        for t0, q in steps:
            if g >= t0: k = q
        # avanzamento morbido verso k: i rossi arrivano a cascata, non tutti insieme
        t_first = steps[0][0]
        for i in range(n):
            x = 120 + (i % 5) * 210; y = 1130 + (i // 5) * 330
            t_in = t_first - .55 + i * .04; q = ob(pr(g, t_in, .25)) if g >= t_in else 0
            rosso = i < k and g >= t_first + i * .03
            col = RED if rosso else 0x8A93B8
            circ(c, x, y, 92 * q, col, .18 if rosso else .1); person(c, x, y + 10, 120 * q, col)
        if k:
            cur = max(t for t, q in steps if g >= t)
            slam(c, g, cur, f'{k * 10}%', 540, 960, 190, RED, 'bk', glow=RED, d=.16)
    return _v(d, [s[0] for s in steps])


def v_scontrino(rows):
    """'Commissioni da 50, 100 euro': uno scontrino che esce dalla stampante, ogni riga si
    stampa quando viene detta. rows=[(t, 'COMMISSIONE', '50€'), ...]."""
    def d(c, g, acc):
        t0 = rows[0][0] - .5; p = oe(pr(g, t0, .45))
        c.save(); c.translate(0, -260 * (1 - p))
        rr(c, 170, 760, 740, 70, 35, 0x1B2340)                                # bocca stampante
        hgt = 260 + 230 * sum(1 for r in rows if g >= r[0])
        c.save(); c.clipRect(skia.Rect.MakeLTRB(0, 795, W, H), True)
        rr(c, 230, 795, 620, hgt, 10, 0xF4F1E8)
        for i in range(0, 620, 40):                                            # bordo seghettato
            tri(c, 230 + i + 20, 795 + hgt + 2, 90, 22, 0xF4F1E8)
        text(c, 'RICEVUTA', 540, 870, 54, 0x2A2A2A, 'bk', shadow=False)
        line(c, 270, 925, 810, 925, 0x9A9A9A, 3)
        for i, (tr, lab, val) in enumerate(rows):
            if g < tr: continue
            q = oe(pr(g, tr, .2)); y = 1010 + i * 230
            text(c, lab, 270, y, 50, 0x3A3A3A, 'b', a=q, align=0, shadow=False)
            text(c, val, 810, y + 90, 120 * lerp(1.6, 1, q), 0x0B9E63, 'bk', a=q, align=1, shadow=False)
        c.restore(); c.restore()
    return _v(d, [r[0] for r in rows])


def v_cloni(t, n=5):
    """'Referenze di qualita'' da clienti piccoli: da una persona escono copie identiche,
    tutte piccole uguali a lei (il passaparola replica il cliente che hai)."""
    def d(c, g, acc):
        cx, cy = 540, 1250
        circ(c, cx, cy, 120, acc, .2, blur=20); person(c, cx, cy + 20, 170, acc)
        for i in range(n):
            t0 = t + .15 + i * .14
            if g < t0: continue
            q = oe(pr(g, t0, .35)); a = math.radians(-160 + i * 35)
            ex, ey = cx + math.cos(a) * 380, cy + 80 + math.sin(a) * 300
            x, y = lerp(cx, ex, q), lerp(cy, ey, q)
            pp = P(acc, .5, 5); pp.setPathEffect(skia.DashPathEffect.Make([16, 14], -g * 120)); c.drawLine(cx, cy, x, y, pp)
            person(c, x, y + 10, 110 * lerp(.4, 1, q), 0x8A93B8)
            text(c, '=', x, y - 95, 60, acc, 'bk', a=q, shadow=False)
    return _v(d)


def v_boccia(t, label_t=None):
    """'Da questo bacino di clienti': una boccia di vetro chiusa con pesciolini piccoli che
    girano sempre in tondo dentro, senza uscita."""
    random.seed(5); F = [(random.uniform(0, 6.28), random.uniform(80, 280), random.uniform(.8, 1.6), random.uniform(24, 38)) for _ in range(12)]
    def d(c, g, acc):
        cx, cy = 540, 1300; p = ob(pr(g, t, .4)) if g >= t else 0
        c.save(); c.translate(cx, cy); c.scale(p, p)
        circ(c, 0, 0, 360, 0x39B8FF, .12); circ(c, 0, 0, 360, 0xBFE6FF, .55, 10)
        rr(c, -160, -380, 320, 60, 30, 0xBFE6FF, .55, 10)                       # bordo bocca
        c.drawRect(skia.Rect.MakeLTRB(-340, 60, 340, 340), P(0x39B8FF, .12))
        for (a0, r, sp, s) in F:
            a = a0 + g * sp; x, y = math.cos(a) * r, math.sin(a) * r * .75
            dirn = 1 if math.cos(a + math.pi / 2) > 0 else -1
            pth = skia.Path(); pth.addOval(skia.Rect.MakeLTRB(-s, -s * .55, s, s * .55))
            pth.moveTo(-s * dirn * .9, 0); pth.lineTo(-s * dirn * 1.6, -s * .5); pth.lineTo(-s * dirn * 1.6, s * .5); pth.close()
            c.save(); c.translate(x, y); c.drawPath(pth, P(0xFF9F43)); c.restore()
        c.restore()
    return _v(d)


def v_lingotti(steps):
    """'100, 200, 500 mila euro': lingotti d'oro che si impilano a ogni cifra detta, la cifra
    sbatte sopra la pila. steps=[(t, '100', 1), (t, '200', 2), (t, '500', 5)] (terzo = lingotti)."""
    def d(c, g, acc):
        cur = None; tot = 0
        for s in steps:
            if g >= s[0]: cur = s
        for si, s in enumerate(steps):
            if g < s[0]: continue
            prev = steps[si - 1][2] if si else 0
            for j in range(prev, s[2]):
                t0 = s[0] + (j - prev) * .05; q = oe(pr(g, t0, .22))
                row, col = divmod(j, 3); x = 230 + col * 210 + (row % 2) * 105; y = 1720 - row * 120
                y = lerp(y - 500, y, q)
                pth = skia.Path(); pth.moveTo(x - 95, y); pth.lineTo(x + 95, y); pth.lineTo(x + 70, y - 95); pth.lineTo(x - 70, y - 95); pth.close()
                c.drawPath(pth, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(x, y - 95), (x, y)], [C(0xFFE27A, q), C(0xC8920A, q)])))
                c.drawPath(pth, P(0x8A6300, .8 * q, 3))
        if cur: slam(c, g, cur[0], cur[1], 540, 1040, 330, GOLD, 'bk', glow=GOLD, d=.16, maxw=900)
    return _v(d, [s[0] for s in steps])


def v_diamante(t):
    """'Il cliente patrimonializzato': un diamante che entra ruotando e manda bagliori."""
    def d(c, g, acc):
        p = ob(pr(g, t, .4)) if g >= t else 0; cx, cy = 540, 1280
        for k in range(8):
            a = math.radians(k * 45 + g * 40); r = 330 + 30 * math.sin(g * 5 + k)
            line(c, cx + math.cos(a) * 250 * p, cy + math.sin(a) * 250 * p, cx + math.cos(a) * r * p, cy + math.sin(a) * r * p, 0x9FE8FF, 8, .6)
        c.save(); c.translate(cx, cy); c.scale(p * (.85 + .15 * abs(math.cos(g * 2))), p)
        top = [(-230, -60), (-130, -190), (130, -190), (230, -60)]; bot = (0, 260)
        pth = skia.Path(); pth.moveTo(*top[0])
        for pt in top[1:]: pth.lineTo(*pt)
        pth.lineTo(*bot); pth.close()
        c.drawPath(pth, P(0x7FDBFF, .35, blur=30))
        c.drawPath(pth, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(-230, -190), (230, 260)], [C(0xE8FBFF), C(0x3FA9F5)])))
        for a_, b_ in [((-230, -60), (230, -60)), ((-130, -190), (-60, -60)), ((130, -190), (60, -60)), ((-60, -60), (0, 260)), ((60, -60), (0, 260))]:
            line(c, *a_, *b_, 0xFFFFFF, 5, .7)
        c.restore()
    return _v(d)


def v_imbuto(t, n=14):
    """'Un sistema di marketing automatizzato': puntini che cadono in un imbuto e ne escono
    come persone in fila, a ritmo costante (la macchina che lavora da sola)."""
    random.seed(9); D = [(random.uniform(250, 830), random.uniform(0, 1.2)) for _ in range(n)]
    def d(c, g, acc):
        p = oe(pr(g, t, .35)); cx = 540
        pth = skia.Path(); pth.moveTo(200, 1000); pth.lineTo(880, 1000); pth.lineTo(600, 1380); pth.lineTo(600, 1500); pth.lineTo(480, 1500); pth.lineTo(480, 1380); pth.close()
        c.save(); c.translate(0, 300 * (1 - p)); c.drawPath(pth, P(acc, .18)); c.drawPath(pth, P(acc, .9, 8)); c.restore()
        for (x0, ph) in D:
            k = ((g - t) * .9 + ph) % 1.2
            if g < t or k > 1: continue
            if k < .5: x, y = lerp(x0, cx, k * 2) , lerp(820, 1380, k * 2)
            else: x, y = cx, lerp(1380, 1520, (k - .5) * 2)
            circ(c, x, y, 18, YEL)
        for i in range(5):
            x = 300 + i * 120 - ((g - t) * 120) % 120; q = cl((g - t) * 2 - i * .3)
            person(c, x, 1690, 90, GRN, q)
    return _v(d)


def v_zona(t, t_pin):
    """'Nella tua area': una mappa a isolati, un cerchio di zona che si allarga e il
    segnaposto che cade al centro; dentro la zona le persone si accendono."""
    random.seed(4); PP = [(random.uniform(150, 930), random.uniform(880, 1760)) for _ in range(26)]
    def d(c, g, acc):
        for i in range(6):
            for j in range(8):
                rr(c, 90 + i * 160, 830 + j * 125, 130, 95, 14, 0x0E3B2C, .9)
        r = 380 * oe(pr(g, t, .6)); cx, cy = 540, 1300
        circ(c, cx, cy, r, GRN, .12); circ(c, cx, cy, r, GRN, .9, 6)
        for (x, y) in PP:
            ins = math.hypot(x - cx, y - cy) < r
            circ(c, x, y, 16 if ins else 10, YEL if ins else 0x5F6B8A, 1 if ins else .6)
        if g >= t_pin:
            q = oe(pr(g, t_pin, .25)); y = lerp(800, cy - 40, q)
            pth = skia.Path(); pth.addCircle(cx, y - 110, 70); pth.moveTo(cx - 62, y - 80); pth.lineTo(cx, y + 20); pth.lineTo(cx + 62, y - 80); pth.close()
            c.drawPath(pth, P(RED)); circ(c, cx, y - 110, 26, WHT)
    return _v(d, [t_pin])


def v_catena(t_break):
    """'Fuori dal circolo di referenze': un anello di maglie di catena che si spezza e da'
    l'uscita a una freccia verde."""
    def d(c, g, acc):
        cx, cy, R, n = 540, 1300, 320, 12
        br = oe(pr(g, t_break, .3)) if g >= t_break else 0
        for i in range(n):
            a = 2 * math.pi * i / n + g * .3; off = 0
            if i in (0, n - 1) and br: off = 90 * br * (1 if i == 0 else -1)
            x = cx + math.cos(a) * R + math.cos(a + math.pi / 2) * off; y = cy + math.sin(a) * R + math.sin(a + math.pi / 2) * off
            c.save(); c.translate(x, y); c.rotate(math.degrees(a) + 90 + (i % 2) * 90)
            c.drawRoundRect(skia.Rect.MakeXYWH(-34, -58, 68, 116), 34, 34, P(0xB8C0D8, .95, 14)); c.restore()
        person(c, cx, cy + 20, 130, WHT)
        if br:
            q = oe(pr(g, t_break + .1, .4)); a = math.radians(-60)
            ex, ey = cx + math.cos(a) * 620 * q, cy + math.sin(a) * 620 * q
            line(c, cx, cy, ex, ey, GRN, 22); tri(c, ex, ey, -60, 44, GRN)
    return _v(d, [t_break])


def v_lente(t, t_find, n=24):
    """'Persone che stanno ricercando attivamente una soluzione': una lente scorre su una
    folla di persone grigie e si ferma su quella che sta cercando, che si accende."""
    def d(c, g, acc):
        tgt = 13
        for i in range(n):
            x = 150 + (i % 6) * 156; y = 950 + (i // 6) * 210
            col = YEL if (i == tgt and g >= t_find) else 0x5F6B8A
            person(c, x, y, 105, col)
        tx, ty = 150 + (tgt % 6) * 156, 950 + (tgt // 6) * 210
        if g < t_find:
            k = pr(g, t, t_find - t); lx = 540 + math.sin(k * 7) * 330; ly = 1150 + math.cos(k * 5) * 240
        else:
            lx, ly = tx, ty - 20
        circ(c, lx, ly, 120, WHT, .12); circ(c, lx, ly, 120, WHT, 1, 14)
        a = math.radians(45); line(c, lx + math.cos(a) * 120, ly + math.sin(a) * 120, lx + math.cos(a) * 260, ly + math.sin(a) * 260, WHT, 30)
        if g >= t_find:
            q = ob(pr(g, t_find, .3)); circ(c, tx, ty - 20, 150 * q, YEL, .25, blur=20)
    return _v(d, [t_find])


def v_scheda(fields):
    """'I numeri di queste persone, con eta', patrimonio, posizione sociale e problema': la
    scheda di un contatto che si compila voce per voce. fields=[(t, 'ETA''), ...]."""
    def d(c, g, acc):
        p = oe(pr(g, fields[0][0] - .6, .4)); c.save(); c.translate(0, 500 * (1 - p))
        c.drawRoundRect(skia.Rect.MakeXYWH(100, 820, 880, 960), 50, 50, P(acc, .4, blur=30))
        rr(c, 100, 820, 880, 960, 50, 0x121A3F); rr(c, 100, 820, 880, 960, 50, acc, .8, 5)
        circ(c, 230, 950, 80, 0x2A3566); person(c, 230, 960, 110, WHT)
        rr(c, 350, 905, 400, 34, 17, 0x8A93B8, .8); rr(c, 350, 965, 260, 26, 13, 0x5F6B8A, .8)
        for i, (tf, lab) in enumerate(fields):
            y = 1110 + i * 160
            text(c, lab, 160, y, 50, 0x8A93B8, 'b', align=0, shadow=False)
            rr(c, 160, y + 40, 760, 22, 11, 0x2A3566)
            if g >= tf:
                q = oe(pr(g, tf, .35)); rr(c, 160, y + 40, 760 * q, 22, 11, GRN)
                b = ob(pr(g, tf + .2, .25)) if g > tf + .2 else 0; circ(c, 880, y, 34 * b, GRN); check(c, 880, y, 32 * b, NAVY)
        c.restore()
    return _v(d, [f[0] for f in fields])


def v_anno(t, t_arrow):
    """'Nel prossimo anno': dodici mesi a calendario che si accendono uno dopo l'altro, e
    una freccia che sale sopra."""
    M = ['G', 'F', 'M', 'A', 'M', 'G', 'L', 'A', 'S', 'O', 'N', 'D']
    def d(c, g, acc):
        for i, m in enumerate(M):
            t0 = t + i * .08; q = ob(pr(g, t0, .25)) if g >= t0 else 0
            x = 150 + (i % 4) * 260; y = 1080 + (i // 4) * 230; h = 22 + i * 4.5
            rr(c, x - 100, y - 90, 200, 180, 26, 0x16204A, q); rr(c, x - 100, y - 90, 200, 180, 26, GRN, .5 * q, 4)
            rr(c, x - 60, y + 70 - h * q, 120, h * q, 12, GRN, .85)
            text(c, m, x, y - 50, 46, WHT, 'bk', a=q, shadow=False)
        if g >= t_arrow:
            q = oe(pr(g, t_arrow, .5)); x2, y2 = lerp(140, 950, q), lerp(1720, 900, q)
            line(c, 140, 1720, x2, y2, YEL, 16); tri(c, x2, y2, -45, 36, YEL)
    return _v(d, [t_arrow])
