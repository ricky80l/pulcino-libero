# Disegni SVG dei pezzi nuovi del magazzino filati (livello 4) e pagina di anteprima con una scena d'esempio.
# Uso: python strumenti/disegni_magazzino.py   (dalla cartella del progetto)
# Scrive assets/grafica/magazzino/*.svg, assets/grafica/mappa/magazzino.svg e strumenti/anteprima_magazzino.html
# Ispirati alle foto del magazzino vero di Riccardo, ma sulle scatole solo scritte inventate (niente marchi).
# Tutti i disegni sono al doppio della grandezza nel gioco. Pareti, soffitto, pavimento e soppalco
# sono pezzi lunghi: nel gioco si disegnano da codice; qui ne mostro l'aspetto nella scena d'esempio.
import os
import random
import sys

QUI = os.path.dirname(__file__)
sys.path.insert(0, QUI)
import disegni_operatori as op  # noqa: E402

CARTELLA = os.path.join(QUI, "..", "assets", "grafica", "magazzino")
MAPPA = os.path.join(QUI, "..", "assets", "grafica", "mappa")

CARTONE = "#C99B62"
CARTONE_LUCE = "#D9B07A"
CARTONE_SCURO = "#8E6A3E"
NASTRO = "#E2C695"
LEGNO = "#C9A26B"
LEGNO_SCURO = "#7A5A30"
BLU = "#2C4F8C"
BLU_SCURO = "#1A3260"
AZZURRO = "#2F6DB5"
AZZURRO_SCURO = "#1C4A80"
GRIGIO = "#A9B0B8"
GRIGIO_SCURO = "#6E757D"
CONI = ["#F4A7B9", "#F2F0EA", "#3A3A40", "#6BBF8A", "#D9C29A", "#C8433A", "#8FB8E8", "#F2C14E"]


def svg(w, h, corpo):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{corpo}\n</svg>\n'


def etichetta(x, y, w=44, h=30):
    # etichetta bianca di spedizione con il codice a barre
    barre = "".join(f'<rect x="{x + 6 + i * 3.2:.1f}" y="{y + h - 12}" width="{1.6 if i % 3 else 2.4}" height="8" fill="#333"/>'
                    for i in range(int((w - 12) / 3.2)))
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="#FAFAF5" stroke="#9A9A9A" stroke-width="1.5"/>'
            f'<path d="M{x + 6} {y + 7} L{x + w - 10} {y + 7} M{x + 6} {y + 13} L{x + w - 18} {y + 13}" stroke="#777" stroke-width="2"/>{barre}')


def scatolone(w, h, scritta, extra=""):
    return svg(w, h, f'''<rect x="3" y="3" width="{w - 6}" height="{h - 6}" rx="4" fill="{CARTONE}" stroke="{CARTONE_SCURO}" stroke-width="5"/>
<path d="M3 {h * 0.18:.0f} L{w - 3} {h * 0.18:.0f}" stroke="{CARTONE_SCURO}" stroke-width="3" opacity="0.6"/>
<rect x="{w / 2 - 14:.0f}" y="3" width="28" height="{h * 0.45:.0f}" fill="{NASTRO}" opacity="0.85"/>
<path d="M8 {h - 10} L{w - 8} {h - 10}" stroke="{CARTONE_LUCE}" stroke-width="4" opacity="0.7"/>
<text x="{w * 0.28:.0f}" y="{h * 0.72:.0f}" text-anchor="middle" font-family="Trebuchet MS, sans-serif" font-size="{min(w, h) * 0.17:.0f}" font-weight="700" fill="{CARTONE_SCURO}" opacity="0.8">{scritta}</text>
{extra}''')


frecce = lambda x, y: (f'<path d="M{x} {y + 18} L{x} {y} M{x - 6} {y + 6} L{x} {y} L{x + 6} {y + 6} M{x + 14} {y + 18} L{x + 14} {y} '
                       f'M{x + 8} {y + 6} L{x + 14} {y} L{x + 20} {y + 6} M{x - 4} {y + 22} L{x + 18} {y + 22}" fill="none" '
                       f'stroke="{CARTONE_SCURO}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')


