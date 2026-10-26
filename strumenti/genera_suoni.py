# Genera i suoni segnaposto del gioco (versi sintetici) in assets/suoni/.
# Uso: python strumenti/genera_suoni.py   (dalla cartella del progetto)
import math
import os
import random
import struct
import wave

FREQ = 22050
CARTELLA = os.path.join(os.path.dirname(__file__), "..", "assets", "suoni")


def tono(f0, f1, durata, vibrato_hz=0.0, vibrato_ampiezza=0.0, armonica=0.3, attacco=0.005, volume=0.6):
    """Nota che scivola da f0 a f1, con inviluppo e un po' di vibrato."""
    n = int(durata * FREQ)
    campioni = []
    fase = 0.0
    for i in range(n):
        t = i / FREQ
        k = i / n
        f = f0 + (f1 - f0) * k
        f *= 1 + vibrato_ampiezza * math.sin(2 * math.pi * vibrato_hz * t)
        fase += 2 * math.pi * f / FREQ
        s = math.sin(fase) + armonica * math.sin(2 * fase)
        inviluppo = min(1.0, t / attacco) * (1 - k) ** 1.5
        campioni.append(s * inviluppo * volume / (1 + armonica))
    return campioni


def rumore(durata, volume=0.5, morbidezza=0.85):
    """Soffio morbido (rumore filtrato) che si spegne."""
    n = int(durata * FREQ)
    campioni = []
    prec = 0.0
    for i in range(n):
        prec = prec * morbidezza + random.uniform(-1, 1) * (1 - morbidezza)
        campioni.append(prec * 3 * volume * (1 - i / n) ** 2)
    return campioni


def silenzio(durata):
    return [0.0] * int(durata * FREQ)


def mescola(*tracce):
    lunghezza = max(len(t) for t in tracce)
    return [sum(t[i] for t in tracce if i < len(t)) for i in range(lunghezza)]


def salva(nome, campioni):
    os.makedirs(CARTELLA, exist_ok=True)
    with wave.open(os.path.join(CARTELLA, nome + ".wav"), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(FREQ)
        f.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, s)) * 32000)) for s in campioni))


random.seed(7)
# "pio!" allegro che sale
salva("salto", tono(1000, 1750, 0.13, vibrato_hz=25, vibrato_ampiezza=0.02))
# "puf" morbido di atterraggio
salva("atterra", rumore(0.09, volume=0.35))
# "pop" del chicco con scintilla
salva("chicco", tono(500, 1400, 0.06, armonica=0.5) + tono(2100, 2300, 0.07, armonica=0.1, volume=0.35))
# "pio-pio!" disperato che scende
salva("colpito", tono(1900, 1000, 0.13, vibrato_hz=30, vibrato_ampiezza=0.05) + silenzio(0.04)
      + tono(1800, 850, 0.17, vibrato_hz=30, vibrato_ampiezza=0.06))
# squittio del topo
salva("squittio", tono(2700, 3300, 0.07, vibrato_hz=45, vibrato_ampiezza=0.06, armonica=0.6, volume=0.4)
      + tono(3300, 2500, 0.1, vibrato_hz=45, vibrato_ampiezza=0.06, armonica=0.6, volume=0.4))
# campanellino del nido
salva("nido", mescola(tono(880, 880, 0.35, armonica=0.4, volume=0.4),
                      silenzio(0.12) + tono(1320, 1320, 0.4, armonica=0.4, volume=0.4)))
# fanfara di fine livello
fanfara = []
for nota, durata in [(784, 0.12), (988, 0.12), (1175, 0.12), (1568, 0.45)]:
    fanfara += tono(nota, nota, durata, armonica=0.5, volume=0.45)
salva("fine", fanfara)
# "tok!" secco della beccata, con un pigolio corto
salva("becco", mescola(rumore(0.03, volume=0.9, morbidezza=0.2), tono(700, 500, 0.05, armonica=0.8, volume=0.5))
      + tono(1500, 1900, 0.06, volume=0.3))
# botta sorda su un ostacolo che resiste
salva("botta", mescola(tono(180, 90, 0.12, armonica=0.6, volume=0.7), rumore(0.06, volume=0.5, morbidezza=0.6)))
# "scrunch" di un ostacolo che va in pezzi
salva("rotto", mescola(rumore(0.28, volume=0.8, morbidezza=0.35), tono(220, 70, 0.2, armonica=0.5, volume=0.5)))
# "QUA-QUA!" nasale dell'oca arrabbiata
def starnazzo(f0, f1, durata):
    return tono(f0, f1, durata, vibrato_hz=35, vibrato_ampiezza=0.04, armonica=1.4, attacco=0.01, volume=0.55)
salva("starnazzo", starnazzo(420, 330, 0.16) + silenzio(0.05) + starnazzo(460, 300, 0.22))
print("suoni creati in", os.path.abspath(CARTELLA))
