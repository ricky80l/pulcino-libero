# Ridipinge un'immagine (PNG con trasparenza) a pennellate, in stile impressionista.
# Uso: python strumenti/ridipingi.py <cartella_originali> <cartella_dipinti> [seme] [stile]
#      stile: "forte" (macchie di colore vivaci) oppure "delicato" (colori più calmi, contorni che restano)
#      Le sottocartelle si ridipingono tutte. Se una cartella ha un info.json (pezzi disegnati da codice,
#      fotografati più grandi), ogni immagine torna alla misura vera e si divide in strisce larghe al massimo
#      LARGHEZZA_STRISCIA, salvate come nome_0.png, nome_1.png... (i telefoni non reggono immagini troppo larghe).
#
# Come un pittore: prima pennellate larghe per le masse di colore, poi via via più fini
# solo dove il quadro si discosta ancora dal modello. Le pennellate seguono le forme
# (vanno lungo i bordi, non attraverso), il colore di ognuna varia un poco ("colore spezzato")
# e alla fine si aggiunge la grana della tela. La sagoma resta quella del disegno.
import json
import os
import sys

import cv2
import numpy as np

PENNELLI = [7, 4, 2]           # raggio delle pennellate, dalla più larga alla più fine (pixel)
LUNGHEZZA = 4.0                # lunghezza di una pennellata, in raggi
SOGLIA = [0.0, 0.06, 0.09]     # quanto deve essere diverso dal modello per ridipingere (per passata)
VARIAZIONE_COLORE = 0.06       # quanto cambia il colore da una pennellata all'altra
LARGHEZZA_STRISCIA = 2048      # larghezza massima di un'immagine nel gioco
LUCE_IMPRESSIONISTA = 0.10     # quanto i colori virano verso toni chiari e luminosi


STILI = {
    "forte": {"variazione": 0.06, "lunghezza": 4.0, "contorni": 0.0},
    "delicato": {"variazione": 0.03, "lunghezza": 6.0, "contorni": 0.65},
}


