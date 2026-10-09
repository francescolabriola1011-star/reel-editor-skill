"""Visual NUOVI scritti per il reel 3265 (8/10/2026), "la paura di investire in marketing".

Regola di Francesco dell'8/10 (correzione 410): ogni video ha grafiche fatte apposta per le
sue frasi. Nessuno di questi esiste in mgkit ne' in vis_3263.py.
Zona utile y 800-1800, centro 540,1200. Tempi assoluti sulla timeline di base.mp4.
"""
import math, random, skia
from mgkit import *
from mgkit import _v


def _coin(c, x, y, r, a=1, sym='€'):
    c.drawCircle(x, y, r, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear(
        [(x - r, y - r), (x + r, y + r)], [C(0xFFE27A, a), C(0xC8920A, a)])))
    circ(c, x, y, r * .78, 0x8A6300, .7 * a, max(2, r * .08))
    if sym: text(c, sym, x, y, r * 1.05, 0x6B4A00, 'bk', a=a, shadow=False)


def v_palla_piede(t, t_tira=None):
    """'La paura ... ti tiene fermo': una persona sulla linea di partenza con una palla al
    piede; la freccia verso il nuovo sistema prova ad allungarsi e torna indietro."""
    def d(c, g, acc):
        if g < t - .05: return
        q = ob(pr(g, t, .35)); gy = 1600
        line(c, 90, gy, 990, gy, 0x5F6B8A, 6, .8 * q)
        tr = math.sin(g * 46) * 5 * cl(g - t - .4)                          # trema
        px, py, ps = 360 + tr, 1330, 300 * q
        person(c, px, py, ps, WHT)
        fx, fy = 380, py + 150
        bx, by0 = 700, 1505
        bq = oe(pr(g, t + .3, .3)) if g >= t + .3 else 0
        by = lerp(900, by0, bq)
        for i in range(7):                                                   # catena a maglie
            ti = t + .45 + i * .05
            if g < ti: continue
            k = (i + .5) / 7; x = lerp(fx, bx - 90, k); y = lerp(fy, by + 20, k) + 26 * math.sin(k * math.pi)
            c.save(); c.translate(x, y); c.rotate(90 * (i % 2) + 20)
            c.drawRoundRect(skia.Rect.MakeXYWH(-26, -16, 52, 32), 16, 16, P(0xB8C0D8, .95, 9)); c.restore()
        if bq:
            c.drawCircle(bx, by, 112, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((bx - 35, by - 40), 150, [C(0x4A5272), C(0x10131F)])))
            text(c, '€', bx, by, 120, acc, 'bk', a=bq, shadow=False)
        ta = t_tira if t_tira else t + .8
        if g >= ta:                                                          # freccia che tira e torna
            k = (g - ta) % 1.1; e = oe(cl(k / .45)) if k < .45 else 1 - oc(cl((k - .45) / .5))
            x2 = lerp(520, 960, e)
            pp = P(GRN, .9, 16); pp.setPathEffect(skia.DashPathEffect.Make([34, 20], -g * 200))
            c.drawLine(520, 1020, x2, 1020, pp); tri(c, x2 + 10, 1020, 0, 34, GRN)
    return _v(d, [t + .55])


def v_tapis(t, t_reset=None):
    """'Rimanere come sei oggi': una persona che cammina su un tapis roulant, il nastro corre
    e la barra di avanzamento sopra si riempie e torna a zero, sempre uguale."""
    def d(c, g, acc):
        q = oe(pr(g, t, .35)); y0 = 1560
        c.save(); c.translate(0, 220 * (1 - q))
        rr(c, 150, y0, 780, 60, 30, 0x2A3566)
        pp = P(0x8A93B8, .9, 8); pp.setPathEffect(skia.DashPathEffect.Make([40, 30], g * 260))
        c.drawLine(190, y0 + 30, 890, y0 + 30, pp)
        for x in (180, 900):
            circ(c, x, y0 + 30, 44, 0x16204A); circ(c, x, y0 + 30, 44, 0x8A93B8, 1, 6)
            a = math.radians(g * 400)
            line(c, x - math.cos(a) * 36, y0 + 30 - math.sin(a) * 36, x + math.cos(a) * 36, y0 + 30 + math.sin(a) * 36, 0x8A93B8, 6)
        line(c, 820, y0, 760, 1230, 0x5F6B8A, 14); rr(c, 700, 1200, 170, 40, 20, 0x5F6B8A)
        bob = abs(math.sin(g * 7)) * 18
        person(c, 470, 1300 - bob, 300, WHT)
        for k in range(2):                                                   # gambe che pedalano sul nastro
            ph = g * 7 + k * math.pi; lx = 470 + math.sin(ph) * 60
            line(c, 470, 1440 - bob, lx, y0 - 8, WHT, 30)
        c.restore()
        rr(c, 140, 930, 800, 56, 28, 0x16204A); rr(c, 140, 930, 800, 56, 28, 0x8A93B8, .5, 4)
        if g >= t + .2:
            k = ((g - t - .2) % 1.3) / 1.3
            rr(c, 140, 930, max(56, 800 * oc(k)), 56, 28, acc, .9)
            if k > .85: arc(c, 990, 958, 30, 30, 290, acc, 8, a=(k - .85) * 6.6); tri(c, 1010, 935, 120, 14, acc, (k - .85) * 6.6)
    return _v(d)


