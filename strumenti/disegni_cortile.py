# Disegni SVG dei pezzi nuovi del cortile (livello 2) e pagina di anteprima.
# Uso: python strumenti/disegni_cortile.py   (dalla cartella del progetto)
# Scrive assets/grafica/cortile/*.svg e strumenti/anteprima_cortile.html
# Tutti i disegni sono al doppio della grandezza nel gioco.
import os

QUI = os.path.dirname(__file__)
CARTELLA = os.path.join(QUI, "..", "assets", "grafica", "cortile")
C = "#5A3E14"  # contorno legno


def svg(w, h, corpo):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{corpo}\n</svg>\n'


PEZZI = {
    # nome: (larghezza, altezza, descrizione, disegno)
    "botte": (120, 150, "Botte: ci si sale sopra", f'''
<rect x="10" y="8" width="100" height="136" rx="22" fill="#B07A3E" stroke="{C}" stroke-width="5"/>
<path d="M38 12 Q30 76 38 140 M60 10 L60 142 M82 12 Q90 76 82 140" fill="none" stroke="#8F5F2A" stroke-width="3"/>
<rect x="6" y="28" width="108" height="12" rx="5" fill="#7D858F" stroke="#3E4E5C" stroke-width="3"/>
<rect x="6" y="110" width="108" height="12" rx="5" fill="#7D858F" stroke="#3E4E5C" stroke-width="3"/>
<ellipse cx="60" cy="12" rx="46" ry="8" fill="#C99A5C" stroke="{C}" stroke-width="4"/>'''),

    "carretto": (360, 200, "Carretto: piattaforma con ruota", f'''
<rect x="10" y="40" width="300" height="56" rx="8" fill="#C98F4E" stroke="{C}" stroke-width="5"/>
<path d="M20 58 L300 58 M20 76 L300 76" stroke="#8F5F2A" stroke-width="3"/>
<rect x="6" y="30" width="308" height="16" rx="6" fill="#DDA562" stroke="{C}" stroke-width="4"/>
<path d="M310 70 L354 92" stroke="{C}" stroke-width="10" stroke-linecap="round"/>
<path d="M310 70 L354 92" stroke="#B07A3E" stroke-width="5" stroke-linecap="round"/>
<circle cx="110" cy="140" r="52" fill="none" stroke="{C}" stroke-width="12"/>
<circle cx="110" cy="140" r="52" fill="none" stroke="#B07A3E" stroke-width="6"/>
<path d="M110 92 L110 188 M62 140 L158 140 M76 106 L144 174 M144 106 L76 174" stroke="#8F5F2A" stroke-width="5"/>
<circle cx="110" cy="140" r="12" fill="#7D858F" stroke="#3E4E5C" stroke-width="4"/>
<rect x="250" y="96" width="14" height="96" rx="4" fill="#B07A3E" stroke="{C}" stroke-width="4"/>'''),

    "tettoia": (320, 64, "Tettoia: ci si salta sopra da sotto", f'''
<path d="M8 12 L312 12 L300 44 L20 44 Z" fill="#D2553A" stroke="#7A2A18" stroke-width="5" stroke-linejoin="round"/>
<path d="M60 12 Q66 28 58 44 M120 12 Q126 28 118 44 M180 12 Q186 28 178 44 M240 12 Q246 28 238 44" fill="none" stroke="#B3402A" stroke-width="4"/>
<rect x="18" y="44" width="284" height="14" rx="4" fill="#B07A3E" stroke="{C}" stroke-width="4"/>'''),

    "ceppi": (240, 160, "Catasta di ceppi: un gradino", f'''
<g stroke="{C}" stroke-width="4">
<rect x="10" y="96" width="220" height="56" rx="26" fill="#A8743C"/>
<rect x="30" y="44" width="180" height="56" rx="26" fill="#B07A3E"/>
<rect x="60" y="4" width="120" height="44" rx="20" fill="#A8743C"/>
</g>
<g fill="#E8C48A" stroke="{C}" stroke-width="4">
<circle cx="38" cy="124" r="24"/><circle cx="90" cy="124" r="24"/><circle cx="142" cy="124" r="24"/><circle cx="194" cy="124" r="24"/>
<circle cx="60" cy="72" r="24"/><circle cx="112" cy="72" r="24"/><circle cx="164" cy="72" r="24"/>
<circle cx="96" cy="26" r="19"/><circle cx="144" cy="26" r="19"/>
</g>
<g fill="none" stroke="#C99A5C" stroke-width="2.5"><circle cx="38" cy="124" r="12"/><circle cx="90" cy="124" r="12"/><circle cx="142" cy="124" r="12"/><circle cx="194" cy="124" r="12"/><circle cx="60" cy="72" r="12"/><circle cx="112" cy="72" r="12"/><circle cx="164" cy="72" r="12"/></g>'''),

    "abbeveratoio": (300, 110, "Abbeveratoio di pietra", '''
<path d="M10 20 L290 20 L276 104 L24 104 Z" fill="#A9A49A" stroke="#5E5446" stroke-width="5" stroke-linejoin="round"/>
<rect x="24" y="22" width="252" height="18" rx="6" fill="#5DB4E3" stroke="#2F7FAF" stroke-width="3"/>
<path d="M60 30 Q80 26 100 30 M170 30 Q190 26 210 30" stroke="#8FD0F2" stroke-width="3" fill="none" stroke-linecap="round"/>
<path d="M60 60 L80 64 M150 78 L180 72 M220 56 L236 60" stroke="#8E877C" stroke-width="4" stroke-linecap="round"/>
<rect x="4" y="12" width="292" height="14" rx="6" fill="#C2BCB0" stroke="#5E5446" stroke-width="4"/>'''),

    "vaso": (110, 124, "Vaso di coccio: si rompe a beccate", f'''
<path d="M20 30 L90 30 L80 118 L30 118 Z" fill="#D9824A" stroke="#7A3A16" stroke-width="5" stroke-linejoin="round"/>
<rect x="12" y="22" width="86" height="18" rx="6" fill="#E89A62" stroke="#7A3A16" stroke-width="4"/>
<path d="M30 70 L80 70" stroke="#B8622E" stroke-width="4"/>
<path d="M55 22 Q52 6 56 0" stroke="#3E7A22" stroke-width="4" fill="none"/>
<ellipse cx="44" cy="12" rx="12" ry="6" fill="#6DBE45" stroke="#3E7A22" stroke-width="2.5" transform="rotate(-25 44 12)"/>
<circle cx="62" cy="6" r="7" fill="#FF9EC0" stroke="#B3407A" stroke-width="2.5"/>'''),

    "steccato": (240, 120, "Steccato (sfondo o muretto)", f'''
<g fill="#E8DCC4" stroke="{C}" stroke-width="4">
<rect x="4" y="34" width="232" height="18" rx="4"/>
<rect x="4" y="80" width="232" height="18" rx="4"/>
<path d="M14 116 L14 20 L28 6 L42 20 L42 116 Z"/>
<path d="M106 116 L106 20 L120 6 L134 20 L134 116 Z"/>
<path d="M198 116 L198 20 L212 6 L226 20 L226 116 Z"/>
</g>'''),

    "cancello": (260, 200, "Cancelletto aperto: l'uscita", f'''
<rect x="8" y="10" width="26" height="188" rx="5" fill="#B07A3E" stroke="{C}" stroke-width="5"/>
<rect x="226" y="10" width="26" height="188" rx="5" fill="#B07A3E" stroke="{C}" stroke-width="5"/>
<g fill="#E8DCC4" stroke="{C}" stroke-width="4" transform="translate(34 0) skewY(14) scale(0.45 1)">
<rect x="0" y="40" width="220" height="16" rx="4"/><rect x="0" y="120" width="220" height="16" rx="4"/>
<rect x="10" y="30" width="22" height="130" rx="4"/><rect x="100" y="30" width="22" height="130" rx="4"/><rect x="190" y="30" width="22" height="130" rx="4"/>
</g>
<circle cx="21" cy="14" r="10" fill="#C99A5C" stroke="{C}" stroke-width="4"/><circle cx="239" cy="14" r="10" fill="#C99A5C" stroke="{C}" stroke-width="4"/>'''),

    "fienile": (560, 480, "Fienile sullo sfondo", f'''
<path d="M30 470 L30 190 L280 40 L530 190 L530 470 Z" fill="#C2553A" stroke="#6E2416" stroke-width="6" stroke-linejoin="round"/>
<path d="M14 196 L280 30 L546 196" fill="none" stroke="#E8DCC4" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M60 210 L60 460 M110 180 L110 460 M160 150 L160 460 M400 150 L400 460 M450 180 L450 460 M500 210 L500 460" stroke="#A84630" stroke-width="4"/>
<rect x="200" y="300" width="160" height="170" fill="#8A3020" stroke="#6E2416" stroke-width="5"/>
<path d="M200 300 L360 470 M360 300 L200 470" stroke="#E8DCC4" stroke-width="12"/>
<rect x="200" y="300" width="160" height="170" fill="none" stroke="#E8DCC4" stroke-width="12"/>
<rect x="236" y="150" width="88" height="80" fill="#5A2010" stroke="#E8DCC4" stroke-width="10"/>
<path d="M240 228 Q262 196 280 224 Q296 194 320 228 Z" fill="#EBC85A" stroke="#8A6420" stroke-width="3"/>'''),
}

