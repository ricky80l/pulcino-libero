# Disegni SVG dell'oca arrabbiata, a pezzi (al doppio della grandezza nel gioco).
# Uso: python strumenti/disegni_oca.py   (dalla cartella del progetto)
import os

CARTELLA = os.path.join(os.path.dirname(__file__), "..", "assets", "grafica", "oca")
G = "#6B6B78"  # contorno grigio
B = "#FFFFFF"
GRIGIO = "#E4E4EA"
ARANCIO = "#FF9A1F"
ARANCIO_SCURO = "#8A4A10"


def svg(w, h, corpo):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{corpo}\n</svg>\n'


PEZZI = {
    # corpo con la coda a punta verso sinistra; base (90, 104)
    "corpo": svg(180, 120, f'''<path d="M20 50 L2 34 L10 62 Z" fill="{B}" stroke="{G}" stroke-width="5" stroke-linejoin="round"/>
<ellipse cx="90" cy="62" rx="76" ry="42" fill="{B}" stroke="{G}" stroke-width="5"/>
<ellipse cx="96" cy="80" rx="52" ry="18" fill="{GRIGIO}"/>'''),
    # ala: perno davanti in alto (84, 18)
    "ala": svg(100, 64, f'''<path d="M90 18 Q60 4 18 16 Q2 30 14 44 Q50 60 88 34 Z" fill="{GRIGIO}" stroke="{G}" stroke-width="5" stroke-linejoin="round"/>
<path d="M30 30 Q50 34 70 28 M24 40 Q46 46 66 38" fill="none" stroke="{G}" stroke-width="3" stroke-linecap="round"/>'''),
    # collo e testa: perno alla base del collo (30, 124); la testa guarda a destra
    "collo": svg(80, 130, f'''<path d="M14 126 Q10 70 26 44 L54 44 Q40 78 46 126 Z" fill="{B}" stroke="{G}" stroke-width="5" stroke-linejoin="round"/>
<circle cx="40" cy="28" r="24" fill="{B}" stroke="{G}" stroke-width="5"/>
<path d="M18 120 Q30 112 44 120" fill="none" stroke="{GRIGIO}" stroke-width="6" stroke-linecap="round"/>'''),
    # becco: perno a sinistra al centro (4, 15)
    "becco": svg(54, 30, f'''<path d="M4 6 Q30 4 50 13 Q30 24 4 22 Z" fill="{ARANCIO}" stroke="{ARANCIO_SCURO}" stroke-width="4" stroke-linejoin="round"/>
<path d="M8 14 L40 14" stroke="{ARANCIO_SCURO}" stroke-width="2.5"/>'''),
    "becco_aperto": svg(54, 30, f'''<path d="M4 4 Q30 -2 52 2 Q30 12 4 13 Z" fill="{ARANCIO}" stroke="{ARANCIO_SCURO}" stroke-width="4" stroke-linejoin="round"/>
<path d="M4 17 Q28 20 46 28 Q26 30 4 26 Z" fill="{ARANCIO}" stroke="{ARANCIO_SCURO}" stroke-width="4" stroke-linejoin="round"/>
<path d="M8 14 Q20 16 30 14" stroke="#C0392B" stroke-width="4" stroke-linecap="round"/>'''),
    # occhi: centro (14, 14)
    "occhio": svg(28, 28, '''<circle cx="14" cy="14" r="6" fill="#1E1A22"/><circle cx="16" cy="11.5" r="2" fill="#FFFFFF"/>'''),
    "occhio_arrabbiato": svg(28, 28, '''<path d="M2 4 L26 11" stroke="#1E1A22" stroke-width="5" stroke-linecap="round"/>
<circle cx="15" cy="17" r="6" fill="#1E1A22"/><circle cx="17" cy="15" r="2" fill="#FFFFFF"/>'''),
    "occhio_stordito": svg(28, 28, '''<path d="M14 14 m0 -2 a2 2 0 1 1 -2 2 a4 4 0 1 1 4 4 a6 6 0 1 1 -6 -6 a8 8 0 1 1 8 8" fill="none" stroke="#1E1A22" stroke-width="2.5" stroke-linecap="round"/>'''),
    # zampa: perno in alto (20, 2)
    "zampa": svg(40, 36, f'''<path d="M20 2 L20 24" stroke="{ARANCIO}" stroke-width="6" stroke-linecap="round"/>
<path d="M20 22 L4 32 Q20 36 36 32 Z" fill="{ARANCIO}" stroke="{ARANCIO_SCURO}" stroke-width="3" stroke-linejoin="round"/>'''),
}

os.makedirs(CARTELLA, exist_ok=True)
for nome, testo in PEZZI.items():
    with open(os.path.join(CARTELLA, nome + ".svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(testo)
print(len(PEZZI), "pezzi dell'oca scritti")