def v_passaparola(t, n=4):
    """'Passaparola, referenze': una fila di persone, una bolla di parola salta dall'una
    all'altra e chi la riceve si accende."""
    def d(c, g, acc):
        xs = [170 + i * (740 / (n - 1)) for i in range(n)]; y = 1420
        hop = .38
        k = (g - t - .25) / hop
        for i, x in enumerate(xs):
            ti = t + i * .07; qi = ob(pr(g, ti, .3)) if g >= ti else 0
            on = k >= i - .05
            col = acc if on else 0x5F6B8A
            circ(c, x, y - 30, 120 * qi, col, .16 if on else .06)
            person(c, x, y, 190 * qi, col)
        if g >= t + .25:
            ki = int(cl(k, 0, n - 1.001)); f = cl(k - ki) if k < n - 1 else 1
            x0, x1 = xs[ki], xs[min(ki + 1, n - 1)]
            bx = lerp(x0, x1, oc(f)); by = 1110 - math.sin(f * math.pi) * 140
            c.save(); c.translate(bx, by); s = 1 + .08 * math.sin(g * 12)
            c.scale(s, s)
            rr(c, -95, -62, 190, 110, 44, WHT); tri(c, -30, 60, 90, 26, WHT)
            for j in range(3): circ(c, -42 + j * 42, -8, 12, NAVY, .4 + .6 * ((g * 3 + j * .3) % 1))
            c.restore()
            for i in range(min(ki + 1, n - 1)):                              # scie della parola passata
                pp = P(acc, .55, 6); pp.setPathEffect(skia.DashPathEffect.Make([14, 14], -g * 90))
                pth = skia.Path(); pth.moveTo(xs[i], 1210); pth.quadTo((xs[i] + xs[i + 1]) / 2, 1040, xs[i + 1], 1210)
                c.drawPath(pth, pp)
    return _v(d)


def v_montagne(t, t_alti, t_bassi):
    """'Ogni mese ci sono i alti e ci sono i bassi': un vagoncino sulle montagne russe che
    scorre, salite verdi e discese rosse; sugli alti e sui bassi detti spunta la freccia."""
    def ty(x, g):
        u = x * .0085 + (g - t) * 2.4
        return 1290 - 260 * math.sin(u) - 70 * math.sin(u * 2.3 + 1)
    def d(c, g, acc):
        q = oe(pr(g, t, .4))
        prev = None
        for x in range(60, 1021, 12):
            y = ty(x, g); y = lerp(1800, y, q)
            if prev:
                col = GRN if y < prev[1] else RED
                line(c, prev[0], prev[1], x, y, col, 14)
                if x % 48 == 0: line(c, x, y + 10, x, 1800, 0x3A4366, 5, .6)
            prev = (x, y)
        cx = 540; cy = lerp(1800, ty(cx, g), q); slope = (ty(cx + 8, g) - ty(cx - 8, g)) / 16
        c.save(); c.translate(cx, cy); c.rotate(math.degrees(math.atan(slope)))
        rr(c, -80, -110, 160, 90, 22, YEL); circ(c, -48, -12, 22, WHT); circ(c, 48, -12, 22, WHT)
        person(c, 0, -150, 90, WHT); c.restore()
        if g >= t_alti:
            p = ob(pr(g, t_alti, .3)); tri(c, 200, 930, -90, 70 * p, GRN)
        if g >= t_bassi:
            p = ob(pr(g, t_bassi, .3)); tri(c, 880, 1720, 90, 70 * p, RED)
    return _v(d, [t_alti, t_bassi])


