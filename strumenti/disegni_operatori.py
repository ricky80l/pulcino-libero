# Disegni SVG dei quattro operatori del magazzino filati, a pezzi (al doppio della grandezza nel gioco),
# e la pagina di anteprima strumenti/anteprima_operatori.html con le loro pose.
# Uso: python strumenti/disegni_operatori.py   (dalla cartella del progetto)
#
# Tutti hanno il camice blu da magazzino (come nella foto di Riccardo); si distinguono per testa e mani.
# Il personaggio è visto di fronte; l'origine è tra i piedi. Misure al doppio: alto circa 340.
import os
import re

QUI = os.path.dirname(__file__)
CARTELLA = os.path.join(QUI, "..", "assets", "grafica", "operatori")

CAMICE = "#2F3E7A"
CAMICE_LUCE = "#3D4F92"
CAMICE_SCURO = "#18203F"
MAGLIA = "#3B3B44"
POLSINO = "#B9E0A5"  # la maglia verde chiaro che spunta dalle maniche
PANTALONI = "#2A2D36"
SCARPE = "#1C1C1C"
LINEA = "#3A2616"  # contorno di viso e mani

OPERATORI = {
    # nome: pelle, capelli, contorno capelli, descrizione
    "moro": {"pelle": "#F2C7A0", "capelli": "#4A2F1B", "bordo": "#2A190D"},
    "biondo": {"pelle": "#F7D6BC", "capelli": "#F0C64A", "bordo": "#A87A16"},
    "indiano": {"pelle": "#A8693E", "capelli": "#1E1A1A", "bordo": "#000000"},
    "marocchino": {"pelle": "#C58A57", "capelli": "#241B16", "bordo": "#0E0907"},
}


def svg(w, h, corpo):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{corpo}\n</svg>\n'


def capelli(nome, o):
    c, b = o["capelli"], o["bordo"]
    if nome == "moro":
        # corti, con la riga di lato e il ciuffo pettinato
        return f'''<path d="M14 58 Q10 18 52 12 Q92 10 98 52 Q90 34 72 30 Q52 40 30 34 Q20 40 14 58 Z" fill="{c}" stroke="{b}" stroke-width="5" stroke-linejoin="round"/>
<path d="M66 30 Q56 22 40 24" fill="none" stroke="{b}" stroke-width="3" stroke-linecap="round"/>'''
    if nome == "biondo":
        # spettinati, a ciocche
        return f'''<path d="M12 60 Q6 30 22 20 L20 6 L36 14 L44 0 L56 12 L70 2 L74 16 L92 10 L88 26 Q102 40 98 60 Q92 40 76 36 L68 44 L60 34 L48 44 L40 34 Q22 40 12 60 Z" fill="{c}" stroke="{b}" stroke-width="5" stroke-linejoin="round"/>'''
    if nome == "indiano":
        # pettinati all'indietro, con un'onda sopra
        return f'''<path d="M14 56 Q8 20 40 10 Q60 0 82 10 Q100 20 98 54 Q92 32 80 28 Q66 22 50 26 Q30 30 14 56 Z" fill="{c}" stroke="{b}" stroke-width="5" stroke-linejoin="round"/>
<path d="M36 18 Q56 8 78 16" fill="none" stroke="#4A4040" stroke-width="3" stroke-linecap="round"/>'''
    # marocchino: ricci, una nuvola di cerchietti
    ricci = []
    for cx, cy, r in [(18, 46, 13), (16, 30, 13), (26, 16, 14), (42, 8, 14), (58, 6, 14), (74, 10, 14), (88, 20, 13),
                      (96, 34, 12), (96, 50, 11), (34, 26, 12), (52, 22, 12), (70, 26, 12)]:
        ricci.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}" stroke="{b}" stroke-width="4"/>')
    ricci.append(f'<path d="M14 40 Q56 20 98 42 L98 30 Q56 4 14 28 Z" fill="{c}"/>')
    for cx, cy in [(26, 18), (44, 10), (62, 9), (80, 14), (20, 34), (92, 30)]:
        ricci.append(f'<path d="M{cx - 5} {cy + 2} q5 -7 10 0" fill="none" stroke="#5A4A40" stroke-width="2.5" stroke-linecap="round"/>')
    return "\n".join(ricci)


