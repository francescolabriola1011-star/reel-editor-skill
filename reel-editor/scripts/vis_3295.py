"""Visual NUOVI per il video YouTube 3295 "il passaparola funziona sempre meno" (8/10/2026).
Regola 410: ogni video le sue grafiche. Spazio del visual: x 0-1080, y 700-1820, centro 540,1260
(mg16.place_visual lo riporta nel riquadro 16:9). Solo colori di marca: YEL, GOLD, WHT, NAVY,
BLUE e STEEL (il "problema", al posto del rosso). Tempi assoluti sulla timeline di base.mp4."""
import math, random, skia
from mg16 import *
from mg16 import _v, STEEL


def _bolla(c, x, y, w, h, col, a=1, coda=1):
    rr(c, x - w / 2, y - h / 2, w, h, h * .45, col, a)
    p = skia.Path(); p.moveTo(x + coda * w * .18, y + h / 2 - 2); p.lineTo(x + coda * w * .32, y + h / 2 + 34); p.lineTo(x + coda * w * .02, y + h / 2 - 2); p.close()
    c.drawPath(p, P(col, a))
    for k in range(3): circ(c, x - 34 + k * 34, y, 10, NAVY, a)


def v_catena(t, n=5, t_rotta=None):
    """Il passaparola come una catena di persone: ognuno passa la bolla al successivo. Da
    t_rotta l'ultimo anello si spegne e la catena si interrompe."""
    xs = [110 + i * 215 for i in range(n)]; y = 1380
    def d(c, g, acc):
        for i, x in enumerate(xs):
            t0 = t + i * .28
            if g < t0: continue
            q = ob(pr(g, t0, .3)); spento = t_rotta and g >= t_rotta and i >= n - 2
            col = STEEL if spento else (acc if i == 0 else WHT)
            person(c, x, y + 30, 175 * q, col, .45 if spento else 1)
            if i < n - 1 and g >= t0 + .18:
                pp = P(STEEL if (t_rotta and g >= t_rotta and i >= n - 3) else acc, .8, 7)
                pp.setPathEffect(skia.DashPathEffect.Make([18, 14], -g * 120))
                p2 = oe(pr(g, t0 + .18, .25)); c.drawLine(x + 70, y - 40, x + 70 + 60 * p2, y - 40, pp)
                if not (t_rotta and g >= t_rotta and i >= n - 3):
                    _bolla(c, x + 105, y - 250, 170, 100, acc if i % 2 == 0 else WHT, cl(p2 * 2))
        if t_rotta and g >= t_rotta:
            q = ob(pr(g, t_rotta, .3)); x = (xs[-3] + xs[-2]) / 2 + 30
            c.save(); c.translate(x, y - 40); c.scale(q, q); circ(c, 0, 0, 70, NAVY); circ(c, 0, 0, 70, STEEL, 1, 8)
            check(c, 0, 0, 70, WHT, False); c.restore()
    return _v(d, [t_rotta] if t_rotta else [])


def v_attenzione(t, t_giu):
    """Soglia dell'attenzione: un indicatore a lancetta che parte alto e crolla a t_giu."""
    cx, cy, r = 540, 1420, 380
    def d(c, g, acc):
        q = ob(pr(g, t, .35)); c.save(); c.translate(cx, cy); c.scale(q, q); c.translate(-cx, -cy)
        for k in range(30):
            a = math.radians(180 + k * 6.2); col = YEL if k > 18 else (GOLD if k > 9 else STEEL)
            line(c, cx + math.cos(a) * (r - 20), cy + math.sin(a) * (r - 20), cx + math.cos(a) * (r + 40), cy + math.sin(a) * (r + 40), col, 16, .9)
        v = .88 if g < t_giu else lerp(.88, .08, oe(pr(g, t_giu, .5))) + .02 * math.sin(g * 30) * (1 - pr(g, t_giu, .8))
        a = math.radians(180 + 180 * v)
        line(c, cx, cy, cx + math.cos(a) * (r - 60), cy + math.sin(a) * (r - 60), WHT, 22); circ(c, cx, cy, 44, acc)
        text(c, 'ATTENZIONE', cx, cy + 130, 64, WHT, 'bk', a=.9, maxw=600)
        c.restore()
    return _v(d, [t_giu])


