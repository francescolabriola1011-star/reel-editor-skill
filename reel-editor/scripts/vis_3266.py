"""Visual NUOVI scritti per il reel 3266 (promotori d'oro, 8/10/2026).
Regola 410: ogni video ha le sue grafiche. Nessuno di questi ripete vis_3263 o vis_3265.
Zona utile y 800-1800, centro 540,1200. Tempi assoluti sulla timeline di base.mp4."""
import math, random, skia
from mgkit import *
from mgkit import _v


def v_scocciatura(t, rifiuti):
    """'Rompere le scatole ad amici e parenti': uno al centro manda onde, quelli intorno
    si prendono una X rossa uno alla volta. rifiuti=[t1, t2, t3, t4]."""
    pos = [(200, 960), (880, 960), (200, 1620), (880, 1620)]
    def d(c, g, acc):
        cx, cy = 540, 1290
        for k in range(3):
            q = ((g - t) * 1.1 + k / 3) % 1
            if g >= t: circ(c, cx, cy, 110 + 330 * q, RED, (1 - q) * .7, 8)
        circ(c, cx, cy, 110, 0x2A1020); person(c, cx, cy + 15, 150, WHT)
        for (x, y), tr in zip(pos, rifiuti):
            p = ob(pr(g, t + .05, .3)) if g >= t + .05 else 0
            no = g >= tr
            person(c, x, y, 120 * p, 0x5F6B8A if no else 0xC9D1F0)
            if no:
                q = ob(pr(g, tr, .22)); circ(c, x + 70, y - 80, 46 * q, RED); check(c, x + 70, y - 80, 42 * q, WHT, False)
    return _v(d, list(rifiuti))


def v_catena_voce(t, t_stop, n=5):
    """'Il passaparola e' bello quando inizia a funzionare': la voce passa da una persona
    all'altra accendendole in fila, con l'arco del messaggio che salta."""
    def d(c, g, acc):
        for i in range(n):
            x = 130 + i * 205; y = 1330; t0 = t + i * (t_stop - t) / n
            on = g >= t0; q = ob(pr(g, t0, .25)) if on else 0
            circ(c, x, y, 95, GRN, .22 * q, blur=18); person(c, x, y + 10, 125, GRN if on else 0x5F6B8A)
            if on and i < n - 1:
                k = pr(g, t0, (t_stop - t) / n); x2 = x + 205 * k; y2 = y - 190 - 90 * math.sin(k * math.pi)
                pth = skia.Path(); pth.moveTo(x, y - 150); pth.quadTo(x + 102, y - 330, x + 205, y - 150)
                pp = P(GRN, .5, 6); pp.setPathEffect(skia.DashPathEffect.Make([14, 14], -g * 100)); c.drawPath(pth, pp)
                rr(c, x2 - 34, y2 - 24, 68, 48, 20, WHT); [circ(c, x2 - 16 + j * 16, y2, 5, NAVY) for j in range(3)]
    return _v(d)


def v_rubrica(t, t_vuota, t_stop):
    """'Se non hai contatti nuovi da poter contattare, tutto quanto si ferma': la rubrica del
    telefono, le righe dei contatti si svuotano una a una, poi il segnale di stop."""
    def d(c, g, acc):
        p = oe(pr(g, t, .35)); c.save(); c.translate(0, 700 * (1 - p))
        rr(c, 250, 800, 580, 980, 70, 0x0E1430); rr(c, 250, 800, 580, 980, 70, 0x8A93B8, .9, 8); rr(c, 450, 830, 180, 26, 13, 0x8A93B8, .6)
        for i in range(5):
            y = 930 + i * 160; tv = t_vuota + i * .28; gone = g >= tv; a = 1 - pr(g, tv, .25) if gone else 1
            rr(c, 300, y, 480, 120, 26, 0x1B2550, a)
            circ(c, 365, y + 60, 38, acc, a); person(c, 365, y + 66, 50, NAVY, a)
            rr(c, 430, y + 34, 250, 22, 11, WHT, .8 * a); rr(c, 430, y + 72, 160, 16, 8, GREY, .8 * a)
            if gone:
                pp = P(GREY, .6 * (1 - a), 4); pp.setPathEffect(skia.DashPathEffect.Make([14, 12], 0))
                c.drawRoundRect(skia.Rect.MakeXYWH(300, y, 480, 120), 26, 26, pp)
        c.restore()
        if g >= t_stop:
            q = ob(pr(g, t_stop, .28)); c.save(); c.translate(540, 1290); c.scale(q, q)
            pth = skia.Path()
            for k in range(8):
                a = math.radians(22.5 + k * 45); (pth.moveTo if k == 0 else pth.lineTo)(math.cos(a) * 250, math.sin(a) * 250)
            pth.close(); c.drawPath(pth, P(RED, .5, blur=30)); c.drawPath(pth, P(RED)); c.drawPath(pth, P(WHT, 1, 12))
            text(c, 'STOP', 0, 0, 150, WHT, 'bk', shadow=False); c.restore()
    return _v(d, [t_stop])


