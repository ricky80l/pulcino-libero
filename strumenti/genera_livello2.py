# Genera la scena del livello 2 (il cortile): scenes/livello_2.tscn
# Uso: python strumenti/genera_livello2.py scenes/livello_2.tscn
# Insegna la beccata un passo alla volta: un sacco a terra, una balla da 2 beccate,
# una salita facoltativa sui tetti del fienile, un sacco da beccare saltando, poi il cancelletto.
import sys
from livelli import *

NON_SOLIDO = {"solido": "false", "z_index": "-5"}

pezzi = [
    # sfondo
    ("Paesaggio", 0, 0, 4440, 720, FUO, {"solido": "false", "z_index": "-10"}),
    ("Fienile", 2240, 400, 280, 240, FIE, {"solido": "false", "z_index": "-8"}),
]
# steccato bianco sullo sfondo, all'inizio e alla fine
for i, x in enumerate(list(range(0, 700, 120)) + list(range(3300, 4100, 120))):
    pezzi.append((f"SteccatoFondo{i + 1}", x, 580, 120, 60, STE, NON_SOLIDO))

pezzi += [
    # terra e bordi
    ("Terra", 0, 640, 4440, 80, TER, {}),
    ("MuroSinistro", -40, 0, 40, 720, LEG, {}),
    ("MuroDestro", 4400, 0, 40, 720, LEG, {}),
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
    # 3: varco in alto chiuso da un sacco: si becca saltando, poi si sale sul gradino
    ("Muro3Alto", 3100, 0, 60, 490, LEG, {}),
    ("Muro3Basso", 3100, 560, 60, 80, LEG, {}),
    # ultimo tratto: abbeveratoio e steccato basso, con l'oca in mezzo
    ("Abbeveratoio", 3350, 585, 150, 55, ABB, {}),
    ("SteccatoBasso", 3760, 580, 120, 60, STE, {}),
    # il cancelletto aperto verso l'orto
    ("Cancello", 4130, 540, 130, 100, CAN, {"solido": "false", "z_index": "-4"}),
]

rompibili = [
    (720, 640, SACCO, 1),
    (1060, 640, VASO, 1), (1120, 640, VASO, 1), (1180, 640, VASO, 1),
    (1570, 640, BALLA, 2),
    (3130, 560, SACCO, 1),
]

# oche arrabbiate: x di partenza, y a terra, quanto passeggiano verso destra
# ognuna ha un ostacolo a ogni lato, contro cui può sbattere caricando
oche = [(2450, 640, 300), (3560, 640, 140)]

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
    (4050, 610),                            # davanti al cancello
]

nidi = [(1720, 640), (2230, 640), (3230, 640), (3950, 640)]

proprieta = {
    "numero": 2,
    "frase_fine": '"Hai attraversato il cortile!"',
    "beccata": "true",
}

scrivi_livello(sys.argv[1], "Livello2", "Cortile", pezzi, chicchi, nidi, rompibili=rompibili,
               uscita=(4220, 610), partenza=(200, 610), limite_destro=4400, proprieta_livello=proprieta,
               oche=oche)
