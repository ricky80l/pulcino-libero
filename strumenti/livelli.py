# Strumento comune per scrivere le scene dei livelli (.tscn) a partire da elenchi di pezzi.
# Lo usano genera_livello1.py, genera_prova_beccata.py e i livelli futuri.

# tipi di pezzo (stesso ordine di Tipo in scripts/blocco.gd)
(PAV, LEG, CAS, MAN, POS, SBA, PAR, RET, ERB, FUO,
 TER, BOT, CAR, TET, CEP, ABB, STE, FIE, CAN,
 TOR, ACQ, INV, CAV, CRL, POM, ANN, SPA, FRA, POZ) = range(29)
# tipi di ostacolo rompibile (stesso ordine di Tipo in scripts/rompibile.gd)
SACCO, BALLA, VASO, ZUCCA = range(4)
# piante che rimbalzano (stesso ordine di Tipo in scripts/pianta.gd)
GIRASOLE, MAIS = range(2)

INTERFACCIA = '''[node name="Interfaccia" type="CanvasLayer" parent="."]
layer = 2

[node name="Contatore" type="Control" parent="Interfaccia"]
margin_left = 16.0
margin_top = 12.0
margin_right = 176.0
margin_bottom = 68.0
rect_pivot_offset = Vector2( 80, 28 )
mouse_filter = 2

[node name="Tavola" type="TextureRect" parent="Interfaccia/Contatore"]
margin_right = 160.0
margin_bottom = 56.0
mouse_filter = 2
texture = ExtResource( 8 )
expand = true

[node name="Icona" type="TextureRect" parent="Interfaccia/Contatore"]
margin_left = 18.0
margin_top = 11.0
margin_right = 44.0
margin_bottom = 44.0
mouse_filter = 2
texture = ExtResource( 9 )
expand = true

[node name="Numero" type="Label" parent="Interfaccia/Contatore"]
margin_left = 48.0
margin_top = 4.0
margin_right = 152.0
margin_bottom = 52.0
custom_fonts/font = ExtResource( 10 )
custom_colors/font_color = Color( 1, 0.96, 0.86, 1 )
text = "0 / 0"
align = 1
valign = 1

[node name="Messaggio" type="Control" parent="Interfaccia"]
anchor_right = 1.0
anchor_bottom = 1.0
mouse_filter = 2

[node name="Sfondo" type="ColorRect" parent="Interfaccia/Messaggio"]
anchor_right = 1.0
anchor_bottom = 1.0
mouse_filter = 2
color = Color( 0, 0, 0, 0.5 )

[node name="Testo" type="Label" parent="Interfaccia/Messaggio"]
anchor_right = 1.0
anchor_bottom = 1.0
custom_fonts/font = ExtResource( 11 )
custom_colors/font_color = Color( 1, 0.96, 0.86, 1 )
text = "Sei scappato dal pollaio!

Premi salto per rigiocare"
align = 1
valign = 1
'''


