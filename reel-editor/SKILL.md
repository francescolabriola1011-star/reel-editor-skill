---
name: reel-editor
description: "Monta i video verticali di Michele (reel, short, TikTok) partendo dal girato: taglia silenzi ed errori (facoltativo), aggiunge sottotitoli parola per parola, B-roll in motion graphics animati e sincronizzati sul parlato, cambi di inquadratura frequenti, musica incalzante ed effetti sonori, e consegna l'mp4 finito. Usa questa skill ogni volta che Michele carica uno o più video e chiede di montarli, rimontarli, editarli, 'fare il montaggio', 'montalo come gli altri', 'come al solito', oppure chiede anche solo una parte del lavoro su un video parlato: mettere i sottotitoli, tagliare i silenzi o gli errori, aggiungere b-roll, motion graphics, animazioni, musica, renderlo più dinamico. Attivala anche quando scrive 'BeReal' intendendo B-roll, quando dice che il video è già tagliato e vuole solo il montaggio, e quando carica più video raw da lavorare in serie."
---

# Reel Editor

Trasforma un video parlato in camera in un reel montato nello stile di Michele: ritmo alto (uno stacco ogni 2 secondi circa), B-roll fatti interamente in motion graphics che illustrano quello che viene detto, sottotitoli con la parola attiva evidenziata, zoom alternati sul volto, base elettronica a 128 bpm con effetti sui tagli.

Gli script in `scripts/` fanno tutto il lavoro meccanico (trascrizione, taglio, render, musica, mix). A te resta la parte che richiede giudizio: decidere cosa tagliare e scrivere la **regia**, cioè un file `edit.py` con la sequenza delle inquadrature. La qualità del risultato dipende quasi tutta da lì.

Serve l'esecuzione di codice con accesso a `github.com` (per scaricare il modello di trascrizione). Se il setup fallisce per la rete, dillo a Michele e fermati: senza trascrizione con i tempi il montaggio non si può sincronizzare.

## Flusso

Usa una cartella di lavoro per ogni video, ad esempio `/home/claude/reel/<nome>`. Negli esempi `S` è la cartella `scripts/` di questa skill e `W` la cartella di lavoro.

### 1. Setup e preparazione

```bash
sh S/setup.sh                       # dipendenze + modelli, la prima volta scarica ~490 MB
python3 S/prep.py <video> W         # porta a 1080x1920 30fps, trova il volto, crea overview.jpg
```

Guarda `W/overview.jpg`: ti dice com'è inquadrato Michele e se il ritaglio verticale è corretto. `prep.py` stampa anche se c'è spazio per i pannelli sopra la testa; se dice NO, non usare `panel=` nella regia.

### 2. Trascrizione

```bash
python3 S/transcribe.py W           # stampa la trascrizione con l'indice di ogni parola e le pause
```

Leggila tutta. Il modello sbaglia soprattutto nomi propri, termini tecnici e numeri: correggi quello che finirà a schermo nei sottotitoli.

```bash
python3 S/words.py W fix 45=lasciano 217=simulatore 20="70-80%"
```

### 3. Taglio di silenzi ed errori (facoltativo)

Decidi così:
- Michele dice che il video è **già tagliato** (o di non tagliare): `python3 S/cut.py W --none`
- In tutti gli altri casi il girato è grezzo: taglia.

```bash
python3 S/cut.py W --drop "12-20,57-63"      # toglie le parole 12-20 e 57-63 e accorcia tutte le pause
python3 S/cut.py W                            # solo silenzi, nessun errore da togliere
python3 S/cut.py W --drop "12-20" --keep-silence   # solo errori, pause intatte
```

`--drop` prende intervalli di indici di parole. Cosa cercare nella trascrizione:
- **Riprese ripetute**: la stessa frase iniziata due o tre volte. Tieni l'ultima versione completa, togli le precedenti per intero.
- **False partenze e autocorrezioni**: "il tuo porta… il tuo portafoglio" → togli il primo pezzo.
- **Fuori copione**: "aspetta", "la rifaccio", "ok", colpi di tosse trascritti, commenti rivolti a chi riprende.
- **Riempitivi a inizio frase** ("ehm", "allora", "cioè") solo se isolati da una pausa: se sono legati alla parola dopo, il taglio si sente.

Non tagliare mai contenuto per accorciare: qui si tolgono errori, la scaletta è di Michele. Nel dubbio tieni, e segnala il dubbio nel messaggio finale.

Dopo il taglio gli indici e i tempi cambiano. Rileggi sempre:

```bash
python3 S/words.py W times          # ogni parola col suo tempo di inizio: è la tua griglia di sincronizzazione
```

