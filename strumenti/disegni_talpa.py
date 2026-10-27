# Disegni SVG della talpa dispettosa (al doppio della grandezza nel gioco).
# Uso: python strumenti/disegni_talpa.py   (dalla cartella del progetto)
import os

CARTELLA = os.path.join(os.path.dirname(__file__), "..", "assets", "grafica", "talpa")
C = "#3A2A20"          # contorno
PELO = "#6B5A4E"
MUSO = "#A89080"
ROSA = "#F2A7B5"


def svg(w, h, corpo):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{corpo}\n</svg>\n'


TESTA = f'''<path d="M14 132 L14 62 Q14 8 60 8 Q106 8 106 62 L106 132 Z" fill="{PELO}" stroke="{C}" stroke-width="5" stroke-linejoin="round"/>
<path d="M44 14 Q50 4 58 12 M62 12 Q70 4 76 14" fill="none" stroke="{C}" stroke-width="3.5" stroke-linecap="round"/>
<ellipse cx="60" cy="74" rx="30" ry="24" fill="{MUSO}"/>'''

PEZZI = {
    # talpa normale: occhi socchiusi e furbi, dentoni
    "talpa": svg(120, 134, TESTA + f'''
<path d="M30 46 Q38 40 46 46 M74 46 Q82 40 90 46" fill="none" stroke="{C}" stroke-width="4" stroke-linecap="round"/>
<path d="M50 84 L50 96 L60 96 L60 84 Z M60 84 L60 96 L70 96 L70 84 Z" fill="#FFFFFF" stroke="{C}" stroke-width="2.5"/>
<ellipse cx="60" cy="66" rx="13" ry="10" fill="{ROSA}" stroke="{C}" stroke-width="3.5"/>
<ellipse cx="56" cy="63" rx="4" ry="3" fill="#FFFFFF" fill-opacity="0.7"/>'''),
    # talpa che fa "bu!": occhi spalancati e bocca aperta
    "talpa_bu": svg(120, 134, TESTA + f'''
<circle cx="40" cy="44" r="9" fill="#FFFFFF" stroke="{C}" stroke-width="3"/><circle cx="42" cy="45" r="4.5" fill="{C}"/>
<circle cx="80" cy="44" r="9" fill="#FFFFFF" stroke="{C}" stroke-width="3"/><circle cx="78" cy="45" r="4.5" fill="{C}"/>
<ellipse cx="60" cy="94" rx="14" ry="12" fill="#5A1E1E" stroke="{C}" stroke-width="3"/>
<path d="M53 83 L53 90 L60 90 L60 83 Z M60 83 L60 90 L67 90 L67 83 Z" fill="#FFFFFF" stroke="{C}" stroke-width="2"/>
<ellipse cx="60" cy="66" rx="14" ry="11" fill="{ROSA}" stroke="{C}" stroke-width="3.5"/>
<ellipse cx="56" cy="63" rx="4" ry="3" fill="#FFFFFF" fill-opacity="0.7"/>'''),
    # zampa con gli artigli, appoggiata al bordo della buca: perno in basso al centro (22, 30)
    "zampa": svg(44, 32, f'''<ellipse cx="22" cy="18" rx="19" ry="12" fill="{ROSA}" stroke="{C}" stroke-width="3.5"/>
<path d="M10 8 L8 2 M18 6 L17 0 M26 6 L27 0 M34 8 L36 2" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
<path d="M10 8 L8 2 M18 6 L17 0 M26 6 L27 0 M34 8 L36 2" stroke="{C}" stroke-width="1.2" stroke-linecap="round"/>'''),
}

os.makedirs(CARTELLA, exist_ok=True)
for nome, testo in PEZZI.items():
    with open(os.path.join(CARTELLA, nome + ".svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(testo)
print(len(PEZZI), "pezzi della talpa scritti")
