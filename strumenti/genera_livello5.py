# Genera la scena del livello 5 (il prato): scenes/livello_5.tscn
# Uso: python strumenti/genera_livello5.py scenes/livello_5.tscn
# Giornata di sole su un grande prato. Insegna la planata un passo alla volta:
# 1. dal mucchio di sassi si plana oltre un fosso largo (senza planare non si arriva);
# 2. una corrente d'aria fissa porta in alto, fino in cima a una rupe che col doppio salto non si raggiunge;
# 3. un soffione da beccare crea la corrente da soli, per salire su un'altra rupe.
# Poi: due strade (in basso tra fascine e tronchi; in alto in volo da una corrente all'altra, con più chicchi),
# il ruscello con l'isolotto e il suo soffione (in alto sopra l'acqua, nascosto, l'uovo d'oro),
# l'ultimo tratto tra tronchi e fascine, la pulcina lontana sulla collinetta, la piuma e il cancelletto.
# Lungo circa 9.500 (vedi CLAUDE.md, "Livelli sempre più ricchi").
import sys
from livelli import *

LARGO = 9500
DECORO = {"solido": "false", "z_index": "-4"}

pezzi = [
    # il prato, con tre fossi d'acqua e il ruscello
    ("PratoA", 0, 640, 1860, 80, ERB, {}),
    ("PratoB", 2400, 640, 1020, 80, ERB, {}),
    ("PratoC", 3900, 640, 720, 80, ERB, {}),
    ("PratoD", 5250, 640, 1500, 80, ERB, {}),
    ("Fosso1", 1860, 680, 540, 40, ACQ, {"solido": "false", "z_index": "-1"}),
    ("Fosso2", 3420, 680, 480, 40, ACQ, {"solido": "false", "z_index": "-1"}),
    ("Fosso3", 4620, 680, 630, 40, ACQ, {"solido": "false", "z_index": "-1"}),
    ("Ruscello", 6750, 680, 800, 40, ACQ, {"solido": "false", "z_index": "-1"}),
    ("PratoE", 7550, 640, LARGO - 7550 + 40, 80, ERB, {}),
    ("MuroSinistro", -40, 0, 40, 720, INV, {}),
    ("MuroDestro", LARGO, 0, 40, 720, INV, {}),

    # 1: fascina da beccare, un sasso, un tronco caduto e un'altra fascina
    ("Sasso1", 880, 575, 130, 65, SAS, {}),
    ("Tronco1", 1100, 588, 190, 52, TRO, {}),

    # 2: il mucchio di sassi, poi il primo fosso largo: si passa solo planando
    ("Mucchio1a", 1500, 560, 260, 80, SAS, {}),
    ("Mucchio1b", 1560, 460, 200, 100, SAS, {}),
    ("Mucchio1c", 1620, 360, 140, 100, SAS, {}),

    # 3: la prima corrente d'aria (qui sotto, Corrente1) e la rupe: col doppio salto non ci si arriva.
    #    Le rupi sono colonne di sassi tutti larghi uguali: nessun gradino scoperto su cui arrampicarsi
    ("Rupe1a", 3110, 540, 220, 100, SAS, {}),
    ("Rupe1b", 3110, 420, 220, 120, SAS, {}),
    ("Rupe1c", 3110, 300, 220, 120, SAS, {}),

    # 4: il soffione (qui sotto, Soffione1) e un'altra rupe, poi il terzo fosso
    ("Rupe2a", 4310, 540, 220, 100, SAS, {}),
    ("Rupe2b", 4310, 410, 220, 130, SAS, {}),
    ("Rupe2c", 4310, 290, 220, 120, SAS, {}),

    # 5: due strade. In basso: fascine, tronco e sasso. In alto: due correnti e i chicchi in cielo
    ("Tronco2", 5700, 588, 190, 52, TRO, {}),
    ("Sasso2", 5980, 560, 150, 80, SAS, {}),

    # 6: il ruscello: dal mucchio si plana sull'isolotto (col suo soffione), poi si salta dall'altra parte
    ("Mucchio2a", 6450, 560, 220, 80, SAS, {}),
    ("Mucchio2b", 6500, 450, 160, 110, SAS, {}),
    ("Isolotto", 7050, 575, 140, 145, SAS, {}),

    # 7: l'ultimo tratto, tranquillo
    ("Tronco3", 7800, 588, 190, 52, TRO, {}),
    ("Sasso3", 8300, 575, 130, 65, SAS, {}),
    ("Cancello", 9150, 540, 130, 100, CAN, {"solido": "false", "z_index": "-4"}),
]

