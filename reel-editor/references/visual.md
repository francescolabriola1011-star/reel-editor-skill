# Catalogo visual, pannelli e primitive

Tutti i tempi sono secondi assoluti sulla timeline (quelli di `words.py W times`). Ogni visual si usa dentro `scene(...)`.

## Indice
1. `scene()` e i titoli
2. Visual a tutto schermo (per concetto)
3. Pannelli sopra la testa
4. Scrivere un visual su misura

## 1. scene() e i titoli

```python
scene(visual, righe, theme='blue', swap=None, top=350, accent=None)
```

- `righe`: lista di `(tempo, 'TESTO', stile)`. Si impilano dall'alto a partire da `top`. Con 4 righe o con una riga `'huge'` più altre due, abbassa `top` a 300-320.
- Stili: `'sm'` (86 px, sale dal basso), `'w'` (122), `'big'` (168), `'acc'` (134, corsivo, colore d'accento, bagliore), `'huge'` (250, come acc). Il testo troppo largo viene rimpicciolito da solo fino a 1000 px, ma una riga `'huge'` oltre le 8 lettere perde tutto l'effetto: usa `'acc'`.
- Colore forzato: `'acc:yel'`, `'huge:red'`, `'w:grn'` (blue, yel, red, grn, gold, wht).
- `theme`: `blue`, `red`, `green`, `gold`, `ocean`, `teal`, `purple`, `dark`. Il colore d'accento segue il tema; `accent='yel'` lo cambia per righe e visual.
- `swap=t`: stacco interno. A `t` le righe con tempo precedente spariscono, entrano quelle con tempo ≥ `t` e la camera stringe del 22% sul visual. Serve per tenere una scena 3-4 secondi senza che si fermi.
- `scene(None, righe)` è una scena di solo testo: va bene per una frase secca di un secondo, non di più.

I visual occupano la zona da y=800 a y=1800 (centro 540, 1200). I titoli stanno sopra.

## 2. Visual a tutto schermo

### Numeri e dati
| Visual | Cosa mostra | Quando |
|---|---|---|
| `v_donut(t, steps, unit='%')` | Ciambella che si riempie. `steps=[(7.0, 70), (7.36, 80)]`: arriva a 70 entro 7.0, scatta a 80 a 7.36 | Percentuali, quote, "X su 10" |
| `v_counter(steps, coin_from=None, coin='€', bars=True)` | Numero gigante che cambia a scatti con barre dietro. `steps=[(18.0, '100'), (18.4, '200'), (18.95, '500')]`. `coin_from`: moneta che gira prima del primo scatto | Cifre in crescendo, importi, anni, "da X a Y". Il testo è libero: `'3X'`, `'10K'`, `'0'` |
| `v_chart(t, dur=1.8, mode='slow', t_badge=None)` | Linea che si disegna. `mode`: `'slow'` sale e si appiattisce, `'up'` accelera, `'down'` crolla. `t_badge`: freccia tonda | Crescita, stallo, calo |
| `v_bars(t, t_line=None, n=6, down=False)` | Istogramma barra dopo barra, `t_line`: freccia di tendenza | Previsioni, risultati mese su mese, andamento |
| `v_versus(t, left, right, t_win=None)` | Due barre a confronto. `left=('PRIMA', .25)`, `right=('DOPO', .95)` | Prima/dopo, loro/tu, metodo A/B |
| `v_people(t, dur=1.6, total=24, prefix='+')` | Contatore + omini che compaiono | Clienti, lead, iscritti. Cifra illustrativa: segnalala |
| `v_money(notes)` | Pioggia di monete e banconote che sbattono. `notes=[(11.4, '50€'), (11.95, '100€')]` (max 3) | Importi piccoli, costi, guadagni, prezzo |

### Persone, mercato, clienti
| Visual | Cosa mostra | Quando |
|---|---|---|
| `v_target(t_aim, t_lock, t_pulse=None)` | Mirino che stringe e aggancia una persona dorata tra tanti puntini | Cliente ideale, nicchia, "quelli giusti", focus |
| `v_radar(t, t_pin=None)` | Radar su mappa che accende persone; `t_pin` fa cadere un segnaposto | Trovare clienti, zona, territorio, intercettare |
| `v_basin(t, dur=1.7, label='TU')` | Cerchia piccola tratteggiata e fuori decine di puntini che si accendono | Uscire dal proprio giro, mercato inesplorato, nuovi contatti |
| `v_network(t, n=5, symbol='€')` | Da una persona partono linee verso nodi grandi | Referenze, passaparola, connessioni, opportunità |
| `v_search(t, query, t_type, type_dur=1.5, t_results=None, top='...', badge='TU')` | Barra di ricerca in cui si digita `query`, poi 3 risultati col primo evidenziato | Qualcuno che cerca, Google, domanda consapevole. Max 2 righe di titolo |
| `v_fish()` | Banco di pesciolini (tema `ocean`) | Metafora dei "pesci piccoli": esempio di visual legato a una frase precisa |

### Processi e concetti
| Visual | Cosa mostra | Quando |
|---|---|---|
| `v_loop(pills, center='LOOP')` | Anello che gira, etichette a pillola che compaiono lungo il giro. `pills=[(34.0, 'CLIENTI PICCOLI'), (34.7, 'CHIEDONO TANTO'), ...]` (2-4) | Circoli viziosi o virtuosi, fasi di un ciclo |
| `v_orbit(center, n=6, speed=260)` | Anello veloce con persone sopra e testo al centro. `center=[(37.95, 'DALLO STESSO'), (38.1, 'CIRCOLO')]` | Sempre le stesse persone, giro chiuso, ripetizione |
| `v_spin(speed=300)` | Doppio anello di frecce, decorativo | Scena-titolo su "ciclo", "loop", "ripetere" |
| `v_escape(t)` | Freccia verde che sfonda un cerchio rosso | Via d'uscita, svolta, "l'unico modo" |
| `v_gears(t)` | Ingranaggi + pipeline con impulsi | Automazione, sistema, processo, macchina |
| `v_sliders(t, label='RISULTATO', prefix='+')` | Finestra di app con cursori che si muovono e numero che cambia | Simulatore, calcolatore, software, dashboard. Max 2 righe di titolo |
| `v_list(items)` | Righe che entrano di lato con spunta o croce. `items=[(1.3, 'Testo breve', True), (1.9, 'Altro', False)]` (max 5) | Elenchi, errori da evitare, requisiti, passi |
| `v_clock()` | Orologio con lancette impazzite | Tempo perso, urgenza, scadenza |
| `v_comment(keyword, t_type, t_send, note_line=None)` | Campo commento in cui si digita la parola, aeroplanino che parte, frecce in basso. `note_line=(75.3, 'TE LO MANDO IN PRIVATO')` | Chiusura "commenta con la parola X" |

## 3. Pannelli sopra la testa

Si passano a `head(..., 'wide', panel=...)`. La scheda entra dall'alto e misura 940x490.

| Pannello | Cosa mostra |
|---|---|
| `p_text(lines, color=YEL)` | Solo testo, 1-3 righe: `[(13.4, 'UN GESTITO DA'), (14.0, 'sei cifre')]` |
| `p_stat(t, value, label, color=GRN)` | Numero grande + etichetta: `p_stat(6.8, '50€', 'PROVVIGIONE MEDIA', RED)` |
| `p_people(t, title, n=30)` | Griglia di omini a onda + titolo `(tempo, 'TESTO')` |
| `p_pulse(t, title, color=GRN)` | Cerchi che si espandono + titolo: novità, apertura |
| `p_strike(t, title, t_strike)` | Parola che viene sbarrata in rosso: cosa abbandonare |

L'inquadratura col pannello deve durare almeno 1,2 secondi, altrimenti la scheda non fa in tempo a entrare e uscire.

## 4. Scrivere un visual su misura

Quando una frase ha un'immagine precisa che il catalogo non copre (i pesciolini sono nati così), scrivila in `edit.py`. Un visual è una funzione che restituisce una funzione di disegno `d(c, g, acc)`: `c` è il canvas, `g` il tempo corrente in secondi, `acc` il colore d'accento del tema.

```python
def v_scala(t, gradini=4):
    """Gradini che compaiono uno dopo l'altro, con un omino che sale."""
    def d(c, g, acc):
        for i in range(gradini):
            t0 = t + i * .25
            if g < t0: continue
            q = ob(pr(g, t0, .3))                          # 0→1 con rimbalzo
            rr(c, 140 + i * 210, 1700 - (i + 1) * 180 * q, 200, (i + 1) * 180 * q, 18, acc, .9)
        k = min(gradini - 1, int(max(0, g - t) / .25))
        person(c, 240 + k * 210, 1700 - (k + 1) * 180 - 70, 110, WHT)
    d.hits = [t + (gradini - 1) * .25]                     # facoltativo: istanti con flash + colpo sonoro
    return d

mg(12.0, 14.2, scene(v_scala(12.1), [(12.05, 'UN PASSO', 'w'), (12.6, 'ALLA VOLTA', 'acc')], theme='green'))
```

Primitive disponibili (tutte in `mgkit`):
- **Tempo**: `pr(g, t0, durata)` avanzamento 0-1; curve `oc` (morbida), `oe` (scatto che frena), `ob` (rimbalzo); `lerp(a, b, x)`.
- **Forme**: `circ(c, x, y, r, colore, a=1, stroke=0, blur=0)`, `rr(c, x, y, w, h, raggio, colore, a, stroke)`, `line(c, x1, y1, x2, y2, colore, spessore, a)`, `arc(c, x, y, r, angolo0, ampiezza, colore, spessore)`, `tri(c, x, y, angolo, lato, colore)`, `check(c, x, y, s, colore, ok=True)`.
- **Oggetti**: `person`, `gear`, `note` (banconota), `ring` (anello di frecce), `pill` (etichetta).
- **Testo**: `text(c, s, x, y, size, colore, k='bk', a=1, sc=1, align=.5, glow=None, maxw=None)`; con animazione d'ingresso `slam`, `pop`, `rise` `(c, g, t0, s, x, y, size, colore, k)`. Font `k`: `'bk'` Black, `'bi'` Black corsivo, `'b'` Bold, `'m'` Medium.
- **Colori**: `BLUE YEL RED GRN GOLD WHT GREY NAVY`.
- Per forme libere usa direttamente `skia.Path()` e `c.drawPath(path, P(colore, alpha, stroke, blur))`.

Regole che fanno la differenza:
- **Niente di fermo.** Ogni elemento entra con un'animazione (0,2-0,4 secondi) e poi continua a muoversi un po' (rotazione, pulsazione, deriva). Un fotogramma statico per più di mezzo secondo sembra una slide.
- **Sfasa gli ingressi** di 0,05-0,12 secondi tra elementi simili: è quello che dà l'effetto "a cascata".
- **Resta nella zona y 800-1800** e a 60 px dai bordi laterali: sopra ci sono i titoli, sotto l'interfaccia di Instagram.
- **Al massimo tre colori** più bianco, presi dalla palette.
- Provalo con `render.py W test` in due o tre istanti (inizio, metà, fine) prima del render completo.

Per casi estremi puoi passare a `mg()` una funzione `f(c, g)` che disegna l'intero fotogramma, sfondo compreso (`bg(c, g, *THEMES['red'][:4])`).
