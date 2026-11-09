extends Node2D
# Un piano del paesaggio lontano, dentro uno strato di parallasse (vedi atmosfera.gd).
# Si disegna da solo secondo il tipo. Le colline si ripetono ogni "larghezza" pixel senza scalini.
# Le altezze sono quelle del livello: il prato davanti è a 640.
# Per il peso sul telefono: solo rettangoli e poligoni (niente cerchi né linee spesse), raggruppati per tipo,
# così la scheda video li disegna in pochi colpi.

var tipo := ""
var larghezza := 2048.0
var tempo := 0.0


func _ready():
	if tipo in ["raggi", "fasci_lucernari", "fasci_fessure"]:
		var luce := CanvasItemMaterial.new()
		luce.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD  # i raggi schiariscono quello che c'è dietro
		material = luce


func _process(delta):
	if tipo == "raggi":
		# i raggi ondeggiano piano, come la luce tra le foglie
		tempo += delta
		rotation = sin(tempo * 0.35) * 0.04
		modulate.a = 0.85 + sin(tempo * 0.8) * 0.15
	elif tipo.begins_with("fasci"):
		# la luce che entra respira piano, come se passasse una nuvola
		tempo += delta
		modulate.a = 0.8 + sin(tempo * 0.5) * 0.2


func _draw():
	match tipo:
		"cielo":
			_cielo()
		"sole":
			_sole()
		"raggi":
			_raggi()
		"nuvole":
			_nuvole()
		"colline_lontane":
			_colline(470.0, [[60.0, 1, 1.0], [26.0, 4, 2.0]], Color("a9d3b6"), Color("c2e0c8"))
		"colline":
			_colline(530.0, [[46.0, 2, 0.5], [18.0, 8, 1.7]], Color("86c45e"), Color("9bd06f"))
			_case_e_alberi()
		"campi":
			_colline(530.0, [[46.0, 2, 0.5], [18.0, 8, 1.7]], Color("86c45e"), Color("9bd06f"))
			_campi()
		"fasci_lucernari":
			_fasci_lucernari()
		"fasci_fessure":
			_fasci_fessure()
		"siepi":
			_siepi()
		"prato_fiori":
			_prato_fiori()


func _cielo():
	# dal blu in alto al celeste chiaro vicino all'orizzonte
	# gli strati fermi partono dal centro dello schermo: il cielo si allarga molto da entrambe le parti
	var punti := PoolVector2Array([Vector2(-1400, -400), Vector2(1400, -400), Vector2(1400, 620), Vector2(-1400, 620)])
	var colori := PoolColorArray([Color("5fb4ec"), Color("5fb4ec"), Color("dcf1fb"), Color("dcf1fb")])
	draw_polygon(punti, colori)
	draw_rect(Rect2(-1400, 620, 2800, 300), Color("dcf1fb"))


func _sole():
	var c := Vector2(170, 290)
	for i in range(6):
		_tondo(c, 130 - i * 14, Color(1.0, 0.95, 0.7, 0.07), 40)  # alone caldo
	_tondo(c, 52, Color("ffe27a"), 32)
	_tondo(c, 44, Color("fff1b3"), 32)


func _raggi():
	# fasci di luce che scendono dal sole verso il prato
	var c := Vector2(170, 290)
	var angoli := [0.95, 1.25, 1.55, 1.85, 2.15]
	for i in range(angoli.size()):
		var a: float = angoli[i]
		var apertura: float = 0.035 + (i % 2) * 0.02
		var lungo := 900.0
		var p1 := c + Vector2(cos(a - apertura), sin(a - apertura)) * lungo
		var p2 := c + Vector2(cos(a + apertura), sin(a + apertura)) * lungo
		draw_polygon(PoolVector2Array([c, p1, p2]),
				PoolColorArray([Color(1, 0.95, 0.75, 0.12), Color(1, 0.95, 0.75, 0.0), Color(1, 0.95, 0.75, 0.0)]))


