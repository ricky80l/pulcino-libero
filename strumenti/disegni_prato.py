# Disegni SVG dei pezzi nuovi del prato (Tappa 25), al doppio della grandezza nel gioco.
# - soffione: soffione gigante con la testa bianca di semi (base dello stelo in basso al centro)
# - soffione_spoglio: lo stesso dopo la beccata, senza semi
# - seme: un seme col suo ciuffetto, per i semi che volano via
# - sasso: sasso grande col muschio, ci si sale sopra
# - tronco: tronco caduto, ci si sale sopra
# - fascina: fascio di rametti legato con lo spago, da beccare
# - fiori: ciuffo di fiori colorati (decorazione)
# - sagoma_pulcina: la pulcina lontana su una collina (indizio della Tappa 24): si capisce solo il fiocco
# Uso: python strumenti/disegni_prato.py   (dalla cartella del progetto), poi python strumenti/stile_finale.py
import math
import os

CARTELLA = os.path.join(os.path.dirname(__file__), "..", "assets", "grafica", "prato")
VERDE = "#6FAE3A"
VERDE_SCURO = "#3E7A22"


def svg(w, h, corpo):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{corpo}\n</svg>\n'


def testa_di_semi(cx, cy, r):
    """Palla di semi: tanti raggi sottili che finiscono con un ciuffetto, sopra un alone bianco."""
    parti = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFFFFF" opacity="0.55"/>',
             f'<circle cx="{cx}" cy="{cy}" r="{r * 0.82}" fill="#FFFFFF" opacity="0.6"/>']
    for k in range(36):
        a = k * math.tau / 36 + (0.05 if k % 2 else 0)
        x2, y2 = cx + math.cos(a) * r * 0.92, cy + math.sin(a) * r * 0.92
        parti.append(f'<path d="M{cx} {cy} L{x2:.1f} {y2:.1f}" stroke="#D8DEE4" stroke-width="2"/>')
        parti.append(f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="5.5" fill="#FFFFFF" stroke="#C9D2DA" stroke-width="1.5"/>')
    parti.append(f'<circle cx="{cx}" cy="{cy}" r="{r * 0.16}" fill="#C9A445" stroke="#8A6A1E" stroke-width="3"/>')
    return "\n".join(parti)


FOGLIE = (f'<path d="M80 296 Q40 286 22 252 Q52 258 78 286 Z" fill="{VERDE}" stroke="{VERDE_SCURO}" stroke-width="4" stroke-linejoin="round"/>\n'
          f'<path d="M80 296 Q122 284 140 246 Q108 256 82 284 Z" fill="{VERDE}" stroke="{VERDE_SCURO}" stroke-width="4" stroke-linejoin="round"/>')
STELO = f'<path d="M80 296 Q74 200 80 112" fill="none" stroke="{VERDE_SCURO}" stroke-width="12" stroke-linecap="round"/>\n' \
        f'<path d="M80 296 Q74 200 80 112" fill="none" stroke="{VERDE}" stroke-width="7" stroke-linecap="round"/>'

# soffione: 160×300, base dello stelo (80, 296), testa di semi centrata a (80, 66)
SOFFIONE = svg(160, 300, STELO + "\n" + FOGLIE + "\n" + testa_di_semi(80, 66, 62))
SOFFIONE_SPOGLIO = svg(160, 300, STELO + "\n" + FOGLIE + "\n"
                       + '<circle cx="80" cy="104" r="12" fill="#C9A445" stroke="#8A6A1E" stroke-width="3"/>\n'
                       + '<path d="M72 98 L66 90 M80 94 L80 84 M88 98 L94 90" stroke="#D8DEE4" stroke-width="2.5" stroke-linecap="round"/>')

# seme: 30×50, il seme in basso e il ciuffetto in alto
SEME = svg(30, 50, '''<path d="M15 46 L15 18" stroke="#B9C2CA" stroke-width="2"/>
<path d="M15 18 L3 6 M15 18 L9 3 M15 18 L15 2 M15 18 L21 3 M15 18 L27 6" stroke="#E6ECF0" stroke-width="2" stroke-linecap="round"/>
<ellipse cx="15" cy="44" rx="3" ry="5" fill="#8A6A1E"/>''')

# sasso: 260×150, appoggiato in basso
SASSO = svg(260, 150, f'''<path d="M10 146 Q4 92 40 60 Q78 22 136 20 Q206 18 238 64 Q262 100 250 146 Z" fill="#A7A89E" stroke="#5E5F57" stroke-width="5" stroke-linejoin="round"/>
<path d="M30 146 Q30 110 58 90 Q90 70 130 74 Q180 76 210 104 Q226 120 228 146 Z" fill="#94958B"/>
<path d="M56 48 Q96 26 140 30 Q120 44 96 50 Q74 56 56 48 Z" fill="#C4C5BB"/>
<path d="M40 60 Q78 22 136 20 Q206 18 238 64 Q196 46 150 44 Q92 40 40 60 Z" fill="#7CB342" stroke="#4E7F22" stroke-width="3" stroke-linejoin="round"/>
<path d="M66 40 L62 30 M100 28 L98 18 M150 26 L152 16 M196 36 L202 28" stroke="#4E7F22" stroke-width="3" stroke-linecap="round"/>
<path d="M150 96 Q170 104 176 122 M70 112 Q84 116 88 128" fill="none" stroke="#6E6F66" stroke-width="3" stroke-linecap="round"/>''')

# tronco: 380×120, sdraiato, appoggiato in basso
TRONCO = svg(380, 120, '''<rect x="40" y="16" width="300" height="96" rx="20" fill="#9A6A3C" stroke="#5A3A1A" stroke-width="5"/>
<path d="M60 40 Q140 34 220 42 Q280 46 320 40 M64 70 Q150 64 240 72 Q290 76 322 70 M70 94 Q160 90 250 96" fill="none" stroke="#6B4424" stroke-width="4" stroke-linecap="round"/>
<ellipse cx="340" cy="64" rx="34" ry="48" fill="#E2C08A" stroke="#5A3A1A" stroke-width="5"/>
<ellipse cx="340" cy="64" rx="22" ry="32" fill="none" stroke="#B8915A" stroke-width="3"/>
<ellipse cx="340" cy="64" rx="10" ry="15" fill="none" stroke="#B8915A" stroke-width="3"/>
<ellipse cx="40" cy="64" rx="30" ry="46" fill="#7E5530" stroke="#5A3A1A" stroke-width="5"/>
<path d="M150 16 Q160 4 176 8 Q168 14 166 18 Z" fill="#7CB342" stroke="#4E7F22" stroke-width="2"/>
<path d="M120 112 Q126 100 138 102 M260 112 Q266 98 280 100" fill="none" stroke="#7CB342" stroke-width="4" stroke-linecap="round"/>''')

# fascina: 130×110, appoggiata in basso
_rami = []
for i, (x1, x2) in enumerate([(14, 116), (10, 120), (18, 112), (8, 122), (22, 108), (12, 118)]):
    y = 30 + i * 12
    _rami.append(f'<path d="M{x1} {y + 4} Q65 {y - 6} {x2} {y + 2}" fill="none" stroke="#5A3A1A" stroke-width="12" stroke-linecap="round"/>')
    _rami.append(f'<path d="M{x1} {y + 4} Q65 {y - 6} {x2} {y + 2}" fill="none" stroke="#9A6A3C" stroke-width="7" stroke-linecap="round"/>')
FASCINA = svg(130, 110, "\n".join(_rami) + '''
<path d="M24 26 L14 12 M108 30 L120 16 M30 92 L18 104 M100 94 L112 104" stroke="#7E5530" stroke-width="5" stroke-linecap="round"/>
<path d="M50 24 L50 104 M80 24 L80 104" stroke="#C9A445" stroke-width="6" stroke-linecap="round"/>
<path d="M50 24 L50 104 M80 24 L80 104" stroke="#8A6A1E" stroke-width="2"/>''')


def fiore(cx, cy, petali, centro, r=11):
    parti = []
    for k in range(5):
        a = k * math.tau / 5 - math.pi / 2
        parti.append(f'<circle cx="{cx + math.cos(a) * r:.1f}" cy="{cy + math.sin(a) * r:.1f}" r="{r * 0.72:.1f}" fill="{petali}" stroke="#00000022" stroke-width="1.5"/>')
    parti.append(f'<circle cx="{cx}" cy="{cy}" r="{r * 0.5:.1f}" fill="{centro}"/>')
    return "\n".join(parti)


# fiori: 160×80, ciuffo di erba con fiori di quattro colori
FIORI = svg(160, 80, f'''<path d="M10 78 Q30 40 44 78 M40 78 Q56 30 70 78 M70 78 Q86 36 100 78 M96 78 Q114 42 126 78 M120 78 Q138 46 150 78" fill="{VERDE}" stroke="{VERDE_SCURO}" stroke-width="3" stroke-linejoin="round"/>
{fiore(34, 34, "#FF9EC0", "#FFD84A")}
{fiore(76, 22, "#FFD84A", "#E08A2E")}
{fiore(114, 36, "#FFFFFF", "#FFD84A")}
{fiore(142, 50, "#B48CF2", "#FFF1B3", 9)}''')

# la pulcina lontana: 90×100, una sagoma morbida color crema e rosa, girata di spalle; si legge bene solo il fiocco
SAGOMA = svg(90, 100, '''<ellipse cx="45" cy="66" rx="30" ry="28" fill="#F1D9C4"/>
<circle cx="45" cy="34" r="20" fill="#F1D9C4"/>
<path d="M36 16 Q40 4 46 14 Q50 4 56 16" fill="none" stroke="#F1D9C4" stroke-width="6" stroke-linecap="round"/>
<path d="M18 62 Q8 56 6 70 Q14 72 20 70 Z M72 62 Q82 56 84 70 Q76 72 70 70 Z" fill="#F4A9BF"/>
<path d="M45 22 Q34 10 26 14 Q24 24 28 30 Q36 30 45 22 Z M45 22 Q56 10 64 14 Q66 24 62 30 Q54 30 45 22 Z" fill="#F59AB5" stroke="#C9667F" stroke-width="2.5" stroke-linejoin="round"/>
<circle cx="45" cy="22" r="5" fill="#FFC4D5" stroke="#C9667F" stroke-width="2"/>
<path d="M36 92 L34 99 M54 92 L56 99" stroke="#E0B48A" stroke-width="4" stroke-linecap="round"/>''')

if __name__ == "__main__":
    os.makedirs(CARTELLA, exist_ok=True)
    pezzi = [("soffione", SOFFIONE), ("soffione_spoglio", SOFFIONE_SPOGLIO), ("seme", SEME), ("sasso", SASSO),
             ("tronco", TRONCO), ("fascina", FASCINA), ("fiori", FIORI), ("sagoma_pulcina", SAGOMA)]
    for nome, testo in pezzi:
        with open(os.path.join(CARTELLA, nome + ".svg"), "w", encoding="utf-8", newline="\n") as f:
            f.write(testo)
    print(len(pezzi), "disegni del prato scritti")
