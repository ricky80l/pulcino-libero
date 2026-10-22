# Scrive i disegni SVG dei dieci luoghi della mappa e della nebbia in assets/grafica/mappa/.
# Uso: python strumenti/disegni_mappa.py   (dalla cartella del progetto)
# Ogni luogo è 240x200 (il doppio della grandezza nel gioco) con la base al centro in basso (120, 190).
import os

CARTELLA = os.path.join(os.path.dirname(__file__), "..", "assets", "grafica", "mappa")
C = "#5A3E14"  # contorno


def svg(w, h, corpo):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{corpo}\n</svg>\n'


OMBRA = '<ellipse cx="120" cy="188" rx="100" ry="11" fill="#000000" fill-opacity="0.12"/>'

LUOGHI = {
    "pollaio": f'''{OMBRA}
<rect x="50" y="86" width="140" height="98" rx="4" fill="#E8D6B0" stroke="{C}" stroke-width="5"/>
<path d="M78 92 L78 180 M106 92 L106 180 M134 92 L134 180 M162 92 L162 180" stroke="#C9B07E" stroke-width="3"/>
<path d="M34 94 L120 26 L206 94 Z" fill="#D2553A" stroke="{C}" stroke-width="5" stroke-linejoin="round"/>
<path d="M66 70 L174 70" stroke="#B3402A" stroke-width="3"/>
<circle cx="120" cy="64" r="10" fill="#FFE58A" stroke="{C}" stroke-width="4"/>
<path d="M100 184 L100 148 Q120 124 140 148 L140 184 Z" fill="#7A4E22" stroke="{C}" stroke-width="4" stroke-linejoin="round"/>
<path d="M140 184 L182 196" stroke="#B07A3E" stroke-width="8" stroke-linecap="round"/>''',

    "cortile": f'''{OMBRA}
<ellipse cx="120" cy="146" rx="106" ry="44" fill="#D8B47A" stroke="#8F5F2A" stroke-width="4"/>
<path d="M18 132 Q120 74 222 132" fill="none" stroke="#B07A3E" stroke-width="6" stroke-linecap="round"/>
<path d="M34 120 L34 142 M66 104 L66 126 M100 96 L100 118 M140 96 L140 118 M174 104 L174 126 M206 120 L206 142" stroke="{C}" stroke-width="6" stroke-linecap="round"/>
<rect x="132" y="116" width="46" height="30" rx="8" fill="#EBC85A" stroke="#8A6420" stroke-width="4"/>
<path d="M146 118 L146 144 M162 118 L162 144" stroke="#C9A040" stroke-width="3"/>
<path d="M66 116 L96 116 L91 146 L71 146 Z" fill="#8FA3B5" stroke="#3E4E5C" stroke-width="4" stroke-linejoin="round"/>
<g fill="#F2C230"><circle cx="104" cy="160" r="3"/><circle cx="116" cy="166" r="3"/><circle cx="126" cy="158" r="3"/></g>
<path d="M22 162 Q120 214 218 162" fill="none" stroke="#B07A3E" stroke-width="6" stroke-linecap="round"/>
<path d="M36 166 L36 188 M76 178 L76 200 M120 182 L120 200 M164 178 L164 200 M204 166 L204 188" stroke="{C}" stroke-width="6" stroke-linecap="round"/>''',

    "orto": f'''{OMBRA}
<rect x="24" y="98" width="192" height="84" rx="18" fill="#8A5A2E" stroke="{C}" stroke-width="5"/>
<path d="M36 120 L204 120 M36 142 L204 142 M36 164 L204 164" stroke="#6E4522" stroke-width="4" stroke-linecap="round"/>
<g fill="#6DBE45" stroke="#3E7A22" stroke-width="2.5">
<ellipse cx="50" cy="112" rx="6" ry="11" transform="rotate(-25 50 112)"/><ellipse cx="58" cy="112" rx="6" ry="11" transform="rotate(25 58 112)"/>
<ellipse cx="96" cy="112" rx="6" ry="11" transform="rotate(-25 96 112)"/><ellipse cx="104" cy="112" rx="6" ry="11" transform="rotate(25 104 112)"/>
<ellipse cx="70" cy="134" rx="6" ry="11" transform="rotate(-25 70 134)"/><ellipse cx="78" cy="134" rx="6" ry="11" transform="rotate(25 78 134)"/>
<ellipse cx="118" cy="134" rx="6" ry="11" transform="rotate(-25 118 134)"/><ellipse cx="126" cy="134" rx="6" ry="11" transform="rotate(25 126 134)"/>
<ellipse cx="50" cy="156" rx="6" ry="11" transform="rotate(-25 50 156)"/><ellipse cx="58" cy="156" rx="6" ry="11" transform="rotate(25 58 156)"/>
<ellipse cx="100" cy="156" rx="6" ry="11" transform="rotate(-25 100 156)"/><ellipse cx="108" cy="156" rx="6" ry="11" transform="rotate(25 108 156)"/>
</g>
<g fill="#F28C28" stroke="#9A4E10" stroke-width="2.5"><path d="M144 116 l6 -12 l6 12 Z"/><path d="M146 160 l6 -12 l6 12 Z"/></g>
<path d="M186 184 L186 62 M160 84 L212 84" stroke="#8F5F2A" stroke-width="6" stroke-linecap="round"/>
<path d="M172 86 L200 86 L196 128 L176 128 Z" fill="#4F7DB8" stroke="{C}" stroke-width="4" stroke-linejoin="round"/>
<circle cx="186" cy="56" r="14" fill="#EBC85A" stroke="{C}" stroke-width="4"/>
<path d="M166 46 L206 46 L186 24 Z" fill="#B07A3E" stroke="{C}" stroke-width="4" stroke-linejoin="round"/>''',

    "prato": f'''{OMBRA}
<ellipse cx="120" cy="162" rx="110" ry="34" fill="#7CC24E" stroke="#4E9A2E" stroke-width="4"/>
<g stroke="#4E9A2E" stroke-width="2"><circle cx="50" cy="156" r="6" fill="#FFFFFF"/><circle cx="80" cy="170" r="6" fill="#FF9EC0"/><circle cx="104" cy="152" r="6" fill="#FFD84A"/><circle cx="190" cy="164" r="6" fill="#FFFFFF"/><circle cx="68" cy="140" r="5" fill="#B48CF2"/><circle cx="200" cy="146" r="5" fill="#FF9EC0"/></g>
<path d="M150 168 Q146 120 150 82" fill="none" stroke="#3E7A22" stroke-width="6" stroke-linecap="round"/>
<ellipse cx="134" cy="128" rx="14" ry="7" fill="#6DBE45" stroke="#3E7A22" stroke-width="3" transform="rotate(-25 134 128)"/>
<ellipse cx="166" cy="116" rx="14" ry="7" fill="#6DBE45" stroke="#3E7A22" stroke-width="3" transform="rotate(25 166 116)"/>
<g fill="#FFD84A" stroke="#C99A05" stroke-width="3">
<ellipse cx="150" cy="52" rx="9" ry="16"/><ellipse cx="150" cy="96" rx="9" ry="16"/><ellipse cx="128" cy="74" rx="16" ry="9"/><ellipse cx="172" cy="74" rx="16" ry="9"/>
<ellipse cx="135" cy="59" rx="9" ry="15" transform="rotate(-45 135 59)"/><ellipse cx="165" cy="59" rx="9" ry="15" transform="rotate(45 165 59)"/>
<ellipse cx="135" cy="89" rx="9" ry="15" transform="rotate(45 135 89)"/><ellipse cx="165" cy="89" rx="9" ry="15" transform="rotate(-45 165 89)"/>
</g>
<circle cx="150" cy="74" r="14" fill="#7A4E12" stroke="{C}" stroke-width="3"/>''',

    "bosco": f'''{OMBRA}
<g stroke="{C}" stroke-width="5"><rect x="72" y="110" width="16" height="72" rx="4" fill="#7A4E22"/><rect x="156" y="104" width="16" height="78" rx="4" fill="#7A4E22"/><rect x="112" y="136" width="16" height="50" rx="4" fill="#7A4E22"/></g>
<g stroke="#2F6B1A" stroke-width="5"><circle cx="80" cy="82" r="46" fill="#4E9A2E"/><circle cx="164" cy="72" r="50" fill="#4E9A2E"/><circle cx="120" cy="118" r="42" fill="#5DAE3A"/></g>
<g fill="#7CC24E"><circle cx="66" cy="66" r="14"/><circle cx="150" cy="54" r="16"/><circle cx="108" cy="104" r="13"/></g>''',

    "stagno": f'''{OMBRA}
<ellipse cx="124" cy="146" rx="104" ry="42" fill="#5DB4E3" stroke="#2F7FAF" stroke-width="5"/>
<ellipse cx="124" cy="146" rx="66" ry="22" fill="#8FD0F2"/>
<g fill="#6DBE45" stroke="#3E7A22" stroke-width="3"><path d="M90 140 a14 9 0 1 0 6 -8 l-6 8 Z"/><path d="M160 156 a14 9 0 1 0 6 -8 l-6 8 Z"/><path d="M140 128 a11 7 0 1 0 5 -6 l-5 6 Z"/></g>
<circle cx="98" cy="134" r="5" fill="#FF9EC0" stroke="#B3407A" stroke-width="2"/>
<path d="M30 150 L30 86 M42 152 L44 96 M54 154 L52 104" stroke="#3E7A22" stroke-width="4" stroke-linecap="round"/>
<g fill="#7A4E22" stroke="{C}" stroke-width="2.5"><rect x="25" y="80" width="10" height="24" rx="5"/><rect x="39" y="90" width="10" height="22" rx="5"/><rect x="47" y="98" width="10" height="20" rx="5"/></g>''',

    "collina": f'''{OMBRA}
<path d="M10 186 Q50 70 120 42 Q196 34 230 186 Z" fill="#A99A84" stroke="#5E5446" stroke-width="5" stroke-linejoin="round"/>
<path d="M120 46 Q150 44 170 76 Q140 70 120 46 Z" fill="#C8BCA8"/>
<g fill="#8A7C68" stroke="#5E5446" stroke-width="4"><ellipse cx="80" cy="130" rx="22" ry="14"/><ellipse cx="150" cy="112" rx="18" ry="12"/><ellipse cx="176" cy="156" rx="24" ry="14"/><ellipse cx="112" cy="166" rx="16" ry="10"/></g>
<g fill="#6DBE45" stroke="#3E7A22" stroke-width="2.5"><path d="M24 186 l6 -16 l6 16 Z"/><path d="M36 186 l6 -12 l6 12 Z"/><path d="M200 186 l6 -16 l6 16 Z"/><path d="M212 186 l6 -12 l6 12 Z"/></g>''',

    "grotta": f'''{OMBRA}
<path d="M14 186 Q34 52 120 36 Q206 48 226 186 Z" fill="#8E8478" stroke="#4B443B" stroke-width="5" stroke-linejoin="round"/>
<path d="M78 186 Q78 102 120 98 Q162 102 162 186 Z" fill="#2A2420" stroke="#4B443B" stroke-width="5" stroke-linejoin="round"/>
<g fill="#8E8478"><path d="M96 108 l6 16 l6 -16 Z"/><path d="M118 100 l5 20 l5 -20 Z"/><path d="M138 106 l6 14 l6 -14 Z"/></g>
<g fill="#6DBE45"><ellipse cx="60" cy="72" rx="20" ry="8"/><ellipse cx="180" cy="80" rx="18" ry="7"/><ellipse cx="44" cy="150" rx="14" ry="6"/></g>
<g fill="#FFE58A"><circle cx="112" cy="150" r="3.5"/><circle cx="128" cy="150" r="3.5"/></g>''',

    "paese": f'''{OMBRA}
<g stroke="{C}" stroke-width="5" stroke-linejoin="round">
<rect x="22" y="112" width="62" height="72" fill="#F2E3C6"/><path d="M14 116 L53 80 L92 116 Z" fill="#C2553A"/>
<rect x="156" y="118" width="62" height="66" fill="#F2E3C6"/><path d="M148 122 L187 88 L226 122 Z" fill="#E08A3A"/>
<rect x="88" y="90" width="66" height="94" fill="#FFF1D8"/><path d="M80 94 L121 50 L162 94 Z" fill="#4F7DB8"/>
</g>
<g fill="#FFE58A" stroke="{C}" stroke-width="3"><rect x="34" y="126" width="16" height="16"/><rect x="104" y="104" width="16" height="16"/><rect x="124" y="104" width="16" height="16"/><rect x="190" y="132" width="16" height="16"/></g>
<g fill="#7A4E22" stroke="{C}" stroke-width="3"><rect x="58" y="150" width="16" height="34"/><rect x="110" y="146" width="22" height="38"/><rect x="166" y="152" width="16" height="32"/></g>''',

    "campanile": f'''{OMBRA}
<rect x="78" y="166" width="84" height="20" rx="3" fill="#C9B48A" stroke="{C}" stroke-width="5"/>
<rect x="90" y="62" width="60" height="106" fill="#E4D3B0" stroke="{C}" stroke-width="5"/>
<path d="M82 66 L120 6 L158 66 Z" fill="#C2553A" stroke="{C}" stroke-width="5" stroke-linejoin="round"/>
<path d="M102 108 L102 84 Q120 66 138 84 L138 108 Z" fill="#5A3E14"/>
<path d="M108 102 Q108 84 120 82 Q132 84 132 102 Z" fill="#F2B705" stroke="#8A5A00" stroke-width="3"/>
<circle cx="120" cy="134" r="14" fill="#FFFFFF" stroke="{C}" stroke-width="4"/>
<path d="M120 134 L120 124 M120 134 L128 138" stroke="{C}" stroke-width="3" stroke-linecap="round"/>
<path d="M108 168 L108 150 Q120 140 132 150 L132 168" fill="#7A4E22" stroke="{C}" stroke-width="3"/>''',
}

NEBBIA = '''<g fill="#DCE5EC"><circle cx="70" cy="116" r="50"/><circle cx="132" cy="88" r="62"/><circle cx="196" cy="112" r="52"/><circle cx="242" cy="130" r="34"/><circle cx="40" cy="136" r="34"/></g>
<g fill="#FFFFFF"><circle cx="70" cy="108" r="50"/><circle cx="132" cy="80" r="62"/><circle cx="196" cy="104" r="52"/><circle cx="242" cy="122" r="34"/><circle cx="40" cy="128" r="34"/></g>'''

os.makedirs(CARTELLA, exist_ok=True)
for nome, corpo in LUOGHI.items():
    with open(os.path.join(CARTELLA, nome + ".svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(svg(240, 200, corpo))
with open(os.path.join(CARTELLA, "nebbia.svg"), "w", encoding="utf-8", newline="\n") as f:
    f.write(svg(280, 180, NEBBIA))
print(len(LUOGHI) + 1, "disegni scritti in", os.path.abspath(CARTELLA))
