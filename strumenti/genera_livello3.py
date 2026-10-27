# Genera la scena del livello 3 (l'orto): scenes/livello_3.tscn
# Uso: python strumenti/genera_livello3.py scenes/livello_3.tscn
# Insegna il doppio salto un passo alla volta: muretto di cassette, primo girasole che rimbalza,
# canale da saltare in lungo, zucca da beccare, pozzo, salita con mais e girasole fino a un tetto alto.
import sys
from livelli import *

NON_SOLIDO = {"solido": "false", "z_index": "-6"}

pezzi = [
    # sfondo e decorazioni
    ("Paesaggio", 0, 0, 4640, 720, FUO, {"solido": "false", "z_index": "-10"}),
    ("Spaventapasseri", 60, 460, 105, 180, SPA, NON_SOLIDO),
    ("Pomodori1", 400, 505, 65, 135, POM, NON_SOLIDO),
    ("Pomodori2", 470, 505, 65, 135, POM, NON_SOLIDO),
    ("Pomodori3", 4120, 505, 65, 135, POM, NON_SOLIDO),
    ("Fragole1", 950, 602, 85, 38, FRA, NON_SOLIDO),
    ("Fragole2", 1300, 602, 85, 38, FRA, NON_SOLIDO),
    ("Fragole3", 2700, 602, 85, 38, FRA, NON_SOLIDO),
    ("Fragole4", 4010, 602, 85, 38, FRA, NON_SOLIDO),
    ("Annaffiatoio", 3950, 592, 65, 48, ANN, NON_SOLIDO),
    ("Cancello", 4300, 540, 130, 100, CAN, {"solido": "false", "z_index": "-4"}),
    # terreno, con il canale d'irrigazione in mezzo
    ("TerraA", 0, 640, 1550, 80, TOR, {}),
    ("Acqua", 1550, 680, 300, 40, ACQ, {"solido": "false", "z_index": "-1"}),
    ("TerraB", 1850, 640, 2790, 80, TOR, {}),
    ("MuroSinistro", -40, 0, 40, 720, LEG, {}),
    ("MuroDestro", 4600, 0, 40, 720, LEG, {}),
    # 1: muretto di cassette alto 204: un salto solo non basta, con due tocchi del doppio salto si passa
    ("Cavolo1", 600, 594, 60, 46, CAV, {}),
    ("Cassetta1", 800, 572, 80, 68, CAS, {}),
    ("Cassetta2", 800, 504, 80, 68, CAS, {}),
    ("Cassetta3", 800, 436, 80, 68, CAS, {}),
    # 4: recinto con un buco in basso chiuso da una zucca (2 beccate)
    ("Cavolo2", 2000, 594, 60, 46, CAV, {}),
    ("Recinto", 2150, 0, 40, 576, LEG, {}),
    # 5: pozzo: la base è un ostacolo, sul tettuccio si sale col doppio salto
    ("Pozzo", 2450, 445, 150, 195, POZ, {"solido": "false", "z_index": "-2"}),
    ("PozzoBase", 2463, 575, 124, 65, INV, {}),
    ("PozzoTetto", 2485, 448, 80, 12, INV, {"attraversabile_da_sotto": "true"}),
    # 6: tetto alto raggiungibile rimbalzando sul girasole e col doppio salto; poi si scavalca il muro
    ("TettoAlto", 3200, 270, 160, 32, TET, {"attraversabile_da_sotto": "true"}),
    ("MuroFinale", 3460, 300, 40, 340, LEG, {}),
    # 7: carriola prima del cancelletto
    ("Carriola", 3800, 572, 115, 68, CRL, {}),
]

piante = [
    (1150, 640, GIRASOLE),   # il primo rimbalzo
    (2850, 640, MAIS),
    (3050, 640, GIRASOLE),
]

rompibili = [
    (2170, 640, ZUCCA, 2),
]

# talpe dispettose: centro della buca, a terra
talpe = [
    (700, 640),    # la prima, tra il cavolo e il muretto: si impara a conoscerla con calma
    (2410, 640),   # dopo la zucca, prima del pozzo
    (4170, 640),   # davanti al cancelletto
]

chicchi = [
    (300, 610), (360, 610),                    # partenza
    (840, 405),                                # in cima al muretto di cassette
    (1150, 380), (1150, 320), (1150, 260),     # colonna sopra il primo girasole
    (1700, 540),                               # sopra il canale
    (1950, 610),
    (2240, 610),                               # dietro la zucca
    (2505, 425), (2545, 425),                  # sul tettuccio del pozzo
    (2850, 400),                               # sopra il mais
    (3050, 380),                               # sopra il girasole
    (3250, 240), (3310, 240),                  # sul tetto alto
    (3480, 270),                               # sul muro finale
    (3700, 610),
    (3857, 545),                               # sulla carriola
    (4050, 560),                               # sopra le fragole
    (4240, 610),
]

nidi = [(1430, 640), (2300, 640), (2750, 640), (3650, 640)]

proprieta = {
    "numero": 3,
    "frase_fine": '"Hai attraversato l\'orto!"',
    "beccata": "true",
    "doppio_salto": "true",
    "abilita_nuova": '"doppio_salto"',
}

scrivi_livello(sys.argv[1], "Livello3", "Orto", pezzi, chicchi, nidi, rompibili=rompibili,
               uscita=(4380, 610), partenza=(200, 610), limite_destro=4600, proprieta_livello=proprieta,
               piante=piante, talpe=talpe)
