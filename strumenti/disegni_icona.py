# Icona del gioco: il pulcino protagonista, quasi di fronte, con un'espressione sicura e simpatica.
# Tre versioni da scegliere (A sole, B volo, C ritratto); quella scelta diventa strumenti/icona.svg
# e Godot la trasforma in icona.png (512×512) per il browser e il telefono.
# Niente sfumature morbide (Godot le trasforma male in immagine): luci, ombre e aloni sono forme sovrapposte.
# Uso: python strumenti/disegni_icona.py [cartella per le prove]   (dalla cartella del progetto)
#      senza cartella scrive strumenti/icona.svg con la versione in VERSIONE (A, B o C; scelta da Riccardo: C)
import math
import os
import sys

QUI = os.path.dirname(__file__)
CONTORNO = "#8A4E0E"
GIALLO = "#FFD03A"
GIALLO_OMBRA = "#F3A21C"
ALA = "#F7B92A"


def raggi(cx, cy, quanti, colore, opacita, lungo=600):
    pezzi = []
    for i in range(quanti):
        a1 = i * math.tau / quanti
        a2 = a1 + math.tau / (quanti * 2)
        p1 = (cx + math.cos(a1) * lungo, cy + math.sin(a1) * lungo)
        p2 = (cx + math.cos(a2) * lungo, cy + math.sin(a2) * lungo)
        pezzi.append(f'M{cx} {cy} L{p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f} Z')
    return f'<path d="{" ".join(pezzi)}" fill="{colore}" opacity="{opacita}"/>'


def alone(cx, cy, raggio, colore, forza=1.0):
    # alone di luce fatto di cerchi sovrapposti sempre più piccoli
    return "".join(f'<circle cx="{cx}" cy="{cy}" r="{raggio * (1 - i * 0.045):.0f}" fill="{colore}" opacity="{0.05 * forza:.3f}"/>'
                   for i in range(20))


def falce(r, dx, dy, passi=240):
    # la parte del cerchio (centro 0,0, raggio r) che resta fuori dallo stesso cerchio spostato di (dx, dy):
    # una falce d'ombra dal lato opposto alla luce. Si gira attorno al cerchio partendo dal punto più in ombra.
    dentro_spostato = lambda x, y: (x - dx) ** 2 + (y - dy) ** 2 < r * r
    centro_ombra = math.atan2(-dy, -dx)
    esterno = []
    for i in range(passi + 1):
        t = centro_ombra - math.pi + math.tau * i / passi
        x, y = r * math.cos(t), r * math.sin(t)
        if not dentro_spostato(x, y):
            esterno.append((x, y))
    interno = []
    for i in range(passi + 1):
        t = centro_ombra + math.pi - math.tau * i / passi
        x, y = dx + r * math.cos(t), dy + r * math.sin(t)
        if x * x + y * y < r * r:
            interno.append((x, y))
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in esterno + interno) + " Z"


