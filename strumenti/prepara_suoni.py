# Suoni veri per il gioco (Tappa 28): per ogni suono del gioco prepara tre candidati (A, B, C) a partire da
# raccolte libere CC0, e una pagina per ascoltarli accanto al vecchio suono sintetico e sceglierli.
# Con le scelte fatte, scrive i suoni scelti in assets/suoni/ (al posto dei sintetici).
#
# Uso:
#   python -P strumenti/prepara_suoni.py <cartella sorgenti> <cartella ascolto>            -> candidati + pagina
#   python -P strumenti/prepara_suoni.py <cartella sorgenti> --scelte "salto=A chicco=B ..."  -> nel gioco
#
# Sorgenti (tutte CC0, cioè libere anche per la vendita e senza obbligo di citazione), da opengameart.org:
#   baby-animals.zip (Technopeasant) -> pigolii di pulcino ("Peeps")
#   kenney_interfaceSounds.zip, RPGsounds_Kenney.zip, jingleSounds_Kenney.zip (Kenney, www.kenney.nl)
#   mouse-2.wav (AntumDeluge), bicycle-horn-1.wav, bung_01/bing_01/bing_02.mp3 e blah/booleh/uah.mp3 (EzduzziteH),
#   swishes.zip (Summoning Wars)
# La cartella sorgenti è quella con gli zip estratti in "estratti/" (vedi la Tappa 28 in CLAUDE.md).
# Serve la libreria "soundfile" (pip install soundfile).
import glob
import json
import os
import sys

import numpy as np
import soundfile as sf
from scipy.signal import resample

QUI = os.path.dirname(os.path.abspath(__file__))
SUONI_GIOCO = os.path.join(QUI, "..", "assets", "suoni")
FREQ = 22050  # come i suoni del gioco: bastano per effetti corti e pesano poco

# cosa fa ogni suono nel gioco (per la pagina di ascolto)
DESCRIZIONI = {
    "salto": "il pulcino salta (\"pio!\")",
    "doppio": "doppio salto: battito d'ali e verso",
    "colpito": "il pulcino viene preso (pio-pio spaventato)",
    "curioso": "il pulcino vede un indizio della pulcina (\"pio?\")",
    "atterra": "il pulcino atterra",
    "chicco": "prende un chicco",
    "becco": "colpo di becco",
    "botta": "beccata su un ostacolo che non si rompe ancora",
    "rotto": "un ostacolo va in pezzi",
    "traballa": "un cono di filato traballa sullo scaffale",
    "rotola": "un cono di filato rotola",
    "squittio": "il topo",
    "starnazzo": "l'oca arrabbiata",
    "bu": "la talpa spunta (\"bu!\")",
    "scava": "la talpa scava",
    "boing": "rimbalzo su girasole e mais",
    "plana": "il pulcino apre le ali e plana",
    "nido": "raggiunge un nido (punto sicuro)",
    "stella": "una stellina a fine livello",
    "uovo": "trova l'uovo d'oro",
    "fine": "fine livello",
    "piuma": "la piuma della pulcina",
}


class Sorgenti:
    def __init__(self, cartella):
        self.cartella = cartella

    def file(self, nome):
        trovati = [p for p in glob.glob(os.path.join(self.cartella, "**", nome + ".*"), recursive=True)
                   if not os.path.basename(p).startswith("._")]
        if not trovati:
            raise SystemExit("Non trovo il suono sorgente: " + nome)
        dati, freq = sf.read(trovati[0], dtype="float32", always_2d=True)
        mono = dati.mean(axis=1)
        if freq != FREQ:
            mono = resample(mono, int(len(mono) * FREQ / freq)).astype("float32")
        return mono

    def pio(self, quale):
        """Uno dei tre pigolii del file Peeps (1, 2 o 3), con un filo di coda."""
        tutto = self.file("Peeps")
        tagli = {1: (0.05, 0.19), 2: (0.27, 0.41), 3: (0.50, 0.64)}[quale]
        return tutto[int(tagli[0] * FREQ):int(tagli[1] * FREQ)]