def scrivi_livello(percorso, nome_nodo, gruppo_pezzi, pezzi, chicchi=(), nidi=(), topi=(), rompibili=(),
                   uscita=(3900, 610), partenza=(450, 610), limite_destro=4200, proprieta_livello=None, oche=(),
                   piante=()):
    """pezzi: (nome, x, y, larghezza, altezza, tipo, extra); rompibili: (x, y, tipo, resistenza);
    oche: (x, y, distanza); piante: (x, y, tipo) con x, y = base a terra;
    proprieta_livello: valori da impostare sullo script del livello (es. numero, frase_fine)."""
    risorse = [
        ("res://scripts/livello.gd", "Script"),
        ("res://scripts/blocco.gd", "Script"),
        ("res://scenes/player.tscn", "PackedScene"),
        ("res://scenes/controlli_touch.tscn", "PackedScene"),
        ("res://scripts/chicco.gd", "Script"),
        ("res://scripts/nido.gd", "Script"),
        ("res://scripts/topo.gd", "Script"),
        ("res://assets/grafica/oggetti/etichetta.svg", "Texture"),
        ("res://assets/grafica/oggetti/chicco.svg", "Texture"),
        ("res://assets/font/fredoka_contatore.tres", "DynamicFont"),
        ("res://assets/font/fredoka_messaggio.tres", "DynamicFont"),
        ("res://scripts/pausa.gd", "Script"),
    ]
    if rompibili:
        risorse.append(("res://scripts/rompibile.gd", "Script"))
    if oche:
        risorse.append(("res://scripts/oca.gd", "Script"))
    if piante:
        risorse.append(("res://scripts/pianta.gd", "Script"))
    id_di = {path: i for i, (path, _t) in enumerate(risorse, 1)}

    out = [f"[gd_scene load_steps={len(risorse) + 2} format=2]\n"]
    for i, (path, tipo) in enumerate(risorse, 1):
        riga = f'[ext_resource path="{path}" type="{tipo}" id={i}]'
        out.append(riga + ("\n" if i == len(risorse) else ""))
    out.append('[sub_resource type="RectangleShape2D" id=1]\nextents = Vector2( 30, 30 )\n')
    radice = f'[node name="{nome_nodo}" type="Node2D"]\nscript = ExtResource( 1 )'
    for k, v in (proprieta_livello or {}).items():
        radice += f"\n{k} = {v}"
    out.append(radice + "\n")

    out.append(f'[node name="{gruppo_pezzi}" type="Node2D" parent="."]\n')
    for nome, x, y, w, h, tipo, extra in pezzi:
        righe = [f'[node name="{nome}" type="StaticBody2D" parent="{gruppo_pezzi}"]']
        if "z_index" in extra:
            righe.append(f"z_index = {extra['z_index']}")
        righe.append(f"position = Vector2( {x}, {y} )")
        righe.append("script = ExtResource( 2 )")
        righe.append(f"tipo = {tipo}")
        righe.append(f"dimensioni = Vector2( {w}, {h} )")
        for k in ("solido", "attraversabile_da_sotto"):
            if k in extra:
                righe.append(f"{k} = {extra[k]}")
        out.append("\n".join(righe) + "\n")

    if rompibili:
        out.append('[node name="Rompibili" type="Node2D" parent="."]\n')
        for i, (x, y, tipo, resistenza) in enumerate(rompibili, 1):
            out.append(f'[node name="Rompibile{i}" type="StaticBody2D" parent="Rompibili"]\n'
                       f'position = Vector2( {x}, {y} )\nscript = ExtResource( {id_di["res://scripts/rompibile.gd"]} )\n'
                       f'tipo = {tipo}\nresistenza = {resistenza}\n')

    if piante:
        out.append('[node name="Piante" type="Node2D" parent="."]\n')
        for i, (x, y, tipo) in enumerate(piante, 1):
            out.append(f'[node name="Pianta{i}" type="StaticBody2D" parent="Piante"]\nposition = Vector2( {x}, {y} )\n'
                       f'script = ExtResource( {id_di["res://scripts/pianta.gd"]} )\ntipo = {tipo}\n')

    out.append('[node name="Nidi" type="Node2D" parent="."]\n')
    for i, (x, y) in enumerate(nidi, 1):
        out.append(f'[node name="Nido{i}" type="Area2D" parent="Nidi"]\nposition = Vector2( {x}, {y} )\nscript = ExtResource( 6 )\n')

    out.append('[node name="Chicchi" type="Node2D" parent="."]\n')
    for i, (x, y) in enumerate(chicchi, 1):
        out.append(f'[node name="Chicco{i}" type="Area2D" parent="Chicchi"]\nposition = Vector2( {x}, {y} )\nscript = ExtResource( 5 )\n')

    out.append('[node name="Nemici" type="Node2D" parent="."]\n')
    for i, (x, y, dist) in enumerate(topi, 1):
        out.append(f'[node name="Topo{i}" type="Area2D" parent="Nemici"]\nposition = Vector2( {x}, {y} )\nscript = ExtResource( 7 )\ndistanza = {dist}.0\n')
    for i, (x, y, dist) in enumerate(oche, 1):
        out.append(f'[node name="Oca{i}" type="KinematicBody2D" parent="Nemici"]\nposition = Vector2( {x}, {y} )\n'
                   f'script = ExtResource( {id_di["res://scripts/oca.gd"]} )\ndistanza = {dist}.0\n')

    out.append(f'''[node name="Uscita" type="Area2D" parent="."]
position = Vector2( {uscita[0]}, {uscita[1]} )

[node name="Forma" type="CollisionShape2D" parent="Uscita"]
shape = SubResource( 1 )

[node name="Player" parent="." instance=ExtResource( 3 )]
position = Vector2( {partenza[0]}, {partenza[1]} )

[node name="Camera2D" type="Camera2D" parent="Player"]
current = true
limit_left = 0
limit_top = 0
limit_right = {limite_destro}
limit_bottom = 720
smoothing_enabled = true
smoothing_speed = 6.0
zoom = Vector2( 0.7, 0.7 )

[node name="ControlliTouch" parent="." instance=ExtResource( 4 )]

[node name="Pausa" type="CanvasLayer" parent="."]
script = ExtResource( 12 )

''' + INTERFACCIA)

    with open(percorso, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out))
