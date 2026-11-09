# Genera la scena del livello 4 (il magazzino filati): scenes/livello_4.tscn
# Uso: python strumenti/genera_livello4.py scenes/livello_4.tscn
# Al chiuso, come nelle foto di Riccardo. Insegna i lanci degli operatori un passo alla volta:
# la bagher sopra una colonna di scatoloni, il tiro a canestro oltre la prima fossa, poi due lanci di fila
# (giravolta oltre la fossa larga, dritti nelle mani della catapulta) fino al soppalco azzurro; poi il portone.
# I coni di filato cadono dagli scaffali e rotolano: si saltano.
# Versione lunga (Tappa R4), circa 8.700: i quattro operatori restano uno per uno (niente "gemelli"),
# più distanziati; tra loro il corridoio degli scaffali (con una passerella alta), il secondo soppalco
# (con il vuoto in mezzo), la scala di scatoloni per scendere e la buca di carico da saltare col doppio salto.
import sys
from livelli import *

DECORO = {"solido": "false", "z_index": "-6"}
SU = {"attraversabile_da_sotto": "true"}
LARGO = 8700


def scaffale(nome, x):
    """Scaffale largo 160 con tre ripiani su cui si sale (in cima a y 370)."""
    return [(nome, x, 370, 160, 270, SCF, DECORO),
            (nome + "a", x + 5, 498, 150, 10, INV, SU),
            (nome + "b", x + 5, 434, 150, 10, INV, SU),
            (nome + "c", x + 5, 370, 150, 10, INV, SU)]


pezzi = [
    # il capannone: parete di mattoni con gli oblò, soffitto di lamiera, pavimento con tre fosse
    ("Parete", 0, 0, LARGO, 720, MAT, {"solido": "false", "z_index": "-10"}),
    ("Soffitto", 0, 0, LARGO, 80, LAM, {"solido": "false", "z_index": "-9"}),
    ("PavimentoA", 0, 640, 1680, 80, CEM, {}),
    ("Fossa1", 1680, 640, 350, 80, FOS, {"solido": "false", "z_index": "-1"}),
    ("PavimentoB", 2030, 640, 1620, 80, CEM, {}),
    ("Fossa2", 3650, 640, 650, 80, FOS, {"solido": "false", "z_index": "-1"}),
    ("PavimentoC", 4300, 640, 2400, 80, CEM, {}),
    ("Fossa3", 6700, 640, 260, 80, FOS, {"solido": "false", "z_index": "-1"}),
    ("PavimentoD", 6960, 640, LARGO - 6960, 80, CEM, {}),
    ("MuroSinistro", -40, 0, 40, 720, INV, {}),
    ("MuroDestro", LARGO, 0, 40, 720, INV, {}),

    # 1: ingresso. Scaffale con i ripiani su cui si sale, pila di cartoni piatti, una scatola da beccare
    ("Scaffale1", 300, 370, 160, 270, SCF, DECORO),
    ("Ripiano1a", 305, 498, 150, 10, INV, SU),
    ("Ripiano1b", 305, 434, 150, 10, INV, SU),
    ("Ripiano1c", 305, 370, 150, 10, INV, SU),
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
    ("Ripiano2", 1305, 370, 150, 10, INV, SU),
    # uovo d'oro segreto: passerella sotto il soffitto, sopra l'operatore della bagher (lancio + doppio salto)
    ("Passerella", 930, 150, 140, 16, SOP, SU),
    # 3: tiro a canestro oltre la prima fossa (operatore biondo, qui sotto)
]

