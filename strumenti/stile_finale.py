# Stile finale della grafica: dai disegni SVG (le sorgenti, scritte dagli strumenti disegni_*.py)
# alle immagini PNG che usa il gioco, nella stessa cartella e con lo stesso nome.
# Uso: python strumenti/stile_finale.py   (dalla cartella del progetto; dopo aver cambiato un disegno)
#
# 1. Raffina: contorni più sottili e del colore dell'oggetto (più scuro), colori un po' più morbidi e caldi.
# 2. Trasforma in immagine con Godot, alla stessa misura del disegno.
# 3. Ombre e luci dipinte: un lato in ombra, un filo di luce sul bordo opposto, una leggera sfumatura.
#    Personaggi (che si voltano): luce dall'alto, così resta giusta anche quando si girano.
#    Oggetti fermi: luce da in alto a sinistra, come il sole del paesaggio.
#    I pezzi piccoli o speciali (occhi, becchi, zampe, nebbia, piastrelle...) si raffinano soltanto.
import colorsys
import os
import re
import shutil
import subprocess
import sys
import tempfile

import cv2
import numpy as np

QUI = os.path.dirname(os.path.abspath(__file__))
PROGETTO = os.path.dirname(QUI)
GRAFICA = os.path.join(PROGETTO, "assets", "grafica")
GODOT = r"C:\Users\ricca\Downloads\Godot_v3.6.3-stable_win64.exe\Godot_v3.6.3-stable_win64.exe"

PERSONAGGI = ("pulcino/", "oca/", "topo/", "talpa/", "operatori/", "accessori/", "autista/", "ape/")
SOLO_RAFFINATI = re.compile(r"(occhio|becco|sopracciglio|esclamativo|zampa|bagliore|etichetta|nebbia|vignetta|mattoni"
                            r"|cono_rotola|uscita|gamba|uovo_vuoto|stella_vuota)")
NON_TOCCARE = ("atmosfera/vignetta",)  # colori già pensati per la luce: si trasformano in immagine e basta


# ---------------- 1. raffinare ----------------

def hex_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgb_hex(r, g, b):
    return "#%02X%02X%02X" % tuple(max(0, min(255, round(v * 255))) for v in (r, g, b))


def ammorbidisci(h):
    r, g, b = hex_rgb(h)
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    r, g, b = colorsys.hls_to_rgb(hh, l * 0.97 + 0.025, s * 0.9)
    return rgb_hex(r * 1.01, g, b * 0.98)


def contorno_da(fill):
    r, g, b = hex_rgb(fill)
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    return rgb_hex(*colorsys.hls_to_rgb(hh, max(0.12, l * 0.42), min(1.0, s * 0.9)))


COLORE = r"#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{3}\b"


def raffina_tag(tag):
    fill = re.search(r'fill="(' + COLORE + r')"', tag)
    stroke = re.search(r'stroke="(' + COLORE + r')"', tag)
    nuovo = tag
    if stroke:
        if fill and fill.group(1).upper() not in ("#FFFFFF", "#FFF"):
            nuovo = nuovo.replace(stroke.group(0), f'stroke="{contorno_da(ammorbidisci(fill.group(1)))}"')
        else:
            nuovo = nuovo.replace(stroke.group(0), f'stroke="{ammorbidisci(stroke.group(1))}"')
    if fill:
        nuovo = nuovo.replace(fill.group(0), f'fill="{ammorbidisci(fill.group(1))}"', 1)
    return re.sub(r'stroke-width="([\d.]+)"', lambda m: f'stroke-width="{max(1.5, float(m.group(1)) * 0.6):.1f}"', nuovo)


def raffina_svg(testo):
    testo = re.sub(r"<(path|rect|circle|ellipse|polygon|line|g)\b[^>]*>", lambda m: raffina_tag(m.group(0)), testo)
    return re.sub(r'stop-color="(' + COLORE + r')"', lambda m: f'stop-color="{ammorbidisci(m.group(1))}"', testo)


# ---------------- 3. ombre e luci ----------------

def sposta(m, dx, dy):
    # valore della maschera nel punto (x+dx, y+dy); fuori dall'immagine conta come vuoto
    h, w = m.shape
    out = np.zeros_like(m)
    ys, ye = max(0, -dy), min(h, h - dy)
    xs, xe = max(0, -dx), min(w, w - dx)
    if ye > ys and xe > xs:
        out[ys:ye, xs:xe] = m[ys + dy:ye + dy, xs + dx:xe + dx]
    return out


