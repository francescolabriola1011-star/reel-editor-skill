"""Visual NUOVI scritti per il reel 3267 (8/10/2026). Regola 410: ogni video le sue grafiche.
Il tema e' vicino al 3266 (rompere le scatole, passaparola, fiducia, agenda): per questo
nessuna immagine qui ripete vis_3266, vis_3265 o vis_3263.
Zona utile y 800-1800, centro 540,1200. Tempi assoluti sulla timeline di base.mp4."""
import math, random, skia
from mgkit import *
from mgkit import _v


def v_messaggi(ts):
    """'Rompere le scatole ad amici e parenti': messaggi mandati uno dopo l'altro, tutti
    visualizzati e nessuna risposta. ts = tempi di invio (3-4)."""
    def d(c, g, acc):
        for i, t0 in enumerate(ts[:4]):
            if g < t0: continue
            q = ob(pr(g, t0, .25)); y = 900 + i * 215; w = [620, 520, 680, 460][i]
            c.save(); c.translate(980, y + 75); c.scale(q, q); c.translate(-980, -(y + 75))
            rr(c, 980 - w, y, w, 150, 60, 0x1E90FF); rr(c, 980 - w + 50, y + 48, w - 190, 22, 11, WHT, .85); rr(c, 980 - w + 50, y + 88, (w - 190) * .6, 18, 9, WHT, .6)
            c.restore()
            if g >= t0 + .35:                                    # doppia spunta: visto, niente risposta
                a = cl((g - t0 - .35) * 5)
                check(c, 905, y + 180, 26, 0x8A93B8, True, a); check(c, 935, y + 180, 26, 0x8A93B8, True, a)
                text(c, 'visualizzato', 870, y + 180, 34, 0x8A93B8, 'm', a=a, align=1, shadow=False)
    return _v(d, list(ts))


def v_batteria(t, dur=1.6):
    """'Il passaparola funziona sempre meno': una batteria che si scarica, da verde a rossa,
    e a fine corsa lampeggia."""
    def d(c, g, acc):
        p = ob(pr(g, t, .35)) if g >= t else 0; k = 1 - .85 * oc(pr(g, t + .3, dur)); cx, cy = 540, 1280
        col = GRN if k > .55 else (YEL if k > .3 else RED)
        c.save(); c.translate(cx, cy); c.scale(p, p)
        rr(c, -330, -170, 620, 340, 50, 0x121A3F); rr(c, -330, -170, 620, 340, 50, WHT, .9, 12); rr(c, 300, -70, 50, 140, 20, WHT, .9)
        blink = 1 if k > .2 else .5 + .5 * math.sin(g * 18)
        rr(c, -300, -140, 560 * k, 280, 30, col, blink)
        c.restore()
        for i in range(4):
            a = cl(1 - k - i * .2) ; line(c, 250 + i * 190, 1620, 250 + i * 190 + 70, 1700 + 30 * a, RED, 14, a)
    return _v(d, [t + .3 + dur])


def v_facce(t, n=3):
    """'Contattare persone che non vorresti contattare': tre facce che entrano e fanno la
    smorfia, bocca all'ingiu' e sopracciglio."""
    def d(c, g, acc):
        for i in range(n):
            t0 = t + i * .22
            if g < t0: continue
            q = ob(pr(g, t0, .3)); x = 210 + i * 330; y = 1300 + 30 * math.sin(g * 3 + i)
            c.save(); c.translate(x, y); c.scale(q, q); c.rotate(6 * math.sin(g * 2 + i))
            circ(c, 0, 0, 140, 0xFFD23F); circ(c, 0, 0, 140, 0xB8860B, 1, 8)
            circ(c, -48, -30, 16, NAVY); circ(c, 48, -30, 16, NAVY)
            line(c, -80, -75, -25, -60, NAVY, 10); line(c, 80, -75, 25, -60, NAVY, 10)
            arc(c, 0, 95, 55, 200, 140, NAVY, 12)
            c.restore()
    return _v(d)