Controlla che il testo tagliato scorra come una frase sola. Se un taglio ha mangiato una parola o lasciato un doppione, rilancia `cut.py` con gli indici corretti (riparte sempre dalla trascrizione originale: rivedi quegli indici con `python3 S/words.py W raw`). Le correzioni fatte con `fix` dopo un taglio vanno rifatte se ritagli, quindi correggi le parole prima di tagliare.

### 4. Regia: scrivi `W/edit.py`

Prima leggi `references/visual.md` (catalogo dei visual e dei pannelli, con i parametri) e `references/esempio_edit.py` (un montaggio completo di 76 secondi, da usare come modello di ritmo e di sintassi).

`edit.py` contiene una lista `SHOTS` di inquadrature consecutive che coprono tutto il video, da 0 alla fine:

```python
from mgkit import *

SHOTS = [
    head(0.00, 1.58, 'wide', title=[(0.2, 'CONSULENTE', 'sm'), (0.95, 'FINANZIARIO,', 'acc')]),
    mg(1.58, 2.84, scene(v_fish(), [(1.62, 'I PESCI', 'big'), (2.05, 'PICCOLI', 'huge')], theme='ocean')),
    head(5.50, 6.55, 'mid'),
    mg(6.55, 8.75, scene(v_donut(6.62, [(7.0, 70), (7.36, 80)]), [(6.6, 'COMPOSTO AL', 'w')], theme='dark')),
    head(23.48, 25.20, 'wide', panel=p_people(23.7, (24.0, 'CLIENTI PICCOLI'))),
    ...
]
DROPS = [33.7, 67.5]   # facoltativo: dove la musica "riparte"
```

- `head(a, b, zoom, panel=, title=)` è il parlato in camera. Zoom `'wide'`, `'mid'` o `'tight'`. I sottotitoli ci vanno sopra da soli.
- `mg(a, b, scene(visual, righe, theme=))` è un B-roll a tutto schermo: sfondo animato, un visual dal catalogo e i titoli cinetici.
- Tutti i tempi sono secondi assoluti presi da `words.py W times`.

#### Come si costruisce una buona regia

Lavora frase per frase sulla trascrizione con i tempi. Per ogni frase chiediti: *c'è un'immagine che la rende più chiara o più forte?* Se sì è un B-roll, se no resta sul volto e cambia zoom.

**Ritmo.** Uno stacco ogni 2 secondi circa è il motivo per cui chi guarda non scorre via. In pratica:
- inquadrature sul volto da 1 a 3,5 secondi, mai due di fila con lo stesso zoom (lo stacco non si vedrebbe);
- scene B-roll da 1,2 a 3,7 secondi; se una frase ne chiede di più, spezzala in due scene oppure usa `swap=` o un visual a scatti (`v_counter`, `v_donut`, `v_loop`, `v_list`), che creano stacchi interni;
- B-roll tra il 45 e il 60% della durata;
- mai più di 9 secondi senza rivedere il volto: è la faccia di Michele che crea fiducia, la grafica la sostiene.

**Apertura.** Il primo secondo e mezzo è il volto con il titolo dell'hook sovrapposto (`title=`), poi subito un B-roll forte sulla parola chiave dell'hook. Chi scorre deve vedere una persona e una promessa prima di qualsiasi grafica.