def scaffale():
    # scaffale blu con quattro ripiani pieni di coni di filato; la base è in basso
    w, h = 320, 540
    rng = random.Random(4)
    pezzi = [f'<rect x="10" y="4" width="14" height="{h - 4}" fill="{BLU}" stroke="{BLU_SCURO}" stroke-width="3"/>',
             f'<rect x="{w - 24}" y="4" width="14" height="{h - 4}" fill="{BLU}" stroke="{BLU_SCURO}" stroke-width="3"/>']
    for k in range(0, h - 20, 26):
        pezzi.append(f'<circle cx="17" cy="{k + 14}" r="2.5" fill="{BLU_SCURO}"/><circle cx="{w - 17}" cy="{k + 14}" r="2.5" fill="{BLU_SCURO}"/>')
    for ripiano in (128, 256, 384, 512):
        # coni in piedi sul ripiano: cono di carta e filato avvolto
        x = 32
        while x < w - 50:
            c = rng.choice(CONI)
            alto = rng.randint(70, 92)
            pezzi.append(f'<path d="M{x} {ripiano} L{x + 8} {ripiano - alto} L{x + 30} {ripiano - alto} L{x + 38} {ripiano} Z" '
                         f'fill="{c}" stroke="#4A4A50" stroke-width="2.5" stroke-linejoin="round"/>'
                         f'<path d="M{x + 6} {ripiano - alto * 0.35:.0f} L{x + 32} {ripiano - alto * 0.35:.0f} M{x + 7} {ripiano - alto * 0.65:.0f} L{x + 31} {ripiano - alto * 0.65:.0f}" '
                         f'stroke="#000" stroke-opacity="0.12" stroke-width="3"/>'
                         f'<rect x="{x + 14}" y="{ripiano - alto - 8}" width="10" height="9" fill="#E8D9B8" stroke="#4A4A50" stroke-width="2"/>')
            x += rng.randint(40, 46)
        pezzi.append(f'<rect x="10" y="{ripiano}" width="{w - 20}" height="12" fill="{GRIGIO}" stroke="{GRIGIO_SCURO}" stroke-width="3"/>')
    return svg(w, h, "\n".join(pezzi))