func _nuvole():
	for n in [[Vector2(200, 270), 1.0], [Vector2(900, 340), 0.8], [Vector2(1450, 250), 1.2]]:
		var c: Vector2 = n[0]
		var s: float = n[1]
		for d in [Vector2(-34, 8), Vector2(0, -10), Vector2(34, 4), Vector2(62, 12), Vector2(-60, 14)]:
			_tondo(c + d * s, 30 * s, Color(0.88, 0.94, 0.98), 24)
		for d in [Vector2(-34, 4), Vector2(0, -14), Vector2(34, 0), Vector2(62, 8), Vector2(-60, 10)]:
			_tondo(c + d * s, 27 * s, Color.white, 24)


# Colline: somma di onde che si ripetono esattamente ogni "larghezza" (onde: [altezza, quante volte, fase])
func _colline(base: float, onde: Array, colore: Color, luce: Color):
	var punti := PoolVector2Array()
	var cresta := PoolVector2Array()
	var x := 0.0
	while x <= larghezza + 0.1:
		var y: float = base
		for o in onde:
			y -= o[0] * (0.5 + 0.5 * sin(TAU * x * o[1] / larghezza + o[2]))
		punti.append(Vector2(x, y))
		cresta.append(Vector2(x, y + 6))
		x += 16.0
	punti.append(Vector2(larghezza, 760))
	punti.append(Vector2(0, 760))
	draw_colored_polygon(punti, colore)
	# bordo più chiaro dove batte il sole: una fascia larga 6 lungo la cresta, fatta come un poligono solo
	var fascia := PoolVector2Array()
	for q in cresta:
		fascia.append(q + Vector2(0, -3))
	for k in range(cresta.size() - 1, -1, -1):
		fascia.append(cresta[k] + Vector2(0, 3))
	draw_colored_polygon(fascia, luce)


func _y_collina(x: float) -> float:
	return 530.0 - 46.0 * (0.5 + 0.5 * sin(TAU * x * 2 / larghezza + 0.5)) - 18.0 * (0.5 + 0.5 * sin(TAU * x * 8 / larghezza + 1.7))


func _case_e_alberi():
	# una cascina lontana con il tetto rosso e qualche albero tondo, velati dalla distanza
	var x := 520.0
	var y: float = _y_collina(x) + 8
	draw_rect(Rect2(x, y - 46, 70, 46), Color("e8d6b8"))
	draw_colored_polygon(PoolVector2Array([Vector2(x - 8, y - 44), Vector2(x + 35, y - 72), Vector2(x + 78, y - 44)]), Color("c9715a"))
	draw_rect(Rect2(x + 28, y - 26, 14, 26), Color("9c7b5a"))
	draw_rect(Rect2(x + 90, y - 30, 40, 30), Color("d6b48e"))
	draw_colored_polygon(PoolVector2Array([Vector2(x + 86, y - 28), Vector2(x + 110, y - 46), Vector2(x + 134, y - 28)]), Color("b8664f"))
	_alberi([180.0, 260.0, 760.0, 1180.0, 1260.0, 1620.0, 1890.0])


# Alberi tondi sulla collina: prima tutti i tronchi, poi tutte le chiome, poi tutti i riflessi
func _alberi(dove: Array):
	for t in dove:
		var ty: float = _y_collina(t) + 10
		draw_rect(Rect2(t - 4, ty - 26, 8, 26), Color("8a6a48"))
	for t in dove:
		_tondo(Vector2(t, _y_collina(t) + 10 - 40), 24, Color("5f9e45"), 24)
	for t in dove:
		_tondo(Vector2(t - 7, _y_collina(t) + 10 - 47), 10, Color("78b85a"), 14)


# Cerchio pieno fatto con un poligono
func _tondo(centro: Vector2, raggio: float, colore: Color, lati := 20):
	var punti := PoolVector2Array()
	for k in range(lati):
		var a := TAU * k / float(lati)
		punti.append(centro + Vector2(cos(a), sin(a)) * raggio)
	draw_colored_polygon(punti, colore)


