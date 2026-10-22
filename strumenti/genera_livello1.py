import sys

PAV, LEG, CAS, MAN, POS, SBA, PAR, RET, ERB, FUO = range(10)

# nome, x, y, larghezza, altezza, tipo, extra
pezzi = [
    # sfondo (decorazioni)
    ("ParetePollaio", 0, 0, 3715, 720, PAR, {"solido": "false", "z_index": "-10"}),
    ("Fuori", 3715, 0, 525, 720, FUO, {"solido": "false", "z_index": "-10"}),
    ("GabbiaSbarre", 316, 436, 368, 204, SBA, {"solido": "false", "z_index": "-5"}),
    # pavimento e muri
    ("PavimentoA", 0, 640, 2000, 80, PAV, {}),
    ("FondoFosso", 2000, 700, 160, 20, PAV, {}),
    ("PavimentoB", 2160, 640, 1555, 80, PAV, {}),
    ("Prato", 3715, 640, 525, 80, ERB, {}),
    ("MuroSinistro", 0, 0, 40, 640, LEG, {}),
    ("MuroDestro", 4200, 0, 40, 720, LEG, {}),
    # gabbia di partenza: si esce saltando il bordo basso a destra
    ("GabbiaLato", 300, 420, 16, 220, SBA, {}),
    ("GabbiaTetto", 300, 420, 400, 16, SBA, {}),
    ("GabbiaBordoBasso", 684, 580, 16, 60, SBA, {}),
    # mangiatoia da scavalcare
    ("Mangiatoia1", 900, 590, 180, 50, MAN, {}),
    # scala di cassette
    ("Cassetta1", 1250, 560, 80, 80, CAS, {}),
    ("Cassetta2", 1330, 560, 80, 80, CAS, {}),
    ("Cassetta3", 1330, 480, 80, 80, CAS, {}),
    ("Cassetta4", 1410, 560, 80, 80, CAS, {}),
    ("Cassetta5", 1410, 480, 80, 80, CAS, {}),
    ("Cassetta6", 1410, 400, 80, 80, CAS, {}),
    # posatoi per superare il recinto interno
    ("Posatoio1", 2300, 540, 140, 16, POS, {"attraversabile_da_sotto": "true"}),
    ("Posatoio2", 2500, 440, 140, 16, POS, {"attraversabile_da_sotto": "true"}),
    ("Posatoio3", 2720, 340, 140, 16, POS, {"attraversabile_da_sotto": "true"}),
    ("Posatoio4", 2940, 260, 140, 16, POS, {"attraversabile_da_sotto": "true"}),
    ("RecintoInterno", 3150, 300, 30, 340, LEG, {}),
    # ultime cassette
    ("Cassetta7", 3350, 560, 80, 80, CAS, {}),
    ("Cassetta8", 3430, 560, 80, 80, CAS, {}),
    ("Cassetta9", 3430, 480, 80, 80, CAS, {}),
    # rete esterna con la buca in basso
    ("ReteEsterna", 3700, 0, 30, 580, RET, {}),
]

# chicchi di mais (centro)
chicchi = [
    (450, 520), (500, 610),            # gabbia
    (692, 540), (800, 610),            # uscita dalla gabbia
    (990, 555),                        # sulla mangiatoia
    (1290, 525), (1370, 445), (1450, 365),  # scala di cassette
    (1760, 560), (1810, 525), (1860, 560),  # arco sopra il topo
    (2080, 670),                       # nel fosso
    (2370, 505), (2570, 405), (2790, 305), (3010, 225),  # posatoi
    (3165, 265),                       # sul recinto
    (3390, 525), (3470, 445),          # ultime cassette
    (3600, 610),                       # davanti alla buca
]
# nidi (centro, appoggiati a terra)
nidi = [(1160, 640), (1560, 640), (2230, 640), (3270, 640)]
# topi: x di partenza, y a terra, distanza verso destra
topi = [(1680, 640, 240)]

out = []
out.append("[gd_scene load_steps=14 format=2]\n")
out.append('[ext_resource path="res://scripts/livello.gd" type="Script" id=1]')
out.append('[ext_resource path="res://scripts/blocco.gd" type="Script" id=2]')
out.append('[ext_resource path="res://scenes/player.tscn" type="PackedScene" id=3]')
out.append('[ext_resource path="res://scenes/controlli_touch.tscn" type="PackedScene" id=4]')
out.append('[ext_resource path="res://scripts/chicco.gd" type="Script" id=5]')
out.append('[ext_resource path="res://scripts/nido.gd" type="Script" id=6]')
out.append('[ext_resource path="res://scripts/topo.gd" type="Script" id=7]')
out.append('[ext_resource path="res://assets/grafica/oggetti/etichetta.svg" type="Texture" id=8]')
out.append('[ext_resource path="res://assets/grafica/oggetti/chicco.svg" type="Texture" id=9]')
out.append('[ext_resource path="res://assets/font/fredoka_contatore.tres" type="DynamicFont" id=10]')
out.append('[ext_resource path="res://assets/font/fredoka_messaggio.tres" type="DynamicFont" id=11]')
out.append('[ext_resource path="res://scripts/pausa.gd" type="Script" id=12]\n')
out.append('[sub_resource type="RectangleShape2D" id=1]\nextents = Vector2( 30, 30 )\n')
out.append('[node name="Livello1" type="Node2D"]\nscript = ExtResource( 1 )\n')
out.append('[node name="Pollaio" type="Node2D" parent="."]\n')
for nome, x, y, w, h, tipo, extra in pezzi:
    righe = [f'[node name="{nome}" type="StaticBody2D" parent="Pollaio"]']
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

out.append('[node name="Nidi" type="Node2D" parent="."]\n')
for i, (x, y) in enumerate(nidi, 1):
    out.append(f'[node name="Nido{i}" type="Area2D" parent="Nidi"]\nposition = Vector2( {x}, {y} )\nscript = ExtResource( 6 )\n')

out.append('[node name="Chicchi" type="Node2D" parent="."]\n')
for i, (x, y) in enumerate(chicchi, 1):
    out.append(f'[node name="Chicco{i}" type="Area2D" parent="Chicchi"]\nposition = Vector2( {x}, {y} )\nscript = ExtResource( 5 )\n')

out.append('[node name="Nemici" type="Node2D" parent="."]\n')
for i, (x, y, dist) in enumerate(topi, 1):
    out.append(f'[node name="Topo{i}" type="Area2D" parent="Nemici"]\nposition = Vector2( {x}, {y} )\nscript = ExtResource( 7 )\ndistanza = {dist}.0\n')

out.append('''[node name="Uscita" type="Area2D" parent="."]
position = Vector2( 3900, 610 )

[node name="Forma" type="CollisionShape2D" parent="Uscita"]
shape = SubResource( 1 )

[node name="Player" parent="." instance=ExtResource( 3 )]
position = Vector2( 450, 610 )

[node name="Camera2D" type="Camera2D" parent="Player"]
current = true
limit_left = 0
limit_top = 0
limit_right = 4200
limit_bottom = 720
smoothing_enabled = true
smoothing_speed = 6.0
zoom = Vector2( 0.7, 0.7 )

[node name="ControlliTouch" parent="." instance=ExtResource( 4 )]

[node name="Pausa" type="CanvasLayer" parent="."]
script = ExtResource( 12 )

[node name="Interfaccia" type="CanvasLayer" parent="."]
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
''')

with open(sys.argv[1], "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(out))
