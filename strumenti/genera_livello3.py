# Genera la scena del livello 3 (l'orto): scenes/livello_3.tscn
# Uso: python strumenti/genera_livello3.py scenes/livello_3.tscn
# Insegna il doppio salto un passo alla volta: muretto di cassette, primo girasole che rimbalza,
# canale da saltare in lungo, zucca da beccare, pozzo, salita con mais e girasole fino a un tetto alto.
# Versione lunga (Tappa R3), circa 7.500: poi il canale largo con l'isolotto in mezzo, due strade (in alto
# dal girasole sui tetti, con una mensola segreta piena di chicchi; in basso tra le talpe), il recinto
# con la zucca, il mais e il muretto di quattro cassette, la carriola, il secondo pozzo e il cancelletto.
import sys
from livelli import *

LARGO = 7500

NON_SOLIDO = {"solido": "false", "z_index": "-6"}

pezzi = [
    # sfondo e decorazioni
    # il paesaggio lontano (cielo, colline con i campi, siepi) è a strati: vedi atmosfera="orto" qui sotto
    ("Spaventapasseri", 60, 460, 105, 180, SPA, NON_SOLIDO),
    # uovo d'oro segreto: sul cappello dello spaventapasseri, alle spalle della partenza (doppio salto)
    ("Cappello", 85, 468, 55, 10, INV, {"attraversabile_da_sotto": "true"}),
    ("Pomodori1", 400, 505, 65, 135, POM, NON_SOLIDO),
    ("Pomodori2", 470, 505, 65, 135, POM, NON_SOLIDO),
    ("Pomodori3", 4120, 505, 65, 135, POM, NON_SOLIDO),
    ("Fragole1", 950, 602, 85, 38, FRA, NON_SOLIDO),
    ("Fragole2", 1300, 602, 85, 38, FRA, NON_SOLIDO),
    ("Fragole3", 2700, 602, 85, 38, FRA, NON_SOLIDO),
    ("Fragole4", 4010, 602, 85, 38, FRA, NON_SOLIDO),
    ("Annaffiatoio", 3950, 592, 65, 48, ANN, NON_SOLIDO),
    ("Spaventapasseri2", 5930, 460, 105, 180, SPA, NON_SOLIDO),
    ("Fragole5", 5800, 602, 85, 38, FRA, NON_SOLIDO),
    ("Pomodori4", 7110, 505, 65, 135, POM, NON_SOLIDO),
    ("Cancello", 7230, 540, 130, 100, CAN, {"solido": "false", "z_index": "-4"}),
    # terreno, con il canale d'irrigazione in mezzo
    ("TerraA", 0, 640, 1550, 80, TOR, {}),
    ("Acqua", 1550, 680, 300, 40, ACQ, {"solido": "false", "z_index": "-1"}),
    ("TerraB", 1850, 640, 2550, 80, TOR, {}),
    ("Acqua2", 4400, 680, 500, 40, ACQ, {"solido": "false", "z_index": "-1"}),
    ("Isolotto", 4610, 640, 80, 80, TOR, {}),   # in mezzo al canale largo: ci si ferma un attimo
    ("TerraC", 4900, 640, LARGO - 4900 + 40, 80, TOR, {}),
    ("MuroSinistro", -40, 0, 40, 720, LEG, {}),
    ("MuroDestro", LARGO, 0, 40, 720, LEG, {}),
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
    # 7: carriola
    ("Carriola", 3800, 572, 115, 68, CRL, {}),
    # 8: canale largo con l'isolotto in mezzo (vedi Acqua2 e Isolotto qui sopra)
    # 9: due strade. In alto: dal girasole sui tetti (sopra il secondo, una mensola segreta piena di chicchi).
    #    In basso: tra due talpe e un cavolo
    ("Tetto2", 5200, 300, 160, 32, TET, {"attraversabile_da_sotto": "true"}),
    ("Tetto3", 5440, 250, 160, 32, TET, {"attraversabile_da_sotto": "true"}),
    ("Tetto4", 5680, 320, 160, 32, TET, {"attraversabile_da_sotto": "true"}),
    ("MensolaSegreta", 5420, 90, 120, 32, TET, {"attraversabile_da_sotto": "true"}),
    ("Cavolo3", 5350, 594, 60, 46, CAV, {}),
    # 10: recinto chiuso da una zucca, poi il mais e il muretto di quattro cassette (più alto del primo)
    ("Recinto2", 6150, 0, 40, 576, LEG, {}),
    ("Cassetta4", 6420, 572, 80, 68, CAS, {}),
    ("Cassetta5", 6420, 504, 80, 68, CAS, {}),
    ("Cassetta6", 6420, 436, 80, 68, CAS, {}),
    ("Cassetta7", 6420, 368, 80, 68, CAS, {}),
    # 11: seconda carriola, la talpa e il secondo pozzo prima del cancelletto
    ("Carriola2", 6700, 572, 115, 68, CRL, {}),
    ("Pozzo2", 6950, 445, 150, 195, POZ, {"solido": "false", "z_index": "-2"}),
    ("Pozzo2Base", 6963, 575, 124, 65, INV, {}),
    ("Pozzo2Tetto", 6985, 448, 80, 12, INV, {"attraversabile_da_sotto": "true"}),
]

