# Disegni SVG degli accessori del pulcino (Tappa 23) e pagina di anteprima con gli accessori indossati
# dai tre stadi di crescita e la bancarella dove si comprano con i chicchi.
# Uso: python strumenti/disegni_accessori.py   (dalla cartella del progetto), poi python strumenti/stile_finale.py
# Ogni accessorio ha un perno (punto del disegno) e un punto sul pulcino dove si aggancia (misure al doppio,
# origine tra i piedi, stadio 1): nel gioco il punto si sposta con l'alzata e la grandezza di ogni stadio.
import os
import sys

QUI = os.path.dirname(__file__)
sys.path.insert(0, QUI)
import disegni_crescita as crescita  # noqa: E402

CARTELLA = os.path.join(QUI, "..", "assets", "grafica", "accessori")
C = "#5A3E14"


def svg(w, h, corpo):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{corpo}\n</svg>\n'


# nome: (larghezza, altezza, perno, punto sul pulcino, angolo, prezzo, nome per la bancarella, disegno)
ACCESSORI = {
    "fiocco": (54, 38, (27, 19), (-16, -96), -15, 40, "Fiocco rosa", f'''
<path d="M27 19 L4 4 Q0 19 4 34 Z M27 19 L50 4 Q54 19 50 34 Z" fill="#F48FB1" stroke="#A84D72" stroke-width="4" stroke-linejoin="round"/>
<circle cx="27" cy="19" r="8" fill="#F06292" stroke="#A84D72" stroke-width="4"/>
<path d="M10 12 L18 16 M44 12 L36 16" stroke="#FFFFFF" stroke-opacity="0.6" stroke-width="3" stroke-linecap="round"/>'''),
    "occhiali": (60, 34, (20, 17), (18, -70), 0, 60, "Occhiali tondi", f'''
<circle cx="20" cy="17" r="14" fill="#CFEAF7" fill-opacity="0.45" stroke="#2F2F38" stroke-width="5"/>
<path d="M34 15 L58 13" stroke="#2F2F38" stroke-width="5" stroke-linecap="round"/>
<path d="M6 17 L0 16" stroke="#2F2F38" stroke-width="5" stroke-linecap="round"/>
<path d="M13 10 Q17 7 22 9" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>'''),
    "sciarpa": (104, 70, (52, 18), (0, -34), 0, 80, "Sciarpa a righe", f'''
<path d="M6 12 Q52 30 98 12 L100 28 Q52 46 4 28 Z" fill="#E8573F" stroke="#8A2A18" stroke-width="4" stroke-linejoin="round"/>
<path d="M28 22 L26 36 M52 26 L52 40 M76 22 L78 36" stroke="#FFF2D6" stroke-width="7"/>
<path d="M14 26 L4 66 L24 66 L28 30 Z" fill="#E8573F" stroke="#8A2A18" stroke-width="4" stroke-linejoin="round"/>
<path d="M8 50 L24 50" stroke="#FFF2D6" stroke-width="7"/>
<path d="M6 66 L4 70 M12 66 L12 70 M18 66 L20 70" stroke="#8A2A18" stroke-width="3" stroke-linecap="round"/>'''),
    "berretto": (92, 52, (42, 46), (4, -90), -6, 100, "Berretto rosso", f'''
<path d="M8 46 Q8 6 46 4 Q80 6 80 46 Z" fill="#D9412E" stroke="#7A1E12" stroke-width="5" stroke-linejoin="round"/>
<path d="M72 40 Q88 38 90 46 L60 48 Z" fill="#B8321F" stroke="#7A1E12" stroke-width="4" stroke-linejoin="round"/>
<circle cx="46" cy="6" r="6" fill="#FFF2D6" stroke="#7A1E12" stroke-width="3"/>
<path d="M22 24 Q30 14 42 12" fill="none" stroke="#F07A66" stroke-width="5" stroke-linecap="round"/>'''),
    "cappello": (120, 60, (60, 50), (2, -88), -8, 120, "Cappello di paglia", f'''
<ellipse cx="60" cy="50" rx="57" ry="9" fill="#E8C66B" stroke="#8A6A1E" stroke-width="4"/>
<path d="M30 50 Q28 14 60 10 Q92 14 90 50 Z" fill="#F0D27A" stroke="#8A6A1E" stroke-width="4" stroke-linejoin="round"/>
<path d="M30 40 Q60 48 90 40 L90 48 Q60 56 30 48 Z" fill="#D9412E" stroke="#7A1E12" stroke-width="3"/>
<path d="M40 22 L80 22 M36 32 L84 32" stroke="#C9A445" stroke-width="2.5"/>
<path d="M14 50 L106 50" stroke="#C9A445" stroke-width="2"/>'''),
}