PEZZI = {
    "scatolone_a": (200, 150, "Scatolone di filati: si impilano in colonne sui bancali",
                    scatolone(200, 150, "LANA", etichetta(120, 84))),
    "scatolone_b": (180, 160, "Scatolone con le frecce «questo lato in alto»",
                    scatolone(180, 160, "FILATI", frecce(130, 96))),
    "scatolone_c": (220, 130, "Scatolone chiaro, un po' ammaccato",
                    svg(220, 130, f'''<path d="M3 6 L217 3 L216 127 L5 127 Z" fill="#E9DFCF" stroke="{CARTONE_SCURO}" stroke-width="5" stroke-linejoin="round"/>
<rect x="96" y="4" width="28" height="56" fill="{NASTRO}" opacity="0.9"/>
<path d="M150 20 Q160 40 150 60" fill="none" stroke="{CARTONE_SCURO}" stroke-width="2.5" opacity="0.5"/>
<text x="56" y="92" text-anchor="middle" font-family="Trebuchet MS, sans-serif" font-size="22" font-weight="700" fill="#9C8A70">COTONE</text>
{etichetta(150, 80)}''')),
    "scatola_rompibile": (110, 90, "Scatola aperta da beccare: si rompe e sparge chicchi",
                          svg(110, 90, f'''<path d="M6 30 L104 30 L100 86 L10 86 Z" fill="{CARTONE}" stroke="{CARTONE_SCURO}" stroke-width="5" stroke-linejoin="round"/>
<path d="M6 30 L0 10 L40 18 L44 30 M104 30 L110 12 L72 16 L68 30" fill="{CARTONE_LUCE}" stroke="{CARTONE_SCURO}" stroke-width="4" stroke-linejoin="round"/>
<ellipse cx="40" cy="32" rx="9" ry="6" fill="#FFC21A" stroke="#8A5A00" stroke-width="2.5"/><ellipse cx="60" cy="30" rx="9" ry="6" fill="#FFC21A" stroke="#8A5A00" stroke-width="2.5"/>
<path d="M30 54 L80 54" stroke="{CARTONE_SCURO}" stroke-width="3" opacity="0.5"/>''')),
    "bancale": (240, 40, "Bancale di legno sotto le colonne di scatoloni",
                svg(240, 40, f'''<rect x="2" y="2" width="236" height="10" fill="{LEGNO}" stroke="{LEGNO_SCURO}" stroke-width="3"/>
<rect x="6" y="12" width="34" height="18" fill="{LEGNO}" stroke="{LEGNO_SCURO}" stroke-width="3"/><rect x="103" y="12" width="34" height="18" fill="{LEGNO}" stroke="{LEGNO_SCURO}" stroke-width="3"/><rect x="200" y="12" width="34" height="18" fill="{LEGNO}" stroke="{LEGNO_SCURO}" stroke-width="3"/>
<rect x="2" y="28" width="236" height="10" fill="{LEGNO}" stroke="{LEGNO_SCURO}" stroke-width="3"/>''')),
    # coni di filato nemici (Tappa 18): disegnati chiari, nel gioco prendono il colore del filato
    "cono_in_piedi": (60, 100, "Cono di filato in piedi sullo scaffale: traballa prima di cadere",
                      svg(60, 100, '''<path d="M6 96 L16 14 L44 14 L54 96 Z" fill="#FFFFFF" stroke="#4A4A50" stroke-width="4" stroke-linejoin="round"/>
<path d="M10 70 L50 70 M12 50 L48 50 M14 32 L46 32" stroke="#000" stroke-opacity="0.12" stroke-width="5"/>
<rect x="22" y="2" width="16" height="14" fill="#E8D9B8" stroke="#4A4A50" stroke-width="3"/>''')),
    "cono_rotola": (64, 64, "Cono di filato che rotola: si salta",
                    svg(64, 64, '''<circle cx="32" cy="32" r="28" fill="#FFFFFF" stroke="#4A4A50" stroke-width="4"/>
<path d="M32 10 A22 22 0 0 1 54 32 M32 16 A16 16 0 0 1 48 32 M10 32 A22 22 0 0 0 32 54 M16 32 A16 16 0 0 0 32 48" fill="none" stroke="#000" stroke-opacity="0.15" stroke-width="4" stroke-linecap="round"/>
<circle cx="32" cy="32" r="9" fill="#E8D9B8" stroke="#4A4A50" stroke-width="3"/><circle cx="32" cy="32" r="3.5" fill="#4A4A50"/>
<path d="M50 14 Q58 6 62 10" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>''')),
    "cartoni_piatti": (260, 230, "Pila di cartoni piatti col foglio bianco sopra: una piattaforma",
                       svg(260, 230, f'''<rect x="6" y="196" width="248" height="30" fill="{LEGNO}" stroke="{LEGNO_SCURO}" stroke-width="3"/>
<rect x="8" y="22" width="244" height="176" fill="{CARTONE}" stroke="{CARTONE_SCURO}" stroke-width="5"/>
{"".join(f'<path d="M10 {y} L250 {y}" stroke="{CARTONE_SCURO}" stroke-width="1.6" opacity="0.55"/>' for y in range(32, 196, 7))}
<path d="M4 8 L256 8 L252 40 L8 40 Z" fill="#F7F7F2" stroke="#9A9A9A" stroke-width="3" stroke-linejoin="round"/>
<path d="M90 26 L90 198 M170 26 L170 198" stroke="#7A8A6A" stroke-width="3" opacity="0.6"/>''')),
    "scaffale": (320, 540, "Scaffale blu con i coni di filato: i ripiani sono piattaforme", scaffale()),
    "transpallet": (230, 150, "Transpallet arancione: ci si può salire sopra",
                    svg(230, 150, f'''<path d="M30 120 L220 120 L220 136 L30 136 Z" fill="#9AA0A6" stroke="#4A4F55" stroke-width="4"/>
<circle cx="200" cy="140" r="8" fill="#333"/><circle cx="60" cy="140" r="9" fill="#333"/>
<path d="M20 70 L56 70 L66 126 L24 126 Z" fill="#E8572A" stroke="#8A2A10" stroke-width="5" stroke-linejoin="round"/>
<path d="M38 72 L8 6" stroke="#2A2A2A" stroke-width="9" stroke-linecap="round"/>
<path d="M2 6 L22 2 L26 14 L6 18 Z" fill="#2A2A2A"/>
<text x="140" y="132" text-anchor="middle" font-family="Trebuchet MS, sans-serif" font-size="11" font-weight="700" fill="#4A4F55">PORTATA 2000</text>''')),
    "portone": (300, 330, "Portone sezionale: è l'uscita del livello",
                svg(300, 330, f'''<rect x="4" y="4" width="292" height="326" fill="#9DA3A8" stroke="#5E646A" stroke-width="5"/>
<rect x="20" y="20" width="260" height="310" fill="#E3E5E7"/>
{"".join(f'<path d="M20 {y} L280 {y}" stroke="#B9BDC1" stroke-width="4"/>' for y in range(58, 330, 38))}
<path d="M20 20 L280 20 M90 20 L90 330 M160 20 L160 330 M230 20 L230 330" stroke="#3A3A40" stroke-width="2" opacity="0.25"/>
<rect x="40" y="250" width="56" height="22" rx="4" fill="#BFE0F5" stroke="#6E757D" stroke-width="3"/><rect x="122" y="250" width="56" height="22" rx="4" fill="#BFE0F5" stroke="#6E757D" stroke-width="3"/><rect x="204" y="250" width="56" height="22" rx="4" fill="#BFE0F5" stroke="#6E757D" stroke-width="3"/>
<rect x="240" y="150" width="22" height="34" rx="3" fill="#F2C14E" stroke="#8A6A10" stroke-width="3"/>''')),
    "estintore": (50, 110, "Estintore (decorazione)",
                  svg(50, 110, '''<rect x="10" y="22" width="30" height="84" rx="12" fill="#D63A2A" stroke="#7A1A10" stroke-width="4"/>
<rect x="14" y="50" width="22" height="26" fill="#F5F5F0"/><path d="M20 22 L20 10 L34 10 L34 22 M34 12 Q46 14 44 40" fill="none" stroke="#2A2A2A" stroke-width="4" stroke-linecap="round"/>''')),
    "uscita": (110, 56, "Cartello verde dell'uscita di emergenza (decorazione)",
               svg(110, 56, '''<rect x="3" y="3" width="104" height="50" rx="4" fill="#2E9B4F" stroke="#1A5E2E" stroke-width="4"/>
<circle cx="40" cy="15" r="5" fill="#FFF"/><path d="M38 21 L32 34 L22 38 M34 30 L44 36 L48 46 M36 26 L46 22 L52 28" fill="none" stroke="#FFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M62 28 L92 28 M82 18 L92 28 L82 38" fill="none" stroke="#FFF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>''')),
}

