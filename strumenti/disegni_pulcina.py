# Disegni SVG degli indizi della pulcina (Tappa 24), al doppio della grandezza nel gioco.
# La pulcina è crema con la punta delle piume rosa; il suo segno è un fiocco rosa lavorato a maglia.
# - piuma: crema con la punta rosa, con lo stelo; nel gioco si ingrandisce di luogo in luogo
# - impronta: piccola orma a tre dita nel fango
# - filo: un filo di lana rosa, ondulato, con un capo sfilacciato
# - fiocco_maglia: fiocco rosa fatto a maglia (righe di punti a V), con il nodo in mezzo
# Uso: python strumenti/disegni_pulcina.py   (dalla cartella del progetto), poi python strumenti/stile_finale.py
import os

CARTELLA = os.path.join(os.path.dirname(__file__), "..", "assets", "grafica", "pulcina")
CREMA = "#FFF1DA"
CREMA_SCURO = "#E8CFA8"
ROSA = "#F59AB5"
ROSA_SCURO = "#C9667F"
ROSA_CHIARO = "#FFC4D5"


def svg(w, h, corpo):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{corpo}\n</svg>\n'


# piuma: 70×150, stelo in basso (35, 146); la punta rosa in alto, curva verso destra, con due "tagli" sul bordo
PIUMA = svg(70, 150, f'''<path d="M34 146 Q32 124 33 100" fill="none" stroke="{CREMA_SCURO}" stroke-width="5" stroke-linecap="round"/>
<path d="M33 104 Q12 98 9 74 L17 70 L8 62 Q8 30 40 6 Q62 26 62 54 L54 58 L62 64 Q58 96 33 104 Z" fill="{CREMA}" stroke="{CREMA_SCURO}" stroke-width="4" stroke-linejoin="round"/>
<path d="M40 6 Q56 18 61 40 Q50 36 41 28 Q30 36 14 38 Q24 16 40 6 Z" fill="{ROSA}"/>
<path d="M40 6 Q56 18 61 40 Q50 36 41 28 Q30 36 14 38 Q24 16 40 6 Z" fill="none" stroke="{ROSA_SCURO}" stroke-width="3" stroke-linejoin="round"/>
<path d="M33 100 Q36 60 41 12" fill="none" stroke="{CREMA_SCURO}" stroke-width="3.5" stroke-linecap="round"/>
<path d="M34 84 L18 76 M36 64 L18 54 M38 46 L24 40 M34 84 L52 76 M36 64 L54 52 M38 46 L52 40" stroke="{CREMA_SCURO}" stroke-width="2.5" stroke-linecap="round" opacity="0.6"/>
<path d="M14 92 Q8 96 5 104 M24 100 Q20 106 20 114" stroke="{CREMA_SCURO}" stroke-width="3" stroke-linecap="round" fill="none"/>''')

# impronta: 36×30, orma di uccellino che cammina verso destra: tre dita avanti e un ditino dietro
IMPRONTA = svg(36, 30, '''<path d="M4 15 L17 15 M17 15 L31 5 M17 15 L33 15 M17 15 L31 25" stroke="#6B4524" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" fill="none" opacity="0.75"/>''')

# filo: 140×44, filo di lana rosa ondulato con un capo sfilacciato a destra
FILO = svg(140, 44, f'''<path d="M6 30 Q22 8 40 24 Q58 40 76 20 Q92 4 108 22 Q118 32 126 26" fill="none" stroke="{ROSA_SCURO}" stroke-width="8" stroke-linecap="round"/>
<path d="M6 30 Q22 8 40 24 Q58 40 76 20 Q92 4 108 22 Q118 32 126 26" fill="none" stroke="{ROSA}" stroke-width="5" stroke-linecap="round"/>
<path d="M14 24 L18 20 M30 16 L34 20 M48 30 L52 26 M66 28 L70 24 M84 12 L88 16 M100 14 L104 18" stroke="{ROSA_CHIARO}" stroke-width="2" stroke-linecap="round"/>
<path d="M126 26 L136 20 M126 26 L137 28 M126 26 L133 36" stroke="{ROSA}" stroke-width="3" stroke-linecap="round"/>''')

# fiocco a maglia: 120×80, centro (60, 40); righe di punti a V sulle due ali
_v = []
for riga in range(4):
    y = 22 + riga * 11
    for x in (20, 32, 82, 94):
        _v.append(f"M{x - 4} {y} L{x} {y + 5} L{x + 4} {y}")
PUNTI = " ".join(_v)
FIOCCO = svg(120, 80, f'''<path d="M60 40 Q36 10 10 16 Q2 40 10 64 Q36 70 60 40 Z" fill="{ROSA}" stroke="{ROSA_SCURO}" stroke-width="4" stroke-linejoin="round"/>
<path d="M60 40 Q84 10 110 16 Q118 40 110 64 Q84 70 60 40 Z" fill="{ROSA}" stroke="{ROSA_SCURO}" stroke-width="4" stroke-linejoin="round"/>
<path d="{PUNTI}" fill="none" stroke="{ROSA_SCURO}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" opacity="0.65"/>
<path d="M54 46 L44 74 L54 70 L58 76 Z M66 46 L76 74 L66 70 L62 76 Z" fill="{ROSA}" stroke="{ROSA_SCURO}" stroke-width="3" stroke-linejoin="round"/>
<rect x="50" y="30" width="20" height="22" rx="8" fill="{ROSA_CHIARO}" stroke="{ROSA_SCURO}" stroke-width="4"/>
<path d="M54 36 L60 41 L66 36 M54 44 L60 49 L66 44" fill="none" stroke="{ROSA_SCURO}" stroke-width="2" stroke-linecap="round" opacity="0.7"/>''')

if __name__ == "__main__":
    os.makedirs(CARTELLA, exist_ok=True)
    for nome, testo in [("piuma", PIUMA), ("impronta", IMPRONTA), ("filo", FILO), ("fiocco_maglia", FIOCCO)]:
        with open(os.path.join(CARTELLA, nome + ".svg"), "w", encoding="utf-8", newline="\n") as f:
            f.write(testo)
    print("4 disegni della pulcina scritti")
