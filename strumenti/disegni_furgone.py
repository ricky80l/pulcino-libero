# Disegni SVG del furgone del Maglificio Granada e del suo autista (a pezzi, al doppio della grandezza nel gioco).
# Il furgone è un furgone alto azzurro visto di lato, con il muso a destra e il portellone dietro aperto:
# simile a quello della foto di Riccardo, ma senza marchi né scritte vere.
# L'autista: moro, robusto con un filo di pancia (spalle larghe, viso pieno), polo blu e jeans. Origine tra i piedi, alto circa 340 come gli operatori.
# Uso: python strumenti/disegni_furgone.py   (dalla cartella del progetto), poi python strumenti/stile_finale.py
import os

QUI = os.path.dirname(__file__)
CARTELLA_FURGONE = os.path.join(QUI, "..", "assets", "grafica", "magazzino")
CARTELLA_AUTISTA = os.path.join(QUI, "..", "assets", "grafica", "autista")
PELLE = "#EBC09A"
LINEA = "#3A2616"
CAPELLI = "#3A2618"
POLO = "#35578A"
POLO_SCURO = "#1F3558"
JEANS = "#3E5F8E"


def svg(w, h, corpo):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{corpo}\n</svg>\n'


# furgone: 660×420, ruote appoggiate in basso (y 420)
AZZURRO = "#79A6DA"
AZZURRO_SCURO = "#4E7BB4"
BORDO = "#2E4E7A"
FURGONE = svg(660, 420, f'''<path d="M58 344 L58 92 Q58 62 88 62 L470 62 Q502 62 522 92 L590 196 Q606 222 606 258 L606 344 Z" fill="{AZZURRO}" stroke="{BORDO}" stroke-width="6" stroke-linejoin="round"/>
<path d="M58 290 L606 290 L606 344 L58 344 Z" fill="{AZZURRO_SCURO}"/>
<path d="M58 344 L58 92 Q58 62 88 62 L470 62 Q502 62 522 92 L590 196 Q606 222 606 258 L606 344 Z" fill="none" stroke="{BORDO}" stroke-width="6" stroke-linejoin="round"/>
<path d="M488 84 Q506 86 518 104 L572 196 L488 196 Z" fill="#CFE6F5" stroke="{BORDO}" stroke-width="5" stroke-linejoin="round"/>
<path d="M420 88 L470 88 L470 196 L420 196 Z" fill="#CFE6F5" stroke="{BORDO}" stroke-width="5"/>
<path d="M500 96 L520 120 M436 100 L454 100" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.8"/>
<path d="M412 70 L412 300 M480 200 L480 300 M250 70 L250 300 M246 70 L246 300" stroke="{BORDO}" stroke-width="4"/>
<rect x="440" y="214" width="26" height="8" rx="3" fill="{BORDO}"/>
<rect x="222" y="190" width="18" height="8" rx="3" fill="{BORDO}"/>
<path d="M548 118 L566 112 L572 140 L554 146 Z" fill="#2F2F38"/>
<path d="M596 236 Q612 236 612 252 L612 268 L588 268 Z" fill="#FFF3C0" stroke="{BORDO}" stroke-width="4" stroke-linejoin="round"/>
<path d="M560 300 L616 300 Q622 300 622 312 L622 350 L560 350 Z" fill="#3A3D44" stroke="#1C1E22" stroke-width="4"/>
<path d="M566 316 L612 316 M566 328 L612 328" stroke="#5A5E66" stroke-width="3"/>
<path d="M40 304 L100 304 L100 350 L40 350 Z" fill="#3A3D44" stroke="#1C1E22" stroke-width="4"/>
<path d="M8 96 L52 70 L52 300 L8 318 Z" fill="{AZZURRO}" stroke="{BORDO}" stroke-width="5" stroke-linejoin="round"/>
<path d="M18 120 L44 106 L44 180 L18 192 Z" fill="#CFE6F5" stroke="{BORDO}" stroke-width="4" stroke-linejoin="round"/>
<path d="M58 120 L58 280" stroke="#3A3D44" stroke-width="10"/>
<path d="M90 76 L400 76" stroke="#A9C8EE" stroke-width="6" stroke-linecap="round" opacity="0.8"/>
<g><circle cx="168" cy="352" r="56" fill="#2B2B30" stroke="#121214" stroke-width="5"/><circle cx="168" cy="352" r="26" fill="#9AA0A6" stroke="#5E646A" stroke-width="4"/>
<circle cx="500" cy="352" r="56" fill="#2B2B30" stroke="#121214" stroke-width="5"/><circle cx="500" cy="352" r="26" fill="#9AA0A6" stroke="#5E646A" stroke-width="4"/></g>
<path d="M104 344 Q168 268 232 344 M436 344 Q500 268 564 344" fill="none" stroke="{BORDO}" stroke-width="6"/>''')

