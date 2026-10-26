# Genera l'area di prova del doppio salto (Tappa 13): scenes/prova_doppio_salto.tscn
# Uso: python strumenti/genera_prova_doppio_salto.py scenes/prova_doppio_salto.tscn
# Un muro troppo alto per un salto solo, una buca troppo larga, una tettoia molto in alto.
import sys
from livelli import *

pezzi = [
    ("Paesaggio", 0, 0, 2400, 720, FUO, {"solido": "false", "z_index": "-10"}),
    ("Prato1", 0, 640, 1000, 80, ERB, {}),
    ("Prato2", 1330, 640, 1070, 80, ERB, {}),
    ("MuroSinistro", -40, 0, 40, 720, LEG, {}),
    ("MuroDestro", 2400, 0, 40, 720, LEG, {}),
    # 1: muro alto 220: con un salto solo non si passa
    ("MuroAlto", 600, 420, 40, 220, LEG, {}),
    # 3: tettoia in alto, raggiungibile solo col doppio salto
    ("TettoiaAlta", 1600, 390, 160, 32, TET, {"attraversabile_da_sotto": "true"}),
]

chicchi = [(620, 390), (1165, 520), (1680, 360), (1900, 610)]
nidi = [(850, 640)]

proprieta = {
    "numero": 3,
    "frase_fine": '"Prova del doppio salto finita!"',
    "beccata": "true",
    "doppio_salto": "true",
    "abilita_nuova": '"doppio_salto"',
    "salva_progressi": "false",
}

scrivi_livello(sys.argv[1], "ProvaDoppioSalto", "Terreno", pezzi, chicchi, nidi,
               uscita=(2250, 610), partenza=(200, 610), limite_destro=2400, proprieta_livello=proprieta)