def v_telefono(t, n=7):
    """Un telefono bombardato: notifiche di offerte uguali alla tua che piovono una dopo l'altra."""
    def d(c, g, acc):
        q = ob(pr(g, t, .35)); c.save(); c.translate(540, 1270); c.scale(q, q)
        c.drawRoundRect(skia.Rect.MakeXYWH(-250, -440, 500, 900), 70, 70, P(acc, .35, blur=34))
        rr(c, -250, -440, 500, 900, 70, 0x111A33); rr(c, -250, -440, 500, 900, 70, WHT, .85, 10); rr(c, -70, -415, 140, 26, 13, WHT, .4)
        c.restore()
        for i in range(n):
            t0 = t + .35 + i * .3
            if g < t0: continue
            p = oe(pr(g, t0, .28)); y = 880 + ((i % 6) * 135) + 60 * (1 - p); x = 540 + (1 - p) * 300 * (1 if i % 2 else -1)
            c.save(); c.translate(x, y); c.scale(p, p)
            rr(c, -230, -52, 460, 104, 26, WHT, .97); rr(c, -205, -30, 60, 60, 14, acc if i % 3 == 0 else (GOLD if i % 3 == 1 else BLUE))
            rr(c, -125, -26, 250 - (i % 3) * 40, 18, 9, NAVY, .75); rr(c, -125, 6, 180 - (i % 2) * 50, 14, 7, STEEL, .7)
            c.restore()
        k = int(max(0, g - t - .35) / .3) + 1
        if g > t + .35:
            circ(c, 760, 840, 50, acc); text(c, str(min(k, n * 3)), 760, 840, 54, NAVY, 'bk', shadow=False)
    return _v(d, [t + .35 + i * .3 for i in range(0, n, 3)])


def v_zona(t, n=9):
    """La tua zona: il tuo punto al centro e i pin dei concorrenti che si moltiplicano intorno."""
    random.seed(29); PT = []
    while len(PT) < n:
        a = random.uniform(0, 6.28); r = random.uniform(170, 430); PT.append((540 + math.cos(a) * r, 1270 + math.sin(a) * r * .8))
    def d(c, g, acc):
        pp = P(WHT, .5, 6); pp.setPathEffect(skia.DashPathEffect.Make([24, 18], g * 50)); c.drawOval(skia.Rect.MakeLTRB(60, 860, 1020, 1680), pp)
        circ(c, 540, 1270, 110, acc, .25, blur=24); circ(c, 540, 1270, 76, acc); text(c, 'TU', 540, 1270, 60, NAVY, 'bk', shadow=False)
        for i, (x, y) in enumerate(PT):
            t0 = t + i * .16
            if g < t0: continue
            q = ob(pr(g, t0, .25)); dy = -160 * (1 - q)
            pth = skia.Path(); pth.moveTo(x, y + dy); pth.cubicTo(x - 52, y - 58 + dy, x - 42, y - 122 + dy, x, y - 122 + dy); pth.cubicTo(x + 42, y - 122 + dy, x + 52, y - 58 + dy, x, y + dy)
            c.drawPath(pth, P(STEEL)); circ(c, x, y - 80 + dy, 16, NAVY)
    return _v(d, [t + i * .16 for i in range(0, n, 3)])


def v_agenda(t, t_vuota=None):
    """Agenda: le caselle si accendono e si spengono come un'onda, e da t_vuota restano vuote."""
    def d(c, g, acc):
        q = ob(pr(g, t, .35)); c.save(); c.translate(540, 1270); c.scale(q, q); c.translate(-540, -1270)
        rr(c, 110, 860, 860, 820, 46, 0x111A33); rr(c, 110, 860, 860, 820, 46, WHT, .8, 6); rr(c, 110, 860, 860, 130, 46, acc)
        for k in (300, 780): rr(c, k, 820, 26, 90, 13, WHT)
        text(c, 'AGENDA', 540, 925, 66, NAVY, 'bk', shadow=False)
        for r in range(4):
            for col in range(5):
                x = 160 + col * 158; y = 1030 + r * 152; ph = math.sin(g * 3.2 - col * .7 - r * .4)
                on = ph > .1 and not (t_vuota and g >= t_vuota)
                rr(c, x, y, 128, 118, 22, acc if on else 0x24305A, .95 if on else .9)
        c.restore()
    return _v(d, [t_vuota] if t_vuota else [])


