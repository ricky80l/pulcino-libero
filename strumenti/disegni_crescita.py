# Disegni SVG dello stadio 3 del pulcino (prato e bosco) e pagina di anteprima con gli stadi 1, 2 e 3 affiancati.
# Uso: python strumenti/disegni_crescita.py   (dalla cartella del progetto)
# Scrive assets/grafica/pulcino/stadio3/*.svg e strumenti/anteprima_crescita3.html
# Stadio 3 (vedi CLAUDE.md): come lo stadio 2, in più piumette chiare sul dorso, giallo più caldo, corpo un po' più grande.
import os
import re

QUI = os.path.dirname(__file__)
PULCINO = os.path.join(QUI, "..", "assets", "grafica", "pulcino")
CARTELLA = os.path.join(PULCINO, "stadio3")
C = "#7A4E12"  # contorno
CALDO = "#FFC53A"  # giallo più caldo dello stadio 3
CALDO_ALA = "#F0AE22"
PANCIA = "#FFE07A"
PIUMETTA = "#FFF2C8"
SCALA = 1.1  # lo stadio 3 è un po' più grande: i pezzi si allargano attorno ai piedi


def svg(w, h, corpo):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{corpo}\n</svg>\n'


def piumetta(x, y, angolo, lungo=16):
    # una piumetta chiara a goccia, con la sua venatura
    return (f'<g transform="translate({x} {y}) rotate({angolo})"><path d="M0 0 Q-6 -{lungo * 0.5} 0 -{lungo} Q6 -{lungo * 0.5} 0 0 Z" '
            f'fill="{PIUMETTA}" stroke="#C9962A" stroke-width="2.5" stroke-linejoin="round"/>'
            f'<path d="M0 -2 L0 -{lungo - 4}" stroke="#E2C27A" stroke-width="1.6"/></g>')


PEZZI = {
    # corpo: centro (55, 55), raggio un po' più grande del 44 degli stadi 1 e 2
    "corpo": svg(110, 110, f'''<circle cx="55" cy="55" r="48" fill="{CALDO}" stroke="{C}" stroke-width="5"/>
<ellipse cx="62" cy="71" rx="29" ry="20" fill="{PANCIA}"/>
<circle cx="80" cy="63" r="6.5" fill="#FF9E9E" fill-opacity="0.75"/>
{piumetta(32, 42, -55, 14)}{piumetta(41, 31, -32, 14)}{piumetta(27, 57, -78, 12)}{piumetta(52, 25, -10, 12)}'''),
    # ciuffo a tre riccioli, come lo stadio 2 ma più caldo; perno (22, 41)
    "ciuffo": svg(52, 44, f'''<path d="M22 41 C10 27 2 15 8 3 C14 13 18 21 22 27 C22 15 26 5 34 3 C34 13 30 23 26 33 C32 23 42 17 50 19 C42 27 32 35 22 41 Z" fill="{CALDO}" stroke="{C}" stroke-width="3.5" stroke-linejoin="round"/>'''),
    # ala con le penne a punta, più lunga; perno (50, 16)
    "ala": svg(60, 54, f'''<path d="M56 18 Q28 2 4 16 Q0 28 9 33 Q4 40 13 45 Q13 52 25 49 Q44 42 56 18 Z" fill="{CALDO_ALA}" stroke="{C}" stroke-width="4" stroke-linejoin="round"/>
<path d="M16 26 Q30 31 44 26 M20 36 Q30 39 40 34" fill="none" stroke="{C}" stroke-width="2.5" stroke-linecap="round"/>'''),
    # codina di piume più folta; perno (32, 30)
    "coda": svg(40, 50, f'''<path d="M34 24 L8 4 L16 21 L2 26 L18 31 L6 44 L22 38 L20 48 L34 36 Z" fill="{CALDO_ALA}" stroke="{C}" stroke-width="3.5" stroke-linejoin="round"/>
<path d="M14 18 L24 26" stroke="{PIUMETTA}" stroke-width="2.5" stroke-linecap="round"/>'''),
}


# ---------------- anteprima ----------------

def leggi(nome):
    testo = open(os.path.join(PULCINO, nome), encoding="utf-8").read().strip()
    return re.sub(r"^<svg[^>]*>\n?|</svg>\s*$", "", testo)


def pezzo(contenuto, perno, posizione, angolo=0.0):
    return (f'<g transform="translate({posizione[0]:.1f} {posizione[1]:.1f}) rotate({angolo})">'
            f'<g transform="translate({-perno[0]} {-perno[1]})">{contenuto}</g></g>')


def interno(testo):
    return re.sub(r"^<svg[^>]*>\n?|</svg>\s*$", "", testo.strip())