def testa(nome, o):
    p = o["pelle"]
    occhi_colore = "#2E6FC4" if nome == "biondo" else "#2A1A10"
    pezzi = [
        # orecchie, collo, viso
        f'<ellipse cx="12" cy="66" rx="9" ry="13" fill="{p}" stroke="{LINEA}" stroke-width="4"/>',
        f'<ellipse cx="100" cy="66" rx="9" ry="13" fill="{p}" stroke="{LINEA}" stroke-width="4"/>',
        f'<rect x="40" y="96" width="32" height="22" fill="{p}" stroke="{LINEA}" stroke-width="4"/>',
        f'<ellipse cx="56" cy="62" rx="44" ry="48" fill="{p}" stroke="{LINEA}" stroke-width="5"/>',
    ]
    if nome == "marocchino":
        # barba corta lungo la mascella
        pezzi.append(f'<path d="M14 66 Q16 108 56 110 Q96 108 98 66 Q92 92 76 96 Q56 88 36 96 Q20 92 14 66 Z" fill="{o["capelli"]}" opacity="0.85"/>')
    pezzi.append(capelli(nome, o))
    pezzi += [
        # sopracciglia, occhi, naso, guance, sorriso
        f'<path d="M30 50 Q38 44 46 49 M66 49 Q74 44 82 50" fill="none" stroke="{o["bordo"] if nome != "biondo" else "#8A6414"}" stroke-width="4.5" stroke-linecap="round"/>',
        f'<ellipse cx="39" cy="62" rx="6.5" ry="8" fill="#FFFFFF"/><ellipse cx="73" cy="62" rx="6.5" ry="8" fill="#FFFFFF"/>',
        f'<circle cx="40" cy="63" r="4.5" fill="{occhi_colore}"/><circle cx="74" cy="63" r="4.5" fill="{occhi_colore}"/>',
        '<circle cx="41.5" cy="61" r="1.6" fill="#FFFFFF"/><circle cx="75.5" cy="61" r="1.6" fill="#FFFFFF"/>',
        f'<path d="M56 66 Q50 78 58 79" fill="none" stroke="{LINEA}" stroke-width="3.5" stroke-linecap="round"/>',
        '<ellipse cx="28" cy="80" rx="7" ry="4.5" fill="#FF8A8A" opacity="0.35"/><ellipse cx="84" cy="80" rx="7" ry="4.5" fill="#FF8A8A" opacity="0.35"/>',
        f'<path d="M40 88 Q56 100 72 88" fill="#FFFFFF" stroke="{LINEA}" stroke-width="4" stroke-linejoin="round"/>',
    ]
    return svg(112, 120, "\n".join(pezzi))


def braccio(o):
    # manica del camice e mano; perno alla spalla (20, 12)
    return svg(40, 136, f'''<path d="M6 10 Q20 0 34 10 L36 104 L4 104 Z" fill="{CAMICE}" stroke="{CAMICE_SCURO}" stroke-width="5" stroke-linejoin="round"/>
<path d="M12 20 L12 96" stroke="{CAMICE_LUCE}" stroke-width="4" stroke-linecap="round"/>
<rect x="6" y="100" width="28" height="9" rx="3" fill="{POLSINO}" stroke="{CAMICE_SCURO}" stroke-width="3"/>
<ellipse cx="20" cy="120" rx="14" ry="14" fill="{o["pelle"]}" stroke="{LINEA}" stroke-width="4"/>
<path d="M10 118 Q8 128 14 130" fill="none" stroke="{LINEA}" stroke-width="3" stroke-linecap="round"/>''')


# camice: perno in basso al centro (75, 176); spalle in alto a y 8
CORPO = svg(150, 180, f'''<path d="M18 22 Q40 4 75 6 Q110 4 132 22 L142 172 Q75 180 8 172 Z" fill="{CAMICE}" stroke="{CAMICE_SCURO}" stroke-width="5" stroke-linejoin="round"/>
<path d="M58 8 L75 50 L92 8 Z" fill="{MAGLIA}" stroke="{CAMICE_SCURO}" stroke-width="4" stroke-linejoin="round"/>
<path d="M56 6 L44 34 L66 40 L75 52 M94 6 L106 34 L84 40 L75 52" fill="{CAMICE_LUCE}" stroke="{CAMICE_SCURO}" stroke-width="4" stroke-linejoin="round"/>
<path d="M75 52 L75 172" stroke="{CAMICE_SCURO}" stroke-width="3"/>
<circle cx="82" cy="70" r="3.5" fill="{CAMICE_SCURO}"/><circle cx="82" cy="100" r="3.5" fill="{CAMICE_SCURO}"/>
<circle cx="82" cy="130" r="3.5" fill="{CAMICE_SCURO}"/><circle cx="82" cy="158" r="3.5" fill="{CAMICE_SCURO}"/>
<path d="M98 66 L122 66" stroke="{CAMICE_SCURO}" stroke-width="3" stroke-linecap="round"/>
<path d="M28 120 L58 120 L58 140 L28 140 Z M92 120 L122 120 L122 140 L92 140 Z" fill="none" stroke="{CAMICE_SCURO}" stroke-width="3" stroke-linejoin="round"/>''')