def dipingi(rgba, rng, stile="forte", misura_pennello=1.0):
    global VARIAZIONE_COLORE, LUNGHEZZA
    VARIAZIONE_COLORE = STILI[stile]["variazione"]
    LUNGHEZZA = STILI[stile]["lunghezza"]
    forza_contorni = STILI[stile]["contorni"]
    alto, largo = rgba.shape[:2]
    pennelli = [max(1, int(round(r * misura_pennello))) for r in PENNELLI]
    colore = rgba[:, :, :3].astype(np.float32) / 255.0
    alfa = rgba[:, :, 3].astype(np.float32) / 255.0

    # il modello: colori pieni anche sotto la trasparenza (così i bordi non diventano neri)
    dentro = (alfa > 0.5).astype(np.uint8)
    modello = cv2.inpaint((colore * 255).astype(np.uint8), 1 - dentro, 3, cv2.INPAINT_TELEA).astype(np.float32) / 255.0

    # tavolozza impressionista: un po' più di luce e di vivacità
    luce = modello.mean(axis=2, keepdims=True)
    modello = np.clip(modello + (modello - luce) * 0.25 + LUCE_IMPRESSIONISTA * (1 - modello) * 0.5, 0, 1)

    tela = cv2.GaussianBlur(modello, (0, 0), pennelli[0])
    for passata, raggio in enumerate(pennelli):
        riferimento = cv2.GaussianBlur(modello, (0, 0), raggio * 0.6)
        grigio = cv2.cvtColor((riferimento * 255).astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
        gx = cv2.Sobel(grigio, cv2.CV_32F, 1, 0, ksize=3)
        gy = cv2.Sobel(grigio, cv2.CV_32F, 0, 1, ksize=3)
        differenza = np.abs(tela - riferimento).mean(axis=2)

        pennellate = []
        passo = max(1, int(raggio))
        for y in range(0, alto, passo):
            for x in range(0, largo, passo):
                px = int(np.clip(x + rng.integers(-passo // 2, passo // 2 + 1), 0, largo - 1))
                py = int(np.clip(y + rng.integers(-passo // 2, passo // 2 + 1), 0, alto - 1))
                if alfa[py, px] < 0.3:
                    continue
                if passata > 0 and differenza[py, px] < SOGLIA[passata]:
                    continue
                pennellate.append((px, py))
        rng.shuffle(pennellate)

        for px, py in pennellate:
            c = riferimento[py, px] + rng.normal(0, VARIAZIONE_COLORE, 3)
            c = np.clip(c, 0, 1)
            # la pennellata cammina lungo il bordo (perpendicolare al gradiente)
            punti = [(px, py)]
            x, y = float(px), float(py)
            dx_prec, dy_prec = 0.0, 0.0
            for _ in range(int(LUNGHEZZA)):
                ix, iy = int(np.clip(x, 0, largo - 1)), int(np.clip(y, 0, alto - 1))
                g = np.array([gx[iy, ix], gy[iy, ix]])
                if np.linalg.norm(g) < 1.0:
                    # dove il colore è uniforme (cielo, muri) pennellate quasi orizzontali, come il pittore
                    angolo = rng.normal(0, 0.3) if not punti[1:] else np.arctan2(dy_prec, dx_prec)
                    d = np.array([np.cos(angolo), np.sin(angolo)])
                else:
                    d = np.array([-g[1], g[0]]) / np.linalg.norm(g)
                if dx_prec * d[0] + dy_prec * d[1] < 0:
                    d = -d
                x, y = x + d[0] * raggio, y + d[1] * raggio
                dx_prec, dy_prec = d
                punti.append((int(round(x)), int(round(y))))
            spessore = max(1, int(round(raggio * rng.uniform(1.4, 2.0))))
            cv2.polylines(tela, [np.array(punti, np.int32)], False, tuple(float(v) for v in c), spessore, cv2.LINE_AA)

    # contorni: le linee scure del disegno restano visibili sotto la pittura (stile delicato)
    if forza_contorni > 0:
        luminosita = colore.mean(axis=2)
        linee = np.clip((0.42 - luminosita) / 0.2, 0, 1) * (alfa > 0.5)
        linee = cv2.GaussianBlur(linee.astype(np.float32), (0, 0), 0.6)[:, :, None] * forza_contorni
        tela = tela * (1 - linee) + colore * linee

    # grana della tela
    grana = rng.normal(0, 0.025, (alto, largo, 1)).astype(np.float32)
    grana = cv2.GaussianBlur(grana, (0, 0), 0.7)[:, :, None]
    tela = np.clip(tela + grana, 0, 1)

    # sagoma: quella del disegno, con il bordo appena sfrangiato come una pennellata
    rumore = cv2.GaussianBlur(rng.normal(0, 1, (alto, largo)).astype(np.float32), (0, 0), 1.5)
    alfa_dipinta = np.clip(alfa + (alfa > 0.05) * (alfa < 0.95) * rumore * 0.4, 0, 1)

    risultato = np.dstack([tela * 255, alfa_dipinta * 255]).astype(np.uint8)
    return risultato


def main():
    origine, destinazione = sys.argv[1], sys.argv[2]
    seme = int(sys.argv[3]) if len(sys.argv) > 3 else 7
    stile = sys.argv[4] if len(sys.argv) > 4 else "forte"
    for cartella, _sotto, file in os.walk(origine):
        uscita = os.path.join(destinazione, os.path.relpath(cartella, origine))
        os.makedirs(uscita, exist_ok=True)
        info = None
        if "info.json" in file:
            with open(os.path.join(cartella, "info.json"), encoding="utf-8") as f:
                info = json.load(f)
        for nome in sorted(file):
            if not nome.lower().endswith(".png"):
                continue
            rgba = cv2.imread(os.path.join(cartella, nome), cv2.IMREAD_UNCHANGED)
            if rgba.shape[2] == 3:
                rgba = np.dstack([rgba, np.full(rgba.shape[:2], 255, np.uint8)])
            rng = np.random.default_rng(seme)
            base = nome[:-4]
            if info is None:
                # disegni piccoli (occhi, becchi) con pennelli più fini
                misura = float(np.clip(min(rgba.shape[:2]) / 240.0, 0.3, 1.0))
                cv2.imwrite(os.path.join(uscita, nome), dipingi(rgba, rng, stile, misura))
            else:
                scala = info[base]["scala"]
                # lo sfondo lontano (fotografato a misura vera) con pennellate più larghe
                dipinto = dipingi(rgba, rng, stile, 1.0 if scala > 1 else 1.5)
                if scala != 1:
                    alto, largo = dipinto.shape[:2]
                    dipinto = cv2.resize(dipinto, (round(largo / scala), round(alto / scala)), interpolation=cv2.INTER_AREA)
                for i, x in enumerate(range(0, dipinto.shape[1], LARGHEZZA_STRISCIA)):
                    cv2.imwrite(os.path.join(uscita, "%s_%d.png" % (base, i)), dipinto[:, x:x + LARGHEZZA_STRISCIA])
            print("dipinto", os.path.join(os.path.relpath(cartella, origine), nome))


if __name__ == "__main__":
    main()