def v_caricamento(t):
    """'Il personal branding e' lento, funziona poco': una barra di caricamento che avanza a
    fatica e si impunta, con la clessidra che gira."""
    def d(c, g, acc):
        p = oe(pr(g, t, .3)); k = .06 + .16 * oc(pr(g, t + .2, 2.4)) + .008 * math.sin(g * 9)
        rr(c, 110, 1380, 860 * p, 90, 45, 0x121A3F); rr(c, 110, 1380, 860 * p, 90, 45, WHT, .7, 6)
        rr(c, 122, 1392, 836 * k * p, 66, 33, acc)
        for i in range(3): circ(c, 470 + i * 70, 1560, 16, WHT, .3 + .7 * abs(math.sin(g * 4 - i * .7)))
        c.save(); c.translate(540, 1080); c.rotate((g - t) * 180 % 180 if int((g - t) * 1.0) % 2 else 0)
        pth = skia.Path(); pth.moveTo(-90, -130); pth.lineTo(90, -130); pth.lineTo(12, 0); pth.lineTo(90, 130); pth.lineTo(-90, 130); pth.lineTo(-12, 0); pth.close()
        c.drawPath(pth, P(WHT, .15)); c.drawPath(pth, P(WHT, .9, 10)); rr(c, -110, -150, 220, 24, 12, WHT); rr(c, -110, 126, 220, 24, 12, WHT)
        tri(c, 0, 70, 90, 50, acc, .9); c.restore()
    return _v(d)


def v_italia(t):
    """'Ti porta contatti da tutta Italia': la penisola stilizzata, i contatti si accendono
    sparsi dal nord al sud, lontani dal punto in cui lavori tu."""
    IT = [(430, 830), (560, 800), (690, 850), (650, 960), (600, 1020), (660, 1120), (760, 1230), (860, 1330), (930, 1420), (900, 1470),
          (820, 1420), (800, 1500), (760, 1600), (700, 1640), (720, 1540), (660, 1450), (580, 1340), (500, 1230), (440, 1120), (400, 1000), (360, 900)]
    PT = [(520, 880), (620, 900), (470, 1010), (560, 1100), (640, 1220), (730, 1320), (820, 1400), (760, 1560), (880, 1440), (590, 980)]
    def d(c, g, acc):
        p = oe(pr(g, t, .4)); pth = skia.Path(); pth.moveTo(*IT[0])
        for q in IT[1:]: pth.lineTo(*q)
        pth.close(); c.drawPath(pth, P(acc, .14 * p)); c.drawPath(pth, P(acc, .8 * p, 7))
        sic = skia.Path(); sic.addOval(skia.Rect.MakeXYWH(560, 1680, 190, 90)); c.drawPath(sic, P(acc, .14 * p)); c.drawPath(sic, P(acc, .8 * p, 7))
        tu = (470, 1010)
        for i, (x, y) in enumerate(PT):
            t0 = t + .3 + i * .1
            if g < t0: continue
            q = ob(pr(g, t0, .22)); me = (x, y) == tu
            if not me: line(c, tu[0], tu[1], lerp(tu[0], x, q), lerp(tu[1], y, q), RED, 4, .5)
            circ(c, x, y, 26 * q, YEL if me else RED); circ(c, x, y, 44 * q, YEL if me else RED, .3, blur=12)
        if g >= t + .3: text(c, 'TU', tu[0] - 80, tu[1], 54, YEL, 'bk')
    return _v(d)


def v_tavolo(t):
    """'Si svolge in presenza': due persone una di fronte all'altra a un tavolo, con le
    righe del dialogo che vanno e vengono."""
    def d(c, g, acc):
        p = oe(pr(g, t, .35)); dx = 400 * (1 - p)
        person(c, 250 - dx, 1300, 240, acc); person(c, 830 + dx, 1300, 240, WHT)
        rr(c, 160, 1500, 760, 50, 25, 0x8A93B8); rr(c, 240, 1550, 40, 180, 12, 0x5F6B8A); rr(c, 800, 1550, 40, 180, 12, 0x5F6B8A)
        for i in range(3):
            k = ((g - t) * .9 + i / 3) % 1; s = 1 if i % 2 == 0 else -1
            x = lerp(360, 720, k) if s > 0 else lerp(720, 360, k)
            if g >= t + .3: rr(c, x - 40, 1010 - i * 70, 80, 44, 22, WHT if s > 0 else acc, math.sin(k * math.pi))
    return _v(d)