# autista: testa con la mascella decisa, capelli scuri corti, un filo di barba, sorriso largo; perno al collo (60, 118)
TESTA = svg(120, 124, f'''<ellipse cx="12" cy="66" rx="9" ry="13" fill="{PELLE}" stroke="{LINEA}" stroke-width="4"/>
<ellipse cx="108" cy="66" rx="9" ry="13" fill="{PELLE}" stroke="{LINEA}" stroke-width="4"/>
<rect x="38" y="96" width="44" height="24" fill="{PELLE}" stroke="{LINEA}" stroke-width="4"/>
<path d="M15 57 Q13 12 60 10 Q107 12 105 57 Q106 98 82 106 Q60 112 38 106 Q14 98 15 57 Z" fill="{PELLE}" stroke="{LINEA}" stroke-width="5"/>
<path d="M34 100 Q60 114 86 100" fill="none" stroke="#C99A72" stroke-width="3.5" stroke-linecap="round" opacity="0.6"/>
<path d="M20 76 Q24 104 60 106 Q96 104 100 76 Q90 96 60 98 Q30 96 20 76 Z" fill="{CAPELLI}" opacity="0.28"/>
<path d="M14 52 Q10 14 58 8 Q104 8 106 50 Q98 30 80 26 Q62 34 40 28 Q22 32 14 52 Z" fill="{CAPELLI}" stroke="#1E120A" stroke-width="5" stroke-linejoin="round"/>
<path d="M32 52 Q42 46 52 51 M68 51 Q78 46 88 52" fill="none" stroke="{CAPELLI}" stroke-width="5" stroke-linecap="round"/>
<ellipse cx="42" cy="64" rx="6.5" ry="7.5" fill="#FFFFFF"/><ellipse cx="78" cy="64" rx="6.5" ry="7.5" fill="#FFFFFF"/>
<circle cx="43" cy="65" r="4.5" fill="#2A1A10"/><circle cx="79" cy="65" r="4.5" fill="#2A1A10"/>
<circle cx="44.5" cy="63" r="1.6" fill="#FFFFFF"/><circle cx="80.5" cy="63" r="1.6" fill="#FFFFFF"/>
<path d="M60 68 Q53 80 62 82" fill="none" stroke="{LINEA}" stroke-width="3.5" stroke-linecap="round"/>
<ellipse cx="28" cy="80" rx="8" ry="5" fill="#FF8A8A" opacity="0.4"/><ellipse cx="92" cy="80" rx="8" ry="5" fill="#FF8A8A" opacity="0.4"/>
<path d="M40 88 Q60 104 80 88" fill="#FFFFFF" stroke="{LINEA}" stroke-width="4" stroke-linejoin="round"/>''')

# corpo: polo blu su un busto robusto, spalle larghe e torace ampio; perno in basso al centro (85, 186), spalle in alto a y 10
CORPO = svg(170, 190, f'''<path d="M14 24 Q48 4 85 4 Q122 4 156 24 L152 100 Q164 142 144 178 Q85 190 26 178 Q6 142 18 100 Z" fill="{POLO}" stroke="{POLO_SCURO}" stroke-width="5" stroke-linejoin="round"/>
<path d="M34 128 Q85 150 136 128" fill="none" stroke="{POLO_SCURO}" stroke-width="3" opacity="0.5"/>
<path d="M66 8 L85 34 L104 8" fill="#2A4A78" stroke="{POLO_SCURO}" stroke-width="4" stroke-linejoin="round"/>
<path d="M85 34 L85 62" stroke="{POLO_SCURO}" stroke-width="3"/><circle cx="85" cy="44" r="3" fill="#E8EEF6"/><circle cx="85" cy="56" r="3" fill="#E8EEF6"/>
<path d="M28 168 Q85 182 142 168 L140 180 Q85 192 30 180 Z" fill="#2A2A30"/>
<rect x="76" y="166" width="18" height="12" rx="2" fill="#C9A445" stroke="#6A5418" stroke-width="2"/>
<path d="M104 70 L128 70 L128 88 L104 88 Z" fill="none" stroke="{POLO_SCURO}" stroke-width="3"/>''')

# braccio: manica corta della polo e avambraccio; perno alla spalla (22, 12)
BRACCIO = svg(44, 136, f'''<path d="M2 10 Q22 -2 42 10 L44 54 L0 54 Z" fill="{POLO}" stroke="{POLO_SCURO}" stroke-width="5" stroke-linejoin="round"/>
<path d="M6 52 L38 52 L35 106 L9 106 Z" fill="{PELLE}" stroke="{LINEA}" stroke-width="4" stroke-linejoin="round"/>
<ellipse cx="22" cy="118" rx="17" ry="16" fill="{PELLE}" stroke="{LINEA}" stroke-width="4"/>
<path d="M12 116 Q10 126 16 128" fill="none" stroke="{LINEA}" stroke-width="3" stroke-linecap="round"/>''')

# gamba: jeans e scarpe da lavoro; perno in alto (24, 6)
GAMBA = svg(48, 126, f'''<path d="M6 4 L42 4 L40 104 L8 104 Z" fill="{JEANS}" stroke="#22344E" stroke-width="4" stroke-linejoin="round"/>
<path d="M24 10 L24 100" stroke="#5878A8" stroke-width="2.5"/>
<path d="M2 102 Q2 96 10 96 L38 96 Q48 96 46 104 L46 116 L2 116 Z" fill="#6A4524" stroke="#3A2410" stroke-width="3" stroke-linejoin="round"/>
<path d="M6 110 L42 110" stroke="#3A2410" stroke-width="2.5"/>''')


if __name__ == "__main__":
    os.makedirs(CARTELLA_AUTISTA, exist_ok=True)
    with open(os.path.join(CARTELLA_FURGONE, "furgone.svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(FURGONE)
    for nome, testo in [("testa", TESTA), ("corpo", CORPO), ("braccio", BRACCIO), ("gamba", GAMBA)]:
        with open(os.path.join(CARTELLA_AUTISTA, nome + ".svg"), "w", encoding="utf-8", newline="\n") as f:
            f.write(testo)
    print("furgone e autista scritti")
