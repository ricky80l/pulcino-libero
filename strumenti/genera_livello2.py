# Genera la scena del livello 2 (il cortile): scenes/livello_2.tscn
# Uso: python strumenti/genera_livello2.py scenes/livello_2.tscn
# Insegna la beccata un passo alla volta: un sacco a terra, una balla da 2 beccate,
# una salita facoltativa sui tetti del fienile, un sacco da beccare saltando, l'abbeveratoio con l'oca.
# Versione lunga (Tappa R2), circa 6.500: poi due strade (in alto sui tetti del secondo fienile, in basso
# con la terza oca), il varco alto da beccare stando sui ceppi, i vasi, l'ultima oca tra abbeveratoio e
# steccato, la balla davanti all'ultima palizzata e il cancelletto.
import sys
from livelli import *

LARGO = 6500

NON_SOLIDO = {"solido": "false", "z_index": "-5"}

pezzi = [
    # sfondo
    # il paesaggio lontano (cielo, colline, cascina, siepi) ora è a strati: vedi atmosfera="cortile" qui sotto
    ("Fienile", 2240, 400, 280, 240, FIE, {"solido": "false", "z_index": "-8"}),
    ("Fienile2", 4420, 400, 280, 240, FIE, {"solido": "false", "z_index": "-8"}),
]
# steccato bianco sullo sfondo, all'inizio e alla fine
for i, x in enumerate(list(range(0, 700, 120)) + list(range(3300, 3980, 120)) + list(range(5180, 6500, 120))):
    pezzi.append((f"SteccatoFondo{i + 1}", x, 580, 120, 60, STE, NON_SOLIDO))

pezzi += [
    # terra e bordi
    ("Terra", 0, 640, LARGO + 40, 80, TER, {}),
    ("MuroSinistro", -40, 0, 40, 720, LEG, {}),
    ("MuroDestro", LARGO, 0, 40, 720, LEG, {}),
    # 1: palizzata con un buco in basso, chiuso da un sacco (beccata a terra)
    ("Palizzata1", 700, 0, 40, 568, LEG, {}),
    # botte e carretto con la tettoia sopra
    ("Botte1", 900, 565, 60, 75, BOT, {}),
    ("Carretto1", 1250, 540, 180, 100, CAR, {}),
    ("TettoiaCarretto", 1300, 410, 160, 32, TET, {"attraversabile_da_sotto": "true"}),
    # 2: palizzata chiusa da una balla di paglia (2 beccate)
    ("Palizzata2", 1550, 0, 40, 572, LEG, {}),
    # salita facoltativa sui tetti del fienile, piena di chicchi
    ("Ceppi1", 1850, 560, 120, 80, CEP, {}),
    ("Carretto2", 1990, 540, 180, 100, CAR, {}),
    ("Tettoia1", 2200, 440, 160, 32, TET, {"attraversabile_da_sotto": "true"}),
    ("Tettoia2", 2400, 330, 160, 32, TET, {"attraversabile_da_sotto": "true"}),
    ("Tettoia3", 2620, 230, 160, 32, TET, {"attraversabile_da_sotto": "true"}),
    # uovo d'oro segreto: trave sopra i tetti del fienile, in una nicchia chiusa da un sacco da beccare
    ("Trave", 2810, 100, 50, 16, LEG, {"attraversabile_da_sotto": "true"}),   # ci si atterra saltando dai tetti
    ("TraveNicchia", 2860, 100, 130, 16, LEG, {}),   # sotto la nicchia è piena: non si entra da sotto
    ("NicchiaTetto", 2860, -300, 130, 320, INV, {}),
    ("NicchiaFondo", 2990, -300, 20, 416, INV, {}),
    # 3: varco in alto chiuso da un sacco: si becca saltando, poi si sale sul gradino
    ("Muro3Alto", 3100, 0, 60, 490, LEG, {}),
    ("Muro3Basso", 3100, 560, 60, 80, LEG, {}),
    # ultimo tratto: abbeveratoio e steccato basso, con l'oca in mezzo
    ("Abbeveratoio", 3350, 585, 150, 55, ABB, {}),
    ("SteccatoBasso", 3760, 580, 120, 60, STE, {}),
    # 7: due strade. In alto: botte, carretto e i tetti del secondo fienile (più chicchi).
    #    In basso: la terza oca, tra il carretto e i ceppi
    ("Botte2", 4010, 565, 60, 75, BOT, {}),
    ("Carretto3", 4100, 540, 180, 100, CAR, {}),
    ("Tettoia4", 4300, 430, 160, 32, TET, {"attraversabile_da_sotto": "true"}),
    ("Tettoia5", 4520, 340, 160, 32, TET, {"attraversabile_da_sotto": "true"}),
    ("Tettoia6", 4760, 430, 160, 32, TET, {"attraversabile_da_sotto": "true"}),
    ("Ceppi2", 4700, 560, 120, 80, CEP, {}),
    # 8: varco alto da beccare stando sui ceppi, poi si sale sul gradino del muro
    ("Ceppi3", 4980, 560, 120, 80, CEP, {}),
    ("Muro5Alto", 5100, 0, 60, 420, LEG, {}),
    ("Muro5Basso", 5100, 490, 60, 150, LEG, {}),
    # 9: l'ultima oca tra il secondo abbeveratoio e il secondo steccato basso
    ("Abbeveratoio2", 5380, 585, 150, 55, ABB, {}),
    ("SteccatoBasso2", 5800, 580, 120, 60, STE, {}),
    # 10: ultima palizzata chiusa da una balla, poi il cancelletto aperto verso l'orto
    ("Palizzata6", 6000, 0, 40, 580, LEG, {}),
    ("Cancello", 6230, 540, 130, 100, CAN, {"solido": "false", "z_index": "-4"}),
]

