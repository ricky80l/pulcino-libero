# Disegni SVG dei pezzi nuovi dell'orto (livello 3) e pagina di anteprima.
# Uso: python strumenti/disegni_orto.py   (dalla cartella del progetto)
# Scrive assets/grafica/orto/*.svg e strumenti/anteprima_orto.html
# Tutti i disegni sono al doppio della grandezza nel gioco; la base è in basso al centro.
import os

QUI = os.path.dirname(__file__)
CARTELLA = os.path.join(QUI, "..", "assets", "grafica", "orto")
C = "#5A3E14"      # contorno legno
V = "#3E7A22"      # contorno verde
VERDE = "#6DBE45"
VERDE_SCURO = "#4E9A2E"


def svg(w, h, corpo):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{corpo}\n</svg>\n'


PEZZI = {
    "girasole": (160, 400, "Girasole: ci atterri sopra, si piega e ti fa rimbalzare", f'''
<path d="M80 400 Q74 260 80 120" fill="none" stroke="{V}" stroke-width="16" stroke-linecap="round"/>
<path d="M80 400 Q74 260 80 120" fill="none" stroke="{VERDE}" stroke-width="9" stroke-linecap="round"/>
<path d="M78 300 Q40 270 14 290 Q40 312 78 300 Z" fill="{VERDE}" stroke="{V}" stroke-width="4" stroke-linejoin="round"/>
<path d="M80 230 Q120 196 148 214 Q122 240 80 230 Z" fill="{VERDE}" stroke="{V}" stroke-width="4" stroke-linejoin="round"/>
<g fill="#FFD84A" stroke="#C99A05" stroke-width="3.5">
<ellipse cx="80" cy="34" rx="14" ry="26"/><ellipse cx="80" cy="126" rx="14" ry="26"/><ellipse cx="34" cy="80" rx="26" ry="14"/><ellipse cx="126" cy="80" rx="26" ry="14"/>
<ellipse cx="47" cy="47" rx="13" ry="24" transform="rotate(-45 47 47)"/><ellipse cx="113" cy="47" rx="13" ry="24" transform="rotate(45 113 47)"/>
<ellipse cx="47" cy="113" rx="13" ry="24" transform="rotate(45 47 113)"/><ellipse cx="113" cy="113" rx="13" ry="24" transform="rotate(-45 113 113)"/>
</g>
<circle cx="80" cy="80" r="32" fill="#7A4E12" stroke="{C}" stroke-width="4"/>
<g fill="#5A3608"><circle cx="70" cy="70" r="4"/><circle cx="88" cy="68" r="4"/><circle cx="80" cy="84" r="4"/><circle cx="66" cy="90" r="4"/><circle cx="94" cy="88" r="4"/><circle cx="80" cy="100" r="3.5"/><circle cx="80" cy="60" r="3.5"/></g>'''),

    "mais": (160, 380, "Canna del mais: altra pianta che rimbalza", f'''
<path d="M80 380 L80 70" stroke="{V}" stroke-width="16" stroke-linecap="round"/>
<path d="M80 380 L80 70" stroke="#8CCB55" stroke-width="9" stroke-linecap="round"/>
<path d="M80 320 Q30 300 10 330 Q40 334 80 330 Z M80 250 Q130 226 152 252 Q120 258 80 262 Z M80 180 Q36 156 18 178 Q46 186 80 192 Z" fill="{VERDE}" stroke="{V}" stroke-width="4" stroke-linejoin="round"/>
<g transform="rotate(-18 100 150)"><ellipse cx="100" cy="150" rx="15" ry="36" fill="#FFC21A" stroke="#8A5A00" stroke-width="4"/>
<path d="M92 128 L108 128 M90 142 L110 142 M90 156 L110 156 M92 170 L108 170" stroke="#E0A010" stroke-width="2.5"/>
<path d="M88 176 Q86 130 100 112 Q92 150 104 186 Z" fill="#8CCB55" stroke="{V}" stroke-width="3"/></g>
<path d="M80 72 Q66 30 56 6 M80 72 Q80 26 80 2 M80 72 Q94 30 106 8 M80 72 Q72 40 66 20 M80 72 Q90 42 96 22" fill="none" stroke="#C99A05" stroke-width="5" stroke-linecap="round"/>'''),

    "zucca": (140, 112, "Zucca: si rompe con due beccate", f'''
<path d="M70 18 Q66 6 74 0" fill="none" stroke="{V}" stroke-width="7" stroke-linecap="round"/>
<g stroke="#9A4A10" stroke-width="4.5">
<ellipse cx="40" cy="66" rx="32" ry="40" fill="#F28C28"/><ellipse cx="100" cy="66" rx="32" ry="40" fill="#F28C28"/>
<ellipse cx="70" cy="64" rx="34" ry="44" fill="#FF9F3A"/></g>
<path d="M58 30 Q54 64 60 100 M82 30 Q86 64 80 100" fill="none" stroke="#D9761E" stroke-width="3"/>
<path d="M76 18 Q96 10 104 22 Q92 30 76 22 Z" fill="{VERDE}" stroke="{V}" stroke-width="3"/>'''),

    "cavolo": (120, 92, "Cavolo: ostacolo basso", f'''
<ellipse cx="60" cy="56" rx="56" ry="34" fill="#8CCB55" stroke="{V}" stroke-width="4.5"/>
<path d="M20 60 Q30 28 60 26 Q90 28 100 60" fill="none" stroke="{V}" stroke-width="3.5"/>
<ellipse cx="60" cy="42" rx="26" ry="20" fill="#B8E08A" stroke="{V}" stroke-width="4"/>
<path d="M60 26 L60 58 M48 32 Q52 46 50 58 M72 32 Q68 46 70 58" stroke="{VERDE_SCURO}" stroke-width="2.5" fill="none"/>'''),

    "carriola": (230, 136, "Carriola: una piattaforma", f'''
<path d="M10 20 L180 20 L160 82 L30 82 Z" fill="#4F7DB8" stroke="#24476E" stroke-width="5" stroke-linejoin="round"/>
<path d="M8 14 L184 14" stroke="#24476E" stroke-width="10" stroke-linecap="round"/>
<path d="M8 14 L184 14" stroke="#7FA3D4" stroke-width="5" stroke-linecap="round"/>
<path d="M170 60 L226 40 M60 82 L50 126 M140 82 L150 112" stroke="{C}" stroke-width="8" stroke-linecap="round"/>
<path d="M170 60 L226 40" stroke="#B07A3E" stroke-width="4" stroke-linecap="round"/>
<circle cx="150" cy="112" r="20" fill="#3A3A3A" stroke="#1E1E1E" stroke-width="4"/><circle cx="150" cy="112" r="6" fill="#9A9A9A"/>
<path d="M30 20 Q60 4 100 12 Q140 2 176 20 Z" fill="#7A5230" stroke="{C}" stroke-width="3"/>'''),

    "pomodori": (130, 270, "Pali dei pomodori (sfondo)", f'''
<path d="M40 268 L40 10 M90 268 L90 20" stroke="{C}" stroke-width="10" stroke-linecap="round"/>
<path d="M40 268 L40 10 M90 268 L90 20" stroke="#B07A3E" stroke-width="5" stroke-linecap="round"/>
<path d="M40 60 Q70 90 90 70 M40 130 Q70 160 90 140 M40 200 Q70 230 90 210" fill="none" stroke="{VERDE_SCURO}" stroke-width="6" stroke-linecap="round"/>
<g fill="{VERDE}" stroke="{V}" stroke-width="3"><ellipse cx="26" cy="90" rx="18" ry="9"/><ellipse cx="104" cy="110" rx="18" ry="9"/><ellipse cx="22" cy="170" rx="18" ry="9"/><ellipse cx="106" cy="190" rx="18" ry="9"/><ellipse cx="66" cy="44" rx="16" ry="8"/></g>
<g fill="#E8432F" stroke="#8A1E12" stroke-width="3"><circle cx="58" cy="90" r="12"/><circle cx="74" cy="104" r="11"/><circle cx="54" cy="164" r="12"/><circle cx="76" cy="226" r="12"/></g>'''),

    "annaffiatoio": (130, 96, "Annaffiatoio (decorazione)", '''
<path d="M30 30 L94 30 L90 92 L34 92 Z" fill="#7D858F" stroke="#3E4E5C" stroke-width="4.5" stroke-linejoin="round"/>
<path d="M90 50 L124 20" stroke="#3E4E5C" stroke-width="10" stroke-linecap="round"/><path d="M90 50 L124 20" stroke="#A3AAB3" stroke-width="5" stroke-linecap="round"/>
<ellipse cx="124" cy="20" rx="7" ry="10" fill="#A3AAB3" stroke="#3E4E5C" stroke-width="3" transform="rotate(40 124 20)"/>
<path d="M36 36 Q62 2 88 36" fill="none" stroke="#3E4E5C" stroke-width="6"/><path d="M36 50 L88 50" stroke="#A3AAB3" stroke-width="4"/>'''),

    "fragole": (170, 76, "Fragole: cespugli bassi lungo i filari", f'''
<g fill="{VERDE}" stroke="{V}" stroke-width="3.5">
<path d="M20 70 Q4 40 26 30 Q40 40 34 70 Z"/><path d="M50 70 Q40 22 70 18 Q84 40 66 70 Z"/><path d="M96 70 Q86 26 114 22 Q130 44 112 70 Z"/><path d="M140 70 Q132 38 156 34 Q168 50 154 70 Z"/>
<path d="M76 70 Q74 44 92 38 Q102 54 92 70 Z"/></g>
<g fill="#E8432F" stroke="#8A1E12" stroke-width="3"><path d="M40 46 Q30 46 32 58 Q38 72 44 72 Q50 72 54 58 Q56 46 46 46 Z"/><path d="M118 52 Q108 52 110 62 Q116 76 122 76 Q128 76 132 62 Q134 52 124 52 Z"/><path d="M80 40 Q72 40 74 50 Q78 62 84 62 Q90 62 94 50 Q96 40 88 40 Z"/></g>
<g fill="#FFE58A"><circle cx="40" cy="56" r="1.6"/><circle cx="46" cy="62" r="1.6"/><circle cx="120" cy="62" r="1.6"/><circle cx="126" cy="68" r="1.6"/><circle cx="82" cy="48" r="1.6"/><circle cx="87" cy="54" r="1.6"/></g>
<g fill="{VERDE_SCURO}"><path d="M38 46 L43 40 L48 46 Z"/><path d="M116 52 L121 46 L126 52 Z"/><path d="M78 40 L84 34 L90 40 Z"/></g>
<g fill="#FFFFFF" stroke="#C9C2B0" stroke-width="1.5"><circle cx="62" cy="30" r="6"/><circle cx="148" cy="44" r="6"/></g>
<g fill="#FFD84A"><circle cx="62" cy="30" r="2.5"/><circle cx="148" cy="44" r="2.5"/></g>'''),

    "pozzo": (230, 300, "Pozzo: la base è un ostacolo, sul tettuccio si sale col doppio salto", f'''
<path d="M40 70 L190 70 L176 4 L54 4 Z" fill="#D2553A" stroke="#7A2A18" stroke-width="5" stroke-linejoin="round"/>
<path d="M70 4 Q74 36 66 70 M115 4 L115 70 M160 4 Q156 36 164 70" fill="none" stroke="#B3402A" stroke-width="4"/>
<rect x="30" y="66" width="170" height="14" rx="4" fill="#B07A3E" stroke="{C}" stroke-width="4"/>
<path d="M54 80 L54 200 M176 80 L176 200" stroke="{C}" stroke-width="14" stroke-linecap="round"/>
<path d="M54 80 L54 200 M176 80 L176 200" stroke="#B07A3E" stroke-width="7"/>
<path d="M54 120 L190 120" stroke="{C}" stroke-width="8" stroke-linecap="round"/>
<path d="M190 120 L206 120 L206 140" fill="none" stroke="#7D858F" stroke-width="5" stroke-linecap="round"/>
<path d="M115 120 L115 168" stroke="#C99A5C" stroke-width="3"/>
<path d="M100 168 L130 168 L126 196 L104 196 Z" fill="#B07A3E" stroke="{C}" stroke-width="4" stroke-linejoin="round"/>
<path d="M98 168 Q115 154 132 168" fill="none" stroke="#7D858F" stroke-width="3"/>
<path d="M20 200 L210 200 L204 298 L26 298 Z" fill="#A9A49A" stroke="#5E5446" stroke-width="5" stroke-linejoin="round"/>
<ellipse cx="115" cy="200" rx="96" ry="14" fill="#C2BCB0" stroke="#5E5446" stroke-width="5"/>
<ellipse cx="115" cy="200" rx="74" ry="8" fill="#2F3A44"/>
<path d="M30 236 L70 236 M90 236 L140 236 M160 236 L200 236 M24 268 L56 268 M76 268 L124 268 M146 268 L204 268 M50 236 L50 268 M115 236 L115 268 M180 236 L180 268 M66 268 L66 296 M136 268 L136 296" stroke="#8E877C" stroke-width="3.5"/>'''),

    "spaventapasseri": (210, 360, "Spaventapasseri (sfondo)", f'''
<path d="M105 358 L105 70" stroke="{C}" stroke-width="12" stroke-linecap="round"/><path d="M105 358 L105 70" stroke="#B07A3E" stroke-width="6"/>
<path d="M10 150 L200 150" stroke="{C}" stroke-width="12" stroke-linecap="round"/><path d="M10 150 L200 150" stroke="#B07A3E" stroke-width="6"/>
<path d="M60 130 L150 130 L160 250 L50 250 Z" fill="#4F7DB8" stroke="#24476E" stroke-width="5" stroke-linejoin="round"/>
<rect x="88" y="170" width="34" height="30" fill="#E8432F" stroke="#8A1E12" stroke-width="3"/>
<path d="M60 136 L20 160 L28 172 L62 156 Z M150 136 L190 160 L182 172 L148 156 Z" fill="#4F7DB8" stroke="#24476E" stroke-width="4" stroke-linejoin="round"/>
<path d="M18 160 L6 176 M24 168 L14 184 M192 160 L204 176 M186 168 L196 184 M70 250 L64 270 M90 250 L88 272 M120 250 L122 272 M140 250 L146 270" stroke="#D9B04A" stroke-width="4" stroke-linecap="round"/>
<circle cx="105" cy="96" r="34" fill="#E8C48A" stroke="{C}" stroke-width="5"/>
<path d="M90 90 L98 98 M98 90 L90 98 M112 90 L120 98 M120 90 L112 98" stroke="{C}" stroke-width="3.5" stroke-linecap="round"/>
<path d="M90 112 Q105 122 120 112" fill="none" stroke="{C}" stroke-width="3.5" stroke-linecap="round"/>
<path d="M56 72 L154 72 L140 60 L126 24 L84 24 L70 60 Z" fill="#B07A3E" stroke="{C}" stroke-width="5" stroke-linejoin="round"/>
<rect x="72" y="58" width="66" height="10" fill="#E8432F"/>'''),
}