def v_divieto(t, t_no):
    """'Non devi rompere le scatole': un megafono che urla, e il cerchio di divieto che gli
    cade sopra."""
    def d(c, g, acc):
        cx, cy = 540, 1280; p = ob(pr(g, t, .35)) if g >= t else 0
        c.save(); c.translate(cx, cy); c.scale(p, p); c.rotate(-12 + 4 * math.sin(g * 14))
        pth = skia.Path(); pth.moveTo(-190, -60); pth.lineTo(120, -190); pth.lineTo(120, 190); pth.lineTo(-190, 60); pth.close()
        c.drawPath(pth, P(WHT)); rr(c, -260, -70, 90, 140, 24, 0xC9D1F0); rr(c, 120, -205, 46, 410, 20, 0xC9D1F0)
        c.restore()
        for k in range(3):
            a0 = -35 + k * 0; r = 300 + k * 70 + 20 * math.sin(g * 9 + k)
            if g < t_no: arc(c, cx + 120, cy - 40, r - 120, -35, 70, WHT, 14, .7 * p)
        if g >= t_no:
            q = oe(pr(g, t_no, .22)); R = lerp(700, 330, q)
            circ(c, cx, cy, R, RED, cl(q * 2), 44); line(c, cx - R * .7, cy - R * .7, cx + R * .7, cy + R * .7, RED, 44, cl(q * 2))
    return _v(d, [t_no])


def v_scudo(t):
    """'Il tuo e' un lavoro di fiducia': uno scudo che si forma, con la spunta dentro e un
    alone che pulsa."""
    def d(c, g, acc):
        cx, cy = 540, 1300; p = ob(pr(g, t, .4)) if g >= t else 0
        pth = skia.Path(); pth.moveTo(0, -330); pth.lineTo(270, -230); pth.lineTo(270, 40)
        pth.quadTo(250, 260, 0, 370); pth.quadTo(-250, 260, -270, 40); pth.lineTo(-270, -230); pth.close()
        c.save(); c.translate(cx, cy); c.scale(p * (1 + .03 * math.sin(g * 5)), p)
        c.drawPath(pth, P(GOLD, .45, blur=40))
        c.drawPath(pth, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, -330), (0, 370)], [C(0xFFE27A), C(0xB8860B)])))
        c.drawPath(pth, P(WHT, .7, 8))
        q = ob(pr(g, t + .35, .3)) if g > t + .35 else 0; check(c, 0, 10, 260 * q, NAVY)
        c.restore()
    return _v(d, [t + .35])


def v_stretta(t):
    """'Stringere la mano prima di affidarti i propri risparmi': due braccia grosse che
    arrivano dai lati, si stringono al centro e scuotono; scintille al contatto."""
    def d(c, g, acc):
        p = oe(pr(g, t - .45, .45)); dx = 560 * (1 - p)
        sh = 22 * math.sin((g - t) * 16) * (1 - pr(g, t, .9)) if g >= t else 0
        cy = 1280 + sh
        for s, pelle, manica in ((-1, 0xFFD9B0, 0x1B2550), (1, 0xE8B98A, 0x2A3566)):
            c.save(); c.translate(540 + s * dx, cy); c.rotate(s * -7)
            x0 = s * 620; x1 = s * 150
            rr(c, min(x0, x1), -120, abs(x0 - x1), 240, 60, manica)                    # manica
            rr(c, x1 - 35, -135, 70, 270, 20, WHT)                                     # polsino
            rr(c, min(x1, s * -70), -105, abs(x1 - s * -70), 210, 90, pelle)           # mano
            for j in range(4):                                                         # dita che avvolgono
                rr(c, s * (-60 + j * 2) - 30, -95 + j * 50, 60, 44, 22, pelle); rr(c, s * (-60 + j * 2) - 30, -95 + j * 50, 60, 44, 22, 0x000000, .12, 3)
            c.restore()
        if g >= t:
            q = pr(g, t, .5)
            for k in range(12):
                a = math.radians(k * 30 + 10); r0, r1 = 200 + 200 * q, 260 + 300 * q
                line(c, 540 + math.cos(a) * r0, 1280 + math.sin(a) * r0, 540 + math.cos(a) * r1, 1280 + math.sin(a) * r1, YEL, 12, 1 - q)
            circ(c, 540, 1280, 300 * oe(q), GOLD, .3 * (1 - q), blur=40)
    return _v(d, [t])