# gamba: perno in alto (22, 6)
GAMBA = svg(44, 126, f'''<path d="M6 4 L38 4 L36 104 L8 104 Z" fill="{PANTALONI}" stroke="#15161B" stroke-width="4" stroke-linejoin="round"/>
<path d="M2 102 Q2 96 10 96 L36 96 Q44 96 42 104 L42 116 L2 116 Z" fill="{SCARPE}" stroke="#000000" stroke-width="3" stroke-linejoin="round"/>
<path d="M6 110 L40 110" stroke="#3A3A3A" stroke-width="2.5"/>''')


def scrivi():
    os.makedirs(CARTELLA, exist_ok=True)
    pezzi = {"corpo": CORPO, "gamba": GAMBA}
    for nome, o in OPERATORI.items():
        pezzi["testa_" + nome] = testa(nome, o)
        pezzi["braccio_" + nome] = braccio(o)
    for nome, testo in pezzi.items():
        with open(os.path.join(CARTELLA, nome + ".svg"), "w", encoding="utf-8", newline="\n") as f:
            f.write(testo)
    print(len(pezzi), "pezzi degli operatori scritti")
    return pezzi


# ---------------- anteprima ----------------

def interno(testo_svg):
    return re.sub(r"^<svg[^>]*>\n?|</svg>\s*$", "", testo_svg.strip())


def pezzo(testo_svg, perno, posizione, angolo=0.0, extra=""):
    return (f'<g transform="translate({posizione[0]} {posizione[1]}) rotate({angolo})"{extra}>'
            f'<g transform="translate({-perno[0]} {-perno[1]})">{interno(testo_svg)}</g></g>')


def operatore(pezzi, nome, braccio_sx=0.0, braccio_dx=0.0, abbassa=0.0, inclina=0.0, gambe=0.0):
    # le gambe restano a terra; busto, testa e braccia si abbassano e si inclinano insieme
    g = [pezzo(pezzi["gamba"], (22, 6), (-20, -120), gambe), pezzo(pezzi["gamba"], (22, 6), (20, -120), -gambe)]
    busto = [
        pezzo(pezzi["braccio_" + nome], (20, 12), (-60, -220), braccio_sx),
        pezzo(pezzi["braccio_" + nome], (20, 12), (60, -220), braccio_dx),
        pezzo(pezzi["corpo"], (75, 176), (0, -56)),
        pezzo(pezzi["testa_" + nome], (56, 116), (0, -226)),
    ]
    # le braccia davanti al camice quando sono alzate o incrociate, dietro quando pendono
    if abs(braccio_sx) > 20 or abs(braccio_dx) > 20:
        busto = busto[2:] + busto[:2]
    g.append(f'<g transform="translate(0 {abbassa}) rotate({inclina} 0 -110)">{"".join(busto)}</g>')
    return "".join(g)


def pulcino(posizione, angolo=0.0):
    base = os.path.join(QUI, "..", "assets", "grafica", "pulcino")
    leggi = lambda n: open(os.path.join(base, n), encoding="utf-8").read()
    su = 8  # stadio 2: un po' più alto sulle zampe (al doppio)
    parti = [
        pezzo(leggi("stadio2/zampa.svg"), (12, 2), (-14, -18 - su)),
        pezzo(leggi("stadio2/zampa.svg"), (12, 2), (12, -18 - su)),
        pezzo(leggi("stadio2/coda.svg"), (30, 28), (-34, -52 - su)),
        pezzo(leggi("stadio2/ciuffo.svg"), (22, 41), (-2, -94 - su)),
        pezzo(leggi("corpo.svg"), (50, 50), (0, -56 - su)),
        pezzo(leggi("stadio2/ala.svg"), (46, 16), (2, -56 - su), -35),
        pezzo(leggi("occhio.svg"), (14, 16), (18, -70 - su)),
        pezzo(leggi("becco_aperto.svg"), (3, 14), (38, -60 - su)),
    ]
    return f'<g transform="translate({posizione[0]} {posizione[1]}) rotate({angolo}) scale(0.9)">{"".join(parti)}</g>'


def fumetto(x, y, testo):
    return (f'<g transform="translate({x} {y})"><rect x="-62" y="-30" width="124" height="44" rx="18" fill="#FFFFFF" stroke="#3A2616" stroke-width="4"/>'
            f'<path d="M-14 12 L-24 34 L4 12 Z" fill="#FFFFFF" stroke="#3A2616" stroke-width="4" stroke-linejoin="round"/>'
            f'<rect x="-18" y="6" width="28" height="9" fill="#FFFFFF"/>'
            f'<text x="0" y="1" text-anchor="middle" font-family="Fredoka, Trebuchet MS, sans-serif" font-size="24" font-weight="600" fill="#3A2616">{testo}</text></g>')


