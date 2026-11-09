# Disegni SVG dell'ape ronzante (Tappa 26), al doppio della grandezza nel gioco. Guarda a destra.
# - corpo: pancia tonda a strisce, pungiglione dietro, testa con occhione, antenne e sorriso (perno al centro della pancia)
# - ala: ala trasparente (perno all'attaccatura), ne servono due che sbattono velocissime
# - icona_ape (in oggetti/): il musetto per la stellina «Mai preso» a fine livello
# Uso: python strumenti/disegni_ape.py   (dalla cartella del progetto), poi python strumenti/stile_finale.py
import os

QUI = os.path.dirname(__file__)
CARTELLA = os.path.join(QUI, "..", "assets", "grafica", "ape")
OGGETTI = os.path.join(QUI, "..", "assets", "grafica", "oggetti")
GIALLO = "#FFD447"
BORDO = "#6A4A10"
STRISCIA = "#4A3410"


def svg(w, h, corpo):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{corpo}\n</svg>\n'


# corpo: 130×100, centro della pancia (56, 58)
CORPO = svg(130, 100, f'''<path d="M14 60 L2 66 L14 70 Z" fill="{STRISCIA}" stroke="{BORDO}" stroke-width="3" stroke-linejoin="round"/>
<ellipse cx="54" cy="60" rx="42" ry="31" fill="{GIALLO}" stroke="{BORDO}" stroke-width="5"/>
<path d="M36 32 Q28 60 36 88 L48 90 Q40 60 48 30 Z" fill="{STRISCIA}"/>
<path d="M62 30 Q54 60 62 90 L72 88 Q66 60 74 32 Z" fill="{STRISCIA}"/>
<ellipse cx="54" cy="60" rx="42" ry="31" fill="none" stroke="{BORDO}" stroke-width="5"/>
<path d="M30 48 Q40 40 52 42" fill="none" stroke="#FFF3B0" stroke-width="5" stroke-linecap="round"/>
<path d="M92 26 Q90 8 80 4 M104 26 Q110 8 122 6" fill="none" stroke="{STRISCIA}" stroke-width="4" stroke-linecap="round"/>
<circle cx="80" cy="4" r="5" fill="{STRISCIA}"/><circle cx="122" cy="6" r="5" fill="{STRISCIA}"/>
<circle cx="98" cy="44" r="25" fill="{GIALLO}" stroke="{BORDO}" stroke-width="5"/>
<ellipse cx="104" cy="38" rx="10" ry="12" fill="#FFFFFF" stroke="{BORDO}" stroke-width="2.5"/>
<circle cx="107" cy="40" r="6" fill="#22252A"/><circle cx="109" cy="37" r="2.2" fill="#FFFFFF"/>
<path d="M98 56 Q106 64 116 56" fill="none" stroke="{BORDO}" stroke-width="3.5" stroke-linecap="round"/>
<ellipse cx="90" cy="54" rx="6" ry="4" fill="#FF8A8A" opacity="0.5"/>''')

# ala: 60×44, attaccatura in basso a sinistra (8, 38)
ALA = svg(60, 44, '''<path d="M8 38 Q2 10 26 4 Q54 0 56 18 Q56 34 8 38 Z" fill="#EAF6FF" fill-opacity="0.75" stroke="#7FA9C8" stroke-width="3" stroke-linejoin="round"/>
<path d="M12 34 Q24 18 44 12 M14 36 Q30 30 50 24" fill="none" stroke="#9CC4E0" stroke-width="2" stroke-linecap="round" opacity="0.8"/>''')

# icona per la stellina: 80×80, il musetto con le antenne
ICONA = svg(80, 80, f'''<path d="M30 20 Q26 6 16 4 M50 20 Q56 6 66 6" fill="none" stroke="{STRISCIA}" stroke-width="4" stroke-linecap="round"/>
<circle cx="16" cy="4" r="5" fill="{STRISCIA}"/><circle cx="66" cy="6" r="5" fill="{STRISCIA}"/>
<circle cx="40" cy="46" r="30" fill="{GIALLO}" stroke="{BORDO}" stroke-width="5"/>
<path d="M14 40 Q40 32 66 40 L66 48 Q40 40 14 48 Z" fill="{STRISCIA}" opacity="0.85"/>
<ellipse cx="30" cy="52" rx="7" ry="8" fill="#FFFFFF" stroke="{BORDO}" stroke-width="2"/><ellipse cx="50" cy="52" rx="7" ry="8" fill="#FFFFFF" stroke="{BORDO}" stroke-width="2"/>
<circle cx="31" cy="53" r="4" fill="#22252A"/><circle cx="51" cy="53" r="4" fill="#22252A"/>
<path d="M32 66 Q40 72 48 66" fill="none" stroke="{BORDO}" stroke-width="3" stroke-linecap="round"/>''')

if __name__ == "__main__":
    os.makedirs(CARTELLA, exist_ok=True)
    for nome, testo, dove in [("corpo", CORPO, CARTELLA), ("ala", ALA, CARTELLA), ("icona_ape", ICONA, OGGETTI)]:
        with open(os.path.join(dove, nome + ".svg"), "w", encoding="utf-8", newline="\n") as f:
            f.write(testo)
    print("disegni dell'ape scritti")