# Campi coltivati a strisce sulle colline (orto), con qualche albero
func _campi():
	var colori := [Color("a7c95a"), Color("c9b45a"), Color("8fbf4e"), Color("d6a85a")]
	var x := 0.0
	var i := 0
	var solchi := []
	while x < larghezza:
		var largo := 150.0 + (i % 3) * 40.0
		var y1: float = _y_collina(x) + 14
		var y2: float = _y_collina(x + largo) + 14
		var c: Color = colori[i % colori.size()]
		draw_colored_polygon(PoolVector2Array([Vector2(x, y1), Vector2(x + largo, y2), Vector2(x + largo, y2 + 46), Vector2(x, y1 + 46)]), c)
		for k in range(1, 4):
			solchi.append([Vector2(x, y1 + k * 11), Vector2(x + largo, y2 + k * 11), c.darkened(0.12)])
		x += largo + 30.0
		i += 1
	# solchi: strisce sottili, dopo tutti i campi
	for q in solchi:
		var da: Vector2 = q[0]
		var a: Vector2 = q[1]
		draw_colored_polygon(PoolVector2Array([da + Vector2(0, -1), a + Vector2(0, -1), a + Vector2(0, 1), da + Vector2(0, 1)]), q[2])
	_alberi([300.0, 980.0, 1500.0, 1840.0])


# Fasci di luce dai lucernari del soffitto del magazzino (stessi punti di _disegna_lamiera in blocco.gd)
func _fasci_lucernari():
	var x := 180.0
	while x < larghezza - 150:
		var alto := 66.0
		var basso := 640.0
		draw_polygon(PoolVector2Array([Vector2(x + 10, alto), Vector2(x + 140, alto), Vector2(x + 220, basso), Vector2(x + 30, basso)]),
				PoolColorArray([Color(1, 0.96, 0.82, 0.16), Color(1, 0.96, 0.82, 0.16), Color(1, 0.96, 0.82, 0.0), Color(1, 0.96, 0.82, 0.0)]))
		x += 460.0


# Lame di luce sottili che entrano dalle fessure tra le assi del pollaio
func _fasci_fessure():
	var x := 260.0
	while x < larghezza - 600:
		for d in [0.0, 46.0]:
			var a: float = x + d
			draw_polygon(PoolVector2Array([Vector2(a, 0), Vector2(a + 12, 0), Vector2(a + 150, 640), Vector2(a + 110, 640)]),
					PoolColorArray([Color(1, 0.94, 0.75, 0.2), Color(1, 0.94, 0.75, 0.2), Color(1, 0.94, 0.75, 0.0), Color(1, 0.94, 0.75, 0.0)]))
		x += 720.0


func _siepi():
	# siepi tonde e fiori, appena dietro lo steccato
	var punti := PoolVector2Array()
	var x := 0.0
	while x <= larghezza + 0.1:
		var y: float = 585.0 - 20.0 * abs(sin(TAU * x * 12 / larghezza)) - 8.0 * (0.5 + 0.5 * sin(TAU * x * 3 / larghezza))
		punti.append(Vector2(x, y))
		x += 12.0
	punti.append(Vector2(larghezza, 760))
	punti.append(Vector2(0, 760))
	draw_colored_polygon(punti, Color("5aa63c"))
	var rng := RandomNumberGenerator.new()
	rng.seed = 5
	for i in range(40):
		var fx := rng.randf_range(10, larghezza - 10)
		var fiore: Color = [Color.white, Color("ffd84a"), Color("ff9ec0")][i % 3]
		_tondo(Vector2(fx, rng.randf_range(588, 630)), 3.5, fiore, 8)


# Il prato fiorito lontano (al posto delle siepi): un'onda d'erba chiara piena di fiori di tanti colori
func _prato_fiori():
	var punti := PoolVector2Array()
	var x := 0.0
	while x <= larghezza + 0.1:
		var y: float = 596.0 - 12.0 * (0.5 + 0.5 * sin(TAU * x * 4 / larghezza)) - 6.0 * (0.5 + 0.5 * sin(TAU * x * 11 / larghezza + 1.0))
		punti.append(Vector2(x, y))
		x += 12.0
	punti.append(Vector2(larghezza, 760))
	punti.append(Vector2(0, 760))
	draw_colored_polygon(punti, Color("8ccf5c"))
	var rng := RandomNumberGenerator.new()
	rng.seed = 11
	var colori := [Color.white, Color("ffd84a"), Color("ff9ec0"), Color("b48cf2"), Color("ff7a6a")]
	for i in range(90):
		var fx := rng.randf_range(8, larghezza - 8)
		_tondo(Vector2(fx, rng.randf_range(592, 640)), rng.randf_range(3.0, 5.0), colori[i % colori.size()], 8)