def v_cerchia(t, t_grandi):
    """Il tuo circolo di clienti piccoli: monetine vicine a te, e fuori portata tre sacchi grandi
    che si accendono a t_grandi (gli amici con 100, 200, 500 mila che non ti arrivano)."""
    def d(c, g, acc):
        circ(c, 330, 1300, 260, WHT, .06); circ(c, 330, 1300, 260, WHT, .4, 5)
        for i in range(8):
            t0 = t + i * .07
            if g < t0: continue
            q = ob(pr(g, t0, .22)); a = i * .785 + g * .4; x = 330 + math.cos(a) * 170; y = 1300 + math.sin(a) * 170
            circ(c, x, y, 34 * q, GOLD); circ(c, x, y, 24 * q, 0x8C6A12, 1, 4)
        person(c, 330, 1310, 120, WHT)
        for i, lab in enumerate(['100', '200', '500']):
            t0 = t_grandi + i * .25
            if g < t0: continue
            q = ob(pr(g, t0, .3)); x = 820; y = 960 + i * 300
            c.save(); c.translate(x, y); c.scale(q, q)
            circ(c, 0, 0, 120, acc, .25, blur=24); rr(c, -110, -90, 220, 190, 70, acc); rr(c, -50, -125, 100, 50, 20, acc)
            text(c, lab + 'K', 0, 6, 70, NAVY, 'bk', shadow=False, maxw=190); c.restore()
            pp = P(STEEL, .7, 6); pp.setPathEffect(skia.DashPathEffect.Make([16, 14], 0)); c.drawLine(560, 1300, x - 130, y, pp)
            check(c, (560 + x - 130) / 2, (1300 + y) / 2, 44, STEEL, False)
    return _v(d, [t_grandi + i * .25 for i in range(3)])


def v_colpe(items):
    """Tre colpe esterne (crisi, governo, situazione esterna) che entrano e vengono sbarrate.
    items = [(tempo, 'TESTO'), ...]"""
    def d(c, g, acc):
        for i, (t0, txt) in enumerate(items[:3]):
            if g < t0: continue
            q = oe(pr(g, t0, .25)); y = 990 + i * 250; x = 540 + 500 * (1 - q)
            rr(c, x - 420, y - 85, 840, 170, 40, 0x1A2238, q); rr(c, x - 420, y - 85, 840, 170, 40, STEEL, .9 * q, 5)
            text(c, txt, x, y, 76, WHT, 'bk', a=q, maxw=740)
            if g >= t0 + .35:
                s = oe(pr(g, t0 + .35, .2)); line(c, x - 380, y + 10, x - 380 + 760 * s, y - 14, acc, 16)
    return _v(d, [i[0] for i in items])


def v_budget(t, t_tu):
    """Una volta servivano budget enormi da multinazionale; oggi bastano poche monete. Un
    grattacielo di banconote a sinistra, poche monete che brillano a destra da t_tu."""
    def d(c, g, acc):
        h = 760 * oe(pr(g, t, .6))
        c.drawRoundRect(skia.Rect.MakeLTRB(130, 1700 - h, 460, 1700), 18, 18, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, 1700 - h), (0, 1700)], [K_C(STEEL, .9), K_C(STEEL, .3)])))
        for k in range(int(h / 70)):
            for j in range(3): rr(c, 160 + j * 100, 1680 - k * 70 - 40, 60, 34, 6, WHT, .25)
        text(c, 'MULTINAZIONALE', 295, 1760, 46, STEEL, 'bk', maxw=380)
        if g >= t_tu:
            for i in range(4):
                q = ob(pr(g, t_tu + i * .1, .25)); y = 1640 - i * 46
                c.save(); c.translate(780, y); c.scale(q, q); circ(c, 0, 0, 120, acc, .18, blur=20) if i == 3 else None
                c.drawOval(skia.Rect.MakeLTRB(-110, -30, 110, 30), P(acc)); c.drawOval(skia.Rect.MakeLTRB(-110, -30, 110, 30), P(0x8C6A12, 1, 5)); c.restore()
            pop(c, g, t_tu + .3, 'TU', 780, 1440, 90, acc, 'bi')
            line(c, 120, 1712, 960, 1712, WHT, 6, .4)
    return _v(d, [t_tu])