def tono(suono, semitoni):
    """Più acuto (semitoni > 0) o più grave, cambiando anche la durata, come un nastro accelerato."""
    fattore = 2 ** (semitoni / 12.0)
    return resample(suono, max(8, int(len(suono) / fattore))).astype("float32")


def dopo(*pezzi, pausa=0.0):
    silenzio = np.zeros(int(pausa * FREQ), dtype="float32")
    uscita = []
    for i, p in enumerate(pezzi):
        if i:
            uscita.append(silenzio)
        uscita.append(p)
    return np.concatenate(uscita)


def insieme(a, b, ritardo=0.0, volume_b=1.0):
    inizio = int(ritardo * FREQ)
    lunghezza = max(len(a), inizio + len(b))
    uscita = np.zeros(lunghezza, dtype="float32")
    uscita[:len(a)] += a
    uscita[inizio:inizio + len(b)] += b * volume_b
    return uscita


def taglia(suono, da=0.0, a=None):
    return suono[int(da * FREQ):(None if a is None else int(a * FREQ))]


def pulisci(suono, picco=0.8):
    """Toglie il silenzio intorno, sfuma i bordi e porta tutti allo stesso picco."""
    forte = np.where(np.abs(suono) > np.abs(suono).max() * 0.02)[0]
    if len(forte):
        suono = suono[max(0, forte[0] - int(0.005 * FREQ)):forte[-1] + int(0.03 * FREQ)]
    n = min(len(suono) // 4, int(0.01 * FREQ))
    if n > 1:
        suono = suono.copy()
        suono[:n] *= np.linspace(0, 1, n)
        suono[-n:] *= np.linspace(1, 0, n)
    massimo = float(np.abs(suono).max()) or 1.0
    return (suono / massimo * picco).astype("float32")


def candidati(s):
    """Per ogni suono del gioco: tre ricette (A, B, C)."""
    return {
        "salto": [s.pio(1), s.pio(3), tono(s.pio(1), 3)],
        "doppio": [insieme(s.file("swish-1"), s.pio(2), 0.04), insieme(taglia(s.file("cloth4"), 0, 0.2), tono(s.pio(1), 2), 0.05),
                   insieme(s.file("swish-9"), tono(s.pio(3), 3), 0.06)],
        "colpito": [tono(dopo(s.pio(1), s.pio(2), s.pio(3), pausa=0.03), 2), dopo(tono(s.pio(1), 4), tono(s.pio(3), 1), pausa=0.04),
                    s.file("Peeps")],
        "curioso": [dopo(s.pio(2), tono(s.pio(2), 5), pausa=0.08), dopo(s.pio(1), tono(s.pio(1), 7), pausa=0.1),
                    insieme(s.pio(3), s.file("question_002"), 0.1, 0.6)],
        "atterra": [s.file("footstep03"), s.file("footstep07"), taglia(s.file("cloth4"), 0, 0.18)],
        "chicco": [s.file("pluck_001"), s.file("pluck_002"), s.file("drop_002")],
        "becco": [s.file("click_001"), s.file("select_001"), taglia(s.file("bookPlace3"), 0, 0.12)],
        "botta": [s.file("bookPlace2"), s.file("chop"), taglia(s.file("doorClose_4"), 0, 0.3)],
        "rotto": [s.file("chop"), insieme(s.file("creak3"), s.file("chop"), 0.08), taglia(s.file("doorClose_2"), 0, 0.4)],
        "traballa": [taglia(s.file("creak1"), 0, 0.45), s.file("metalLatch"), s.file("creak3")],
        "rotola": [taglia(s.file("scroll_001"), 0, 0.6), taglia(s.file("knifeSlice2"), 0, 0.5), taglia(s.file("handleCoins"), 0, 0.5)],
        "squittio": [s.file("mouse-2"), taglia(s.file("mouse-2"), 0, 0.45), tono(taglia(s.file("mouse-2"), 0, 0.5), 3)],
        "starnazzo": [s.file("bicycle-horn-1"), tono(s.file("bicycle-horn-1"), -3),
                      dopo(tono(taglia(s.file("bicycle-horn-1"), 0, 0.25), 1), tono(taglia(s.file("bicycle-horn-1"), 0, 0.3), -1), pausa=0.05)],
        "bu": [s.file("uah"), s.file("blah"), s.file("booleh")],
        "scava": [dopo(s.file("footstep01"), s.file("footstep05"), pausa=0.02), s.file("cloth2"), s.file("scratch_004")],
        "boing": [s.file("bung_01"), s.file("bing_01"), s.file("bing_02")],
        "plana": [s.file("swish-9"), taglia(s.file("cloth1"), 0, 0.45), taglia(s.file("clothBelt"), 0, 0.45)],
        "nido": [s.file("maximize_004"), s.file("confirmation_002"), s.file("glass_004")],
        "stella": [s.file("glass_004"), s.file("confirmation_004"), s.file("bong_001")],
        "uovo": [s.file("jingles_STEEL09"), s.file("jingles_PIZZA04"), s.file("jingles_SAX10")],
        "fine": [s.file("jingles_STEEL01"), s.file("jingles_PIZZA07"), s.file("jingles_SAX07")],
        "piuma": [insieme(s.file("glass_004"), s.file("swish-2"), 0.0, 0.5), s.file("glass_001"), s.file("maximize_006")],
    }


def scrivi(suono, percorso):
    sf.write(percorso, pulisci(suono), FREQ, subtype="PCM_16")


PAGINA = """<!DOCTYPE html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Suoni del pulcino</title>
<style>
:root { --sfondo:#fff8e8; --testo:#3a2616; --legno:#b07a3e; --bordo:#7a4e12; --scelto:#2f9e8f; --riga:#f1e3c4; }
@media (prefers-color-scheme: dark) { :root { --sfondo:#2a2118; --testo:#f6ead3; --legno:#8a5c2a; --bordo:#d9b47a; --scelto:#3fb3a3; --riga:#3a2e22; } }
body { margin:0; padding:16px; background:var(--sfondo); color:var(--testo); font-family:"Trebuchet MS", system-ui, sans-serif; }
h1 { font-size:24px; margin:0 0 6px; } p { margin:0 0 14px; line-height:1.4; max-width:760px; }
.suono { display:flex; flex-wrap:wrap; align-items:center; gap:8px; padding:10px; border-radius:12px; margin-bottom:8px; background:var(--riga); }
.nome { width:100%; font-weight:bold; } .nome span { font-weight:normal; opacity:.8; }
button { font:inherit; font-size:16px; padding:8px 14px; border-radius:10px; border:2px solid var(--bordo); background:var(--legno); color:#fff8e8; cursor:pointer; min-width:64px; }
button.vecchio { background:transparent; color:var(--testo); }
button.scelto { background:var(--scelto); border-color:var(--scelto); }
#riepilogo { position:sticky; bottom:0; background:var(--sfondo); padding:10px 0; border-top:2px solid var(--bordo); margin-top:12px; }
textarea { width:100%; box-sizing:border-box; font:inherit; font-size:14px; height:70px; border-radius:10px; padding:8px; background:var(--riga); color:var(--testo); border:2px solid var(--bordo); }
</style></head><body>
<h1>Suoni del pulcino: ascolta e scegli</h1>
<p>Per ogni suono: <b>Vecchio</b> è quello di adesso; <b>A</b>, <b>B</b> e <b>C</b> sono i candidati veri. Tocca per ascoltare,
tocca <b>Scegli</b> sotto la lettera che preferisci (o il Vecchio, per tenerlo). In fondo si compila da solo il riepilogo: copialo e incollalo nella chat.</p>
<div id="elenco"></div>
<div id="riepilogo"><b>Le tue scelte</b> (copiale nella chat):<textarea id="scelte" readonly></textarea>
<button id="copia">Copia le scelte</button></div>
<script>
const SUONI = __SUONI__;
const scelte = {};
try { Object.assign(scelte, JSON.parse(localStorage.getItem('scelte_suoni') || '{}')); } catch (e) {}
const elenco = document.getElementById('elenco');
let lettore = new Audio();
function suona(file) { lettore.pause(); lettore = new Audio(file); lettore.play(); }
function aggiorna() {
  document.getElementById('scelte').value = Object.keys(SUONI).map(n => n + '=' + (scelte[n] || '?')).join(' ');
  try { localStorage.setItem('scelte_suoni', JSON.stringify(scelte)); } catch (e) {}
  document.querySelectorAll('button.scegli').forEach(b => b.classList.toggle('scelto', scelte[b.dataset.nome] === b.dataset.lettera));
}
for (const [nome, descrizione] of Object.entries(SUONI)) {
  const riga = document.createElement('div'); riga.className = 'suono';
  riga.innerHTML = '<div class="nome">' + nome + ' <span>— ' + descrizione + '</span></div>';
  for (const lettera of ['Vecchio', 'A', 'B', 'C']) {
    const gruppo = document.createElement('div');
    const ascolta = document.createElement('button');
    ascolta.textContent = '▶ ' + lettera; if (lettera === 'Vecchio') ascolta.className = 'vecchio';
    ascolta.onclick = () => suona(nome + '_' + lettera + '.wav');
    const scegli = document.createElement('button');
    scegli.textContent = 'Scegli'; scegli.className = 'scegli'; scegli.dataset.nome = nome; scegli.dataset.lettera = lettera;
    scegli.onclick = () => { scelte[nome] = lettera; aggiorna(); };
    gruppo.append(ascolta, document.createElement('br'), scegli);
    riga.append(gruppo);
  }
  elenco.append(riga);
}
document.getElementById('copia').onclick = () => { const t = document.getElementById('scelte'); t.select(); try { navigator.clipboard.writeText(t.value); } catch (e) { document.execCommand('copy'); } };
aggiorna();
</script></body></html>
"""


def prepara_ascolto(sorgenti, cartella):
    os.makedirs(cartella, exist_ok=True)
    for nome, ricette in candidati(sorgenti).items():
        vecchio = os.path.join(SUONI_GIOCO, nome + ".wav")
        if os.path.exists(vecchio):
            dati, freq = sf.read(vecchio, dtype="float32", always_2d=True)
            sf.write(os.path.join(cartella, nome + "_Vecchio.wav"), dati, freq, subtype="PCM_16")
        for lettera, suono in zip("ABC", ricette):
            scrivi(suono, os.path.join(cartella, "%s_%s.wav" % (nome, lettera)))
    with open(os.path.join(cartella, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(PAGINA.replace("__SUONI__", json.dumps(DESCRIZIONI, ensure_ascii=False)))
    print("Candidati e pagina di ascolto in", cartella)


def metti_nel_gioco(sorgenti, testo):
    scelte = dict(coppia.split("=") for coppia in testo.split())
    tutti = candidati(sorgenti)
    for nome, lettera in scelte.items():
        if lettera in ("Vecchio", "?") or nome not in tutti:
            continue
        scrivi(tutti[nome]["ABC".index(lettera)], os.path.join(SUONI_GIOCO, nome + ".wav"))
        print("nel gioco:", nome, "=", lettera)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    sorgenti = Sorgenti(sys.argv[1])
    if sys.argv[2] == "--scelte":
        metti_nel_gioco(sorgenti, sys.argv[3])
    else:
        prepara_ascolto(sorgenti, sys.argv[2])