os.makedirs(CARTELLA, exist_ok=True)
for nome, (w, h, _d, corpo) in PEZZI.items():
    with open(os.path.join(CARTELLA, nome + ".svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(svg(w, h, corpo))


# ---------- pagina di anteprima (tutto dentro la pagina, si apre anche dal telefono) ----------
def immagine(nome, scala=1.0, extra=""):
    w, h, _d, corpo = PEZZI[nome]
    return f'<svg viewBox="0 0 {w} {h}" width="{int(w * scala)}" height="{int(h * scala)}" {extra}>{corpo}</svg>'


def posa(nome, x, y, scala=0.5, piega=None):
    w, h, _d, _c = PEZZI[nome]
    stile = f"position:absolute;left:{x - w * scala / 2}px;top:{y - h * scala}px;transform-origin:50% 100%;"
    if piega:
        stile += f"transform:rotate({piega[0]}deg) scaleY({piega[1]});"
    return f'<div style="{stile}">{immagine(nome, scala)}</div>'


def pulcino(x, y):
    return (f'<div style="position:absolute;left:{x - 30}px;top:{y - 62}px"><svg viewBox="0 0 70 72" width="60" height="62">'
            '<path d="M24 50 L18 62 M44 50 L50 62" stroke="#E07A10" stroke-width="4" stroke-linecap="round"/>'
            '<path d="M8 30 L0 22 L4 34 L0 40 L10 40 Z" fill="#F5BE2E" stroke="#7A4E12" stroke-width="2.5"/>'
            '<circle cx="35" cy="34" r="22" fill="#FFD447" stroke="#7A4E12" stroke-width="3"/>'
            '<circle cx="44" cy="28" r="5" fill="#fff" stroke="#7A4E12" stroke-width="2"/><circle cx="46" cy="28" r="2.6" fill="#2A1A08"/>'
            '<path d="M56 30 L68 34 L56 38 Z" fill="#FF8C1A" stroke="#7A4E12" stroke-width="2"/>'
            '<path d="M34 13 q-6 -10 0 -12 q2 6 4 8 q2 -8 8 -7 q-4 5 -6 10" fill="#FFD447" stroke="#7A4E12" stroke-width="2"/></svg></div>')


scena = "".join([
    posa("spaventapasseri", 120, 300, 0.45),
    posa("pomodori", 260, 300, 0.5), posa("pomodori", 320, 300, 0.5),
    posa("fragole", 360, 300, 0.5),
    posa("cavolo", 420, 300, 0.5), posa("zucca", 500, 300, 0.5),
    posa("girasole", 600, 300, 0.5),
    posa("girasole", 700, 300, 0.5, piega=(-8, 0.9)),
    pulcino(706, 205),
    posa("mais", 800, 300, 0.5),
    posa("carriola", 900, 300, 0.5), posa("annaffiatoio", 990, 300, 0.5),
    posa("pozzo", 1100, 300, 0.5), posa("fragole", 1200, 300, 0.5),
])

schede = "\n".join(
    f'<div class="scheda"><div class="disegno">{immagine(n, 0.42 if PEZZI[n][1] > 200 else (0.6 if PEZZI[n][0] > 180 else 0.8))}</div><p>{PEZZI[n][2]}</p></div>'
    for n in PEZZI)

terra = ('<svg viewBox="0 0 400 60" width="100%" height="60" preserveAspectRatio="none">'
         '<rect width="400" height="60" fill="#7A5230"/>'
         '<path d="M0 8 Q20 0 40 8 T80 8 T120 8 T160 8 T200 8 T240 8 T280 8 T320 8 T360 8 T400 8 L400 0 L0 0 Z" fill="#8A5E36"/>'
         '<path d="M0 26 L400 26 M0 44 L400 44" stroke="#5E3E20" stroke-width="5"/>'
         '<g fill="#6DBE45"><circle cx="40" cy="10" r="5"/><circle cx="130" cy="8" r="5"/><circle cx="230" cy="10" r="5"/><circle cx="330" cy="8" r="5"/></g></svg>')

html = f'''<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pezzi dell'orto</title>
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
.scena {{ position:relative; width:1270px; height:340px; background:linear-gradient(#8cc8f2 0 88%, #7a5230 88%); }}
.terra {{ border-radius:12px; overflow:hidden; border:1px solid var(--bordo); }}
</style></head><body>
<h1>L'orto: i pezzi nuovi</h1>
<p class="nota">Scena d'esempio (sul telefono si scorre di lato). Il secondo girasole è piegato sotto il peso del pulcino: quando ci atterri si piega e ti rilancia in alto, poi torna dritto ondeggiando.</p>
<div class="scena-box"><div class="scena">{scena}</div></div>
<h2>Il terreno dell'orto</h2>
<p class="nota">Terra scura con i solchi e le piantine appena spuntate (disegnata dal gioco, si allunga quanto serve).</p>
<div class="terra">{terra}</div>
<h2>I pezzi uno per uno</h2>
<div class="griglia">{schede}</div>
<p class="nota" style="margin-top:16px">Riusiamo anche: chicchi, nidi, sacchi, cassette e il cancelletto come uscita. Le buche della talpa arrivano nella Tappa 15.</p>
</body></html>
'''
with open(os.path.join(QUI, "anteprima_orto.html"), "w", encoding="utf-8", newline="\n") as f:
    f.write(html)
print(len(PEZZI), "disegni e anteprima scritti")