def v_cassaforte(t, t_open):
    """'Affidarti i propri risparmi': una cassaforte che entra, la manopola gira, lo
    sportello si apre e dentro c'e' l'oro."""
    def d(c, g, acc):
        cx, cy = 540, 1300; p = ob(pr(g, t, .35)) if g >= t else 0; o = oe(pr(g, t_open, .4)) if g >= t_open else 0
        c.save(); c.translate(cx, cy); c.scale(p, p)
        rr(c, -330, -330, 660, 660, 50, 0x2A3566); rr(c, -330, -330, 660, 660, 50, 0x8A93B8, 1, 12)
        rr(c, -270, -270, 540, 540, 30, 0x0A0F24)
        for i in range(9):
            r, col = divmod(i, 3); q = cl(o * 2 - i * .08)
            circ(c, -150 + col * 150, 160 - r * 120, 58 * q, GOLD); text(c, '€', -150 + col * 150, 160 - r * 120, 60, 0x7A5A00, 'bk', sc=q, shadow=False)
        c.save(); c.translate(-270, 0); c.scale(max(.04, 1 - o), 1)                 # sportello che ruota sul cardine
        rr(c, 0, -270, 540, 540, 30, 0x3B4A8A); rr(c, 0, -270, 540, 540, 30, 0xAEB6D6, 1, 8)
        c.save(); c.translate(270, 0); c.rotate((g - t) * 220 if g < t_open else 0)
        circ(c, 0, 0, 110, 0xAEB6D6); circ(c, 0, 0, 80, 0x2A3566)
        for k in range(4): line(c, 0, 0, math.cos(k * 1.57) * 105, math.sin(k * 1.57) * 105, 0xAEB6D6, 16)
        c.restore(); c.restore(); c.restore()
    return _v(d, [t_open])


def v_circuito(t, t_on):
    """'Un sistema di marketing automatizzato': un interruttore che scatta su ON e la
    corrente che corre lungo il circuito accendendo i nodi."""
    N = [(200, 1150), (400, 1000), (620, 1090), (860, 980), (880, 1300), (680, 1450), (420, 1380), (220, 1560), (560, 1650), (860, 1620)]
    E = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 0), (6, 7), (7, 8), (8, 9), (9, 4), (2, 5)]
    def d(c, g, acc):
        p = oe(pr(g, t, .35)); on = g >= t_on; k = pr(g, t_on, 1.2) if on else 0
        for i, (a, b) in enumerate(E):
            line(c, *N[a], *N[b], 0x2A3566, 10, p)
            q = cl(k * len(E) - i)
            if q > 0: line(c, N[a][0], N[a][1], lerp(N[a][0], N[b][0], q), lerp(N[a][1], N[b][1], q), acc, 10)
        for i, (x, y) in enumerate(N):
            lit = on and k * len(N) > i
            circ(c, x, y, 34 * p, acc if lit else 0x2A3566); circ(c, x, y, 56, acc, .3 if lit else 0, blur=16)
        c.save(); c.translate(540, 1260); c.scale(p, p)
        rr(c, -150, -75, 300, 150, 75, GRN if on else 0x5F6B8A); s = oe(pr(g, t_on, .2)) if on else 0
        circ(c, lerp(-75, 75, s), 0, 60, WHT); text(c, 'ON' if on else 'OFF', lerp(60, -60, s), 0, 46, NAVY if on else WHT, 'bk', shadow=False)
        c.restore()
    return _v(d, [t_on])


