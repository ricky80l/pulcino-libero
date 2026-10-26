# Genera la scena del livello 1 (il pollaio): scenes/livello_1.tscn
# Uso: python strumenti/genera_livello1.py scenes/livello_1.tscn
import sys
from livelli import *

# nome, x, y, larghezza, altezza, tipo, extra
pezzi = [
    # sfondo (decorazioni)
    ("ParetePollaio", 0, 0, 3715, 720, PAR, {"solido": "false", "z_index": "-10"}),
    ("Fuori", 3715, 0, 525, 720, FUO, {"solido": "false", "z_index": "-10"}),
    ("GabbiaSbarre", 316, 436, 368, 204, SBA, {"solido": "false", "z_index": "-5"}),
    # pavimento e muri
    ("PavimentoA", 0, 640, 2000, 80, PAV, {}),
    ("FondoFosso", 2000, 700, 160, 20, PAV, {}),
    ("PavimentoB", 2160, 640, 1555, 80, PAV, {}),
    ("Prato", 3715, 640, 525, 80, ERB, {}),
    ("MuroSinistro", 0, 0, 40, 640, LEG, {}),
    ("MuroDestro", 4200, 0, 40, 720, LEG, {}),
    # gabbia di partenza: si esce saltando il bordo basso a destra
    ("GabbiaLato", 300, 420, 16, 220, SBA, {}),
    ("GabbiaTetto", 300, 420, 400, 16, SBA, {}),
    ("GabbiaBordoBasso", 684, 580, 16, 60, SBA, {}),
    # mangiatoia da scavalcare
    ("Mangiatoia1", 900, 590, 180, 50, MAN, {}),
    # scala di cassette
    ("Cassetta1", 1250, 560, 80, 80, CAS, {}),
    ("Cassetta2", 1330, 560, 80, 80, CAS, {}),
    ("Cassetta3", 1330, 480, 80, 80, CAS, {}),
    ("Cassetta4", 1410, 560, 80, 80, CAS, {}),
    ("Cassetta5", 1410, 480, 80, 80, CAS, {}),
    ("Cassetta6", 1410, 400, 80, 80, CAS, {}),
    # posatoi per superare il recinto interno
    ("Posatoio1", 2300, 540, 140, 16, POS, {"attraversabile_da_sotto": "true"}),
    ("Posatoio2", 2500, 440, 140, 16, POS, {"attraversabile_da_sotto": "true"}),
    ("Posatoio3", 2720, 340, 140, 16, POS, {"attraversabile_da_sotto": "true"}),
    ("Posatoio4", 2940, 260, 140, 16, POS, {"attraversabile_da_sotto": "true"}),
    ("RecintoInterno", 3150, 300, 30, 340, LEG, {}),
    # ultime cassette
    ("Cassetta7", 3350, 560, 80, 80, CAS, {}),
    ("Cassetta8", 3430, 560, 80, 80, CAS, {}),
    ("Cassetta9", 3430, 480, 80, 80, CAS, {}),
    # rete esterna con la buca in basso
    ("ReteEsterna", 3700, 0, 30, 580, RET, {}),
]

# chicchi di mais (centro)
chicchi = [
    (450, 520), (500, 610),            # gabbia
    (692, 540), (800, 610),            # uscita dalla gabbia
    (990, 555),                        # sulla mangiatoia
    (1290, 525), (1370, 445), (1450, 365),  # scala di cassette
    (1760, 560), (1810, 525), (1860, 560),  # arco sopra il topo
    (2080, 670),                       # nel fosso
    (2370, 505), (2570, 405), (2790, 305), (3010, 225),  # posatoi
    (3165, 265),                       # sul recinto
    (3390, 525), (3470, 445),          # ultime cassette
    (3600, 610),                       # davanti alla buca
]
# nidi (centro, appoggiati a terra)
nidi = [(1160, 640), (1560, 640), (2230, 640), (3270, 640)]
# topi: x di partenza, y a terra, distanza verso destra
topi = [(1680, 640, 240)]

scrivi_livello(sys.argv[1], "Livello1", "Pollaio", pezzi, chicchi, nidi, topi,
               uscita=(3900, 610), partenza=(450, 610), limite_destro=4200)
