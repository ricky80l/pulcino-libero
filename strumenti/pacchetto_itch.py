# Prepara il pacchetto da caricare su itch.io: pubblicazione/itch/pulcino-libero-web.zip
# È la stessa versione web di docs/ (index.html in cima, come chiede itch.io), senza i file che servono solo a GitHub.
# Uso: python strumenti/pacchetto_itch.py   (dalla cartella del progetto, dopo esportazione e versione_web.py)
import os
import zipfile

QUI = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(QUI, "..", "docs")
ZIP = os.path.join(QUI, "..", "pubblicazione", "itch", "pulcino-libero-web.zip")
SALTA = {".gdignore", ".nojekyll"}

if not os.path.exists(os.path.join(DOCS, "index.html")):
    raise SystemExit("Manca docs/index.html: prima esporta il gioco.")
os.makedirs(os.path.dirname(ZIP), exist_ok=True)
quanti = 0
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for nome in sorted(os.listdir(DOCS)):
        percorso = os.path.join(DOCS, nome)
        if nome in SALTA or not os.path.isfile(percorso) or nome.endswith(".TMP"):
            continue
        z.write(percorso, nome)
        quanti += 1
print("Pacchetto per itch.io: %d file, %.1f MB -> %s" % (quanti, os.path.getsize(ZIP) / 1048576, os.path.abspath(ZIP)))
