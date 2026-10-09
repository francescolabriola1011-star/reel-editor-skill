"""Visual NUOVI per il video YouTube 3296 "i due numeri del marketing" (8/10/2026).
Nessuno ripete vis_3295. Spazio del visual: x 0-1080, y 700-1820, centro 540,1260.
Solo colori di marca (YEL, GOLD, WHT, NAVY, BLUE, STEEL). Tempi assoluti su base.mp4."""
import math, random, skia
from mg16 import *
from mg16 import _v, STEEL


def v_bilancia(t, t_sx, t_dx, sx='COSTO', dx='VALORE'):
    """Bilancia: a sinistra quanto ti costa un cliente, a destra quanto ti vale. Da t_dx il
    piatto del valore scende e la bilancia pende dalla parte giusta."""
    cx, cy = 540, 1060
    def d(c, g, acc):
        q = ob(pr(g, t, .35)); ang = 0 if g < t_dx else -11 * oe(pr(g, t_dx, .6))
        rr(c, cx - 14, cy, 28, 560 * q, 10, WHT, .9); rr(c, cx - 170, cy + 560 * q - 10, 340, 34, 17, WHT, .9)
        c.save(); c.translate(cx, cy); c.rotate(ang)
        rr(c, -440, -14, 880, 28, 14, acc); circ(c, 0, 0, 34, acc)
        for side, lab, t0, col in ((-1, sx, t_sx, STEEL), (1, dx, t_dx, acc)):
            if g < t0: continue
            p = ob(pr(g, t0, .3)); x = side * 400
            c.save(); c.translate(x, 0); c.rotate(-ang)
            line(c, -110, 210, 0, 10, WHT, 5, .7); line(c, 110, 210, 0, 10, WHT, 5, .7)
            c.drawArc(skia.Rect.MakeLTRB(-150, 150, 150, 290), 0, 180, True, P(col, .9))
            text(c, lab, 0, 340, 58, col, 'bk', a=p, maxw=320)
            c.restore()
        c.restore()
    return _v(d, [t_sx, t_dx])


def v_moltiplica(t, t_due, a='1€', b='2€'):
    """Ogni euro investito ne torna due: una moneta entra a sinistra, una freccia e a t_due
    escono due monete a destra."""
    def coin(c, x, y, s, lab, col):
        c.save(); c.translate(x, y); c.scale(s, s); circ(c, 0, 0, 150, col, .25, blur=26); circ(c, 0, 0, 125, col); circ(c, 0, 0, 96, 0x8C6A12, 1, 6)
        text(c, lab, 0, 4, 100, NAVY, 'bk', shadow=False, maxw=170); c.restore()
    def d(c, g, acc):
        if g >= t: coin(c, 220, 1260, ob(pr(g, t, .3)), a, GOLD)
        if g >= t + .3:
            p = oe(pr(g, t + .3, .4)); line(c, 390, 1260, 390 + 260 * p, 1260, WHT, 18); tri(c, 400 + 260 * p, 1260, 0, 34, WHT)
        if g >= t_due:
            coin(c, 860, 1110, ob(pr(g, t_due, .3)), a, acc); coin(c, 860, 1410, ob(pr(g, t_due + .15, .3)), a, acc)
            pop(c, g, t_due + .3, b, 860, 1660, 90, acc, 'bi')
    return _v(d, [t_due])


def v_vanita(t, t_spegni):
    """Metriche di vanita': cuore, occhio e fumetto con i contatori che salgono, poi da
    t_spegni si spengono in grigio e accanto resta il cartello CLIENTI 0."""
    icons = ['cuore', 'occhio', 'fumetto']
    def ico(c, kind, x, y, s, col):
        c.save(); c.translate(x, y); c.scale(s, s)
        if kind == 'cuore':
            p = skia.Path(); p.moveTo(0, 60); p.cubicTo(-120, -20, -70, -110, 0, -50); p.cubicTo(70, -110, 120, -20, 0, 60); c.drawPath(p, P(col))
        elif kind == 'occhio':
            c.drawOval(skia.Rect.MakeLTRB(-95, -55, 95, 55), P(col)); circ(c, 0, 0, 36, NAVY); circ(c, 0, 0, 16, col)
        else:
            rr(c, -90, -65, 180, 110, 40, col); tri(c, -40, 60, 100, 26, col)
        c.restore()
    def d(c, g, acc):
        off = g >= t_spegni
        for i, k in enumerate(icons):
            t0 = t + i * .2
            if g < t0: continue
            q = ob(pr(g, t0, .3)); y = 960 + i * 260; col = STEEL if off else [acc, WHT, GOLD][i]
            ico(c, k, 230, y, q, col)
            k = oc(pr(g, t0, 1.6)) * [.8, .95, .7][i]          # niente cifre: a schermo solo numeri DETTI
            rr(c, 380, y - 28, 560, 56, 28, 0x24305A, q); rr(c, 380, y - 28, 560 * k, 56, 28, STEEL if off else col, q)
        if off:
            p = ob(pr(g, t_spegni + .2, .3)); c.save(); c.translate(540, 1690); c.scale(p, p)
            rr(c, -330, -70, 660, 140, 70, acc); text(c, 'CLIENTI', -40, 0, 72, NAVY, 'bk', shadow=False, maxw=440); circ(c, 230, 0, 46, NAVY); check(c, 230, 0, 52, acc, False); c.restore()
    return _v(d, [t_spegni])


