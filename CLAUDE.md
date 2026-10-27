# Il Pulcino Libero — istruzioni per Claude Code

Questo file guida lo sviluppo del gioco. Leggilo tutto prima di iniziare e rispettalo in ogni sessione.

## Chi sono e come lavoriamo

Sono Riccardo. Non scrivo codice a mano: descrivo cosa voglio e tu lo realizzi. Io provo il gioco, ti dico cosa non va, tu correggi.

- Parlami in italiano, in modo semplice, senza gergo tecnico non spiegato.
- Lavora **una tappa alla volta**. Alla fine di ogni tappa c'è uno **STOP**: fermati, spiegami in poche righe cosa hai fatto e cosa devo provare, e **aspetta il mio ok** prima di passare alla tappa successiva.
- Se una scelta non è scritta qui e cambia il gioco in modo visibile, chiedimela prima di farla.
- Non aggiungere funzioni che non ho chiesto.

## Il gioco in breve

Platform 2D per telefono. Un pulcino scappa dal pollaio e, livello dopo livello, scopre un mondo sempre più grande fino a conquistare la propria libertà. Tono rilassante ma divertente, con una vena goliardica: animazioni esagerate, versi buffi, nemici ridicoli. Difficoltà gentile: punzecchia, non frustra.

Struttura: livelli separati scelti da una mappa, ognuno sblocca il successivo. Dieci livelli previsti: pollaio, cortile, orto, prato, bosco, stagno, collina rocciosa, temporale o grotta, paese degli umani, campanile/tetto finale.

Il pulcino cresce: in ogni zona impara un'abilità (beccata, doppio salto, planata, galleggiare, scivolata) e cambia aspetto, da batuffolo a giovane pollo.

**Regola di identità:** nessun riferimento a prodotti Nintendo. Niente funghi, tubi verdi, monete, font o personaggi simili. Gli oggetti vengono dal mondo del pulcino: chicchi di mais da raccogliere, nidi e buche come passaggi.

## Scelte tecniche (non cambiarle senza chiedermelo)

- Motore: **Godot 3.6** (serie 3.x), linguaggio **GDScript**.
- Renderer: **GLES2**, per girare su telefoni modesti e sul web.
- Il PC di sviluppo è un Windows di circa 10 anni: tieni tutto leggero.
- Obiettivo principale: **telefono**, schermo orizzontale (1280×720 come base, con scalatura `2d` / `keep`).
- Controlli: tastiera sul PC per i test (frecce + spazio); sul telefono pulsanti a schermo grandi e semitrasparenti, frecce sinistra/destra in basso a sinistra, salto in basso a destra.
- Usa le azioni di input di Godot (`move_left`, `move_right`, `jump`) sia per tastiera sia per i pulsanti touch, così la logica è una sola.
- I valori del movimento (velocità, gravità, forza del salto, ecc.) devono essere variabili `export` modificabili dall'editor, con commenti in italiano che spiegano a cosa servono: li regoleremo insieme a sensazione.

## Organizzazione del progetto

```
res://
  scenes/      scene (.tscn): player, livelli, interfaccia
  scripts/     script GDScript
  assets/      grafica e suoni (all'inizio solo segnaposto)
```

Nomi di file e cartelle in minuscolo con trattini bassi. Commenti nel codice in italiano, brevi.

## Scelte già fatte (non cambiarle senza chiedermelo)

- **Grafica:** stile cartoon vettoriale. Immagini SVG in `assets/grafica/`, disegnate al doppio della grandezza; i personaggi sono a pezzi animati da codice. I pezzi lunghi del livello (pavimenti, pareti) si disegnano da codice nello stesso stile.
- **Inquadratura:** telecamera con zoom 0.7, perché il pulcino si veda bene sul telefono.
- **Animazioni e suoni:** schiaccia-e-allunga, polvere, versi buffi. I suoni sono segnaposto sintetici creati da `strumenti/genera_suoni.py`.
- **Testi:** font Fredoka (licenza OFL, in `assets/font/`).
- **Modalità dipinta (in prova):** un selettore sulla mappa, accanto a «Crediti» («Stile: Cartoon / Dipinto»; solo lì, non nel menu di pausa), scambia i disegni con versioni ridipinte a pennellate da `strumenti/ridipingi.py` (stile «delicato»), salvate in `assets/dipinto/`. Il telefono ricorda la scelta. Per ora c'è solo nel cortile; lo stile predefinito resta il cartoon.
- **Pubblicazione:** dopo ogni modifica il gioco va esportato in `docs/` e caricato su GitHub. Si gioca su https://ricky80l.github.io/pulcino-libero/.