os.makedirs(CARTELLA, exist_ok=True)
for nome, (w, h, _desc, corpo) in PEZZI.items():
    with open(os.path.join(CARTELLA, nome + ".svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(svg(w, h, corpo))

# ---------- pagina di anteprima (le immagini sono dentro la pagina, così si apre ovunque) ----------
def immagine(nome, scala=1.0):
    w, h, _d, corpo = PEZZI[nome]
    return f'<svg viewBox="0 0 {w} {h}" width="{int(w*scala)}" height="{int(h*scala)}">{corpo}</svg>'


def pulcino():
    return ('<svg viewBox="0 0 70 70" width="56" height="56">'
            '<circle cx="35" cy="38" r="24" fill="#FFD447" stroke="#7A4E12" stroke-width="3"/>'
            '<ellipse cx="38" cy="46" rx="14" ry="10" fill="#FFE58A"/>'
            '<circle cx="42" cy="32" r="5" fill="#fff" stroke="#7A4E12" stroke-width="2"/><circle cx="44" cy="32" r="2.6" fill="#2A1A08"/>'
            '<path d="M58 34 L68 38 L58 42 Z" fill="#FF8C1A" stroke="#7A4E12" stroke-width="2"/>'
            '<path d="M32 15 q-4 -9 2 -10 q0 5 3 7" fill="#FFD447" stroke="#7A4E12" stroke-width="2"/></svg>')


schede = "\n".join(
    f'<div class="scheda"><div class="disegno">{immagine(n, 0.6 if PEZZI[n][0] > 300 else 0.8)}</div><p>{PEZZI[n][2]}</p></div>'
    for n in PEZZI)

def posa(nome, x, y, scala=0.5):
    w, h, _d, _c = PEZZI[nome]
    return f'<div style="position:absolute;left:{x}px;top:{y - h*scala}px">{immagine(nome, scala)}</div>'

scena = "".join([
    posa("fienile", 520, 300, 0.5),
    posa("steccato", 40, 300, 0.5), posa("steccato", 160, 300, 0.5), posa("steccato", 280, 300, 0.5),
    posa("botte", 120, 300, 0.5),
    posa("carretto", 240, 300, 0.5),
    posa("tettoia", 300, 175, 0.5),
    posa("ceppi", 440, 300, 0.5),
    posa("vaso", 600, 300, 0.5),
    posa("abbeveratoio", 670, 300, 0.5),
    posa("cancello", 800, 300, 0.5),
    f'<div style="position:absolute;left:60px;top:250px">{pulcino()}</div>',
])

html = f'''<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pezzi del cortile</title>
<style>
:root {{ --testo:#3a2a10; --sfondo:#fbf6ea; --carta:#ffffff; --bordo:#e2d6bd; }}
@media (prefers-color-scheme: dark) {{ :root {{ --testo:#f4ead6; --sfondo:#22201b; --carta:#2e2b24; --bordo:#4a4436; }} }}
body {{ margin:0; padding:16px; font-family: system-ui, sans-serif; background:var(--sfondo); color:var(--testo); }}
h1 {{ font-size:22px; font-weight:600; margin:0 0 4px; }}
p.nota {{ margin:0 0 16px; opacity:.8; }}
.griglia {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(200px,1fr)); gap:12px; }}
.scheda {{ background:var(--carta); border:1px solid var(--bordo); border-radius:12px; padding:12px; text-align:center; }}
.disegno {{ height:150px; display:flex; align-items:center; justify-content:center; }}
.disegno svg {{ max-width:100%; height:auto; }}
.scheda p {{ margin:8px 0 0; font-size:14px; }}
.scena-box {{ overflow-x:auto; margin:8px 0 24px; border-radius:12px; border:1px solid var(--bordo); }}
.scena {{ position:relative; width:940px; height:340px; background:linear-gradient(#8cc8f2 0 88%, #c9a06a 88%); }}
.scena::after {{ content:""; position:absolute; left:0; right:0; top:300px; height:10px; background:#7cc24e; }}
</style></head><body>
<h1>Il cortile: i pezzi nuovi</h1>
<p class="nota">Scena d'esempio (scorri di lato sul telefono), poi i pezzi uno per uno. Riusiamo anche sacchi, balle, chicchi e nidi.</p>
<div class="scena-box"><div class="scena">{scena}</div></div>
<div class="griglia">{schede}</div>
</body></html>
'''
with open(os.path.join(QUI, "anteprima_cortile.html"), "w", encoding="utf-8", newline="\n") as f:
    f.write(html)
print(len(PEZZI), "disegni e anteprima scritti")