def v_garanzie(items):
    """Tre scudi con la spunta, uno per garanzia. items = [(tempo, 'CONTATTI'), ...]"""
    def d(c, g, acc):
        for i, (t0, lab) in enumerate(items[:3]):
            if g < t0: continue
            q = ob(pr(g, t0, .35)); x = 200 + i * 340; y = 1220
            c.save(); c.translate(x, y); c.scale(q, q)
            s = skia.Path(); s.moveTo(0, -170); s.lineTo(140, -120); s.lineTo(130, 40); s.cubicTo(110, 130, 40, 170, 0, 200); s.cubicTo(-40, 170, -110, 130, -130, 40); s.lineTo(-140, -120); s.close()
            c.drawPath(s, P(acc, .3, blur=20)); c.drawPath(s, P(acc)); c.drawPath(s, P(0x8C6A12, 1, 6)); check(c, 0, 0, 120, NAVY, True)
            c.restore()
            text(c, lab, x, y + 280, 50, WHT, 'bk', a=cl(q), maxw=320)
    return _v(d, [i[0] for i in items])


def v_dado_formula(t, t_formula):
    """Fortuna contro metodo: un dado che rotola e non si ferma mai (viralita'), poi a
    t_formula a destra entra un cruscotto con le lancette ferme sul valore (scientifico)."""
    def d(c, g, acc):
        roll = g * 400 if g < t_formula else t_formula * 400 + 40 * math.sin(g * 9)
        c.save(); c.translate(270, 1260 + 40 * math.sin(g * 7)); c.rotate(roll)
        rr(c, -130, -130, 260, 260, 40, STEEL if g >= t_formula else WHT)
        for (px, py) in [(-60, -60), (60, 60), (0, 0), (60, -60), (-60, 60)]: circ(c, px, py, 22, NAVY)
        c.restore()
        text(c, 'FORTUNA', 270, 1530, 56, STEEL if g >= t_formula else WHT, 'bk', maxw=380)
        if g >= t_formula:
            q = ob(pr(g, t_formula, .35)); c.save(); c.translate(810, 1240); c.scale(q, q)
            rr(c, -210, -200, 420, 400, 40, 0x121A3F); rr(c, -210, -200, 420, 400, 40, acc, 1, 6)
            for k in range(3):
                y = -110 + k * 110; v = [.72, .55, .84][k]
                rr(c, -160, y - 10, 320, 20, 10, 0x2A3566); rr(c, -160, y - 10, 320 * v * oe(pr(g, t_formula + .2 + k * .15, .4)), 20, 10, acc)
            c.restore()
            text(c, 'METODO', 810, 1530, 56, acc, 'bi', a=q, maxw=380)
    return _v(d, [t_formula])