# 4 (nuovo): il corridoio degli scaffali. In alto: sui ripiani e sulla passerella (più chicchi).
#    In basso: una scatola da beccare, i cartoni e una pila di scatoloni che vuole il doppio salto
pezzi += scaffale("Scaffale3", 2250) + scaffale("Scaffale4", 2550) + scaffale("Scaffale5", 2900)
pezzi += [
    ("Passerella2", 2640, 200, 200, 16, SOP, SU),
    ("Cartoni3", 3150, 525, 130, 115, CRT, {}),
    ("Bancale3", 3350, 620, 120, 20, BAN, {}),
    ("Scatolone3p", 3355, 545, 110, 75, SCA, {}),
    ("Scatolone3q", 3360, 465, 100, 80, SCB, {}),

    # 5: giravolta oltre la fossa larga, dritti nelle mani della catapulta che lancia sul soppalco
    # 6: soppalco azzurro, con i pilastri, uno scaffale sopra e il transpallet sotto
    ("Soppalco", 4500, 330, 900, 16, SOP, SU),
    ("Pilastro1", 4520, 346, 14, 294, PIL, DECORO),
    ("Pilastro2", 4943, 346, 14, 294, PIL, DECORO),
    ("Pilastro3", 5366, 346, 14, 294, PIL, DECORO),
    ("ScaffaleSoppalco", 5120, 195, 80, 135, SCF, {"solido": "false", "z_index": "-7"}),
    ("RipianoSoppalco", 5122, 195, 76, 10, INV, SU),
    ("Transpallet", 4700, 565, 115, 75, TRP, {}),
    ("Scatolone2a", 4900, 560, 110, 80, SCB, {}),

    # 7 (nuovo): secondo soppalco, oltre un vuoto da saltare; sotto, la strada bassa tra cartoni e una scatola
    ("Soppalco2", 5560, 330, 760, 16, SOP, SU),
    ("Pilastro4", 5580, 346, 14, 294, PIL, DECORO),
    ("Pilastro5", 5940, 346, 14, 294, PIL, DECORO),
    ("Pilastro6", 6300, 346, 14, 294, PIL, DECORO),
    ("ScaffaleSoppalco2", 5950, 195, 80, 135, SCF, {"solido": "false", "z_index": "-7"}),
    ("RipianoSoppalco2", 5952, 195, 76, 10, INV, SU),
    ("Cartoni4", 5700, 525, 130, 115, CRT, {}),
    # scala di scatoloni per scendere dal secondo soppalco
    ("Bancale4", 6340, 620, 120, 20, BAN, {}),
    ("Scatolone4a", 6345, 545, 110, 75, SCA, {}),
    ("Scatolone4b", 6350, 465, 100, 80, SCB, {}),

    # 8 (nuovo): la buca di carico (vedi Fossa3), poi transpallet, cartoni e uno scaffale con un cono
    ("Transpallet2", 7100, 565, 115, 75, TRP, {}),
    ("Cartoni5", 7250, 525, 130, 115, CRT, {}),
]
pezzi += scaffale("Scaffale6", 7400)
pezzi += [
    # 9: in fondo, cartoni, una colonnina di scatoloni e il portone d'uscita
    ("Cartoni2", 7620, 525, 130, 115, CRT, {}),
    ("Bancale2", 7790, 620, 120, 20, BAN, {}),
    ("Scatolone3a", 7795, 545, 110, 75, SCC, {}),
    # il furgone azzurro davanti al portone, col portellone aperto: ci si sale sul tetto dalla colonnina di scatoloni
    ("Furgone", 7970, 430, 330, 210, FUR, {"solido": "false", "z_index": "-3"}),
    ("TettoFurgone", 8000, 462, 245, 10, INV, SU),
    ("Estintore2", 8450, 585, 25, 55, EST, DECORO),
    ("Portone", 8510, 475, 150, 165, POR, {"solido": "false", "z_index": "-4"}),
]

operatori = [
    (1000, 640, MORO, 1, 1),         # bagher: su, sopra la colonna di scatoloni
    (1600, 640, BIONDO, 1, 1.1),     # tiro a canestro oltre la prima fossa
    (3560, 640, MAROCCHINO, 1, 1),   # giravolta oltre la fossa larga...
    (4352, 640, INDIANO, 1, 1),      # ...dritti nelle mani della catapulta, che lancia sul soppalco
]