def v_ufficio(t):
    """'I contatti nella tua area, direttamente in ufficio con te': un palazzo con la porta
    accesa e le persone che arrivano in fila ed entrano."""
    def d(c, g, acc):
        p = oe(pr(g, t, .35)); c.save(); c.translate(0, 500 * (1 - p))
        rr(c, 560, 900, 400, 860, 24, 0x16204A); rr(c, 560, 900, 400, 860, 24, acc, .8, 6)
        for r in range(4):
            for col in range(3): rr(c, 600 + col * 115, 950 + r * 150, 85, 100, 12, YEL, .25 + .5 * abs(math.sin(g * 1.5 + r + col)))
        rr(c, 700, 1580, 120, 180, 16, YEL)
        c.restore()
        for i in range(5):
            x = 620 - ((i * 150 - (g - t) * 170) % 620)
            if x > 600 or g < t: continue
            a = cl((600 - x) / 80) * cl((x + 40) / 120); person(c, x, 1700, 105, GRN, a)
        line(c, 60, 1770, 1020, 1770, 0x5F6B8A, 6)
    return _v(d)


def v_lampadine(t, n=4):
    """'Persone consapevoli del problema, che vogliono investire': persone in fila, sopra
    ognuna si accende una lampadina."""
    def d(c, g, acc):
        for i in range(n):
            x = 165 + i * 250; t0 = t + .2 + i * .22; on = g >= t0; q = ob(pr(g, t0, .25)) if on else 0
            person(c, x, 1560, 150, WHT if on else 0x5F6B8A)
            if on:
                circ(c, x, 1180, 110 * q, YEL, .3, blur=24); circ(c, x, 1170, 62 * q, YEL); rr(c, x - 28 * q, 1225, 56 * q, 44 * q, 10, 0xC9D1F0)
                for k in range(6):
                    a = math.radians(180 + k * 36); line(c, x + math.cos(a) * 85 * q, 1170 + math.sin(a) * 85 * q, x + math.cos(a) * 120 * q, 1170 + math.sin(a) * 120 * q, YEL, 8)
    return _v(d)


def v_notifiche(ts, testo='Nuovo appuntamento'):
    """'Riempirti l'agenda di appuntamenti': le notifiche di un nuovo appuntamento che
    cadono una sull'altra. ts = tempi di arrivo (3-4)."""
    def d(c, g, acc):
        for i, t0 in enumerate(ts[:4]):
            if g < t0: continue
            q = oe(pr(g, t0, .25)); y = lerp(700, 900 + i * 215, q)
            rr(c, 96, y + 10, 900, 180, 44, 0x000000, .35); rr(c, 90, y, 900, 180, 44, 0xF4F6FF)
            rr(c, 120, y + 30, 120, 120, 28, GRN); check(c, 180, y + 90, 70, WHT)
            text(c, testo, 270, y + 62, 54, NAVY, 'bk', align=0, shadow=False, maxw=680)
            rr(c, 270, y + 110, 420, 22, 11, 0x8A93B8, .7); text(c, 'ora', 950, y + 50, 34, 0x8A93B8, 'm', align=1, shadow=False)
    return _v(d, list(ts))


def v_scarica(t, t_done):
    """'Ho preparato una guida': un documento con la freccia di download, la barra che si
    riempie e la spunta finale."""
    def d(c, g, acc):
        cx, cy = 540, 1230; p = ob(pr(g, t, .35)) if g >= t else 0
        c.save(); c.translate(cx, cy); c.scale(p, p)
        pth = skia.Path(); pth.moveTo(-200, -300); pth.lineTo(90, -300); pth.lineTo(200, -190); pth.lineTo(200, 300); pth.lineTo(-200, 300); pth.close()
        c.drawPath(pth, P(acc, .4, blur=30)); c.drawPath(pth, P(0xF4F6FF)); tri(c, 150, -245, 135, 50, 0xC9D1F0)
        for i in range(3): rr(c, -140, -150 + i * 70, 280 - i * 60, 24, 12, 0x8A93B8, .7)
        done = g >= t_done
        if not done:
            b = 14 * math.sin(g * 9); line(c, 0, 60 + b, 0, 190 + b, acc, 26); tri(c, 0, 210 + b, 90, 52, acc)
        else:
            q = ob(pr(g, t_done, .25)); circ(c, 0, 140, 90 * q, GRN); check(c, 0, 140, 84 * q, WHT)
        c.restore()
        k = pr(g, t + .2, max(.2, t_done - t - .2)); rr(c, 190, 1640, 700, 40, 20, 0x2A3566); rr(c, 190, 1640, 700 * k, 40, 20, GRN if done else acc)
    return _v(d, [t_done])
