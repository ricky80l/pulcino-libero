# Genera la scena del livello 4 (il magazzino filati): scenes/livello_4.tscn
# Uso: python strumenti/genera_livello4.py scenes/livello_4.tscn
# Al chiuso, come nelle foto di Riccardo. Insegna i lanci degli operatori un passo alla volta:
# la bagher sopra una colonna di scatoloni, il tiro a canestro oltre la prima fossa, poi due lanci di fila
# (giravolta oltre la fossa larga, dritti nelle mani della catapulta) fino al soppalco azzurro; poi il portone.
# I coni di filato cadono dagli scaffali e rotolano: si saltano.
import sys
from livelli import *

DECORO = {"solido": "false", "z_index": "-6"}
LARGO = 5200

pezzi = [
    # il capannone: parete di mattoni con gli oblò, soffitto di lamiera, pavimento con due fosse
    ("Parete", 0, 0, LARGO, 720, MAT, {"solido": "false", "z_index": "-10"}),
    ("Soffitto", 0, 0, LARGO, 80, LAM, {"solido": "false", "z_index": "-9"}),
    ("PavimentoA", 0, 640, 1680, 80, CEM, {}),
    ("Fossa1", 1680, 640, 350, 80, FOS, {"solido": "false", "z_index": "-1"}),
    ("PavimentoB", 2030, 640, 620, 80, CEM, {}),
    ("Fossa2", 2650, 640, 650, 80, FOS, {"solido": "false", "z_index": "-1"}),
    ("PavimentoC", 3300, 640, 1900, 80, CEM, {}),
    ("MuroSinistro", -40, 0, 40, 720, INV, {}),
    ("MuroDestro", LARGO, 0, 40, 720, INV, {}),

    # 1: ingresso. Scaffale con i ripiani su cui si sale, pila di cartoni piatti, una scatola da beccare
    ("Scaffale1", 300, 370, 160, 270, SCF, DECORO),
    ("Ripiano1a", 305, 498, 150, 10, INV, {"attraversabile_da_sotto": "true"}),
    ("Ripiano1b", 305, 434, 150, 10, INV, {"attraversabile_da_sotto": "true"}),
    ("Ripiano1c", 305, 370, 150, 10, INV, {"attraversabile_da_sotto": "true"}),
    ("Estintore1", 480, 585, 25, 55, EST, DECORO),
    ("CartelloUscita", 520, 230, 55, 28, USC, DECORO),
    ("Cartoni1", 560, 525, 130, 115, CRT, {}),

    # 2: la colonna di scatoloni, troppo alta anche per il doppio salto: ci vuole la bagher
    ("Bancale1", 1080, 620, 120, 20, BAN, {}),
    ("Scatolone1a", 1085, 545, 110, 75, SCA, {}),
    ("Scatolone1b", 1090, 465, 100, 80, SCB, {}),
    ("Scatolone1c", 1080, 400, 120, 65, SCC, {}),
    ("Scatolone1d", 1085, 320, 110, 80, SCA, {}),
    ("Scaffale2", 1300, 370, 160, 270, SCF, DECORO),
    ("Ripiano2", 1305, 370, 150, 10, INV, {"attraversabile_da_sotto": "true"}),

    # 4: soppalco azzurro, con i pilastri, uno scaffale sopra e il transpallet sotto
    ("Soppalco", 3500, 330, 900, 16, SOP, {"attraversabile_da_sotto": "true"}),
    ("Pilastro1", 3520, 346, 14, 294, PIL, DECORO),
    ("Pilastro2", 3943, 346, 14, 294, PIL, DECORO),
    ("Pilastro3", 4366, 346, 14, 294, PIL, DECORO),
    ("ScaffaleSoppalco", 4120, 195, 80, 135, SCF, {"solido": "false", "z_index": "-7"}),
    ("RipianoSoppalco", 4122, 195, 76, 10, INV, {"attraversabile_da_sotto": "true"}),
    ("Transpallet", 3700, 565, 115, 75, TRP, {}),
    ("Scatolone2a", 3900, 560, 110, 80, SCB, {}),

    # 5: in fondo, cartoni, una colonnina di scatoloni e il portone d'uscita
    ("Cartoni2", 4550, 525, 130, 115, CRT, {}),
    ("Bancale2", 4720, 620, 120, 20, BAN, {}),
    ("Scatolone3a", 4725, 545, 110, 75, SCC, {}),
    ("Estintore2", 4860, 585, 25, 55, EST, DECORO),
    ("Portone", 4900, 475, 150, 165, POR, {"solido": "false", "z_index": "-4"}),
]

operatori = [
    (1000, 640, MORO, 1, 1),         # bagher: su, sopra la colonna di scatoloni
    (1600, 640, BIONDO, 1, 1.1),     # tiro a canestro oltre la prima fossa
    (2560, 640, MAROCCHINO, 1, 1),   # giravolta oltre la fossa larga...
    (3352, 640, INDIANO, 1, 1),      # ...dritti nelle mani della catapulta, che lancia sul soppalco
]

rompibili = [
    (820, 640, SCATOLA, 1),
    (1460, 640, SCATOLA, 1),
    (4300, 330, SCATOLA, 2),   # sul soppalco, dopo lo scaffale (così non ferma i coni)
]

chicchi = [
    (200, 610), (380, 340),                      # partenza, in cima allo scaffale
    (625, 495),                                  # sui cartoni
    (900, 610),
    (1140, 290), (1140, 230),                    # in cima alla colonna e sopra
    (1760, 430), (1880, 410),                    # sopra la prima fossa
    (2300, 610),
    (2850, 470), (3050, 480),                    # sopra la fossa larga
    (3650, 300), (3800, 300), (4200, 300), (4300, 300),   # sul soppalco
    (3757, 535),                                 # sul transpallet
    (4615, 495),                                 # sui cartoni in fondo
    (4780, 515),                                 # sulla colonnina
    (4700, 610), (4975, 600),                    # davanti al portone
]

# coni di filato che cadono e rotolano: (base del cono in piedi, verso)
coni = [
    (440, 370, 1),     # dallo scaffale dell'ingresso: rotola fino ai cartoni, per conoscerlo con calma
    (1320, 370, -1),   # dallo scaffale dopo la colonna: rotola verso la colonna, si salta
    (4160, 195, -1),   # dallo scaffale sul soppalco: rotola incontro al pulcino lungo il soppalco
]

nidi = [(260, 640), (1350, 640), (2150, 640), (3600, 330), (4480, 640)]

proprieta = {
    "numero": 4,
    "frase_fine": '"Sei uscito dal Maglificio Madrid!"',
    "beccata": "true",
    "doppio_salto": "true",
}

scrivi_livello(sys.argv[1], "Livello4", "Magazzino", pezzi, chicchi, nidi, rompibili=rompibili,
               uscita=(4975, 610), partenza=(150, 610), limite_destro=LARGO, proprieta_livello=proprieta,
               operatori=operatori, coni=coni)