# la bancarella: tettoia a strisce, banco di legno, cassette di chicchi
BANCARELLA = svg(240, 200, f'''<ellipse cx="120" cy="190" rx="100" ry="10" fill="#000000" fill-opacity="0.12"/>
<rect x="30" y="56" width="12" height="130" fill="#B07A3E" stroke="{C}" stroke-width="4"/>
<rect x="198" y="56" width="12" height="130" fill="#B07A3E" stroke="{C}" stroke-width="4"/>
<path d="M14 30 L226 30 L216 70 L24 70 Z" fill="#FFFFFF" stroke="#8A2A18" stroke-width="4" stroke-linejoin="round"/>
<path d="M44 30 L50 70 L66 70 L62 30 Z M98 30 L100 70 L116 70 L116 30 Z M150 30 L150 70 L166 70 L168 30 Z M202 30 L200 70 L216 70 L218 30 Z" fill="#E8573F"/>
<path d="M24 70 Q36 82 48 70 Q60 82 72 70 Q84 82 96 70 Q108 82 120 70 Q132 82 144 70 Q156 82 168 70 Q180 82 192 70 Q204 82 216 70" fill="#E8573F" stroke="#8A2A18" stroke-width="3"/>
<rect x="22" y="120" width="196" height="66" rx="6" fill="#C98F4E" stroke="{C}" stroke-width="5"/>
<path d="M30 140 L210 140 M30 162 L210 162" stroke="#A8743A" stroke-width="3"/>
<rect x="44" y="96" width="56" height="28" fill="#D9B07A" stroke="{C}" stroke-width="4"/>
<g fill="#FFC21A" stroke="#8A5A00" stroke-width="2"><ellipse cx="56" cy="96" rx="6" ry="8"/><ellipse cx="70" cy="93" rx="6" ry="8"/><ellipse cx="84" cy="96" rx="6" ry="8"/><ellipse cx="63" cy="88" rx="6" ry="8"/><ellipse cx="77" cy="88" rx="6" ry="8"/></g>
<path d="M140 120 Q140 92 160 92 Q182 92 182 120 Z" fill="#F0D27A" stroke="#8A6A1E" stroke-width="4"/>
<ellipse cx="161" cy="120" rx="30" ry="5" fill="#E8C66B" stroke="#8A6A1E" stroke-width="3"/>''')


def interno(testo):
    import re
    return re.sub(r"^<svg[^>]*>\n?|</svg>\s*$", "", testo.strip())


def con_accessori(stadio, nomi):
    # come monta() di disegni_crescita, più gli accessori agganciati e spostati come nel gioco
    su = 0 if stadio == 1 else 8
    k = crescita.SCALA if stadio == 3 else 1.0
    pezzi = [crescita.monta(stadio)]
    for nome in nomi:
        w, h, perno, punto, angolo, *_ , testo = ACCESSORI[nome]
        x, y = punto[0] * k, (punto[1] - su) * k
        pezzi.append(f'<g transform="translate({x:.1f} {y:.1f}) rotate({angolo})"><g transform="translate({-perno[0]} {-perno[1]})">{interno(svg(w, h, testo))}</g></g>')
    return "".join(pezzi)