def traiettoria(d):
    return f'<path d="{d}" fill="none" stroke="#E07A10" stroke-width="5" stroke-dasharray="4 12" stroke-linecap="round"/>'


MOSSE = [
    ("moro", "Italiano moro", "La «bagher»", "Mani unite come a pallavolo: lancia il pulcino dritto in alto, il lancio più alto di tutti.",
     dict(braccio_sx=-38, braccio_dx=38, abbassa=22, gambe=10),
     lambda: traiettoria("M0 -350 L0 -470") + pulcino((0, -500)), fumetto(120, -400, "Su!")),
    ("biondo", "Italiano biondo", "Il «tiro a canestro»", "Braccia in alto verso destra: lancia il pulcino ad arco lungo, in avanti.",
     dict(braccio_sx=172, braccio_dx=-150, inclina=6),
     lambda: traiettoria("M70 -360 Q200 -520 330 -300") + pulcino((300, -330), 30), fumetto(-110, -400, "Vai!")),
    ("indiano", "Indiano", "La «catapulta»", "Si piega e scatta: lancia il pulcino in diagonale verso l'alto, perfetto per salire sul soppalco.",
     dict(braccio_sx=-95, braccio_dx=-125, abbassa=34, inclina=14, gambe=14),
     lambda: traiettoria("M80 -300 L260 -500") + pulcino((280, -520), 20), fumetto(-110, -400, "Op-là!")),
    ("marocchino", "Marocchino con i ricci", "La «giravolta»", "Gira su se stesso a braccia larghe e lancia il pulcino lontanissimo, in orizzontale.",
     dict(braccio_sx=95, braccio_dx=-95, gambe=6),
     lambda: (traiettoria("M150 -230 L400 -250")
              + '<path d="M-150 -130 Q0 -60 150 -130" fill="none" stroke="#3D4F92" stroke-width="5" stroke-dasharray="14 10" stroke-linecap="round"/>'
              + pulcino((420, -230), 75)), fumetto(-40, -400, "Volaaa!")),
]


def anteprima(pezzi):
    schede = []
    for nome, chi, mossa, spiega, posa, extra, battuta in MOSSE:
        scena = (f'<svg viewBox="-260 -600 820 620" width="100%" style="max-width:520px">'
                 f'<rect x="-260" y="-600" width="820" height="620" fill="#EDE4D3"/>'
                 f'<rect x="-260" y="0" width="820" height="20" fill="#C9C2B5"/>'
                 f'<g transform="translate(-150 0) scale(0.75)">{operatore(pezzi, nome)}</g>'
                 f'<g transform="translate(110 0)">{operatore(pezzi, nome, **posa)}{extra()}{battuta}</g>'
                 f'</svg>')
        schede.append(f'<div class="scheda"><h2>{chi}</h2><div class="mossa">{mossa}</div>{scena}<p>{spiega}</p></div>')
    pagina = f'''<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Gli operatori</title>
<style>
:root {{ --testo:#3a2a10; --sfondo:#fbf6ea; --carta:#ffffff; --bordo:#e2d6bd; }}
@media (prefers-color-scheme: dark) {{ :root {{ --testo:#f4ead6; --sfondo:#22201b; --carta:#2e2b24; --bordo:#4a4436; }} }}
body {{ margin:0; padding:16px; font-family: system-ui, sans-serif; background:var(--sfondo); color:var(--testo); }}
h1 {{ font-size:22px; font-weight:600; margin:0 0 4px; }}
p.nota {{ margin:0 0 14px; opacity:.85; }}
.griglia {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(320px,1fr)); gap:14px; }}
.scheda {{ background:var(--carta); border:1px solid var(--bordo); border-radius:12px; padding:12px; }}
.scheda h2 {{ font-size:18px; font-weight:600; margin:0; }}
.mossa {{ font-weight:600; color:#C0611A; margin:2px 0 8px; }}
.scheda svg {{ display:block; border-radius:8px; }}
.scheda p {{ margin:8px 0 0; font-size:14px; }}
</style></head><body>
<h1>Gli operatori del magazzino filati</h1>
<p class="nota">Bozzetti per la Tappa 16. In ogni riquadro: a sinistra l'operatore fermo (più piccolo), a destra mentre fa la sua mossa, con il pulcino lanciato e la sua traiettoria (puntini arancioni). Tutti con il camice blu da magazzino.</p>
<div class="griglia">{"".join(schede)}</div>
</body></html>
'''
    with open(os.path.join(QUI, "anteprima_operatori.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(pagina)
    print("anteprima scritta")


if __name__ == "__main__":
    anteprima(scrivi())
