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
open(PAGINA, "w", encoding="utf-8", newline="\n").write(testo)
print("Pacchetto del gioco:", nome)