def K_C(h, a=1.0):
    return skia.Color((h >> 16) & 255, (h >> 8) & 255, h & 255, int(255 * max(0, min(1, a))))


def v_imbuto(steps):
    """Il sistema: contatti che entrano dall'alto, diventano appuntamenti e poi chiusure.
    steps = [(tempo, 'CONTATTI'), (tempo, 'APPUNTAMENTI'), (tempo, 'CHIUSURE')]"""
    lv = [(1000, 1000), (1290, 800), (1560, 600)]
    random.seed(4); DOT = [(random.uniform(-1, 1), random.uniform(0, 1)) for _ in range(40)]
    def d(c, g, acc):
        for i, ((t0, lab), (y, w)) in enumerate(zip(steps, lv)):
            if g < t0: continue
            q = ob(pr(g, t0, .3), 1.2); col = [WHT, GOLD, acc][i]
            pth = skia.Path(); w2 = w * .78
            pth.moveTo(540 - w / 2 * q, y - 110); pth.lineTo(540 + w / 2 * q, y - 110); pth.lineTo(540 + w2 / 2 * q, y + 110); pth.lineTo(540 - w2 / 2 * q, y + 110); pth.close()
            c.drawPath(pth, P(col, .18)); c.drawPath(pth, P(col, .9, 6))
            text(c, lab, 540, y, 66, col, 'bk', a=q, maxw=w2 - 70)
        if g >= steps[0][0]:
            for k, (u, ph) in enumerate(DOT):
                f = ((g - steps[0][0]) * .55 + ph) % 1; y = 860 + f * 860
                lim = 1 if g >= steps[-1][0] else (.66 if g >= steps[1][0] else .33)
                if f > lim or (f > .33 and k % 2) or (f > .66 and k % 3): continue
                w = 820 - 440 * f; circ(c, 540 + u * w * .42, y, 9, acc if f > .6 else WHT, .9)
    return _v(d, [s[0] for s in steps])


def v_tappe(steps):
    """Linea del tempo con le tappe dette da Francesco: steps = [(tempo, '24 ORE', 'prime richieste'), ...]"""
    def d(c, g, acc):
        x0, x1, y = 120, 960, 1300
        p = oe(pr(g, steps[0][0] - .2, max(.4, steps[-1][0] - steps[0][0] + .4)))
        line(c, x0, y, x1, y, WHT, 10, .2); line(c, x0, y, x0 + (x1 - x0) * p, y, acc, 12)
        for i, (t0, big, small) in enumerate(steps):
            x = x0 + (x1 - x0) * (i + .5) / len(steps)
            if g < t0: circ(c, x, y, 22, WHT, .3); continue
            q = ob(pr(g, t0, .3)); circ(c, x, y, 60 * q, acc, .3, blur=14); circ(c, x, y, 34 * q, acc)
            up = i % 2 == 0; yy = y - 190 if up else y + 190
            text(c, big, x, yy, 100, WHT, 'bk', sc=q, maxw=330); text(c, small, x, yy + 80, 50, acc, 'b', a=q, maxw=330, shadow=False)
    return _v(d, [s[0] for s in steps])


