"""ESEMPIO COMPLETO di edit.py — reel di 76 s "I pesci piccoli rallentano la tua crescita di portafoglio".
40 inquadrature (una ogni 1,9 s), 20 scene b-roll (circa 60% del tempo), 3 pannelli, 2 ripartenze musicali.
Accanto a ogni riga c'è la frase detta in quel momento: nota come ogni titolo entra sul tempo esatto della parola in words.json."""
from mgkit import *

SHOTS = [
    # --- HOOK: volto subito, titolo sul busto, poi b-roll entro 2 secondi
    head(0.00, 1.58, 'wide', title=[(0.2, 'CONSULENTE', 'sm'), (0.95, 'FINANZIARIO,', 'acc')]),
    mg(1.58, 2.84, scene(v_fish(), [(1.62, 'I PESCI', 'big'), (2.05, 'PICCOLI', 'huge')], theme='ocean')),
    mg(2.84, 5.50, scene(v_chart(2.9, 1.75, 'slow', t_badge=3.95),
                         [(2.88, 'STANNO RALLENTANDO', 'w'), (3.5, 'LA TUA CRESCITA', 'acc'), (4.25, 'DI PORTAFOGLIO', 'w')])),
    head(5.50, 6.55, 'mid'),                                   # "Se oggi il tuo portafoglio è"
    mg(6.55, 8.75, scene(v_donut(6.62, [(7.0, 70), (7.36, 80)]),   # "composto al 70, 80%"
                         [(6.6, 'COMPOSTO AL', 'w'), (8.2, 'DA CLIENTI PICCOLI', 'acc')], theme='dark')),
    head(8.75, 9.93, 'tight'),                                 # "da clienti che ti hanno lasciato"
    mg(9.93, 13.30, scene(v_money([(11.4, '50€'), (11.95, '100€')]),  # "una piccola provvigione da 50, 100 euro"
                          [(10.02, 'UNA PICCOLA', 'w'), (10.65, 'PROVVIGIONE', 'acc:yel')], theme='green')),
    head(13.30, 14.63, 'mid'),                                 # "e ti aspetti che da questi arrivino"
    mg(14.63, 16.12, scene(v_network(14.72), [(14.7, 'REFERENZE', 'big'), (15.3, 'PATRIMONIALIZZATE?', 'acc')], theme='gold')),
    mg(16.12, 19.90, scene(v_counter([(18.0, '100'), (18.4, '200'), (18.95, '500')], coin_from=16.3),   # "un gestito da 100, 200, 500 mila euro"
                           [(16.25, 'CHE MAGARI', 'sm'), (16.85, 'TI LASCIANO', 'w'), (17.35, 'UN GESTITO DA', 'acc')], theme='gold')),
    mg(19.90, 21.70, scene(v_clock(), [(19.98, 'STAI', 'w'), (20.3, 'PERDENDO', 'big'), (20.67, 'SOLO', 'w'), (21.0, 'TEMPO', 'huge:yel')], theme='red', top=300)),
    head(21.70, 23.48, 'mid'),                                 # "Se hai un portafoglio completamente"
    head(23.48, 25.20, 'wide', panel=p_people(23.7, (24.0, 'CLIENTI PICCOLI'))),
    head(25.20, 27.22, 'tight'),                               # "diventa molto complesso andare a"
    mg(27.22, 30.90, scene(v_target(27.9, 28.45, t_pulse=29.3), swap=29.3, theme='gold', lines=[
        (27.28, 'ANDARE A PRENDERE', 'sm'), (27.9, 'I CLIENTI PIÙ', 'w'), (28.45, 'PATRIMONIALIZZATI', 'acc'),
        (29.3, 'QUELLI CHE', 'w'), (29.75, 'TI INTERESSANO', 'acc:yel')])),
    head(30.90, 31.95, 'mid'),                                 # "Ecco che così continui in un"
    mg(31.95, 33.10, scene(v_spin(), [(32.0, 'CIRCOLO', 'big'), (32.62, 'VIZIOSO', 'huge')], theme='red')),
    mg(33.10, 36.83, scene(v_loop([(34.0, 'CLIENTI PICCOLI'), (34.7, 'CHIEDONO TANTO'), (35.85, 'LASCIANO POCO')]),
                           [(33.2, 'LAVORI CON', 'w')], theme='purple')),
    mg(36.83, 38.40, scene(v_orbit([(37.95, 'DALLO STESSO'), (38.1, 'CIRCOLO')]),
                           [(36.9, 'E OTTIENI', 'sm'), (37.62, 'REFERENZE', 'acc:yel')], theme='red')),
    head(38.40, 39.93, 'tight'),                               # "dello stesso circolo di persone"
    mg(39.93, 41.62, scene(v_escape(40.5), [(40.08, "L'UNICO MODO", 'w'), (40.78, 'PER USCIRNE', 'acc')], theme='green')),
    head(41.62, 42.55, 'mid'),
    head(42.55, 43.60, 'tight'),                               # "patrimonializzati"
    head(43.60, 45.35, 'wide', panel=p_pulse(43.6, (44.35, 'NUOVO BACINO'))),
    mg(45.35, 47.85, scene(v_gears(45.38), [(45.6, 'GRAZIE AL', 'sm'), (46.12, 'MARKETING', 'big'), (46.62, 'AUTOMATIZZATO', 'acc')])),
    head(47.85, 48.95, 'mid'),
    mg(48.95, 52.45, scene(v_radar(48.95, t_pin=50.33), swap=50.3, theme='teal', lines=[
        (49.02, 'INTERCETTA', 'big'), (49.95, 'LE PERSONE', 'acc'), (50.33, 'NELLA TUA', 'w'), (50.95, 'AREA', 'huge:yel')])),
    head(52.45, 54.43, 'tight'),                               # "che in questo momento hanno un problema"
    mg(54.43, 57.70, scene(v_search(54.5, 'consulente finanziario', 55.5, 1.5, t_results=57.0, top='Il consulente giusto'),
                           [(54.62, 'STANNO CERCANDO', 'w'), (55.33, 'LA SOLUZIONE', 'acc')])),
    head(57.70, 59.15, 'mid'),
    mg(59.15, 61.75, scene(v_basin(59.75), [(59.3, 'PERSONE', 'big'), (59.9, 'FUORI DAL TUO', 'w'), (60.5, 'BACINO', 'huge')], theme='gold', top=320)),
    head(61.75, 63.10, 'tight'),
    head(63.10, 64.40, 'wide', panel=p_strike(63.2, (63.6, 'PASSAPAROLA'), 64.0)),
    head(64.40, 65.60, 'mid'),
    mg(65.60, 67.85, scene(v_people(66.0, 1.6, 24), [(65.74, 'QUANTI CLIENTI', 'w'), (66.4, 'IN PIÙ?', 'huge:yel')], theme='green', top=320)),
    head(67.85, 68.95, 'mid'),
    mg(68.95, 71.00, scene(v_sliders(68.97, 'NUOVI CLIENTI'), [(69.0, 'HO PREPARATO UN', 'sm'), (69.95, 'SIMULATORE', 'acc')])),
    mg(71.00, 73.30, scene(v_bars(71.05, t_line=72.3), [(71.03, 'ESATTAMENTE', 'sm'), (71.72, 'LE PREVISIONI', 'acc'), (72.35, 'CHE TI PUOI ASPETTARE', 'sm')], theme='green')),
    head(73.30, 74.55, 'mid'),                                 # "Commenta qui sotto con la parola"
    mg(74.55, 76.50, scene(v_comment('SIMULATORE', 74.66, 75.2, note_line=(75.3, 'TE LO MANDO IN PRIVATO')), [(74.58, 'COMMENTA', 'big')], top=380)),
]
DROPS = [33.7, 67.5]      # la musica riparte su "circolo vizioso" e prima della chiamata all'azione
BPM = 128
