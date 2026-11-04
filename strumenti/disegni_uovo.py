# Disegni SVG dell'uovo d'oro segreto (uno per luogo) e della sua sagoma vuota per la mappa.
# Uso: python strumenti/disegni_uovo.py   (dalla cartella del progetto), poi python strumenti/stile_finale.py
import os

CARTELLA = os.path.join(os.path.dirname(__file__), "..", "assets", "grafica", "oggetti")


def svg(w, h, corpo):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{corpo}\n</svg>\n'


UOVO = "M30 4 C46 4 56 28 56 46 C56 62 44 72 30 72 C16 72 4 62 4 46 C4 28 14 4 30 4 Z"
PEZZI = {
    # uovo d'oro: base in basso al centro (30, 72)
    "uovo_oro": svg(60, 76, f'''<path d="{UOVO}" fill="#F6C430" stroke="#8C600A" stroke-width="5"/>
<path d="M14 50 Q30 58 46 50" fill="none" stroke="#FFE27A" stroke-width="4" stroke-linecap="round"/>
<ellipse cx="21" cy="26" rx="6" ry="10" fill="#FFF6C8" transform="rotate(20 21 26)"/>
<circle cx="40" cy="20" r="3" fill="#FFF6C8"/>'''),
    # sagoma vuota per la mappa: uovo non ancora trovato
    "uovo_vuoto": svg(60, 76, f'''<path d="{UOVO}" fill="#FFFFFF" fill-opacity="0.35" stroke="#8C7A5A" stroke-width="5" stroke-dasharray="9 7"/>'''),
}

os.makedirs(CARTELLA, exist_ok=True)
for nome, testo in PEZZI.items():
    with open(os.path.join(CARTELLA, nome + ".svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(testo)
print(len(PEZZI), "disegni dell'uovo scritti")
