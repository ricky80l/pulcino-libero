# Icona del gioco: il pulcino (come nel cortile e nell'orto) che salta di gioia davanti al sole che sorge.
# Scrive strumenti/icona.svg; Godot la trasforma in icona.png (512×512) per il browser e il telefono.
# Uso: python strumenti/disegni_icona.py   (dalla cartella del progetto)
import math
import os
import re

QUI = os.path.dirname(__file__)
PULCINO = os.path.join(QUI, "..", "assets", "grafica", "pulcino")


def interno(nome):
    testo = open(os.path.join(PULCINO, nome), encoding="utf-8").read().strip()
    return re.sub(r"^<svg[^>]*>\n?|</svg>\s*$", "", testo)


def pezzo(nome, perno, posizione, angolo=0.0):
    return (f'<g transform="translate({posizione[0]} {posizione[1]}) rotate({angolo})">'
            f'<g transform="translate({-perno[0]} {-perno[1]})">{interno(nome)}</g></g>')


su = 8  # stadio 2: un po' più alto sulle zampe (misure al doppio, come nel gioco)
pulcino = "".join([
    pezzo("stadio2/zampa.svg", (12, 2), (-14, -18 - su), 35),
    pezzo("stadio2/zampa.svg", (12, 2), (12, -18 - su), 25),
    pezzo("stadio2/coda.svg", (30, 28), (-34, -52 - su), -15),
    pezzo("stadio2/ciuffo.svg", (22, 41), (-2, -94 - su), -8),
    pezzo("corpo.svg", (50, 50), (0, -56 - su)),
    pezzo("stadio2/ala.svg", (46, 16), (2, -56 - su), 50),
    pezzo("occhio.svg", (14, 16), (18, -70 - su)),
    pezzo("becco_aperto.svg", (3, 14), (38, -60 - su), -8),
])

# raggi del sole che sorge dietro il pulcino
centro = (256, 290)
raggi = []
for i in range(16):
    a1 = i * math.tau / 16
    a2 = a1 + math.tau / 32
    p1 = (centro[0] + math.cos(a1) * 520, centro[1] + math.sin(a1) * 520)
    p2 = (centro[0] + math.cos(a2) * 520, centro[1] + math.sin(a2) * 520)
    raggi.append(f'<path d="M{centro[0]} {centro[1]} L{p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f} Z"/>')

scintille = "".join(
    f'<path transform="translate({x} {y}) scale({s})" d="M0 -14 Q2 -2 14 0 Q2 2 0 14 Q-2 2 -14 0 Q-2 -2 0 -14 Z" fill="#FFFFFF"/>'
    for x, y, s in [(92, 120, 1.3), (420, 96, 1.0), (440, 250, 0.8), (70, 300, 0.7)])

icona = f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
<defs>
<linearGradient id="cielo" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#4FB0EE"/><stop offset="0.75" stop-color="#BDE6FB"/>
</linearGradient>
<radialGradient id="sole" cx="0.5" cy="0.5" r="0.5">
<stop offset="0" stop-color="#FFF4C2"/><stop offset="0.7" stop-color="#FFE27A"/><stop offset="1" stop-color="#FFD24A"/>
</radialGradient>
</defs>
<rect width="512" height="512" fill="url(#cielo)"/>
<g fill="#FFFFFF" opacity="0.28">{"".join(raggi)}</g>
<circle cx="{centro[0]}" cy="{centro[1]}" r="175" fill="url(#sole)"/>
<path d="M-20 430 Q130 360 300 410 Q420 440 540 390 L540 540 L-20 540 Z" fill="#A8D977"/>
<path d="M-20 470 Q180 410 360 455 Q450 476 540 450 L540 540 L-20 540 Z" fill="#6DBE45"/>
<path d="M-20 470 Q180 410 360 455 Q450 476 540 450" fill="none" stroke="#4E9A2E" stroke-width="6"/>
<ellipse cx="262" cy="468" rx="92" ry="14" fill="#2E6B1A" opacity="0.3"/>
{scintille}
<g transform="translate(236 405) scale(2.4)">{pulcino}</g>
</svg>
'''

with open(os.path.join(QUI, "icona.svg"), "w", encoding="utf-8", newline="\n") as f:
    f.write(icona)
print("icona scritta")