def v_videochiamata(t, t_firma):
    """Lavorare da remoto su tutta Italia: un portatile con la videochiamata e, a t_firma, un
    contratto che scivola fuori con la firma che si scrive."""
    def d(c, g, acc):
        q = ob(pr(g, t, .35)); c.save(); c.translate(540, 1200); c.scale(q, q)
        rr(c, -380, -260, 760, 470, 30, 0x121A3F); rr(c, -380, -260, 760, 470, 30, WHT, .85, 8)
        p = skia.Path(); p.moveTo(-460, 230); p.lineTo(460, 230); p.lineTo(400, 280); p.lineTo(-400, 280); p.close(); c.drawPath(p, P(WHT, .85))
        for i, x in enumerate((-180, 180)):
            rr(c, x - 160, -220, 320, 280, 20, 0x24305A); person(c, x, -60, 150, [WHT, acc][i])
        for k in range(3): circ(c, -60 + k * 60, 140, 18, [STEEL, acc, WHT][k])
        c.restore()
        if g >= t_firma:
            s = oe(pr(g, t_firma, .4)); y = 1700 - 180 * s
            c.save(); c.translate(760, y); c.rotate(-6)
            rr(c, -170, -150, 340, 300, 16, WHT); [rr(c, -120, -110 + k * 40, 240 - k * 30, 14, 7, STEEL, .6) for k in range(4)]
            w = oe(pr(g, t_firma + .3, .6)); pth = skia.Path(); pth.moveTo(-110, 90)
            for k in range(1, 40):
                u = k / 39
                if u > w: break
                pth.lineTo(-110 + 220 * u, 90 + 22 * math.sin(u * 18))
            c.drawPath(pth, P(NAVY, 1, 5)); c.restore()
    return _v(d, [t_firma])


def v_pila_video(t, n=12):
    """3-4 video al giorno: miniature di video che si impilano senza fine."""
    def d(c, g, acc):
        k = int(max(0, g - t) / .14) + 1
        for i in range(min(k, n)):
            t0 = t + i * .14; q = oe(pr(g, t0, .25)); col, row = i % 4, i // 4
            x = 160 + col * 255; y = 980 + row * 270 - 200 * (1 - q)
            c.save(); c.translate(x, y); c.rotate((i * 37 % 9) - 4)
            rr(c, -110, -100, 220, 200, 22, 0x1E2A50, q); rr(c, -110, -100, 220, 200, 22, WHT, .7 * q, 4); tri(c, 6, 0, 0, 40, acc, q)
            c.restore()
    return _v(d, [t + i * .14 for i in range(0, n, 4)])


def v_scalini(steps):
    """Sappiamo quanto costa ogni passo: tre scalini che salgono (richiesta, appuntamento,
    cliente) con il segno di controllo su ciascuno. steps = [(tempo, 'RICHIESTA'), ...]"""
    def d(c, g, acc):
        for i, (t0, lab) in enumerate(steps[:3]):
            if g < t0: continue
            q = ob(pr(g, t0, .3), 1.2); x = 100 + i * 300; h = 260 + i * 220
            c.drawRoundRect(skia.Rect.MakeLTRB(x, 1720 - h * q, x + 270, 1720), 22, 22, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, 1720 - h), (0, 1720)], [K_C([WHT, GOLD, acc][i]), K_C([WHT, GOLD, acc][i], .25)])))
            text(c, lab, x + 135, 1720 - h * q - 60, 46, WHT, 'bk', a=cl(q), maxw=290)
            if g >= t0 + .25:
                b = ob(pr(g, t0 + .25, .25)); circ(c, x + 135, 1720 - h * q + 80, 46 * b, NAVY); check(c, x + 135, 1720 - h * q + 80, 46 * b, [WHT, GOLD, acc][i], True)
    return _v(d, [s[0] for s in steps])


def K_C(h, a=1.0):
    return skia.Color((h >> 16) & 255, (h >> 8) & 255, h & 255, int(255 * max(0, min(1, a))))


def v_folla(t, t_pochi, pochi=(10, 20, 30)):
    """Non servono 100.000 persone: una folla enorme di puntini grigi, e da t_pochi se ne
    accendono pochi, che diventano i contatti giusti. pochi = numeri detti a voce."""
    random.seed(77); D = [(random.uniform(40, 1040), random.uniform(820, 1800)) for _ in range(420)]
    sel = D[::14][:30]
    def d(c, g, acc):
        for (x, y) in D:
            circ(c, x, y, 9, STEEL, .45 * pr(g, t, .4))
        if g >= t_pochi:
            for i, (x, y) in enumerate(sel):
                q = ob(pr(g, t_pochi + i * .03, .25)); circ(c, x, y, 34 * q, acc, .3, blur=10); circ(c, x, y, 18 * q, acc)
            for i, n in enumerate(pochi):
                t0 = t_pochi + .25 + i * .35
                if g >= t0:
                    pill(c, g, t0, str(n), 220 + i * 320, 1260, [WHT, GOLD, acc][i])
    return _v(d, [t_pochi + .25 + i * .35 for i in range(len(pochi))])