rompibili = [
    (820, 640, SCATOLA, 1),
    (1460, 640, SCATOLA, 1),
    (2470, 640, SCATOLA, 1),   # tra i primi due scaffali del corridoio
    (5300, 330, SCATOLA, 2),   # sul soppalco, dopo lo scaffale (così non ferma i coni)
    (6020, 640, SCATOLA, 1),   # sotto il secondo soppalco
    (6240, 330, SCATOLA, 2),   # in fondo al secondo soppalco
]

chicchi = [
    (200, 610), (380, 340),                      # partenza, in cima allo scaffale
    (625, 495),                                  # sui cartoni
    (900, 610),
    (1140, 290), (1140, 230),                    # in cima alla colonna e sopra
    (1775, 315), (1900, 285),                    # sopra la prima fossa, sulla traiettoria del canestro
    (2300, 610),
    (2335, 340), (2630, 340), (2980, 340),       # in cima agli scaffali del corridoio
    (2680, 170), (2740, 170), (2800, 170),       # sulla passerella alta
    (2470, 560),                                 # sopra la scatola
    (3215, 495),                                 # sui cartoni
    (3410, 435),                                 # in cima alla pila di scatoloni
    (3500, 610),
    (3830, 428), (4040, 410),                    # sopra la fossa larga, sulla traiettoria della giravolta
    (4650, 300), (4800, 300), (5200, 300), (5300, 300),   # sul soppalco
    (4757, 535),                                 # sul transpallet
    (5490, 165),                                 # sopra il vuoto tra i soppalchi (in cima al salto)
    (5700, 300), (5850, 300), (6100, 300),       # sul secondo soppalco
    (5765, 495),                                 # sui cartoni sotto il secondo soppalco
    (6080, 610),                                 # dietro la scatola sotto il secondo soppalco
    (6400, 435),                                 # sulla scala di scatoloni
    (6760, 510), (6830, 465), (6910, 335),       # sopra la buca di carico, sul doppio salto preso dal bordo
    (7157, 535),                                 # sul secondo transpallet
    (7315, 495),                                 # sui cartoni
    (7480, 340),                                 # in cima all'ultimo scaffale
    (7685, 495),                                 # sui cartoni in fondo
    (7850, 515),                                 # sulla colonnina
    (7770, 610),
    (8060, 432), (8130, 432), (8200, 432),       # sul tetto del furgone
    (8585, 600),                                 # davanti al portone
]

# coni di filato che cadono e rotolano: (base del cono in piedi, verso)
coni = [
    (440, 370, 1),     # dallo scaffale dell'ingresso: rotola fino ai cartoni, per conoscerlo con calma
    (1320, 370, -1),   # dallo scaffale dopo la colonna: rotola verso la colonna, si salta
    (3040, 370, -1),   # dall'ultimo scaffale del corridoio: rotola incontro al pulcino
    (5160, 195, -1),   # dallo scaffale sul soppalco: rotola incontro al pulcino lungo il soppalco
    (5990, 195, -1),   # dallo scaffale sul secondo soppalco
    (7520, 370, -1),   # dall'ultimo scaffale, prima dei cartoni in fondo
]

nidi = [(260, 640), (1350, 640), (2150, 640), (3090, 640), (4600, 330), (5640, 330), (6560, 640),
        (7040, 640), (7570, 640)]

proprieta = {
    "numero": 4,
    "frase_fine": '"Sei uscito dal Maglificio Granada!"',
    "beccata": "true",
    "doppio_salto": "true",
}

scrivi_livello(sys.argv[1], "Livello4", "Magazzino", pezzi, chicchi, nidi, rompibili=rompibili,
               uscita=(8585, 610), partenza=(150, 610), limite_destro=LARGO, proprieta_livello=proprieta,
               operatori=operatori, coni=coni, atmosfera="magazzino", uovo=(1000, 150),
               autista=(8370, 640),
               # il fiocco a maglia sul tetto del furgone (l'autista lo indica), e la piuma
               indizi=[(8120, 446, "fiocco", 1.0), (8440, 640, "piuma", 1.1)])
