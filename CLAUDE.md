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

Struttura: livelli separati scelti da una mappa, ognuno sblocca il successivo. Undici livelli previsti: pollaio, cortile, orto, magazzino filati, prato, bosco, stagno, collina rocciosa, temporale o grotta, paese degli umani, campanile/tetto finale.

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
- **Stile finale (scelto da Riccardo):** i disegni SVG sono le sorgenti; il gioco usa le immagini PNG accanto, create da `strumenti/stile_finale.py` (da rilanciare dopo ogni disegno nuovo o cambiato). Lo strumento raffina (contorni più sottili e del colore dell'oggetto, colori un po' più morbidi) e dipinge ombre e luci: dall'alto per i personaggi (così restano giuste quando si voltano), da in alto a sinistra per gli oggetti fermi. Gli SVG non vengono esportati.
- **Profondità e luce:** paesaggio a strati che scorrono a velocità diverse (parallasse), raggi di sole o fasci di luce, pollini o polvere nell'aria, ombre a terra sotto i personaggi e luce calda ai bordi (`scripts/atmosfera.gd`); sulla mappa, ombre delle nuvole e degli alberi.
- **Livelli sempre più ricchi (scelta di Riccardo):** ogni livello nuovo è più lungo ed elaborato del precedente: più tratti, più segreti e percorsi alternativi, più combinazioni delle abilità imparate.
- **Inquadratura:** telecamera con zoom 0.7, perché il pulcino si veda bene sul telefono.
- **Animazioni e suoni:** schiaccia-e-allunga, polvere, versi buffi. I suoni sono segnaposto sintetici creati da `strumenti/genera_suoni.py`.
- **Testi:** font Fredoka (licenza OFL, in `assets/font/`).
- **Modalità dipinta (in prova):** un selettore sulla mappa, accanto a «Crediti» («Stile: Cartoon / Dipinto»; solo lì, non nel menu di pausa), scambia i disegni con versioni ridipinte a pennellate da `strumenti/ridipingi.py` (stile «delicato»), salvate in `assets/dipinto/`. Il telefono ricorda la scelta. Per ora c'è solo nel cortile; lo stile predefinito resta il cartoon.
- **Conta solo finire il livello (regola di Riccardo):** uovo d'oro, chicchi, stelline, borsellino e record si salvano solo quando il pulcino arriva all'uscita. Se esci prima (pausa → mappa, o chiudi il gioco) non resta niente di quella partita.
- **Telefono a schermo intero:** sul telefono, al primo tocco il gioco va a schermo intero e in orizzontale (dove il browser lo permette; su iPhone si ottiene aggiungendo il gioco alla schermata Home). L'avviso di Chrome «per uscire dallo schermo intero…» non si può togliere da una pagina: per questo il gioco è anche **installabile come app** (scelta di Riccardo): `versione_web.py` scrive `docs/manifest.json` (schermo intero, orizzontale), le icone e `docs/aiutante.js` (un service worker che non tiene niente in memoria). Aperto dall'icona sulla schermata Home parte già a schermo intero, senza avviso, e non chiede lo schermo intero. A gioco caricato, sul telefono compare in alto un invito a installarlo (pagina_caricamento.html): su Android «Gioca come un'app!» con Installa / Non ora (apre la finestra di installazione di Chrome); su iPhone spiega «Condividi → Aggiungi alla schermata Home». Dopo «Non ora» non ricompare per 7 giorni; se il gioco è già installato non compare mai.
- **Pubblicazione:** dopo ogni modifica il gioco va esportato in `docs/` e caricato su GitHub. Si gioca su https://ricky80l.github.io/pulcino-libero/. Subito dopo l'esportazione si lancia sempre `python strumenti/versione_web.py`: dà al pacchetto del gioco un nome con l'impronta del contenuto (`index-xxxxxxxxxx.pck`), così il telefono scarica subito la versione nuova ma riusa quella in memoria se non è cambiata (scelta di Riccardo, "modo 2").

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
La fattoria vista dall'alto, in stile cartoon, con un sentiero che collega i luoghi del viaggio.
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
| 2 | cortile, orto, magazzino filati | ciuffo grande a tre riccioli, ala con le prime penne a punta, codina di piume, zampe un po' più lunghe |
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

## Tappe del livello 4 (Maglificio Granada, il magazzino filati)

Il pulcino entra nel **Maglificio Granada** (così si chiama il luogo sulla mappa), un magazzino di filati ispirato a quello vero di Riccardo: pareti di mattoni a due colori con gli oblò, soffitto di lamiera con i lucernari, scaffali blu pieni di coni di filato, colonne di scatoloni sui bancali, un transpallet arancione, il portone sezionale e il **soppalco azzurro** con la ringhiera. Sulle scatole niente marchi veri: solo scritte inventate.