def v_telefono_freddo(t, t_meno):
    """'Chiamate a freddo ... funzionano sempre meno': una cornetta coperta di brina, le onde
    di squillo si fanno deboli e le tacche del segnale cadono una alla volta."""
    random.seed(11); FR = [(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(14, 34)) for _ in range(16)]
    def d(c, g, acc):
        q = ob(pr(g, t, .35)) if g >= t else 0; cx, cy = 450, 1300
        dec = cl((g - t_meno) / 1.4) if g >= t_meno else 0
        for k in range(3):
            w = ((g - t) * 1.2 + k / 3) % 1
            arc(c, cx, cy, 180 + 220 * w, -60, 120, 0xBFE6FF, 10, (1 - w) * .8 * (1 - .8 * dec))
        c.save(); c.translate(cx, cy); c.rotate(-30 + 6 * math.sin(g * 30) * (1 - dec)); c.scale(q, q)
        pth = skia.Path(); pth.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-60, -230, 60, 230), 50, 50))
        c.drawPath(pth, P(0x0E2A4A)); c.drawPath(pth, P(0xBFE6FF, .9, 10))
        rr(c, -110, -290, 220, 110, 50, 0xBFE6FF); rr(c, -110, 180, 220, 110, 50, 0xBFE6FF)
        for (fx, fy, s) in FR:                                               # cristalli di brina
            x, y = fx * 90, fy * 240; a = .3 + .5 * cl((g - t) * 1.5)
            for k in range(3):
                an = math.radians(k * 60 + g * 20)
                line(c, x - math.cos(an) * s, y - math.sin(an) * s, x + math.cos(an) * s, y + math.sin(an) * s, WHT, 3, a)
        c.restore()
        for i in range(4):                                                   # tacche del segnale
            x = 760 + i * 62; h = 70 + i * 55; yb = 1520
            off = t_meno + (3 - i) * .32
            fall = oe(pr(g, off, .3)) if g >= off else 0
            col = GRN if fall == 0 else RED
            rr(c, x, yb - h + 260 * fall * fall, 44, h, 10, col, (1 - fall) * .95 + .05)
    return _v(d, [t_meno])


def v_scatola_nera(t, t_q):
    """'Non conoscere come funzionano i numeri': simboli di soldi e percentuali entrano in
    una scatola nera e dalla scatola escono solo punti interrogativi."""
    random.seed(21); S = [random.choice(['€', '%', '€', '%']) for _ in range(10)]
    def d(c, g, acc):
        q = ob(pr(g, t, .35)) if g >= t else 0; cx, cy = 540, 1330
        c.save(); c.translate(cx, cy); c.scale(q, q); c.rotate(2 * math.sin(g * 3))
        top = skia.Path(); top.moveTo(-250, -150); top.lineTo(0, -270); top.lineTo(250, -150); top.lineTo(0, -30); top.close()
        lft = skia.Path(); lft.moveTo(-250, -150); lft.lineTo(0, -30); lft.lineTo(0, 260); lft.lineTo(-250, 140); lft.close()
        rgt = skia.Path(); rgt.moveTo(250, -150); rgt.lineTo(0, -30); rgt.lineTo(0, 260); rgt.lineTo(250, 140); rgt.close()
        c.drawPath(top, P(0x2A2F45)); c.drawPath(lft, P(0x14172A)); c.drawPath(rgt, P(0x0B0D18))
        for p_ in (top, lft, rgt): c.drawPath(p_, P(acc, .55, 4))
        c.restore()
        for i, s in enumerate(S):                                            # simboli che entrano
            ti = t + .2 + i * .17; k = pr(g, ti, .55)
            if g < ti or k >= 1: continue
            side = -1 if i % 2 else 1
            x = lerp(cx + side * 470, cx, oc(k)); y = lerp(900 + (i % 3) * 60, cy - 160, oc(k))
            text(c, s, x, y, 90 * (1 - .6 * k), WHT, 'bk', a=1 - k * k)
        if g >= t_q:
            for k in range(5):
                tk = t_q + k * .12
                if g < tk: continue
                w = ((g - tk) * .7) % 1
                x = cx + math.sin(k * 2.1 + g) * 300; y = cy - 160 - w * 260
                text(c, '?', x, y, 110 + 30 * (k % 2), acc, 'bi', a=(1 - w), glow=acc)
            pop(c, g, t_q, '?', cx, cy + 80, 220, WHT, 'bk')
    return _v(d, [t_q])