def pulcino(ali_su=False, occhiolino=False):
    # disegnato attorno al centro del corpo (0, 0), raggio 150; guarda leggermente verso destra
    ala_sx = ('M-128 -10 C-200 -70 -230 -150 -196 -170 C-180 -120 -150 -90 -112 -70 Z'
              if ali_su else 'M-132 10 C-190 -10 -214 -60 -196 -86 C-168 -56 -140 -40 -110 -40 Z')
    ala_dx = ('M132 -6 C206 -60 236 -140 204 -164 C188 -114 156 -86 116 -64 Z'
              if ali_su else 'M128 40 C176 40 204 10 200 -16 C172 6 146 12 118 8 Z')
    occhio_sx = ('<path d="M-92 -34 Q-60 -52 -28 -34" fill="none" stroke="#3A1E08" stroke-width="12" stroke-linecap="round"/>'
                 if occhiolino else
                 '<ellipse cx="-60" cy="-36" rx="30" ry="37" fill="#FFFFFF" stroke="#5A3008" stroke-width="7"/>'
                 '<circle cx="-50" cy="-38" r="19" fill="#2B1608"/><circle cx="-43" cy="-47" r="7.5" fill="#FFFFFF"/>'
                 '<circle cx="-56" cy="-29" r="3.5" fill="#FFFFFF"/>')
    return f'''
<g fill="{ALA}" stroke="{CONTORNO}" stroke-width="9" stroke-linejoin="round"><path d="{ala_sx}"/><path d="{ala_dx}"/></g>
<path d="M-4 -142 C-34 -176 -58 -206 -40 -236 C-26 -206 -14 -192 -2 -176 C-6 -214 8 -246 34 -252 C30 -220 22 -196 18 -170
C34 -196 62 -212 86 -204 C64 -186 40 -168 26 -140 Z" fill="{GIALLO}" stroke="{CONTORNO}" stroke-width="9" stroke-linejoin="round"/>
<circle cx="0" cy="0" r="150" fill="{GIALLO}"/>
<path d="{falce(150, -26, -30)}" fill="{GIALLO_OMBRA}" opacity="0.8"/>
<ellipse cx="14" cy="64" rx="96" ry="64" fill="#FFF0B4" opacity="0.75"/>
<ellipse cx="-60" cy="-96" rx="42" ry="22" fill="#FFFFFF" opacity="0.45" transform="rotate(-28 -60 -96)"/>
<circle cx="0" cy="0" r="150" fill="none" stroke="{CONTORNO}" stroke-width="10"/>
<ellipse cx="-96" cy="22" rx="24" ry="15" fill="#FF8A80" opacity="0.55"/>
<ellipse cx="112" cy="16" rx="24" ry="15" fill="#FF8A80" opacity="0.55"/>
<path d="M-88 -84 Q-62 -100 -34 -88" fill="none" stroke="#7A4410" stroke-width="9" stroke-linecap="round"/>
<path d="M30 -94 Q62 -110 92 -94" fill="none" stroke="#7A4410" stroke-width="9" stroke-linecap="round"/>
{occhio_sx}
<ellipse cx="60" cy="-40" rx="33" ry="40" fill="#FFFFFF" stroke="#5A3008" stroke-width="7"/>
<circle cx="70" cy="-42" r="21" fill="#2B1608"/><circle cx="78" cy="-52" r="8.5" fill="#FFFFFF"/><circle cx="64" cy="-31" r="4" fill="#FFFFFF"/>
<path d="M-34 12 Q12 -6 58 12 Q30 28 12 30 Q-12 28 -34 12 Z" fill="#FF9A2E" stroke="#8A3A0A" stroke-width="7" stroke-linejoin="round"/>
<path d="M-26 22 Q12 74 50 22 Q30 32 12 34 Q-8 32 -26 22 Z" fill="#EE6A1E" stroke="#8A3A0A" stroke-width="7" stroke-linejoin="round"/>
<path d="M-6 40 Q12 58 30 40 Q12 46 -6 40 Z" fill="#E8474A"/>
<path d="M-18 8 Q4 2 22 8" fill="none" stroke="#FFD08A" stroke-width="5" stroke-linecap="round"/>'''


def icona(versione):
    if versione == "A":  # sole: il pulcino davanti a un sole che si allarga, caldo e luminoso
        sfondo = (f'<rect width="512" height="512" fill="#FF9A1E"/>{raggi(256, 300, 14, "#FFE27A", 0.22)}'
                  f'{alone(256, 300, 300, "#FFF2B0", 1.4)}')
        figura = f'<g transform="translate(256 318) scale(1.05)">{pulcino()}</g>'
    elif versione == "B":  # volo: ali spalancate nel cielo, il sole dietro come un'aureola
        sfondo = (f'<rect width="512" height="512" fill="#3FA6EC"/><rect y="256" width="512" height="256" fill="#62B8F0"/>'
                  f'{raggi(256, 250, 14, "#FFFFFF", 0.13)}{alone(256, 250, 250, "#FFE680", 1.3)}'
                  '<circle cx="256" cy="250" r="150" fill="#FFE27A" opacity="0.5"/>'
                  '<path d="M-20 470 Q90 430 170 458 Q250 486 330 456 Q420 424 532 462 L532 532 L-20 532 Z" fill="#FFFFFF" opacity="0.92"/>')
        figura = f'<g transform="translate(256 280) rotate(-6) scale(0.86)">{pulcino(ali_su=True)}</g>'
    else:  # ritratto: il pulcino da vicino che fa l'occhiolino, su un blu-verde intenso che lo fa risaltare
        sfondo = (f'<rect width="512" height="512" fill="#0F6C82"/>{alone(256, 300, 330, "#3CC4CC", 1.5)}'
                  f'{raggi(256, 290, 16, "#FFFFFF", 0.09)}{alone(256, 300, 230, "#FFE47A", 0.9)}')
        figura = f'<g transform="translate(256 330) scale(1.12)">{pulcino(occhiolino=True)}</g>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">\n'
            f'{sfondo}\n{figura}\n</svg>\n')


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cartella = sys.argv[1]
        os.makedirs(cartella, exist_ok=True)
        for v in "ABC":
            open(os.path.join(cartella, f"icona_{v}.svg"), "w", encoding="utf-8", newline="\n").write(icona(v))
        print("tre versioni scritte in", cartella)
    else:
        open(os.path.join(QUI, "icona.svg"), "w", encoding="utf-8", newline="\n").write(icona(os.environ.get("VERSIONE", "C")))
        print("icona scritta")