Qui non si impara un'abilità nuova. La novità sono **quattro operatori** in camice blu che aiutano il pulcino: ci si salta sulle mani e lo lanciano **in alto** (sopra le colonne di scatoloni, fino al soppalco) o **in avanti** (oltre un varco). **Ognuno ha la sua mossa**, esagerata e buffa:

- **operatore italiano moro:** la «bagher», mani unite come a pallavolo, lancio dritto verso l'alto (il più alto);
- **operatore italiano biondo:** il «tiro a canestro», lancio ad arco lungo in avanti;
- **operatore indiano:** la «catapulta», si piega e lancia in diagonale verso l'alto, ottimo per salire sul soppalco;
- **operatore marocchino con i capelli ricci:** la «giravolta», gira su se stesso e lancia lontanissimo in orizzontale.

Gli operatori sono disegnati con rispetto e senza caricature: si distinguono per capelli, carnagione e piccoli dettagli. Esultano con versi in italiano («Op-là!», «Vai!», «Su!»).

Il nemico nuovo sono i **coni di filato che rotolano**: cadono dal soppalco o dagli scaffali e rotolano sul pavimento srotolando il filo. Si saltano. Se un cono tocca il pulcino, lui riparte dall'ultimo nido. Le abilità imparate restano: si becca e si fa il doppio salto.

Il pulcino resta allo stadio 2 di crescita, come nel cortile e nell'orto.

In fondo al magazzino, davanti al portone, c'è un **furgone azzurro** (come quello della foto di Riccardo, senza marchi) con il portellone aperto: ci si sale sul tetto, dove ci sono dei chicchi. Accanto c'è il suo **autista**, moro, robusto con un filo di pancia: si gratta la pancia, saluta, guarda l'orologio e si sorprende quando il pulcino gli passa vicino («Ehi, pulcino!»).

### Tappa 16 — Gli operatori
I quattro operatori con il camice blu, ognuno con la sua mossa, animati in modo esagerato (si piegano, caricano il lancio, esultano). Si provano in una piccola area di prova, come per la beccata.
Prima di disegnarli mostrami i bozzetti.
**STOP:** i lanci sono divertenti e si controllano bene, anche dal telefono.

### Tappa 17 — Il magazzino
Il livello del magazzino, più grande e più in verticale dell'orto, con il soppalco azzurro.
- Insegna i lanci un passo alla volta: prima un lancio in alto su una colonna di scatoloni, poi un lancio in avanti oltre un varco, poi due lanci di fila fino al soppalco.
- Ci sono chicchi, nidi e un'uscita (il portone), e qualche scatolone da beccare.
- Sulla mappa compare il nuovo luogo, il magazzino, al quarto posto dopo l'orto; il prato e gli altri luoghi slittano di un posto.
- Prima di disegnarli mostrami i pezzi nuovi del magazzino.

**STOP:** il livello si completa dall'inizio alla fine ed è divertente.

### Tappa 18 — I coni di filato che rotolano
I coni di filato che cadono e rotolano, con il filo che si srotola dietro di loro, sistemati nel magazzino dove rendono il livello più vivo senza frustrare. Si vede un attimo prima da dove arrivano, per esempio un cono che traballa sullo scaffale.
**STOP:** fine del livello 4.

## Tappe di rifacimento: livelli più lunghi ed elaborati (scelta di Riccardo)

Dal primo luogo in poi i livelli crescono decisamente: pollaio circa 5.500, cortile 6.500, orto 7.500, Maglificio Granada 8.500, e i luoghi seguenti ancora di più (circa +1.000 a luogo). Più tratti, percorsi alternativi (una strada alta più difficile con più chicchi e una bassa più facile), piccole zone segrete, gli stessi personaggi e oggetti in combinazioni nuove. Restano uova d'oro, stelline, operatori, furgone e tutto il resto (le uova si spostano se serve).
Per ogni luogo: prima mostrami tutto il percorso nuovo visto dall'alto, poi costruiscilo.

### Tappa R1 — Il pollaio più lungo
**STOP:** il pollaio nuovo è più ricco ma resta un tutorial gentile (solo camminare e saltare).

### Tappa R2 — Il cortile più lungo
**STOP:** il cortile nuovo è più lungo, più vario e si completa bene.

### Tappa R3 — L'orto più lungo
**STOP:** l'orto nuovo è più lungo, più vario e si completa bene.

### Tappa R4 — Il Maglificio Granada più lungo
**STOP:** il Maglificio nuovo è più lungo, più vario e si completa bene.

## Tappe per un viaggio più intrigante (scelte da Riccardo, prima del prato)

