# Prepara la musica del gioco: dai brani originali (MP3 scaricati) a file OGG corti e leggeri in assets/musica/.
# Uso: python -P strumenti/prepara_musica.py <cartella con gli MP3 originali>   (dalla cartella del progetto)
#
# I brani sono di Kevin MacLeod (incompetech.com), licenza Creative Commons Attribuzione 4.0: l'autore va citato
# nei Crediti del gioco (vedi scripts/crediti.gd). Gli originali NON stanno nel progetto (pesano troppo); si riscaricano da:
#   https://incompetech.com/music/royalty-free/mp3-royaltyfree/Easy%20Lemon.mp3      -> easy_lemon.mp3
#   https://incompetech.com/music/royalty-free/mp3-royaltyfree/Carefree.mp3          -> carefree.mp3
#   https://incompetech.com/music/royalty-free/mp3-royaltyfree/Cheery%20Monday.mp3   -> cheery_monday.mp3
#
# Per ogni brano: toglie il silenzio iniziale, lo accorcia a un numero intero di battute (circa un minuto e mezzo),
# sfuma il finale (nel gioco il brano si ripete: sfuma e riparte), porta tutti allo stesso volume e comprime.
# Serve la libreria "soundfile" (pip install soundfile).
import os
import sys

import numpy as np
import soundfile as sf

QUI = os.path.dirname(os.path.abspath(__file__))
USCITA = os.path.join(QUI, "..", "assets", "musica")
VOLUME = 0.09  # volume medio uguale per tutti i brani (poi nel gioco la musica sta sotto ai suoni)
QUALITA = 0.72  # compressione: più alto = file più piccolo e suono un po' meno fine

# nome nel gioco: (file originale, battiti al minuto, quante battute tenere; 0 = tutto il brano)
BRANI = {
    "mappa": ("easy_lemon.mp3", 82, 32),
    "aperto": ("carefree.mp3", 96, 36),
    "chiuso": ("cheery_monday.mp3", 102, 0),
}


def prepara(nome, file, bpm, battute, cartella):
    dati, freq = sf.read(os.path.join(cartella, file), dtype="float32", always_2d=True)
    mono = dati.mean(axis=1)
    suono = np.where(np.abs(mono) > 0.01)[0]
    inizio = max(0, suono[0] - int(0.02 * freq))
    if battute > 0:
        fine = inizio + int(round(battute * 4 * 60.0 / bpm * freq))
        sfumata = 3.0
    else:
        fine = min(len(dati), suono[-1] + int(0.4 * freq))  # il brano ha già il suo finale
        sfumata = 0.6
    pezzo = dati[inizio:fine].copy()
    n = int(sfumata * freq)
    pezzo[-n:] *= np.linspace(1.0, 0.0, n, dtype="float32")[:, None] ** 2
    pezzo[:int(0.02 * freq)] *= np.linspace(0.0, 1.0, int(0.02 * freq), dtype="float32")[:, None]
    # stesso volume medio per tutti, senza superare il massimo
    medio = float(np.sqrt((pezzo.mean(axis=1) ** 2).mean()))
    guadagno = min(VOLUME / medio, 0.95 / float(np.abs(pezzo).max()))
    pezzo *= guadagno
    os.makedirs(USCITA, exist_ok=True)
    destinazione = os.path.join(USCITA, nome + ".ogg")
    with sf.SoundFile(destinazione, "w", samplerate=freq, channels=pezzo.shape[1], format="OGG", subtype="VORBIS",
                      compression_level=QUALITA) as f:
        for i in range(0, len(pezzo), 65536):  # a pezzi: la libreria non regge scritture enormi in un colpo
            f.write(pezzo[i:i + 65536])
    print("%s: %.1f s, %.2f MB, volume medio %.3f, picco %.2f" % (
        nome, len(pezzo) / freq, os.path.getsize(destinazione) / 1048576, medio * guadagno, np.abs(pezzo).max()))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Uso: python -P strumenti/prepara_musica.py <cartella con gli MP3 originali>")
    for nome, (file, bpm, battute) in BRANI.items():
        prepara(nome, file, bpm, battute, sys.argv[1])
