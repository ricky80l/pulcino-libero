# Disegni SVG dei premi: l'uovo d'oro segreto (uno per luogo) con la sua sagoma vuota per la mappa,
# e la stellina degli obiettivi, piena e vuota.
# Uso: python strumenti/disegni_premi.py   (dalla cartella del progetto), poi python strumenti/stile_finale.py
import math
import os

CARTELLA = os.path.join(os.path.dirname(__file__), "..", "assets", "grafica", "oggetti")


def svg(w, h, corpo):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{corpo}\n</svg>\n'


UOVO = "M30 4 C46 4 56 28 56 46 C56 62 44 72 30 72 C16 72 4 62 4 46 C4 28 14 4 30 4 Z"
# stella a cinque punte un po' paffuta
_punti = []
for _i in range(10):
    _r = 46 if _i % 2 == 0 else 22
    _a = math.radians(-90 + _i * 36)
    _punti.append(f"{50 + _r * math.cos(_a):.1f} {52 + _r * math.sin(_a):.1f}")
STELLA = "M" + " L".join(_punti) + " Z"
PEZZI = {
    # uovo d'oro: base in basso al centro (30, 72)
    "uovo_oro": svg(60, 76, f'''<path d="{UOVO}" fill="#F6C430" stroke="#8C600A" stroke-width="5"/>
<path d="M14 50 Q30 58 46 50" fill="none" stroke="#FFE27A" stroke-width="4" stroke-linecap="round"/>
<ellipse cx="21" cy="26" rx="6" ry="10" fill="#FFF6C8" transform="rotate(20 21 26)"/>
<circle cx="40" cy="20" r="3" fill="#FFF6C8"/>'''),
    # sagoma vuota per la mappa: uovo non ancora trovato
    "uovo_vuoto": svg(60, 76, f'''<path d="{UOVO}" fill="#FFFFFF" fill-opacity="0.35" stroke="#8C7A5A" stroke-width="5" stroke-dasharray="9 7"/>'''),
    # stellina degli obiettivi: centro (50, 50)
    "stella": svg(100, 100, f'''<path d="{STELLA}" fill="#FFD447" stroke="#9A6A08" stroke-width="6" stroke-linejoin="round"/>
<path d="M50 22 L56 40" stroke="#FFF3B0" stroke-width="5" stroke-linecap="round"/>'''),
    "stella_vuota": svg(100, 100, f'''<path d="{STELLA}" fill="#000000" fill-opacity="0.18" stroke="#FFF5DC" stroke-opacity="0.8" stroke-width="5" stroke-linejoin="round" stroke-dasharray="10 7"/>'''),
}

os.makedirs(CARTELLA, exist_ok=True)
for nome, testo in PEZZI.items():
    with open(os.path.join(CARTELLA, nome + ".svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(testo)
print(len(PEZZI), "disegni dei premi scritti")