Quattro novità che danno voglia di esplorare, rigiocare e arrivare alla fine. Valgono per i luoghi già fatti e per tutti quelli futuri.

### Tappa 21 — Le uova d'oro segrete
In ogni luogo c'è un **uovo d'oro** nascosto: dietro un muro da beccare, in cima a un posto difficile, in una stanzetta segreta. Prenderlo fa una festa di scintille e un verso speciale. Il telefono ricorda quali uova hai trovato; sulla mappa, sotto il cartello di ogni luogo, si vede l'uovo vuoto o pieno.
Prima di nasconderle, mostrami dove le metto in ogni luogo.
**STOP:** le uova sono difficili da trovare ma non impossibili, e trovarle dà soddisfazione.

### Tappa 22 — Obiettivi e stelline
Ogni livello ha **tre stelline** facoltative: tutti i chicchi, l'uovo d'oro, finire senza farsi prendere. Il messaggio di fine livello mostra le stelline prese, una alla volta con un suono; sotto ogni stella un disegnino (chicco, uovo, musetto del nemico del luogo) e cosa è successo davvero («26 su 29 chicchi, ne mancano 3», «Uovo trovato!», «Preso 2 volte»), così si capisce anche alla prima partita; sulla mappa si vedono le migliori ottenute in ogni luogo.
**STOP:** le stelline sono chiare e fanno venire voglia di rigiocare.

### Tappa 23 — Chicchi da spendere
I chicchi raccolti in ogni partita si mettono da parte nel **borsellino** del pulcino. Sulla mappa c'è una **bancarella** dove si spendono per gli **accessori** del pulcino (per esempio cappellino di paglia, berretto, fiocco, sciarpa, occhiali), che poi si vedono addosso a lui in ogni luogo e a ogni stadio di crescita. Niente soldi veri: solo chicchi.
Prima di disegnarli mostrami gli accessori e la bancarella.
**STOP:** comprare e indossare gli accessori è facile e divertente.

### Tappa 24 — Le piume misteriose
Alla fine di ogni luogo il pulcino trova una **piuma misteriosa**, sempre più grande, di qualcuno che lo aspetta al campanile. Una breve scena senza parole sulla mappa (pochi secondi, si può saltare) racconta il ritrovamento; le piume raccolte si vedono sulla mappa e tracciano la strada verso il campanile. Il mistero si scopre solo alla fine del viaggio.

**Scelta di Riccardo:** alla fine del viaggio c'è una **pulcina**. Entra nella storia a poco a poco attraverso elementi visivi, luogo dopo luogo (per esempio le sue piume, un fiocco, impronte, una sagoma lontana), senza mai mostrarsi del tutto prima del campanile.
Prima di farle, mostrami la storia scena per scena.

