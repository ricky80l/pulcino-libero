# Genera l'area di prova della planata (Tappa 20): scenes/prova_planata.tscn
# Uso: python strumenti/genera_prova_planata.py scenes/prova_planata.tscn
# Due prove: si sale su un terrazzino di cassette e si plana oltre un fosso largo, poi di nuovo
# da un terrazzino più alto oltre un fosso ancora più largo. Senza planare non si arriva dall'altra parte.
# I pezzi del prato vero arrivano con la Tappa 21: qui si usano quelli già fatti.
import sys
from livelli import *

pezzi = [
    # prato con due fossi larghi
    ("PratoA", 0, 640, 900, 80, ERB, {}),
    ("PratoB", 1550, 640, 850, 80, ERB, {}),
    ("PratoC", 3150, 640, 850, 80, ERB, {}),
    ("MuroSinistro", -40, 0, 40, 720, INV, {}),
    ("MuroDestro", 4000, 0, 40, 720, INV, {}),
    # 1: scalini di cassette fino al terrazzino alto 300, poi il fosso largo 650
    ("Scalino1", 520, 540, 100, 100, CAS, {}),
    ("Scalino2", 620, 440, 100, 200, CAS, {}),
    ("Terrazzino1", 720, 340, 180, 32, TET, {"attraversabile_da_sotto": "true"}),
    ("Palo1", 880, 372, 20, 268, LEG, {"solido": "false", "z_index": "-6"}),
    # 2: di nuovo su, e il fosso largo 750
    ("Scalino3", 2050, 540, 100, 100, CAS, {}),
    ("Scalino4", 2150, 440, 100, 200, CAS, {}),
    ("Terrazzino2", 2250, 330, 150, 32, TET, {"attraversabile_da_sotto": "true"}),
    ("Palo2", 2380, 362, 20, 278, LEG, {"solido": "false", "z_index": "-6"}),
    ("Cancello", 3800, 540, 130, 100, CAN, {"solido": "false", "z_index": "-4"}),
]

chicchi = [
    (300, 610), (810, 310),
    (1050, 420), (1200, 470), (1350, 520), (1500, 570),     # lungo la planata sopra il primo fosso
    (2325, 300),
    (2550, 410), (2750, 460), (2950, 510), (3100, 560),     # lungo la planata sopra il secondo fosso
    (3500, 610),
]

nidi = [(250, 640), (1700, 640), (3300, 640)]

proprieta = {
    "numero": 5,
    "frase_fine": '"Hai imparato a planare!"',
    "beccata": "true",
    "doppio_salto": "true",
    "planata": "true",
    "abilita_nuova": '"planata"',
    "salva_progressi": "false",
}

scrivi_livello(sys.argv[1], "ProvaPlanata", "Prato", pezzi, chicchi, nidi,
               uscita=(3860, 610), partenza=(150, 610), limite_destro=4000, proprieta_livello=proprieta,
               atmosfera="cortile")