def monta(stadio):
    # stessi punti di aspetto_pulcino.gd (al doppio); lo stadio 3 allarga tutto attorno ai piedi
    if stadio == 1:
        su, k = 0, 1.0
        parti = {"zampa": (leggi("zampa.svg"), (12, 2)), "ciuffo": (leggi("ciuffo.svg"), (20, 32)),
                 "ala": (leggi("ala.svg"), (38, 12)), "coda": None, "corpo": (leggi("corpo.svg"), (50, 50))}
    elif stadio == 2:
        su, k = 8, 1.0
        parti = {"zampa": (leggi("stadio2/zampa.svg"), (12, 2)), "ciuffo": (leggi("stadio2/ciuffo.svg"), (22, 41)),
                 "ala": (leggi("stadio2/ala.svg"), (46, 16)), "coda": (leggi("stadio2/coda.svg"), (30, 28)),
                 "corpo": (leggi("corpo.svg"), (50, 50))}
    else:
        su, k = 8, SCALA
        parti = {"zampa": (leggi("stadio2/zampa.svg"), (12, 2)), "ciuffo": (interno(PEZZI["ciuffo"]), (22, 41)),
                 "ala": (interno(PEZZI["ala"]), (50, 16)), "coda": (interno(PEZZI["coda"]), (32, 30)),
                 "corpo": (interno(PEZZI["corpo"]), (55, 55))}
    p = lambda x, y: (x * k, (y - su) * k)
    g = [pezzo(*parti["zampa"], p(-14, -18)), pezzo(*parti["zampa"], p(12, -18))]
    if parti["coda"]:
        g.append(pezzo(*parti["coda"], p(-34, -52)))
    g += [pezzo(*parti["ciuffo"], p(-2, -94)), pezzo(*parti["corpo"], p(0, -56)), pezzo(*parti["ala"], p(2, -56)),
          pezzo(leggi("occhio.svg"), (14, 16), p(18, -70)), pezzo(leggi("becco.svg"), (3, 14), p(38, -60))]
    return "".join(g)


def anteprima():
    schede = []
    for stadio, titolo, spiega in [
        (1, "Stadio 1 — pollaio", "Batuffolo tondo, ciuffetto, alucce corte."),
        (2, "Stadio 2 — cortile, orto, Maglificio Granada", "Ciuffo a tre riccioli, ala con le prime penne, codina, zampe più lunghe."),
        (3, "Stadio 3 — prato, bosco (nuovo)", "In più: piumette chiare sul dorso, giallo più caldo, corpo un po' più grande (+10%), ala e codina un po' più folte."),
    ]:
        disegno = (f'<svg viewBox="-80 -175 200 185" width="220" height="203"><ellipse cx="0" cy="2" rx="46" ry="6" fill="#000" opacity="0.1"/>'
                   f'{monta(stadio)}</svg>')
        schede.append(f'<div class="scheda{" nuova" if stadio == 3 else ""}"><div class="disegno">{disegno}</div><h2>{titolo}</h2><p>{spiega}</p></div>')
    vicino = (f'<svg viewBox="-80 -175 200 185" width="300" height="277">{monta(3)}</svg>')
    pagina = f'''<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Il pulcino cresce</title>
<style>
:root {{ --testo:#3a2a10; --sfondo:#fbf6ea; --carta:#ffffff; --bordo:#e2d6bd; }}
@media (prefers-color-scheme: dark) {{ :root {{ --testo:#f4ead6; --sfondo:#22201b; --carta:#2e2b24; --bordo:#4a4436; }} }}
body {{ margin:0; padding:16px; font-family: system-ui, sans-serif; background:var(--sfondo); color:var(--testo); }}
h1 {{ font-size:22px; font-weight:600; margin:0 0 4px; }}
p.nota {{ margin:0 0 14px; opacity:.85; }}
.griglia {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(230px,1fr)); gap:14px; }}
.scheda {{ background:var(--carta); border:1px solid var(--bordo); border-radius:12px; padding:12px; text-align:center; }}
.scheda.nuova {{ border:2px solid #E0A010; }}
.scheda h2 {{ font-size:16px; font-weight:600; margin:6px 0 2px; }}
.scheda p {{ margin:4px 0 0; font-size:14px; }}
.disegno {{ display:flex; justify-content:center; background:#cfe9fb; border-radius:8px; }}
.vicino {{ margin-top:16px; background:var(--carta); border:1px solid var(--bordo); border-radius:12px; padding:12px; text-align:center; }}
</style></head><body>
<h1>Il pulcino cresce: lo stadio 3</h1>
<p class="nota">Bozzetto per la Tappa 19. I tre stadi alla stessa scala, uno accanto all'altro. Nel gioco i pezzi restano animati come adesso (ali, ciuffo, codina, zampe).</p>
<div class="griglia">{"".join(schede)}</div>
<div class="vicino"><h2 style="font-size:16px;margin:0 0 6px">Stadio 3 da vicino: le piumette chiare sul dorso</h2>{vicino}</div>
</body></html>
'''
    with open(os.path.join(QUI, "anteprima_crescita3.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(pagina)


if __name__ == "__main__":
    os.makedirs(CARTELLA, exist_ok=True)
    for nome, testo in PEZZI.items():
        with open(os.path.join(CARTELLA, nome + ".svg"), "w", encoding="utf-8", newline="\n") as f:
            f.write(testo)
    anteprima()
    print(len(PEZZI), "pezzi dello stadio 3 scritti, anteprima pronta")
