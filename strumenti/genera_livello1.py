# Genera la scena del livello 1 (il pollaio): scenes/livello_1.tscn
# Uso: python strumenti/genera_livello1.py scenes/livello_1.tscn
# È il tutorial mascherato: si cammina e si salta, niente altro. Versione lunga (Tappa R1), circa 5.500:
# gabbia di partenza, mangiatoia, scala di cassette, poi due strade (in alto sui posatoi con più chicchi,
# in basso col topo), il fosso, le mangiatoie a gradini col secondo topo, la salita sui posatoi fino al
# recinto (con l'uovo d'oro sulla mensola alta), le ultime cassette, la strada alta finale e la buca nella rete.
import sys
from livelli import *

LARGO = 5500
FINE_PARETE = 5015  # dove finisce il pollaio e comincia il prato fuori

# nome, x, y, larghezza, altezza, tipo, extra
pezzi = [
    # sfondo (decorazioni)
    ("ParetePollaio", 0, 0, FINE_PARETE, 720, PAR, {"solido": "false", "z_index": "-10"}),
    # fuori dall'uscita si vede il paesaggio a strati (atmosfera="pollaio" qui sotto)
    ("GabbiaSbarre", 316, 436, 368, 204, SBA, {"solido": "false", "z_index": "-5"}),
    # pavimento e muri
    ("PavimentoA", 0, 640, 2350, 80, PAV, {}),
    ("FondoFosso", 2350, 700, 160, 20, PAV, {}),
    ("PavimentoB", 2510, 640, FINE_PARETE - 2510, 80, PAV, {}),
    ("Prato", FINE_PARETE, 640, LARGO - FINE_PARETE, 80, ERB, {}),
    ("MuroSinistro", 0, 0, 40, 640, LEG, {}),
    ("MuroDestro", LARGO, 0, 40, 720, LEG, {}),

    # 1: gabbia di partenza: si esce saltando il bordo basso a destra
    ("GabbiaLato", 300, 420, 16, 220, SBA, {}),
    ("GabbiaTetto", 300, 420, 400, 16, SBA, {}),
    ("GabbiaBordoBasso", 684, 580, 16, 60, SBA, {}),
    # 2: mangiatoia da scavalcare
    ("Mangiatoia1", 900, 590, 180, 50, MAN, {}),
    # 3: scala di cassette
    ("Cassetta1", 1250, 560, 80, 80, CAS, {}),
    ("Cassetta2", 1330, 560, 80, 80, CAS, {}),
    ("Cassetta3", 1330, 480, 80, 80, CAS, {}),
    ("Cassetta4", 1410, 560, 80, 80, CAS, {}),
    ("Cassetta5", 1410, 480, 80, 80, CAS, {}),
    ("Cassetta6", 1410, 400, 80, 80, CAS, {}),
    # 4: due strade: in alto sui posatoi (più chicchi), in basso col topo; si ritrovano dopo
    ("PosatoioAlto1", 1570, 400, 140, 16, POS, {"attraversabile_da_sotto": "true"}),
    ("PosatoioAlto2", 1790, 360, 140, 16, POS, {"attraversabile_da_sotto": "true"}),
    ("PosatoioAlto3", 2010, 400, 140, 16, POS, {"attraversabile_da_sotto": "true"}),
    # 6: le mangiatoie a gradini, col secondo topo in mezzo
    ("Mangiatoia2", 2650, 590, 180, 50, MAN, {}),
    ("Cassetta7", 2860, 560, 80, 80, CAS, {}),
    ("Cassetta7b", 2960, 560, 80, 80, CAS, {}),
    ("Mangiatoia3", 2860, 510, 180, 50, MAN, {}),   # appoggiata sulle due cassette
    ("Cassetta8", 3220, 560, 80, 80, CAS, {}),   # gradino dopo il topo (una cassetta sola: si sale con un salto)
    # 7: posatoi in salita fino al recinto interno; sopra l'ultimo, la mensola alta con l'uovo d'oro
    ("Posatoio1", 3350, 540, 140, 16, POS, {"attraversabile_da_sotto": "true"}),
    ("Posatoio2", 3550, 440, 140, 16, POS, {"attraversabile_da_sotto": "true"}),
    ("Posatoio3", 3770, 340, 140, 16, POS, {"attraversabile_da_sotto": "true"}),
    ("Posatoio4", 3990, 260, 140, 16, POS, {"attraversabile_da_sotto": "true"}),
    ("Mensola", 3890, 120, 110, 16, LEG, {"attraversabile_da_sotto": "true"}),
    ("RecintoInterno", 4200, 300, 30, 340, LEG, {}),
    # 8: ultime cassette
    ("Cassetta10", 4400, 560, 80, 80, CAS, {}),
    ("Cassetta11", 4480, 560, 80, 80, CAS, {}),
    ("Cassetta12", 4480, 480, 80, 80, CAS, {}),
    # 9: strada alta finale, facoltativa, piena di chicchi, prima della rete
    ("Posatoio5", 4650, 470, 140, 16, POS, {"attraversabile_da_sotto": "true"}),
    ("Posatoio6", 4860, 400, 120, 16, POS, {"attraversabile_da_sotto": "true"}),
    # rete esterna con la buca in basso
    ("ReteEsterna", FINE_PARETE - 15, 0, 30, 580, RET, {}),
]

# chicchi di mais (centro)
chicchi = [
    (450, 520), (500, 610),                   # gabbia
    (692, 540), (800, 610),                   # uscita dalla gabbia
    (990, 555),                               # sulla mangiatoia
    (1290, 525), (1370, 445), (1450, 365),    # scala di cassette
    (1640, 365), (1860, 325), (2080, 365),    # strada alta sui posatoi
    (1760, 560), (1840, 560),                 # strada bassa, sopra il topo
    (2430, 670),                              # nel fosso
    (2740, 555), (2950, 475), (3260, 525),    # mangiatoie a gradini e cassetta dopo il topo
    (3370, 505), (3570, 405), (3790, 305), (4010, 225),   # posatoi
    (4215, 265),                              # sul recinto
    (4440, 525), (4520, 445),                 # ultime cassette
    (4720, 435), (4920, 365),                 # strada alta finale
    (4750, 610),                              # sotto la strada alta
    (4950, 610),                              # davanti alla buca
    (5250, 610),                              # fuori, sul prato
]
# nidi (centro, appoggiati a terra)
nidi = [(1160, 640), (2260, 640), (3330, 640), (4320, 640), (5120, 640)]
# topi: x di partenza, y a terra, distanza verso destra
topi = [(1650, 640, 260), (3055, 640, 140)]  # il secondo tra la mangiatoia rialzata e la cassetta

scrivi_livello(sys.argv[1], "Livello1", "Pollaio", pezzi, chicchi, nidi, topi,
               uscita=(5250, 610), partenza=(450, 610), limite_destro=LARGO, atmosfera="pollaio",
               uovo=(3945, 120))