## Tappe del livello 1 (pollaio) — completato

Costruiamo solo il livello 1. La mappa e il livello 2 vengono dopo.

### Tappa 1 — Progetto vuoto
Crea il progetto Godot 3.6 con le impostazioni sopra (GLES2, risoluzione, scalatura, azioni di input) e la struttura delle cartelle.
**STOP:** spiegami come aprirlo nell'editor. Va bene se si apre senza errori.

### Tappa 2 — Il pulcino che salta
Un pulcino segnaposto (anche un quadrato giallo con due occhi) che cammina e salta su qualche piattaforma, con la tastiera. Il salto deve essere piacevole: accelerazione e frenata morbide, salto più alto se tengo premuto, un piccolo margine per saltare anche appena dopo essere scesi da un bordo.
**STOP:** dimmi quali valori posso regolare e come. Si va avanti solo quando il salto mi piace.

### Tappa 3 — Pulsanti per il telefono
Aggiungi i pulsanti a schermo e spiegami come esportare e provare il gioco sul telefono (versione web o Android, scegli la più semplice e motivala).
**STOP:** si va avanti quando riesco a giocare dal telefono.

### Tappa 4 — Il pollaio
Piattaforme e ostacoli a tema pollaio (mangiatoie, cassette, gabbia da cui scappare) e un'uscita che completa il livello. Grafica ancora segnaposto. È il tutorial mascherato: insegna solo a camminare e saltare.
**STOP:** il livello si completa dall'inizio alla fine.

### Tappa 5 — Chicchi e primo nemico
Chicchi di mais da raccogliere con un contatore, e un primo nemico buffo e lento. Se il pulcino viene toccato, riparte dall'ultimo punto sicuro: niente punizioni pesanti.
**STOP:** il livello è divertente così com'è.

### Tappa 6 — Grafica vera
Solo ora si sostituiscono i segnaposto con la grafica del pulcino e del pollaio. Prima di iniziare, proponimi lo stile e come produrre le immagini.
**STOP:** fine del livello 1.

## Tappe della mappa

### Tappa 7 — Più livelli e salvataggio
Il gioco passa da un livello solo a tanti.
- Finire un livello riporta alla mappa (per ora una schermata provvisoria) e sblocca il livello successivo.
- I livelli già finiti si possono sempre rigiocare.
- Il telefono ricorda i livelli sbloccati e il record di chicchi di ogni livello, anche chiudendo il browser.

**STOP:** finisco il pollaio, chiudo il browser, lo riapro e il progresso c'è ancora.

I luoghi sbloccati ma non ancora costruiti restano nella nebbia. Finito l'ultimo livello costruito, il messaggio di fine dice: «Per ora il viaggio si ferma qui: nuovi luoghi in arrivo!».

### Tappa 8 — La mappa disegnata
La fattoria vista dall'alto, in stile cartoon, con un sentiero che collega i dieci luoghi.
- Il pulcino cammina lungo il sentiero fino al luogo scelto.
- I luoghi non ancora sbloccati sono coperti dalla nebbia.
- Sotto ogni luogo finito si vede il record di chicchi (per esempio 17 / 20).
- Comandi: frecce per spostarsi e salto per entrare; sul telefono si può anche toccare direttamente il luogo.

Prima di iniziare, mostrami un bozzetto.
**STOP:** la mappa è chiara e si usa bene dal telefono.

## Tappe del livello 2 (cortile)

Nel cortile il pulcino impara la **beccata**, che serve a rompere ostacoli (sacchi di mangime, balle di paglia, gusci…) per aprire passaggi o far uscire chicchi. La beccata non ha effetto sui nemici.

Il nemico nuovo è l'**oca arrabbiata**: starnazza, abbassa il collo e carica di corsa in linea retta. Si schiva saltando, e se sbatte contro qualcosa resta stordita.

### Tappa 9 — La beccata
Nuova azione di input `peck`, usata sia dalla tastiera sia dal pulsante a schermo.
- Sul PC si becca con il tasto X.
- Sul telefono c'è un nuovo pulsante accanto al salto.
- L'animazione è esagerata: il pulcino si sbilancia in avanti col becco e fa un verso buffo. Si può beccare anche in aria.
- Gli ostacoli rompibili vanno in pezzi che volano via.
- Si prova in una piccola area di prova.

**STOP:** la beccata è piacevole da usare e il nuovo pulsante è comodo sul telefono.

