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
    # musetti per la terza stellina ("mai preso"): il nemico del luogo, riconoscibile anche piccolo
    "icona_topo": svg(80, 80, '''<circle cx="16" cy="24" r="14" fill="#9AA0A8" stroke="#4E535A" stroke-width="5"/>
<circle cx="64" cy="24" r="14" fill="#9AA0A8" stroke="#4E535A" stroke-width="5"/>
<circle cx="16" cy="24" r="7" fill="#F2A7B4"/><circle cx="64" cy="24" r="7" fill="#F2A7B4"/>
<path d="M40 76 Q12 70 12 48 Q12 26 40 26 Q68 26 68 48 Q68 70 40 76 Z" fill="#B4BAC2" stroke="#4E535A" stroke-width="5" stroke-linejoin="round"/>
<circle cx="29" cy="46" r="5.5" fill="#22252A"/><circle cx="51" cy="46" r="5.5" fill="#22252A"/>
<circle cx="31" cy="44" r="2" fill="#FFFFFF"/><circle cx="53" cy="44" r="2" fill="#FFFFFF"/>
<ellipse cx="40" cy="62" rx="7" ry="5.5" fill="#E77F96" stroke="#4E535A" stroke-width="3"/>
<path d="M30 62 L12 58 M30 66 L13 68 M50 62 L68 58 M50 66 L67 68" stroke="#4E535A" stroke-width="2.5" stroke-linecap="round"/>'''),
    "icona_oca": svg(80, 80, '''<path d="M10 74 Q8 40 24 22 Q40 6 58 18 Q70 28 64 46 Q60 58 48 64 Q40 70 40 76 Z" fill="#FFFFFF" stroke="#7A7F86" stroke-width="5" stroke-linejoin="round"/>
<path d="M58 30 Q78 30 78 40 Q78 48 60 46 Z" fill="#F29A2E" stroke="#9A5A10" stroke-width="4" stroke-linejoin="round"/>
<path d="M60 40 L76 40" stroke="#9A5A10" stroke-width="3" stroke-linecap="round"/>
<circle cx="44" cy="30" r="6" fill="#22252A"/><circle cx="46" cy="28" r="2.2" fill="#FFFFFF"/>
<path d="M36 20 L50 24" stroke="#22252A" stroke-width="4" stroke-linecap="round"/>'''),
    "stella_vuota": svg(100, 100,f'''<path d="{STELLA}" fill="#000000" fill-opacity="0.18" stroke="#FFF5DC" stroke-opacity="0.8" stroke-width="5" stroke-linejoin="round" stroke-dasharray="10 7"/>'''),
}

os.makedirs(CARTELLA, exist_ok=True)
for nome, testo in PEZZI.items():
    with open(os.path.join(CARTELLA, nome + ".svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(testo)
print(len(PEZZI), "disegni dei premi scritti")