def v_due_cerchi(t, t_nuovo):
    """'Un circolo diverso da quello del passaparola': a sinistra il solito giro, grigio e
    piccolo; a destra si apre un cerchio nuovo, piu' grande, pieno di persone accese."""
    random.seed(8); A = [(random.uniform(0, 6.28), random.uniform(30, 150)) for _ in range(6)]
    B = [(random.uniform(0, 6.28), random.uniform(40, 250)) for _ in range(14)]
    def d(c, g, acc):
        p = oe(pr(g, t, .35)); lx, ly = 280, 1400
        circ(c, lx, ly, 200 * p, 0x5F6B8A, .15); circ(c, lx, ly, 200 * p, 0x8A93B8, .8, 6)
        for a, r in A: person(c, lx + math.cos(a + g * .3) * r, ly + math.sin(a + g * .3) * r, 60 * p, 0x8A93B8)
        if g >= t_nuovo:
            q = ob(pr(g, t_nuovo, .4)); rx, ry = 720, 1180
            circ(c, rx, ry, 310 * q, acc, .18); circ(c, rx, ry, 310 * q, acc, 1, 8); circ(c, rx, ry, 330 * q, acc, .4, blur=24)
            for i, (a, r) in enumerate(B):
                k = cl((g - t_nuovo - .15 - i * .04) * 5)
                person(c, rx + math.cos(a - g * .25) * r, ry + math.sin(a - g * .25) * r, 62 * k, YEL)
    return _v(d, [t_nuovo])


def v_nastro(t):
    """'Un sistema di marketing automatizzato': un nastro trasportatore che gira da solo e
    porta avanti contatti uno dopo l'altro, con il braccio che li timbra."""
    def d(c, g, acc):
        p = oe(pr(g, t, .35)); y = 1500; c.save(); c.translate(0, 500 * (1 - p))
        rr(c, 60, y, 960, 90, 45, 0x1B2550); rr(c, 60, y, 960, 90, 45, acc, .8, 6)
        for i in range(9): circ(c, 110 + i * 108, y + 45, 26, acc, .9, 5); line(c, 110 + i * 108, y + 45, 110 + i * 108 + math.cos(g * 6) * 22, y + 45 + math.sin(g * 6) * 22, acc, 5)
        off = ((g - t) * 260) % 240
        for i in range(-1, 5):
            x = i * 240 + off + 60; done = x > 540
            rr(c, x - 75, y - 170, 150, 160, 24, 0x16204A); rr(c, x - 75, y - 170, 150, 160, 24, GRN if done else GREY, .9, 5)
            person(c, x, y - 85, 90, GRN if done else 0x8A93B8)
        st = abs(math.sin((g - t) * math.pi * 260 / 240)); ay = 900 + 190 * st
        rr(c, 505, 780, 70, ay - 780, 20, 0x8A93B8); rr(c, 440, ay, 200, 70, 20, YEL)
        c.restore()
    return _v(d)


def v_salvadanaio(t, t_q):
    """'Il problema di investire il proprio denaro': monete che cadono in un barattolo di
    vetro e si accumulano ferme, con il punto interrogativo sopra."""
    def d(c, g, acc):
        cx = 540; p = oe(pr(g, t, .35)); c.save(); c.translate(0, 600 * (1 - p))
        rr(c, 330, 1100, 420, 600, 60, 0x9FE8FF, .12); rr(c, 330, 1100, 420, 600, 60, 0xBFE6FF, .8, 10); rr(c, 300, 1050, 480, 70, 30, 0xBFE6FF, .8, 10)
        n = int(cl((g - t) / 1.6) * 12)
        for i in range(n):
            row, col = divmod(i, 3); x = 420 + col * 120 + (row % 2) * 30; y = 1640 - row * 78
            circ(c, x, y, 52, GOLD); circ(c, x, y, 38, 0xB8860B, .9, 5); text(c, '€', x, y, 54, 0x7A5A00, 'bk', shadow=False)
        k = ((g - t) * 2.2) % 1
        if n < 12: circ(c, cx + 30 * math.sin(g * 9), lerp(820, 1150, k), 52, GOLD); text(c, '€', cx + 30 * math.sin(g * 9), lerp(820, 1150, k), 54, 0x7A5A00, 'bk', shadow=False)
        c.restore()
        if g >= t_q: pop(c, g, t_q, '?', 860, 980, 300, acc, 'bk', glow=acc, rot=12)
    return _v(d, [t_q])