# fiori sparsi nell'erba (solo decorazione)
for i, x in enumerate([330, 560, 1000, 1350, 2470, 2700, 3500, 4000, 4700, 5300, 5550, 6150, 7650, 8050, 8500, 8850, 9350]):
    pezzi.append((f"Fiori{i + 1}", x, 600, 80, 40, FIO, DECORO))

rompibili = [
    (720, 640, FASCINA, 1),
    (1340, 640, FASCINA, 1),
    (5500, 640, FASCINA, 1),
    (6270, 640, FASCINA, 2),
    (8060, 640, FASCINA, 1),
]

# soffioni: base dello stelo e quanto in alto porta la corrente che nasce beccandoli
soffioni = [
    (4150, 640, 460),
    (7120, 575, 450),   # sull'isolotto: porta fin lassù, dove è nascosto l'uovo d'oro
]

# correnti d'aria fisse: base al centro, larghezza, altezza
correnti = [
    (2900, 640, 110, 470),
    (5400, 640, 110, 430),
    (5950, 560, 110, 300),   # parte dal sasso della strada bassa: la strada alta atterra sul mucchio prima del ruscello
]

chicchi = [
    (300, 610), (380, 610),                                  # partenza
    (800, 610), (945, 545), (1195, 555), (1250, 555), (1420, 610),   # fascine, sasso, tronco
    (1540, 530), (1590, 430), (1690, 330),                   # su per il mucchio di sassi (sui gradini scoperti)
    (1945, 210), (2070, 255), (2200, 302), (2330, 350),      # la prima planata (sulla traiettoria vera)
    (2520, 610),
    (2900, 500), (2900, 380), (2900, 260),                   # nella prima corrente
    (3190, 270), (3270, 270),                                # in cima alla rupe
    (3500, 152), (3620, 196), (3740, 240),                   # planando oltre il secondo fosso
    (4040, 610),
    (4150, 420), (4150, 300),                                # nella corrente del soffione
    (4390, 260), (4470, 260),                                # in cima alla seconda rupe
    (4720, 150), (4900, 215), (5080, 281),                   # planando oltre il terzo fosso
    (5600, 610), (5795, 555), (6055, 525), (6380, 610),      # strada bassa
    (5400, 400), (5400, 250), (5600, 218), (5780, 284), (6010, 246), (6130, 200), (6300, 265),   # strada alta, in cielo
    (6475, 530), (6580, 420),                                # sul mucchio prima del ruscello (sui gradini scoperti)
    (6820, 296), (6940, 340), (7040, 376),                   # planando verso l'isolotto
    (7120, 400), (7120, 260),                                # nella corrente del soffione dell'isolotto
    (7380, 284), (7560, 322),                                # dall'isolotto all'altra riva
    (7700, 610), (7895, 555), (8150, 610), (8365, 545), (8600, 610), (8900, 610), (9240, 610),   # ultimo tratto
]

nidi = [(450, 640), (1430, 640), (2480, 640), (3960, 640), (5320, 640), (6400, 640), (7620, 640), (8600, 640)]

proprieta = {
    "numero": 5,
    "frase_fine": '"Hai attraversato il prato!"',
    "beccata": "true",
    "doppio_salto": "true",
    "planata": "true",
    "abilita_nuova": '"planata"',
}

scrivi_livello(sys.argv[1], "Livello5", "Prato", pezzi, chicchi, nidi, rompibili=rompibili,
               uscita=(9240, 610), partenza=(200, 610), limite_destro=LARGO, proprieta_livello=proprieta,
               atmosfera="prato", uovo=(7300, 130), soffioni=soffioni, correnti=correnti,
               # la pulcina lontana sulla collinetta e la piuma, vicino all'uscita
               indizi=[(8760, 640, "sagoma", 0.6), (9050, 640, "piuma", 1.25)])
