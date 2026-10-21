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

## Tappe del livello 1 (pollaio)

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