def v_imballato(t, n=5):
    """'Ti tiene immobilizzato': una persona che viene avvolta da fasce di nastro una dopo
    l'altra e si dimena senza riuscire a muoversi."""
    def d(c, g, acc):
        q = ob(pr(g, t - .3, .3)) if g >= t - .3 else 0
        wig = math.sin(g * 28) * 7 * cl(g - t)
        c.save(); c.translate(540 + wig, 0); c.rotate(math.sin(g * 19) * 1.5)
        person(c, 0, 1300, 420 * q, 0x8A93B8)
        for i in range(n):
            ti = t + i * .13
            if g < ti: continue
            k = oe(pr(g, ti, .22)); y = 1060 + i * 120; ang = -10 if i % 2 else 10
            c.save(); c.translate(0, y); c.rotate(ang)
            rr(c, -260 * k, -32, 520 * k, 64, 10, acc, .92)
            for j in range(-3, 4): line(c, j * 70 * k, -32, j * 70 * k + 26, 32, WHT, 4, .35)
            c.restore()
        c.restore()
    return _v(d, [t + (n - 1) * .13])


def v_dosatore(t, t_out, n=5):
    """'Sai esattamente quanto investi per acquisire un cliente': monete che cadono una alla
    volta nella macchina, la lancetta segna la dose e dal fondo esce un cliente."""
    def d(c, g, acc):
        q = oe(pr(g, t, .35)); c.save(); c.translate(0, 300 * (1 - q))
        rr(c, 260, 1060, 560, 470, 50, 0x16204A); rr(c, 260, 1060, 560, 470, 50, acc, .9, 6)
        rr(c, 470, 1040, 140, 26, 13, 0x0A0F24)
        cx, cy = 540, 1290                                                   # quadrante
        arc(c, cx, cy, 150, 200, 140, 0x2A3566, 26)
        k = sum(1 for i in range(n) if g >= t + .25 + i * .22) / n
        arc(c, cx, cy, 150, 200, 140 * k, GRN, 26)
        ang = math.radians(200 + 140 * k + 2 * math.sin(g * 20))
        line(c, cx, cy, cx + math.cos(ang) * 130, cy + math.sin(ang) * 130, WHT, 10); circ(c, cx, cy, 18, WHT)
        rr(c, 470, 1500, 140, 40, 12, 0x0A0F24)
        c.restore()
        for i in range(n):
            ti = t + .1 + i * .22; k2 = pr(g, ti, .2)
            if g < ti or k2 >= 1: continue
            _coin(c, 540, lerp(820, 1050, k2 * k2), 50)
        if g >= t_out:
            p = ob(pr(g, t_out, .35)); y = lerp(1500, 1690, oe(pr(g, t_out, .35)))
            circ(c, 540, y, 95 * p, YEL, .25, blur=18); person(c, 540, y + 10, 130 * p, YEL)
            b = ob(pr(g, t_out + .25, .25)) if g > t_out + .25 else 0
            circ(c, 640, y - 70, 34 * b, GRN); check(c, 640, y - 70, 30 * b, NAVY)
    return _v(d, [t_out])


def v_ciclo_vita(t, dur=2.2, n=8):
    """'Quanto questo cliente ti rende nel suo ciclo di vita': un anello di tempo si chiude
    attorno al cliente e lungo il giro cadono monete che si impilano accanto."""
    def d(c, g, acc):
        cx, cy, R = 540, 1260, 300; k = oc(pr(g, t, dur))
        q = ob(pr(g, t - .2, .3)) if g >= t - .2 else 0
        circ(c, cx, cy, 130 * q, acc, .18, blur=16); person(c, cx, cy + 30, 190 * q, WHT)
        c.save(); c.translate(cx, cy); c.rotate(max(0, g - t - dur) * 40); c.translate(-cx, -cy)
        arc(c, cx, cy, R, -90, 360, 0x2A3566, 18)
        arc(c, cx, cy, R, -90, 360 * k, acc, 18)
        a = math.radians(-90 + 360 * k); circ(c, cx + math.cos(a) * R, cy + math.sin(a) * R, 26, WHT)
        for i in range(n):
            ki = (i + 1) / n
            if k < ki: continue
            ti = t + dur * (1 - (1 - ki) ** (1 / 3)) if ki < 1 else t + dur
            p = ob(pr(g, ti, .25))
            a = math.radians(-90 + 360 * ki)
            _coin(c, cx + math.cos(a) * R, cy + math.sin(a) * R, 40 * p * (1 + .08 * math.sin(g * 8 + i)))
        c.restore()
        for i in range(n):
            ki = (i + 1) / n
            if k < ki: continue
            ti = t + dur * (1 - (1 - ki) ** (1 / 3)) if ki < 1 else t + dur
            pp = oe(pr(g, ti + .1, .3))
            _coin(c, 900, lerp(1720, 1720 - i * 34, pp), 52, a=pp, sym='')
    return _v(d)


