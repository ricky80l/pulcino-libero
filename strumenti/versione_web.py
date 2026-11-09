# Dà al pacchetto del gioco (docs/index.pck) un nome con l'"impronta" del suo contenuto, per esempio
# docs/index-3fa9c21b.pck, e aggiorna docs/index.html perché carichi quello.
# Così il telefono scarica subito la versione nuova appena è pubblicata (il nome è nuovo, non può usare
# quella vecchia in memoria), ma se il gioco non è cambiato riusa quella che ha già e parte veloce.
# Il motore (index.wasm, index.js) cambia solo con una nuova versione di Godot e resta com'è.
# Uso: python strumenti/versione_web.py   (dalla cartella del progetto, subito dopo ogni esportazione in docs/)
import glob
import hashlib
import json
import os
import re
import time

from PIL import Image

QUI = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(QUI, "..", "docs")
PAGINA = os.path.join(DOCS, "index.html")
PACCHETTO = os.path.join(DOCS, "index.pck")

if not os.path.exists(PACCHETTO):
    raise SystemExit("Manca docs/index.pck: prima esporta il gioco.")

impronta = hashlib.sha1(open(PACCHETTO, "rb").read()).hexdigest()[:10]
nome = "index-%s.pck" % impronta

# via i pacchetti delle versioni precedenti, poi il pacchetto appena esportato prende il nome nuovo
for vecchio in glob.glob(os.path.join(DOCS, "index-*.pck")):
    os.remove(vecchio)
os.replace(PACCHETTO, os.path.join(DOCS, nome))

# la pagina: nella configurazione del motore, il pacchetto da caricare e la sua grandezza (per la barra)
testo = open(PAGINA, encoding="utf-8").read()
trovato = re.search(r"const GODOT_CONFIG = (\{.*?\});", testo)
if not trovato:
    raise SystemExit("Non trovo GODOT_CONFIG in docs/index.html")
config = json.loads(trovato.group(1))
grandezze = {k: v for k, v in config.get("fileSizes", {}).items() if not k.endswith(".pck")}
grandezze[nome] = os.path.getsize(os.path.join(DOCS, nome))
config["fileSizes"] = grandezze
config["mainPack"] = nome
testo = testo.replace(trovato.group(0), "const GODOT_CONFIG = %s;" % json.dumps(config, separators=(",", ":")))
# a volte Windows (o l'antivirus) tiene occupato il file per un attimo: si riprova
for prova in range(10):
    try:
        open(PAGINA, "w", encoding="utf-8", newline="\n").write(testo)
        break
    except OSError:
        if prova == 9:
            raise
        time.sleep(0.5)
print("Pacchetto del gioco:", nome)

# Il gioco come app (scelta di Riccardo): la "carta d'identità" per Chrome, le icone e un aiutante.
# Installato sulla schermata Home parte a schermo intero e in orizzontale, senza l'avviso del browser.
VERDE = "#2f9e8f"  # lo sfondo dell'icona
with open(os.path.join(DOCS, "manifest.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump({
        "name": "Il Pulcino Libero",
        "short_name": "Pulcino Libero",
        "start_url": "./index.html",
        "scope": "./",
        "display": "fullscreen",
        "orientation": "landscape",
        "background_color": VERDE,
        "theme_color": VERDE,
        "icons": [
            {"src": "icona-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "icona-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": "icona-maschera-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    }, f, ensure_ascii=False, indent=1)
# l'aiutante non tiene niente in memoria: ogni richiesta va in rete come sempre (l'impronta continua a funzionare)
with open(os.path.join(DOCS, "aiutante.js"), "w", encoding="utf-8", newline="\n") as f:
    f.write("// Aiutante del gioco come app: serve a Chrome per poterlo installare sulla schermata Home.\n"
            "// Non tiene niente in memoria: ogni richiesta va in rete come sempre.\n"
            "self.addEventListener('install', function () { self.skipWaiting(); });\n"
            "self.addEventListener('activate', function (e) { e.waitUntil(self.clients.claim()); });\n"
            "self.addEventListener('fetch', function (e) { e.respondWith(fetch(e.request)); });\n")
# icone: quella del gioco, e una con un po' di margine per le icone tonde di Android ("maskable")
icona = Image.open(os.path.join(QUI, "..", "icona.png")).convert("RGBA")
icona.resize((512, 512), Image.LANCZOS).save(os.path.join(DOCS, "icona-512.png"))
icona.resize((192, 192), Image.LANCZOS).save(os.path.join(DOCS, "icona-192.png"))
maschera = Image.new("RGBA", (512, 512), VERDE)
piccola = icona.resize((400, 400), Image.LANCZOS)
maschera.alpha_composite(piccola, (56, 56))
maschera.save(os.path.join(DOCS, "icona-maschera-512.png"))
print("App: manifest.json, aiutante.js e icone scritti")
