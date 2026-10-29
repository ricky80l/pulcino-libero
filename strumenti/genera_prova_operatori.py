# Genera l'area di prova degli operatori (Tappa 16): scenes/prova_operatori.tscn
# Uso: python strumenti/genera_prova_operatori.py scenes/prova_operatori.tscn
# Quattro prove in fila, una per operatore: la colonna di cassette (bagher), il fosso (canestro),
# il soppalco provvisorio (catapulta) e il fosso larghissimo (giravolta). I pezzi del magazzino vero
# arrivano con la Tappa 17: qui si usano quelli del cortile.
import sys
from livelli import *

NON_SOLIDO = {"solido": "false", "z_index": "-6"}

pezzi = [
    ("Paesaggio", 0, 0, 3600, 720, FUO, {"solido": "false", "z_index": "-10"}),
    # terreno con due fossi
    ("TerraA", 0, 640, 1150, 80, TER, {}),
    ("TerraB", 1500, 640, 950, 80, TER, {}),
    ("TerraC", 2950, 640, 650, 80, TER, {}),
    ("MuroSinistro", -40, 0, 40, 720, LEG, {}),
    ("MuroDestro", 3600, 0, 40, 720, LEG, {}),
    # 1: colonna di cassette alta 340: troppo per il doppio salto, ci vuole la bagher
    ("Cassetta1", 520, 572, 80, 68, CAS, {}),
    ("Cassetta2", 520, 504, 80, 68, CAS, {}),
    ("Cassetta3", 520, 436, 80, 68, CAS, {}),
    ("Cassetta4", 520, 368, 80, 68, CAS, {}),
    ("Cassetta5", 520, 300, 80, 68, CAS, {}),
    # 3: soppalco provvisorio, alto 310: ci si arriva con la catapulta
    ("Soppalco", 1900, 330, 400, 24, LEG, {"attraversabile_da_sotto": "true"}),
    ("Palo1", 1910, 354, 16, 286, LEG, NON_SOLIDO),
    ("Palo2", 2274, 354, 16, 286, LEG, NON_SOLIDO),
    ("Cancello", 3400, 540, 130, 100, CAN, {"solido": "false", "z_index": "-4"}),
]

operatori = [
    (450, 640, MORO, 1, 1),        # bagher: dritto in alto, poi si va verso la colonna
    (1080, 640, BIONDO, 1, 1),     # tiro a canestro oltre il primo fosso
    (1750, 640, INDIANO, 1, 1),    # catapulta fino al soppalco
    (2380, 640, MAROCCHINO, 1, 1), # giravolta oltre il fosso largo
]

chicchi = [
    (560, 270),                                # in cima alla colonna
    (1250, 430), (1350, 400),                  # sopra il primo fosso
    (2000, 300), (2100, 300), (2200, 300),     # sul soppalco
    (2650, 500), (2800, 520),                  # sopra il fosso largo
    (3250, 610),
]

nidi = [(250, 640), (1620, 640), (3050, 640)]

proprieta = {
    "numero": 4,
    "frase_fine": '"Hai provato tutti gli operatori!"',
    "beccata": "true",
    "doppio_salto": "true",
    "salva_progressi": "false",
}

scrivi_livello(sys.argv[1], "ProvaOperatori", "Magazzino", pezzi, chicchi, nidi,
               uscita=(3460, 610), partenza=(150, 610), limite_destro=3600, proprieta_livello=proprieta,
               operatori=operatori)