### Tappa 10 — Il cortile
Il livello del cortile: più grande e più in verticale del pollaio.
- Insegna la beccata un passo alla volta: prima un ostacolo da rompere per passare, poi ostacoli in alto, poi la beccata in aria.
- Ci sono chicchi, nidi e un'uscita.
- Si disegna subito nello stile cartoon già scelto, ma prima di disegnarli mostrami i pezzi nuovi del cortile.

**STOP:** il livello si completa dall'inizio alla fine ed è divertente.

### Tappa 11 — L'oca arrabbiata
L'oca, con le sue animazioni esagerate e i suoi versi, sistemata nel cortile dove rende il livello più vivo senza frustrare. Se tocca il pulcino, lui riparte dall'ultimo nido, come con il topo.
**STOP:** l'oca è buffa e la difficoltà è giusta.

### Crescita del pulcino (scelta da Riccardo)
Il pulcino cresce a tappe lungo tutto il viaggio, a piccoli passi. Ogni stadio aggiunge qualcosa al precedente. Nei livelli l'aspetto dipende dal livello che si sta giocando; sulla mappa, da quanto si è andati avanti.

| Stadio | Livelli | Aspetto |
|---|---|---|
| 1 | pollaio | batuffolo tondo, ciuffetto, alucce corte |
| 2 | cortile, orto | ciuffo grande a tre riccioli, ala con le prime penne a punta, codina di piume, zampe un po' più lunghe |
| 3 | prato, bosco | in più: piumette chiare sul dorso, giallo più caldo, corpo un po' più grande |
| 4 | stagno, collina | in più: una piccola cresta rossa, ali più lunghe, colore che schiarisce verso il crema |
| 5 | grotta, paese | quasi pollo: corpo ovale color crema, cresta più grande, piccoli bargigli, coda di penne |
| 6 | campanile | giovane pollo con cresta, bargigli e coda (il disegno «alla fine del viaggio» dell'anteprima) |

I disegni di ogni stadio si fanno quando si costruisce il primo livello in cui compare.

### Tappa 12 — Il pulcino cresce
Dopo il pollaio il pulcino cresce un po': proponimi il nuovo aspetto (per esempio ciuffo più grande o prime piume sulle ali). L'aspetto dipende da quanto è avanti nel gioco e si vede sia nella mappa sia nel cortile.
**STOP:** fine del livello 2.

## Tappe del livello 3 (orto)

Nell'orto il pulcino impara il **doppio salto**: un secondo salto a mezz'aria, con un battito d'ali buffo e un verso. Si usa lo stesso pulsante del salto, quindi non serve un pulsante nuovo. Le abilità imparate restano: nell'orto si può ancora beccare.

Il nemico nuovo è la **talpa dispettosa**: spunta all'improvviso dalle buche nel terreno con un «bu!» e si rintana. Bisogna passare quando è sotto terra.

La novità dell'orto sono le **piante che si piegano**: girasoli e canne del mais su cui si atterra, che si piegano sotto il peso e fanno rimbalzare un po', come trampolini morbidi.

Il pulcino resta allo stadio 2 di crescita, come nel cortile.

### Tappa 13 — Il doppio salto
Il secondo salto si fa premendo di nuovo salto mentre si è in aria, una sola volta prima di toccare terra.
- L'animazione è esagerata: ali che sbattono forte, un piccolo sbuffo di piume e un verso.
- È disponibile solo dai livelli in cui il pulcino l'ha imparato.
- Si prova in una piccola area di prova, come per la beccata.

**STOP:** il doppio salto è piacevole e si controlla bene, anche dal telefono.

### Tappa 14 — L'orto
Il livello dell'orto, con le piante che si piegano.
- Insegna il doppio salto un passo alla volta: prima un ostacolo alto un po' più di un salto normale, poi salti più lunghi, poi il doppio salto partendo da una pianta che rimbalza.
- Ci sono chicchi, nidi e un'uscita, e qualche ostacolo da beccare per non dimenticare la beccata.
- Si disegna subito nello stile cartoon, ma prima di disegnarli mostrami i pezzi nuovi dell'orto.

**STOP:** il livello si completa dall'inizio alla fine ed è divertente.

### Tappa 15 — La talpa dispettosa
La talpa, con le sue animazioni esagerate e il suo «bu!», sistemata nell'orto dove rende il livello più vivo senza frustrare. Si vede un attimo prima da dove sta per spuntare, per esempio dalla terra che si muove. Se tocca il pulcino, lui riparte dall'ultimo nido.
**STOP:** fine del livello 3.