piante = [
    (1150, 640, GIRASOLE),   # il primo rimbalzo
    (2850, 640, MAIS),
    (3050, 640, GIRASOLE),
    (5050, 640, GIRASOLE),   # porta alla strada alta sui tetti
    (6290, 640, MAIS),       # aiuta a salire sul muretto di quattro cassette
]

rompibili = [
    (2170, 640, ZUCCA, 2),
    (6170, 640, ZUCCA, 2),
]

# talpe dispettose: centro della buca, a terra
talpe = [
    (700, 640),    # la prima, tra il cavolo e il muretto: si impara a conoscerla con calma
    (2410, 640),   # dopo la zucca, prima del pozzo
    (4170, 640),   # prima del canale largo
    (5250, 640),   # strada bassa
    (5520, 640),   # strada bassa
    (6880, 640),   # tra la carriola e il pozzo
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
    (4505, 560), (4650, 610), (4800, 560),     # canale largo e isolotto
    (4960, 610),
    (5050, 400),                               # sopra il girasole
    (5240, 270), (5300, 270), (5480, 220), (5720, 290),   # strada alta sui tetti
    (5440, 60), (5480, 60), (5520, 60),        # mensola segreta
    (5380, 560), (5650, 610),                  # strada bassa
    (6230, 610),                               # dietro la zucca
    (6290, 410),                               # sopra il mais
    (6460, 335),                               # in cima al muretto
    (6757, 545),                               # sulla seconda carriola
    (7025, 425),                               # sul tettuccio del secondo pozzo
    (7200, 610),                               # davanti al cancello
]

nidi = [(1430, 640), (2300, 640), (2750, 640), (3650, 640), (4320, 640), (4980, 640), (5960, 640), (6620, 640)]

proprieta = {
    "numero": 3,
    "frase_fine": '"Hai attraversato l\'orto!"',
    "beccata": "true",
    "doppio_salto": "true",
    "abilita_nuova": '"doppio_salto"',
}

scrivi_livello(sys.argv[1], "Livello3", "Orto", pezzi, chicchi, nidi, rompibili=rompibili,
               uscita=(7310, 610), partenza=(200, 610), limite_destro=LARGO, proprieta_livello=proprieta,
               piante=piante, talpe=talpe, atmosfera="orto", uovo=(112, 468),
               # un filo rosa impigliato al cancelletto, e la piuma
               indizi=[(7300, 550, "filo", 1.4, {"rotation_degrees": 8.0}), (7190, 640, "piuma", 0.9)])