rompibili = [
    (720, 640, SACCO, 1),
    (1060, 640, VASO, 1), (1120, 640, VASO, 1), (1180, 640, VASO, 1),
    (1570, 640, BALLA, 2),
    (3130, 560, SACCO, 1),
    (2900, 100, SACCO, 1),   # davanti all'uovo d'oro, sulla trave
    (5130, 490, SACCO, 1),   # il varco alto, beccato stando sui ceppi
    (5230, 640, VASO, 1), (5290, 640, VASO, 1),
    (6020, 640, BALLA, 2),   # davanti all'ultima palizzata
]

# oche arrabbiate: x di partenza, y a terra, quanto passeggiano verso destra
# ognuna ha un ostacolo a ogni lato, contro cui può sbattere caricando
oche = [(2450, 640, 300), (3560, 640, 140), (4320, 640, 260), (5560, 640, 160)]

chicchi = [
    (320, 610), (400, 610),                 # partenza
    (800, 610),                             # dietro il primo sacco
    (930, 530),                             # sulla botte
    (1060, 555), (1120, 555), (1180, 555),  # sopra i vasi
    (1290, 510), (1340, 510),               # sul carretto
    (1380, 380),                            # sulla tettoia del carretto
    (1650, 610),                            # dietro la balla
    (1880, 530),                            # sui ceppi
    (2280, 410), (2480, 300),               # tetti del fienile
    (2660, 200), (2740, 200),               # in cima
    (3200, 610),                            # dietro il sacco in alto
    (3420, 550),                            # sull'abbeveratoio
    (3820, 545),                            # sopra lo steccato basso
    (4040, 530),                            # sulla botte
    (4190, 505),                            # sul carretto
    (4380, 400), (4600, 310), (4840, 400),  # strada alta: tetti del secondo fienile
    (4450, 560),                            # strada bassa: sopra l'oca (si prende saltandola)
    (4760, 530),                            # sui ceppi
    (5040, 530),                            # sui ceppi davanti al varco
    (5180, 610),                            # dietro il varco
    (5230, 555), (5290, 555),               # sopra i vasi
    (5450, 550),                            # sul secondo abbeveratoio
    (5640, 500),                            # sopra l'ultima oca
    (5860, 545),                            # sopra il secondo steccato
    (6090, 610),                            # dietro la balla
    (6190, 610),                            # davanti al cancello
]

nidi = [(1720, 640), (2230, 640), (3230, 640), (3950, 640), (4950, 640), (5340, 640), (6120, 640)]

proprieta = {
    "numero": 2,
    "frase_fine": '"Hai attraversato il cortile!"',
    "beccata": "true",
    "abilita_nuova": '"beccata"',
}

scrivi_livello(sys.argv[1], "Livello2", "Cortile", pezzi, chicchi, nidi, rompibili=rompibili,
               uscita=(6320, 610), partenza=(200, 610), limite_destro=LARGO, proprieta_livello=proprieta,
               oche=oche, atmosfera="cortile", uovo=(2960, 100),
               # impronte piccole nel fango che passano il cancelletto verso l'orto, e la piuma
               indizi=[(6120, 656, "impronte", 1.0, {"numero_impronte": 7}), (6205, 640, "piuma", 0.75)])