def v_provetta(t, t_full):
    """'Il metodo scientifico': una beuta da laboratorio su una griglia millimetrata che si
    riempie di liquido verde con bolle, mentre la curva sul foglio si disegna precisa."""
    def d(c, g, acc):
        q = ob(pr(g, t, .35)) if g >= t else 0
        for i in range(9):                                                   # carta millimetrata
            line(c, 120 + i * 105, 860, 120 + i * 105, 1760, acc, 2, .18 * q)
        for j in range(9):
            line(c, 120, 860 + j * 112, 960, 860 + j * 112, acc, 2, .18 * q)
        c.save(); c.translate(540, 1330); c.scale(q, q)
        fl = skia.Path(); fl.moveTo(-70, -330); fl.lineTo(-70, -120); fl.lineTo(-280, 300); fl.quadTo(-300, 360, -230, 360)
        fl.lineTo(230, 360); fl.quadTo(300, 360, 280, 300); fl.lineTo(70, -120); fl.lineTo(70, -330); fl.close()
        lv = oc(pr(g, t + .2, t_full - t - .2)) if g >= t + .2 else 0
        c.save(); c.clipPath(fl, skia.ClipOp.kIntersect, True)
        yl = lerp(360, -60, lv) + 10 * math.sin(g * 6)
        c.drawRect(skia.Rect.MakeLTRB(-320, yl, 320, 380), P(GRN, .85))
        for b in range(9):
            w = ((g * .9 + b * .13) % 1); bx = -180 + b * 45 + 14 * math.sin(g * 4 + b)
            by = lerp(340, yl, w)
            if by > yl: circ(c, bx, by, 9 + b % 3 * 4, WHT, .55)
        c.restore()
        c.drawPath(fl, P(WHT, .95, 10)); rr(c, -95, -360, 190, 34, 14, WHT)
        for m in range(4): line(c, -200 + m * 20, 240 - m * 110, -150 + m * 20, 240 - m * 110, WHT, 5, .7)
        c.restore()
        if g >= t_full:
            p = ob(pr(g, t_full, .3)); circ(c, 860, 960, 70 * p, GRN); check(c, 860, 960, 64 * p, NAVY)
    return _v(d, [t_full])