def v_commenti(t, t_zero):
    """Tanti commenti sotto un reel virale che scorrono, e accanto il contatore dei clienti
    che a t_zero resta fermo a zero."""
    def d(c, g, acc):
        c.save(); c.clipRect(skia.Rect.MakeLTRB(80, 820, 700, 1760))
        off = (g - t) * 260
        for i in range(14):
            y = 1760 - ((i * 135 + off) % 1900) + 100
            rr(c, 100, y, 580, 110, 30, 0x1E2A50); circ(c, 160, y + 55, 34, [GOLD, WHT, BLUE][i % 3])
            rr(c, 220, y + 30, 300 - (i % 3) * 60, 18, 9, WHT, .8); rr(c, 220, y + 64, 200 - (i % 2) * 50, 14, 7, STEEL, .7)
        c.restore()
        if g >= t_zero:
            q = ob(pr(g, t_zero, .3)); c.save(); c.translate(870, 1260); c.scale(q, q)
            rr(c, -150, -180, 300, 360, 40, 0x121A3F); rr(c, -150, -180, 300, 360, 40, acc, 1, 6)
            text(c, 'CLIENTI', 0, -100, 46, acc, 'bk', shadow=False, maxw=260); circ(c, 0, 50, 90, STEEL, .5); check(c, 0, 50, 110, WHT, False)
            c.restore()
    return _v(d, [t_zero])


def v_scappa(t):
    """Scappa e lascia perdere: una porta che si apre e una freccia che esce di corsa."""
    def d(c, g, acc):
        q = ob(pr(g, t, .3)); c.save(); c.translate(640, 1260); c.scale(q, q)
        rr(c, -170, -300, 340, 600, 20, 0x121A3F); rr(c, -170, -300, 340, 600, 20, WHT, .9, 8)
        o = oe(pr(g, t + .25, .4)); p = skia.Path(); p.moveTo(-160, -290); p.lineTo(-160 + 300 * (1 - o * .7), -290 + 40 * o); p.lineTo(-160 + 300 * (1 - o * .7), 290 - 40 * o); p.lineTo(-160, 290); p.close()
        c.drawPath(p, P(acc)); circ(c, -160 + 270 * (1 - o * .7), 0, 14, NAVY)
        c.restore()
        if g >= t + .5:
            s = oe(pr(g, t + .5, .4)); x = lerp(560, 120, s)
            line(c, 600, 1260, x, 1260, WHT, 26); tri(c, x - 10, 1260, 180, 46, WHT)
    return _v(d, [t + .5])


def v_slot(t, t_scelta, label='CHIAMATA CONOSCITIVA'):
    """Prenotare la chiamata: un calendario della settimana, il cursore sceglie lo slot e a
    t_scelta lo slot si accende con l'etichetta."""
    def d(c, g, acc):
        q = oe(pr(g, t, .35)); c.save(); c.translate(0, 500 * (1 - q))
        rr(c, 90, 880, 900, 780, 40, 0xF4F6FB); rr(c, 90, 880, 900, 110, 40, acc); rr(c, 90, 950, 900, 40, 0, acc)
        text(c, 'PRENOTA', 540, 935, 60, NAVY, 'bk', shadow=False)
        for col in range(5):
            text(c, ['LUN', 'MAR', 'MER', 'GIO', 'VEN'][col], 200 + col * 170, 1050, 36, NAVY, 'bk', shadow=False)
            for r in range(4):
                x, y = 135 + col * 170, 1100 + r * 130; on = g >= t_scelta and col == 2 and r == 1
                rr(c, x, y, 130, 100, 18, acc if on else 0xDCE1EC)
        if g >= t_scelta:
            b = ob(pr(g, t_scelta + .1, .3)); c.save(); c.translate(540, 1590); c.scale(b, b)
            rr(c, -390, -55, 780, 110, 55, NAVY); text(c, label, 0, 0, 46, acc, 'bk', shadow=False, maxw=720); c.restore()
        mx = lerp(950, 520, oe(pr(g, t + .3, max(.3, t_scelta - t - .3)))); my = lerp(1700, 1290, oe(pr(g, t + .3, max(.3, t_scelta - t - .3))))
        cur = skia.Path(); cur.moveTo(0, 0); cur.lineTo(0, 70); cur.lineTo(18, 54); cur.lineTo(32, 86); cur.lineTo(44, 80); cur.lineTo(30, 50); cur.lineTo(54, 50); cur.close()
        c.save(); c.translate(mx, my); c.drawPath(cur, P(NAVY)); c.drawPath(cur, P(WHT, 1, 4)); c.restore()
        c.restore()
    return _v(d, [t_scelta])