def mattoni_piastrella():
    # piastrella di mattoni che si ripete sulla parete (512×128: una potenza di due, per poterla ripetere sul web)
    rng = random.Random(11)
    pezzi = ['<rect width="512" height="128" fill="#D9D4CC"/>']
    for r in range(8):
        rosata = (r // 2) % 2 == 0
        sfasa = 0 if r % 2 == 0 else -32
        for k in range(9):
            mescolato = rosata if rng.random() > 0.18 else not rosata
            c = rng.choice(["#B9806E", "#C69486", "#B07766"]) if mescolato else rng.choice(["#8F939A", "#9A9EA5", "#868A91"])
            pezzi.append(f'<rect x="{sfasa + k * 64 + 2}" y="{r * 16 + 2}" width="60" height="12" fill="{c}"/>')
    return svg(512, 128, "\n".join(pezzi))


# il magazzino sulla mappa, visto dall'alto un po' di sbieco (stessa misura degli altri luoghi)
MAPPA_MAGAZZINO = svg(240, 200, '''<ellipse cx="120" cy="188" rx="104" ry="11" fill="#000000" fill-opacity="0.12"/>
<rect x="20" y="78" width="200" height="108" fill="#B9806E" stroke="#5A3E2E" stroke-width="5"/>
<path d="M20 100 L220 100 M20 122 L220 122 M20 144 L220 144 M20 166 L220 166" stroke="#8C8F96" stroke-width="7"/>
<path d="M14 82 L120 30 L226 82 Z" fill="#C9CCCF" stroke="#6E757D" stroke-width="5" stroke-linejoin="round"/>
<path d="M40 72 L120 34 M70 76 L120 52 M200 72 L120 34 M170 76 L120 52" stroke="#A8ADB3" stroke-width="3"/>
<rect x="92" y="54" width="56" height="16" fill="#EAF4FA" stroke="#6E757D" stroke-width="3"/>
<rect x="88" y="120" width="64" height="66" fill="#E3E5E7" stroke="#5E646A" stroke-width="4"/>
<path d="M88 136 L152 136 M88 152 L152 152 M88 168 L152 168" stroke="#B9BDC1" stroke-width="3"/>
<circle cx="50" cy="104" r="11" fill="#EAF4FA" stroke="#6E757D" stroke-width="4"/><circle cx="190" cy="104" r="11" fill="#EAF4FA" stroke="#6E757D" stroke-width="4"/>
<path d="M30 180 Q60 172 70 186 M168 184 Q190 170 214 182" fill="none" stroke="#2C4F8C" stroke-width="5" stroke-linecap="round"/>''')


# ---------------- scena d'esempio (in pixel del gioco: metà dei disegni) ----------------

def interno(testo):
    import re
    return re.sub(r"^<svg[^>]*>\n?|</svg>\s*$", "", testo.strip())


def metti(nome_o_svg, x, y, w, h):
    testo = PEZZI[nome_o_svg][3] if nome_o_svg in PEZZI else nome_o_svg
    pw, ph = PEZZI[nome_o_svg][0], PEZZI[nome_o_svg][1]
    return f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="0 0 {pw} {ph}" preserveAspectRatio="none">{interno(testo)}</svg>'


def mattoni(w, h):
    # parete di mattoni a due colori, come nelle foto: file alternate grigie e rosate, con qualche mattone mescolato
    rng = random.Random(9)
    pezzi = [f'<rect width="{w}" height="{h}" fill="#D9D4CC"/>']
    alto, lungo = 16, 44
    for r in range(0, h // alto + 1):
        rosata = (r // 2) % 2 == 0
        sfasa = 0 if r % 2 == 0 else -lungo / 2
        x = sfasa
        while x < w:
            if rng.random() < 0.15:
                rosata_qui = not rosata
            else:
                rosata_qui = rosata
            c = rng.choice(["#B9806E", "#C69486", "#B07766"]) if rosata_qui else rng.choice(["#8F939A", "#9A9EA5", "#868A91"])
            pezzi.append(f'<rect x="{x + 1:.0f}" y="{r * alto + 1}" width="{lungo - 2}" height="{alto - 2}" fill="{c}"/>')
            x += lungo
    return "".join(pezzi)


def oblo(cx, cy):
    return (f'<circle cx="{cx}" cy="{cy}" r="24" fill="#8C9096" stroke="#5E646A" stroke-width="3"/>'
            f'<circle cx="{cx}" cy="{cy}" r="17" fill="#EAF4FA" stroke="#6E757D" stroke-width="3"/>'
            f'<path d="M{cx - 8} {cy - 6} Q{cx} {cy - 13} {cx + 7} {cy - 9}" fill="none" stroke="#FFF" stroke-width="3" stroke-linecap="round"/>')


def soffitto(w):
    pezzi = [f'<rect width="{w}" height="70" fill="#C9CCCF"/>']
    for x in range(0, w, 12):
        pezzi.append(f'<rect x="{x}" y="0" width="6" height="70" fill="#B5BABF"/>')
    for x in (180, 640, 1060):
        pezzi.append(f'<rect x="{x}" y="10" width="150" height="46" fill="#EEF6FB" stroke="#9DA3A8" stroke-width="3"/>')
    pezzi.append(f'<rect y="66" width="{w}" height="12" fill="#A8ADB3" stroke="#7E848A" stroke-width="2"/>')
    for x in range(100, w, 260):
        pezzi.append(f'<rect x="{x}" y="78" width="80" height="6" rx="3" fill="#F5F8FA" stroke="#9DA3A8" stroke-width="1.5"/>')
    return "".join(pezzi)


def soppalco(x, y, w, h_terra):
    pezzi = []
    for px in (x + 20, x + w - 34):
        pezzi.append(f'<rect x="{px}" y="{y + 16}" width="14" height="{h_terra - y - 16}" fill="{AZZURRO}" stroke="{AZZURRO_SCURO}" stroke-width="2"/>')
    pezzi.append(f'<rect x="{x}" y="{y}" width="{w}" height="16" fill="{AZZURRO}" stroke="{AZZURRO_SCURO}" stroke-width="2.5"/>')
    pezzi.append(f'<rect x="{x}" y="{y - 5}" width="{w}" height="5" fill="{GRIGIO}" stroke="{GRIGIO_SCURO}" stroke-width="1.5"/>')
    pezzi.append(f'<path d="M{x + 3} {y - 5} L{x + 3} {y - 52} M{x + w - 3} {y - 5} L{x + w - 3} {y - 52} M{x} {y - 50} L{x + w} {y - 50} M{x} {y - 28} L{x + w} {y - 28}" stroke="{AZZURRO}" stroke-width="5" stroke-linecap="round"/>')
    for px in range(x + 40, x + w - 20, 40):
        pezzi.append(f'<path d="M{px} {y - 5} L{px} {y - 50}" stroke="{AZZURRO}" stroke-width="4"/>')
    return "".join(pezzi)


def colonna(x, terra, tipi):
    # colonna di scatoloni su un bancale; tipi: lista di (nome, larghezza, altezza) dal basso
    pezzi = [metti("bancale", x - 2, terra - 20, 124, 20)]
    y = terra - 20
    for nome, w, h in tipi:
        y -= h
        pezzi.append(metti(nome, x + (120 - w) / 2, y, w, h))
    return "".join(pezzi), y


def scena():
    W, H, TERRA = 1270, 520, 470
    s = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg">', mattoni(W, TERRA)]
    s += [oblo(330, 150), oblo(980, 150), soffitto(W)]
    s.append(f'<rect y="{TERRA}" width="{W}" height="{H - TERRA}" fill="#D8DCD8"/><path d="M0 {TERRA} L{W} {TERRA}" stroke="#A9AEAA" stroke-width="4"/>')
    s.append(f'<path d="M0 {TERRA + 24} L{W} {TERRA + 24}" stroke="#C7CCC8" stroke-width="2"/>')
    s.append(metti("scaffale", 40, TERRA - 270, 160, 270))
    s.append(metti("estintore", 215, TERRA - 55, 25, 55))
    s.append(metti("uscita", 250, 210, 55, 28))
    c1, _ = colonna(300, TERRA, [("scatolone_a", 100, 75), ("scatolone_b", 90, 80), ("scatolone_c", 110, 65), ("scatolone_a", 100, 75)])
    s.append(c1)
    s.append(soppalco(600, 220, 420, TERRA))
    s.append(metti("scaffale", 640, 220 - 5 - 135, 80, 135))
    s.append(metti("cartoni_piatti", 470, TERRA - 115, 130, 115))
    s.append(metti("transpallet", 760, TERRA - 75, 115, 75))
    s.append(metti("scatola_rompibile", 900, TERRA - 45, 55, 45))
    s.append(metti("portone", 1110, TERRA - 165, 150, 165))
    # operatori e pulcino (gli operatori sono a metà misura come nel gioco)
    pezzi_op = {"corpo": op.CORPO, "gamba": op.GAMBA}
    for nome, o in op.OPERATORI.items():
        pezzi_op["testa_" + nome] = op.testa(nome, o)
        pezzi_op["braccio_" + nome] = op.braccio(o)
    s.append(f'<g transform="translate(250 {TERRA}) scale(0.5)">{op.operatore(pezzi_op, "moro", -38, 38, 4)}</g>')
    s.append(f'<g transform="translate(700 {TERRA}) scale(0.5)">{op.operatore(pezzi_op, "indiano", -38, 38, 4)}</g>')
    s.append(f'<g transform="translate(560 {TERRA - 115}) scale(0.5)">{op.pulcino((0, 0))}</g>')
    s.append("</svg>")
    return "".join(s)


def anteprima():
    schede = []
    for nome, (w, h, spiega, testo) in PEZZI.items():
        schede.append(f'<div class="scheda"><div class="disegno">{testo.replace("<svg ", "<svg style=\'max-height:170px\' ", 1)}</div><p>{spiega}</p></div>')
    schede.append(f'<div class="scheda"><div class="disegno">{MAPPA_MAGAZZINO.replace("<svg ", "<svg style=\'max-height:170px\' ", 1)}</div><p>Il magazzino sulla mappa</p></div>')
    pagina = f'''<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pezzi del magazzino</title>
<style>
:root {{ --testo:#3a2a10; --sfondo:#fbf6ea; --carta:#ffffff; --bordo:#e2d6bd; }}
@media (prefers-color-scheme: dark) {{ :root {{ --testo:#f4ead6; --sfondo:#22201b; --carta:#2e2b24; --bordo:#4a4436; }} }}
body {{ margin:0; padding:16px; font-family: system-ui, sans-serif; background:var(--sfondo); color:var(--testo); }}
h1 {{ font-size:22px; font-weight:600; margin:0 0 4px; }}
h2 {{ font-size:17px; font-weight:600; margin:20px 0 8px; }}
p.nota {{ margin:0 0 12px; opacity:.85; }}
.griglia {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(190px,1fr)); gap:12px; }}
.scheda {{ background:var(--carta); border:1px solid var(--bordo); border-radius:12px; padding:12px; text-align:center; }}
.disegno {{ height:180px; display:flex; align-items:flex-end; justify-content:center; }}
.disegno svg {{ max-width:100%; height:auto; }}
.scheda p {{ margin:8px 0 0; font-size:14px; }}
.scena-box {{ overflow-x:auto; border-radius:12px; border:1px solid var(--bordo); }}
</style></head><body>
<h1>Il magazzino filati: i pezzi nuovi</h1>
<p class="nota">Scena d'esempio al chiuso, come nelle foto (sul telefono si scorre di lato): pareti di mattoni a due colori con gli oblò, soffitto di lamiera con i lucernari, pavimento grigio chiaro, scaffali blu con i coni di filato, colonne di scatoloni sui bancali, il soppalco azzurro con la ringhiera, il transpallet e il portone d'uscita. Pareti, soffitto, pavimento e soppalco nel gioco si disegnano da codice con questo aspetto.</p>
<div class="scena-box">{scena()}</div>
<h2>I pezzi uno per uno</h2>
<div class="griglia">{"".join(schede)}</div>
</body></html>
'''
    with open(os.path.join(QUI, "anteprima_magazzino.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(pagina)


if __name__ == "__main__":
    os.makedirs(CARTELLA, exist_ok=True)
    for nome, (w, h, spiega, testo) in PEZZI.items():
        with open(os.path.join(CARTELLA, nome + ".svg"), "w", encoding="utf-8", newline="\n") as f:
            f.write(testo)
    with open(os.path.join(MAPPA, "magazzino.svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(MAPPA_MAGAZZINO)
    with open(os.path.join(CARTELLA, "mattoni.svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(mattoni_piastrella())
    anteprima()
    print(len(PEZZI) + 1, "disegni del magazzino scritti, anteprima pronta")