def v_provincia(t, t_lucchetto):
    """Esclusiva provinciale: la sagoma di una provincia, un solo pin dentro e il lucchetto che
    si chiude a t_lucchetto."""
    pts = [(300, 900), (520, 860), (760, 930), (880, 1110), (830, 1330), (900, 1520), (700, 1690), (470, 1650), (290, 1520), (220, 1300), (250, 1100)]
    def d(c, g, acc):
        p = oe(pr(g, t, .7)); pth = skia.Path(); pth.moveTo(*pts[0])
        for q_ in pts[1:]: pth.lineTo(*q_)
        pth.close(); pp = P(acc, 1, 10); pp.setPathEffect(skia.TrimPathEffect.Make(0, max(.001, min(.999, p)))); c.drawPath(pth, P(acc, .1 * p)); c.drawPath(pth, pp)
        if g >= t + .4:
            q = ob(pr(g, t + .4, .3)); x, y = 540, 1270
            c.save(); c.translate(x, y); c.scale(q, q)
            pin = skia.Path(); pin.moveTo(0, 0); pin.cubicTo(-80, -90, -64, -190, 0, -190); pin.cubicTo(64, -190, 80, -90, 0, 0); c.drawPath(pin, P(WHT)); circ(c, 0, -125, 26, NAVY); c.restore()
        if g >= t_lucchetto:
            q = ob(pr(g, t_lucchetto, .3)); s = oe(pr(g, t_lucchetto + .2, .2))
            c.save(); c.translate(800, 1560); c.scale(q, q)
            arc(c, 0, -60 + 26 * s, 52, 180, 180, WHT, 18); rr(c, -80, -60, 160, 130, 24, acc); circ(c, 0, 0, 16, NAVY); c.restore()
    return _v(d, [t_lucchetto])


def v_prenota(t, t_click, label='PRENOTA LA CALL', url='aieliteadvisory.it'):
    """Finestra del browser sul sito con il pulsante: il cursore arriva e clicca a t_click."""
    def d(c, g, acc):
        q = oe(pr(g, t, .35)); c.save(); c.translate(0, 600 * (1 - q))
        c.drawRoundRect(skia.Rect.MakeXYWH(80, 880, 920, 760), 40, 40, P(acc, .35, blur=30)); rr(c, 80, 880, 920, 760, 40, 0xF4F6FB)
        rr(c, 80, 880, 920, 96, 40, 0xDCE1EC); rr(c, 80, 940, 920, 36, 0, 0xDCE1EC)
        for i in range(3): circ(c, 130 + i * 40, 928, 12, [STEEL, GOLD, acc][i])
        rr(c, 270, 904, 660, 50, 25, WHT); text(c, url, 300, 929, 32, NAVY, 'm', align=0, shadow=False, maxw=600)
        rr(c, 160, 1030, 540, 40, 20, NAVY, .85); rr(c, 160, 1100, 700, 26, 13, STEEL, .5); rr(c, 160, 1146, 620, 26, 13, STEEL, .5)
        b = 1 + .08 * (1 - pr(g, t_click, .25)) if g >= t_click else 1 + .02 * math.sin(g * 6)
        c.save(); c.translate(540, 1380); c.scale(b, b)
        if g >= t_click: circ(c, 0, 0, 260 * oe(pr(g, t_click, .5)), acc, .4 * (1 - pr(g, t_click, .5)), 10)
        rr(c, -330, -75, 660, 150, 75, acc); text(c, label, 0, 0, 56, NAVY, 'bk', shadow=False, maxw=600); c.restore()
        mx = lerp(900, 600, oe(pr(g, t + .3, max(.3, t_click - t - .3)))); my = lerp(1600, 1410, oe(pr(g, t + .3, max(.3, t_click - t - .3))))
        cur = skia.Path(); cur.moveTo(0, 0); cur.lineTo(0, 70); cur.lineTo(18, 54); cur.lineTo(32, 86); cur.lineTo(44, 80); cur.lineTo(30, 50); cur.lineTo(54, 50); cur.close()
        c.save(); c.translate(mx, my); c.drawPath(cur, P(NAVY)); c.drawPath(cur, P(WHT, 1, 4)); c.restore()
        c.restore()
    return _v(d, [t_click])