def ombreggia(rgba, dall_alto):
    img = rgba.astype(np.float32) / 255.0
    colore, alfa = img[:, :, :3], img[:, :, 3]
    h, w = alfa.shape
    piena = (alfa > 0.5).astype(np.float32)
    lato = min(h, w)
    s = int(np.clip(lato * 0.16, 3, 22))
    l = int(np.clip(lato * 0.07, 2, 9))
    bordo = max(2, int(lato * 0.035))
    ox, oy = (0, 1) if dall_alto else (1, 1)
    ombra = piena * (1 - sposta(piena, ox * s, oy * s))
    ombra = cv2.GaussianBlur(ombra, (0, 0), s * 0.45) * piena
    interno = cv2.erode(piena, np.ones((bordo * 2 + 1, bordo * 2 + 1), np.uint8))
    luce = interno * (1 - sposta(interno, -ox * l, -oy * l))
    luce = cv2.GaussianBlur(luce, (0, 0), l * 0.5) * interno
    risultato = colore * np.linspace(1.05, 0.93, h, dtype=np.float32)[:, None, None]
    risultato = risultato * (1 - 0.30 * ombra[:, :, None])
    risultato = np.clip(risultato + (1 - risultato) * 0.38 * luce[:, :, None], 0, 1)
    return (np.dstack([risultato, alfa]) * 255).astype(np.uint8)


# ---------------- tutto insieme ----------------

def main():
    sorgenti = []
    for cartella, _, file in os.walk(GRAFICA):
        for nome in file:
            if nome.endswith(".svg"):
                sorgenti.append(os.path.relpath(os.path.join(cartella, nome), GRAFICA).replace("\\", "/")[:-4])
    lavoro = tempfile.mkdtemp(prefix="stile_")
    try:
        # 1. disegni raffinati in una cartella di lavoro
        for rel in sorgenti:
            testo = open(os.path.join(GRAFICA, rel + ".svg"), encoding="utf-8").read()
            if rel not in NON_TOCCARE:
                testo = raffina_svg(testo)
            dest = os.path.join(lavoro, "svg", rel + ".svg")
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            open(dest, "w", encoding="utf-8", newline="\n").write(testo)
        # 2. Godot li trasforma in immagini (alla stessa misura del disegno)
        elenco = os.path.join(lavoro, "elenco.txt")
        open(elenco, "w", encoding="utf-8").write("\n".join(sorgenti))
        script = os.path.join(PROGETTO, "_stile_finale_temporaneo.gd")
        open(script, "w", encoding="utf-8").write(
            'extends SceneTree\n'
            'func _initialize():\n'
            '\tvar lavoro := OS.get_environment("LAVORO")\n'
            '\tvar f := File.new()\n'
            '\tf.open(lavoro + "/elenco.txt", File.READ)\n'
            '\tfor rel in f.get_as_text().split("\\n"):\n'
            '\t\tvar img := Image.new()\n'
            '\t\timg.load(lavoro + "/svg/" + rel + ".svg")\n'
            '\t\tvar d := Directory.new()\n'
            '\t\td.make_dir_recursive((lavoro + "/png/" + rel).get_base_dir())\n'
            '\t\timg.save_png(lavoro + "/png/" + rel + ".png")\n'
            '\tquit()\n')
        try:
            subprocess.run([GODOT, "--no-window", "--path", PROGETTO, "-s", "res://_stile_finale_temporaneo.gd"],
                           env=dict(os.environ, LAVORO=lavoro.replace("\\", "/")), check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        finally:
            os.remove(script)
        # 3. ombre e luci, e l'immagine finale accanto alla sorgente
        for rel in sorgenti:
            rgba = cv2.imread(os.path.join(lavoro, "png", rel + ".png"), cv2.IMREAD_UNCHANGED)
            if rgba is None:
                print("ATTENZIONE: non riesco a trasformare", rel)
                continue
            if not SOLO_RAFFINATI.search(rel) and rel not in NON_TOCCARE:
                rgba = ombreggia(rgba, rel.startswith(PERSONAGGI))
            cv2.imwrite(os.path.join(GRAFICA, rel + ".png"), rgba)
        print(len(sorgenti), "immagini finali scritte in assets/grafica")
    finally:
        shutil.rmtree(lavoro, ignore_errors=True)


if __name__ == "__main__":
    main()