def v_moltiplica(t, step=.28, levels=5):
    """'E scalabile': una tessera cliente si duplica a ogni battito, 1, 2, 4, 8, 16, e la
    griglia si riempie (nessuna cifra a schermo, solo le tessere)."""
    def d(c, g, acc):
        lv = 0
        for i in range(levels):
            if g >= t + i * step: lv = i
        n = 2 ** lv; cols = {1: 1, 2: 2, 4: 2, 8: 4, 16: 4}[n]; rows = n // cols
        size = min(760 / cols, 860 / rows) * .82
        for i in range(n):
            r, col = divmod(i, cols)
            x = 540 + (col - (cols - 1) / 2) * size / .82; y = 1300 + (r - (rows - 1) / 2) * size / .82
            born = t + lv * step if i >= n // 2 and lv > 0 else t
            p = ob(pr(g, born, .22)) if g >= born else 0
            c.save(); c.translate(x, y); c.scale(p, p); c.rotate(3 * math.sin(g * 4 + i))
            rr(c, -size / 2, -size / 2, size, size, size * .18, 0x16204A); rr(c, -size / 2, -size / 2, size, size, size * .18, acc, .9, max(3, size * .03))
            person(c, 0, size * .05, size * .55, WHT if i < n // 2 or lv == 0 else acc)
            c.restore()
    return _v(d, [t + i * step for i in range(1, levels)])


def v_app_simulatore(t, t_fill):
    """'Un simulatore che ti mostra quanti clienti puoi ottenere': uno smartphone con una
    manopola che gira e una griglia di clienti che si accendono uno dopo l'altro."""
    def d(c, g, acc):
        q = oe(pr(g, t, .4)); c.save(); c.translate(0, 600 * (1 - q))
        c.drawRoundRect(skia.Rect.MakeXYWH(250, 820, 580, 960), 70, 70, P(acc, .45, blur=30))
        rr(c, 250, 820, 580, 960, 70, 0x0A0F24); rr(c, 250, 820, 580, 960, 70, WHT, .9, 8)
        rr(c, 470, 850, 140, 24, 12, 0x2A3566)
        cx, cy = 540, 1060; rot = 160 * oc(pr(g, t + .3, 1.6)) + 6 * math.sin(g * 5)
        circ(c, cx, cy, 120, 0x16204A); arc(c, cx, cy, 120, 135, 270, 0x2A3566, 20)
        arc(c, cx, cy, 120, 135, 270 * oc(pr(g, t + .3, 1.6)), acc, 20)
        a = math.radians(135 + 270 * oc(pr(g, t + .3, 1.6))); circ(c, cx + math.cos(a) * 120, cy + math.sin(a) * 120, 24, WHT)
        c.save(); c.translate(cx, cy); c.rotate(rot); line(c, 0, 0, 0, -80, WHT, 12); c.restore(); circ(c, cx, cy, 20, WHT)
        for i in range(20):
            x = 320 + (i % 5) * 110; y = 1290 + (i // 5) * 115; ti = t_fill + i * .05
            on = g >= ti; p = ob(pr(g, ti, .2)) if on else 1
            person(c, x, y, 78 * (p if on else 1), GRN if on else 0x2A3566)
        c.restore()
    return _v(d, [t_fill])


def v_dm(keyword, t_type, t_send, t_lock=None):
    """'Commenta con la parola ... e te lo mando in privato': il commento con la parola si
    scrive sotto un post, poi la busta vola nella casella dei messaggi privati che si chiude
    col lucchetto."""
    def d(c, g, acc):
        q = oe(pr(g, t_type - .4, .35)); c.save(); c.translate(0, 240 * (1 - q))
        rr(c, 70, 830, 940, 170, 85, WHT)
        circ(c, 160, 915, 52, 0xD5DBF0); person(c, 160, 920, 48, GREY)
        n = int(len(keyword) * pr(g, t_type, .55) + .001); f = font('bk', 78)
        if f.measureText(keyword) > 660: f = font('bk', 78 * 660 / f.measureText(keyword))
        c.drawString(keyword[:n], 240, 943, f, P(NAVY))
        if n < len(keyword) and int(g * 4) % 2 == 0: rr(c, 246 + f.measureText(keyword[:n]), 875, 7, 80, 3, acc)
        c.restore()
        ix, iy = 540, 1430                                                   # casella privata
        bq = ob(pr(g, t_send - .2, .3)) if g >= t_send - .2 else 0
        c.save(); c.translate(ix, iy); c.scale(bq, bq)
        rr(c, -230, -150, 460, 300, 40, 0x16204A); rr(c, -230, -150, 460, 300, 40, acc, .9, 7)
        pth = skia.Path(); pth.moveTo(-200, -120); pth.lineTo(0, 30); pth.lineTo(200, -120)
        c.drawPath(pth, P(acc, .9, 7)); c.restore()
        if g >= t_send:                                                      # busta che vola
            k = oc(pr(g, t_send, .55))
            ex, ey = lerp(860, ix, k), lerp(915, iy, k) - math.sin(k * math.pi) * 200
            s = lerp(1, .5, k)
            if k < 1:
                c.save(); c.translate(ex, ey); c.rotate(-20 * (1 - k)); c.scale(s, s)
                rr(c, -90, -60, 180, 120, 14, YEL); pe = skia.Path(); pe.moveTo(-90, -60); pe.lineTo(0, 10); pe.lineTo(90, -60)
                c.drawPath(pe, P(NAVY, .8, 6)); c.restore()
        tl = t_lock if t_lock else t_send + .6
        if g >= tl:
            p = ob(pr(g, tl, .3)); lx, ly = ix + 210, iy - 140
            c.save(); c.translate(lx, ly); c.scale(p, p)
            arc(c, 0, -30, 40, 180, 180, GRN, 14); rr(c, -55, -30, 110, 90, 18, GRN); circ(c, 0, 15, 12, NAVY)
            c.restore()
        for k in range(3):                                                   # frecce verso il basso
            y = 1680 + k * 50 + 16 * math.sin(g * 11 - k * .7); pth = skia.Path(); pth.moveTo(490, y - 20); pth.lineTo(540, y + 20); pth.lineTo(590, y - 20)
            c.drawPath(pth, P(YEL, .4 + .3 * k, 18))
    return _v(d, [t_send])