**Storia scelta (Riccardo):** la pulcina è **crema con la punta delle piume rosa**; il suo segno è un **fiocco rosa lavorato a maglia** (diverso dal fiocco della bancarella), fatto col filo del Maglificio. La piuma si trova da sola all'uscita (conta solo finendo il livello); la scena sulla mappa (circa 4 secondi, si salta con un tocco, una volta sola per luogo) fa volare la piuma lungo il sentiero, dove resta posata: piume sempre più grandi, una scia verso la nebbia del campanile. Indizi luogo per luogo:
1. pollaio: piuma piccolissima impigliata nella rete, sulla buca d'uscita;
2. cortile: impronte piccole nel fango davanti al cancelletto, verso l'orto;
3. orto: un filo rosa impigliato al cancelletto d'uscita (tutti gli indizi stanno vicino all'uscita, dove si passa per forza);
4. Maglificio: il fiocco a maglia sul tetto del furgone, l'autista lo indica sorpreso;
5. prato: sagoma lontana su una collina; 6. bosco: un pigolio lontano che risponde; 7. stagno: il riflesso del fiocco nell'acqua; 8. collina: la sagoma più vicina saluta controluce; 9. grotta: disegno di due pulcini sulla roccia; 10. paese: un'ombra che corre sul muro verso il campanile; 11. campanile: lei, finalmente (da decidere).
Per ora si fanno i luoghi 1–4; gli altri insieme ai loro livelli.
**Come si capisce che sono indizi:** tutto quello che è della pulcina è crema e rosa (nient'altro nel gioco è rosa) e luccica piano di rosa; quando il pulcino ci passa vicino frena un istante, gli spunta un «?» rosa e fa «pio?» (suono `curioso`); sulla mappa la piuma si posa insieme al suo indizio. Indizi nei livelli: `scripts/indizio_pulcina.gd` (parametro `indizi` di `livelli.py`); scena e scia sulla mappa in `mappa.gd`; `Progressi.piume` / `piume_viste`. Un luogo nuovo con la piuma va aggiunto a `Progressi.LUOGHI_CON_PIUMA`.
**STOP:** le scene sono brevi, poetiche e fanno venire voglia di andare avanti.

## Tappe del livello 5 (prato)

Il pulcino esce all'aperto in un grande prato in una **giornata di sole** di primavera: fiori colorati, farfalle, cielo azzurro e colline lontane. È il primo luogo dello **stadio 3** di crescita (vedi la tabella «Crescita del pulcino»).

Nel prato il pulcino impara la **planata**: mentre scende, tenendo premuto salto apre le ali e scende piano, planando lontano. Si usa lo stesso pulsante del salto. Le abilità imparate restano: si becca e si fa il doppio salto (si può fare il doppio salto e poi planare).

La novità del prato sono i **soffioni e le correnti d'aria**:
- **correnti d'aria:** colonne di vento con petali e semi che girano verso l'alto; se il pulcino ci plana dentro, lo sollevano, così arriva in posti alti;
- **soffioni giganti:** beccandoli, i semi volano via e creano per qualche secondo una corrente d'aria in quel punto.

Il nemico nuovo è l'**ape ronzante**: vola avanti e indietro tra i fiori seguendo il suo giro, con un ronzio buffo che si sente solo da vicino. Non insegue il pulcino: si passa sotto o sopra quando è lontana. Se tocca il pulcino, lui riparte dall'ultimo nido.

### Tappa 19 — Il pulcino cresce ancora
Lo stadio 3: piumette chiare sul dorso, giallo più caldo, corpo un po' più grande. Si vede dal prato in poi e sulla mappa quando il prato è raggiunto.
Prima di disegnarlo mostrami un bozzetto accanto agli stadi 1 e 2.
**STOP:** il nuovo aspetto mi piace.

### Tappa 20 — La planata
Tenendo premuto salto mentre scende, il pulcino apre le ali e plana.
- L'animazione è buffa: ali spalancate che fremono, piumette che si arruffano, un «frrr» leggero.
- Mentre plana scende piano e si controlla bene a destra e a sinistra; lasciando il tasto ricade normalmente.
- Compare l'avviso «Nuova abilità!» con le istruzioni, come per la beccata e il doppio salto.
- È disponibile solo dai livelli in cui il pulcino l'ha imparata. Si prova in una piccola area di prova.

**STOP:** la planata è piacevole e si controlla bene, anche dal telefono.

### Tappa 25 — Il prato
Il livello del prato, con le correnti d'aria e i soffioni giganti.
- Insegna la planata un passo alla volta: prima una discesa planando oltre un fosso, poi una corrente d'aria che porta in alto, poi un soffione da beccare per crearsi la corrente da soli.
- Ci sono chicchi, nidi e un'uscita, e qualche ostacolo da beccare e da superare col doppio salto per non dimenticarli.
- Prima di disegnarli mostrami i pezzi nuovi del prato.

**STOP:** il livello si completa dall'inizio alla fine ed è divertente.

**Com'è fatto (Tappa 25):** `scenes/livello_5.tscn` da `strumenti/genera_livello5.py`, lungo circa 9.500, al posto dell'area di prova della planata (tolta). Pezzi nuovi in `assets/grafica/prato/` (`disegni_prato.py`): sasso col muschio e tronco caduto (si sale sopra; le rupi sono colonne di sassi tutti larghi uguali: **dove serve la corrente non ci devono essere gradini per arrampicarsi**, regola di Riccardo), fascina da beccare (rompibile), fiori, soffione, sagoma della pulcina. Le **correnti d'aria** (`scripts/corrente.gd`) sollevano chi ci sta dentro tenendo premuto salto, anche se ci arriva planando (`player.in_corrente`); il **soffione** (`scripts/soffione.gd`) beccato fa nascere una corrente per 7 secondi e poi ricresce. In cima a una corrente il «frrr» della planata non si ripete (`player.senza_planare`). Fossi e ruscello sono d'acqua. Uovo d'oro in alto sopra il ruscello, raggiungibile dalla corrente del soffione dell'isolotto. Indizio della pulcina: la sua sagoma spunta un attimo sulla collinetta prima dell'uscita, poi la piuma. I chicchi in volo stanno sulle traiettorie registrate.

### Tappa 26 — L'ape ronzante
L'ape, con le sue animazioni esagerate e il suo ronzio, sistemata nel prato dove rende il livello più vivo senza frustrare. Il suo giro si vede bene e il ronzio avvisa quando è vicina. Se tocca il pulcino, lui riparte dall'ultimo nido.
**STOP:** fine del livello 5.
