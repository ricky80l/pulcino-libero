# Genera l'area di prova della beccata (Tappa 9): scenes/prova_beccata.tscn
# Uso: python strumenti/genera_prova_beccata.py scenes/prova_beccata.tscn
# Tre ostacoli in fila: un sacco da 1 beccata, una balla da 2, e un sacco in alto da beccare saltando.
import sys
from livelli import *

pezzi = [
    ("Paesaggio", 0, 0, 2400, 720, FUO, {"solido": "false", "z_index": "-10"}),
    ("Prato", 0, 640, 2400, 80, ERB, {}),
    ("MuroSinistro", -40, 0, 40, 720, LEG, {}),
    ("MuroDestro", 2400, 0, 40, 720, LEG, {}),
    # 1: palo alto con un varco in basso, chiuso da un sacco
    ("Palo1", 700, 0, 40, 568, LEG, {}),
    # 2: palo alto con un varco in basso, chiuso da una balla di paglia
    ("Palo2", 1150, 0, 40, 572, LEG, {}),
    # 3: varco in alto chiuso da un sacco: si becca saltando, poi si sale sul gradino
    ("Muro3Alto", 1650, 0, 60, 490, LEG, {}),
    ("Muro3Basso", 1650, 560, 60, 80, LEG, {}),
]

rompibili = [
    (720, 640, SACCO, 1),
    (1170, 640, BALLA, 2),
    (1680, 560, SACCO, 1),
]

chicchi = [(450, 610), (900, 610), (950, 610), (1400, 610), (1760, 610), (2000, 560)]

proprieta = {
    "numero": 2,
    "frase_fine": '"Prova della beccata finita!"',
    "beccata": "true",
    "salva_progressi": "false",
}

scrivi_livello(sys.argv[1], "ProvaBeccata", "Terreno", pezzi, chicchi, rompibili=rompibili,
               uscita=(2250, 610), partenza=(200, 610), limite_destro=2400, proprieta_livello=proprieta)