def v_lingotto(t, t_shine):
    """'Piani in oro': un lingotto grande che entra, con il riflesso che lo attraversa e le
    scintille."""
    def d(c, g, acc):
        cx, cy = 540, 1330; p = ob(pr(g, t, .4)) if g >= t else 0
        c.save(); c.translate(cx, cy); c.scale(p, p); c.rotate(-6)
        top = skia.Path(); top.moveTo(-300, -40); top.lineTo(-200, -180); top.lineTo(260, -180); top.lineTo(360, -40); top.close()
        front = skia.Path(); front.moveTo(-300, -40); front.lineTo(360, -40); front.lineTo(300, 170); front.lineTo(-240, 170); front.close()
        c.drawPath(front, P(GOLD, .5, blur=40))
        c.drawPath(top, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, -180), (0, -40)], [C(0xFFF0A8), C(0xFFD23F)])))
        c.drawPath(front, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, -40), (0, 170)], [C(0xFFC53D), C(0xA87400)])))
        text(c, 'ORO', 30, 65, 130, 0x7A5A00, 'bk', shadow=False)
        if g >= t_shine:
            k = pr(g, t_shine, .5); c.save(); c.clipPath(front, True)
            c.drawRect(skia.Rect.MakeXYWH(lerp(-400, 420, k), -60, 90, 260), P(WHT, .55, blur=14)); c.restore()
        c.restore()
        for i in range(6):
            a = i * 1.05 + g * .8; r = 400 + 30 * math.sin(g * 4 + i); s = 26 * abs(math.sin(g * 3 + i)) * p
            x, y = cx + math.cos(a) * r, cy - 60 + math.sin(a) * r * .6
            line(c, x - s, y, x + s, y, WHT, 6); line(c, x, y - s, x, y + s, WHT, 6)
    return _v(d, [t_shine])


def v_agenda(t, t_fill):
    """'Riempirti l'agenda di appuntamenti': una settimana a colonne, le caselle si riempiono
    di appuntamenti una dopo l'altra."""
    G = ['L', 'M', 'M', 'G', 'V']
    def d(c, g, acc):
        p = oe(pr(g, t, .35)); c.save(); c.translate(0, 600 * (1 - p))
        rr(c, 90, 830, 900, 920, 44, 0x121A3F); rr(c, 90, 830, 900, 920, 44, acc, .8, 5); rr(c, 90, 830, 900, 120, 44, acc, .9)
        for i, gg in enumerate(G): text(c, gg, 180 + i * 180, 890, 60, NAVY, 'bk', shadow=False)
        order = [(r, col) for r in range(4) for col in range(5)]; random.seed(3); random.shuffle(order)
        for k, (r, col) in enumerate(order[:14]):
            x = 180 + col * 180; y = 1060 + r * 175; rr(c, x - 75, y - 70, 150, 140, 22, 0x1B2550)
            tf = t_fill + k * .13
            if g >= tf:
                q = ob(pr(g, tf, .22)); rr(c, x - 75 * q, y - 70 * q, 150 * q, 140 * q, 22, GRN); person(c, x, y + 8, 78 * q, NAVY)
        for (r, col) in order[14:]:
            rr(c, 180 + col * 180 - 75, 1060 + r * 175 - 70, 150, 140, 22, 0x1B2550)
        c.restore()
    return _v(d, [t_fill])


def v_guida(t, t_open):
    """'Ho preparato una guida': un libretto che entra chiuso, si apre e mostra le righe
    della spiegazione che si scrivono."""
    def d(c, g, acc):
        cx, cy = 540, 1300; p = ob(pr(g, t, .35)) if g >= t else 0; o = oe(pr(g, t_open, .35)) if g >= t_open else 0
        c.save(); c.translate(cx, cy); c.scale(p, p)
        w = lerp(190, 380, o)
        rr(c, -w, -300, w, 600, 26, 0xF4F1E8); rr(c, 0, -300, w, 600, 26, 0xFFFFFF)
        line(c, 0, -300, 0, 300, 0xB9B4A6, 6)
        if o < .3:
            rr(c, -190, -300, 380, 600, 26, acc, 1 - o * 3); text(c, 'GUIDA', 0, -30, 96, WHT, 'bk', a=1 - o * 3, shadow=False)
        else:
            for i in range(6):
                k = cl((g - t_open - .2 - i * .08) * 4)
                rr(c, -w + 40, -230 + i * 85, (w - 80) * k, 26, 13, 0x8A93B8, .8); rr(c, 40, -230 + i * 85, (w - 80) * k, 26, 13, acc if i == 2 else 0x8A93B8, .8)
        c.restore()
    return _v(d, [t_open])