def anteprima():
    righe = []
    for stadio in (1, 2, 3):
        celle = []
        for nomi in (["cappello"], ["berretto"], ["fiocco"], ["sciarpa"], ["occhiali"], ["cappello", "sciarpa", "occhiali"]):
            celle.append(f'<div class="cella"><svg viewBox="-80 -190 200 200" width="130" height="130">{con_accessori(stadio, nomi)}</svg></div>')
        righe.append(f'<h2>Stadio {stadio}</h2><div class="fila">{"".join(celle)}</div>')
    articoli = "".join(
        f'<div class="articolo"><svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="max-width:90px;max-height:60px">{interno(svg(w, h, testo))}</svg>'
        f'<div class="nome">{nome_b}</div><div class="prezzo"><span class="chicco"></span>{prezzo}</div>'
        f'<div class="pulsante">{"Indossa" if i == 2 else "Compra"}</div></div>'
        for i, (nome, (w, h, _p, _q, _a, prezzo, nome_b, testo)) in enumerate(ACCESSORI.items()))
    pagina = f'''<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Gli accessori</title>
<style>
:root {{ --testo:#3a2a10; --sfondo:#fbf6ea; --carta:#ffffff; --bordo:#e2d6bd; }}
@media (prefers-color-scheme: dark) {{ :root {{ --testo:#f4ead6; --sfondo:#22201b; --carta:#2e2b24; --bordo:#4a4436; }} }}
body {{ margin:0; padding:16px; font-family: system-ui, sans-serif; background:var(--sfondo); color:var(--testo); }}
h1 {{ font-size:22px; font-weight:600; margin:0 0 4px; }} h2 {{ font-size:17px; font-weight:600; margin:16px 0 6px; }}
p.nota {{ margin:0 0 12px; opacity:.85; }}
.fila {{ display:flex; flex-wrap:wrap; gap:8px; }}
.cella {{ background:#cfe9fb; border-radius:10px; }}
.banco {{ display:flex; flex-wrap:wrap; gap:16px; align-items:flex-start; }}
.negozio {{ background:#B9874C; border:5px solid #5A3E14; border-radius:16px; padding:14px; color:#FFF5DC; font-family:"Trebuchet MS",sans-serif; max-width:640px; }}
.negozio .testa {{ display:flex; justify-content:space-between; align-items:center; font-size:22px; font-weight:700; margin-bottom:10px; }}
.borsellino {{ background:#7A5428; border-radius:10px; padding:4px 12px; }}
.griglia {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(110px,1fr)); gap:10px; }}
.articolo {{ background:#D9B07A; border:3px solid #5A3E14; border-radius:12px; padding:8px; text-align:center; color:#3A2616; }}
.articolo .nome {{ font-size:13px; font-weight:700; margin-top:4px; }}
.prezzo {{ font-size:15px; font-weight:700; }}
.chicco {{ display:inline-block; width:9px; height:12px; background:#FFC21A; border:2px solid #8A5A00; border-radius:50%; margin-right:4px; vertical-align:-1px; }}
.pulsante {{ margin-top:6px; background:#5A8F3A; color:white; border-radius:8px; padding:3px 0; font-size:13px; font-weight:700; }}
</style></head><body>
<h1>Tappa 23: gli accessori del pulcino</h1>
<p class="nota">Bozzetti. Ogni accessorio si aggancia al pulcino e cresce con lui (stadio 1, 2 e 3). Se ne può indossare uno per tipo: un cappello in testa (cappello, berretto o fiocco), la sciarpa al collo, gli occhiali. L'ultima colonna li mostra insieme.</p>
{"".join(righe)}
<h2>La bancarella</h2>
<div class="banco">
<div><svg viewBox="0 0 240 200" width="240" height="200">{interno(BANCARELLA)}</svg><p class="nota" style="max-width:240px">Sulla mappa: un pulsante «Bancarella» accanto a «Crediti» (e questo disegno nel pannello).</p></div>
<div class="negozio"><div class="testa"><span>La bancarella</span><span class="borsellino"><span class="chicco"></span>137</span></div>
<div class="griglia">{articoli}</div>
<p style="margin:10px 0 0;font-size:14px">I chicchi del borsellino: tutti quelli raccolti nelle partite finite. Un accessorio comprato resta tuo: «Indossa» / «Togli».</p></div>
</div>
</body></html>
'''
    with open(os.path.join(QUI, "anteprima_accessori.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(pagina)


if __name__ == "__main__":
    os.makedirs(CARTELLA, exist_ok=True)
    for nome, (w, h, *_ , testo) in ACCESSORI.items():
        with open(os.path.join(CARTELLA, nome + ".svg"), "w", encoding="utf-8", newline="\n") as f:
            f.write(svg(w, h, testo))
    with open(os.path.join(QUI, "..", "assets", "grafica", "mappa", "bancarella.svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(BANCARELLA)
    anteprima()
    print(len(ACCESSORI), "accessori e la bancarella scritti, anteprima pronta")