**Sincronizzazione.** È la differenza tra un montaggio che sembra professionale e uno che sembra un template.
- Fai partire la scena 0,05-0,1 secondi *prima* della parola che illustra.
- Ogni riga di titolo ha il tempo di inizio della parola corrispondente: il testo deve sbattere a schermo mentre viene pronunciato, non prima.
- Lo stesso vale per i parametri di tempo dei visual (lo scatto del contatore sul numero pronunciato, l'aggancio del mirino sulla parola chiave).

**Titoli cinetici.** Sono le parole di Michele, in maiuscolo, ridotte alle parole chiave: da una a tre parole per riga, al massimo tre o quattro righe per scena. Non riscrivere il concetto con parole tue e non aggiungere informazioni che lui non dice. Stili: `'sm'` riga piccola di raccordo, `'w'` bianca, `'big'` bianca grande, `'acc'` colore d'accento corsivo, `'huge'` enorme per una parola corta. Una sola riga d'accento per scena, sulla parola che conta.

**Scelta del visual.** Scegli quello che rappresenta *letteralmente* il concetto: percentuale → `v_donut`, cifre che crescono → `v_counter`, un elenco → `v_list`, un confronto → `v_versus`, cercare clienti → `v_radar` o `v_target`, un processo automatico → `v_gears`, uno strumento o un software → `v_sliders`, e così via. Non riusare lo stesso visual due volte nello stesso video se non per richiamo voluto. Se nel catalogo non c'è niente di adatto, scrivi un visual su misura (vedi in fondo a `references/visual.md`): un'immagine pensata per quella frase vale più di una generica riciclata.

**Temi colore.** Seguono il significato: `red` e `purple` per problemi, errori, perdite; `green` per soluzione, risultati, soldi che entrano; `gold` per patrimonio e valore; `blue` per sistemi, strumenti, passaggi neutri; `teal` e `ocean` per scene d'ambiente. Alterna: due scene consecutive con lo stesso tema sembrano una scena sola.

**Pannelli.** Su un'inquadratura `'wide'` puoi far scendere una scheda sopra la testa (`panel=`) per etichettare un concetto senza togliere il volto. Due o tre per minuto, non di più.

**Chiusura.** Se il video finisce con "commenta con la parola X", chiudi con `v_comment('X', ...)`.

**Numeri.** A schermo vanno solo numeri che Michele pronuncia. Alcuni visual mostrano cifre illustrative (`v_people`, `v_sliders`): se li usi, scegli valori neutri e segnalalo nel messaggio finale, perché chi guarda li legge come promesse.

**Musica.** `DROPS` indica uno o due momenti in cui la base si svuota per due battute e riparte con un colpo: mettili sui punti di svolta (dal problema alla soluzione, prima della chiamata all'azione). Se non lo scrivi vengono piazzati in automatico.

Altre opzioni di `edit.py`: `SUBS = False` (niente sottotitoli), `SUB_UPPER = True`, `SUB_COLOR = YEL`, `SUBS_ON_MG = True` (sottotitoli anche sui B-roll: di norma no, i titoli cinetici bastano), `BPM = 128`, `SFX = False`.

### 5. Controllo prima del render

```bash
python3 S/render.py W sheet         # valida la timeline e crea W/check_1.jpg, check_2.jpg...
```

Stampa gli avvisi sul ritmo (inquadrature troppo lunghe, buchi, titoli fuori scena): risolvili. Poi **guarda le immagini `check_N.jpg`**: c'è un fotogramma per ogni inquadratura. Cerca testi che escono dai bordi, righe che si sovrappongono al visual, scene vuote, pannelli che coprono la fronte. Per vedere istanti precisi: `python3 S/render.py W test W/t.jpg 3.2 7.5 12.0`.

Il render completo costa minuti, il foglio di controllo secondi: correggi qui.

### 6. Render, musica, mix

```bash
python3 S/render.py W all --budget 230     # rilancia lo stesso comando finché stampa "OK render completo"
python3 S/music.py W
python3 S/mix.py W /mnt/user-data/outputs/<nome>_montato.mp4
```

Il render procede a blocchi e riprende da dove era arrivato (circa 7 fotogrammi al secondo: un minuto di video richiede 4-5 minuti). Se modifichi `edit.py` i blocchi vengono rifatti da capo. `mix.py` normalizza la voce e abbassa la musica quando Michele parla; con `--music file.mp3` usa una traccia sua, con `--no-music` nessuna, con `--music-vol 0.15` la abbassa.

Consegna il file con `present_files`.

### 7. Messaggio finale

Breve. Michele deve sapere solo ciò che non può vedere da solo o che deve controllare:
- quanto è stato tagliato e quali frasi sono state tolte come errori (così può dire se una andava tenuta);
- parole della trascrizione di cui non eri sicuro;
- eventuali numeri illustrativi messi a schermo;
- che la musica è generata e non l'hai potuta ascoltare, quindi volume e gusto vanno verificati.

## Più video

Lavorali uno alla volta, ognuno nella sua cartella, e consegna ogni file appena pronto. Varia visual e temi tra un video e l'altro: una serie in cui ogni reel si apre con la stessa animazione sembra fatta in serie.

## Se qualcosa non va

- **Volto non trovato o zoom fuori centro**: correggi a mano `face_cx`, `face_cy`, `face_h`, `chin_y` in `W/layout.json` guardando `overview.jpg` (coordinate su 1080x1920), poi rifai `sheet`.
- **Sottotitoli troppo alti o bassi**: dipendono da `chin_y` e `face_h` in `layout.json`.
- **Video orizzontale**: `prep.py` lo ritaglia al centro e avvisa. Se Michele non è al centro, dillo prima di proseguire.
- **Taglio che si sente**: allarga le pause con `--pad 0.10` o alza `--max-pause 0.40`.
- **Michele chiede una modifica dopo la consegna**: cambia solo `edit.py` (o rilancia `cut.py` se riguarda i tagli) e ripeti dal passo 5. La cartella di lavoro conserva tutto il resto.
