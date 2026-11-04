extends CanvasLayer
# La bancarella, aperta dal pulsante sulla mappa: si spendono i chicchi del borsellino per gli accessori.
# Ferma la mappa finché è aperta. A sinistra il pulcino che prova gli accessori, a destra le cose in vendita.

const Stile = preload("res://scripts/stile.gd")
const ACCESSORI = preload("res://scripts/accessori.gd")
const PULCINO = preload("res://scripts/pulcino_mappa.gd")
const BANCARELLA = preload("res://assets/grafica/mappa/bancarella.png")
const CHICCO = preload("res://assets/grafica/oggetti/chicco.png")
const FONT_TITOLO = preload("res://assets/font/fredoka_messaggio.tres")
const FONT = preload("res://assets/font/fredoka_piccolo.tres")

var borsellino: Label
var avviso: Label
var pulsanti := {}  # accessorio -> pulsante Compra / Indossa / Togli
var schede := {}
var manichino: Node2D  # il pulcino che prova gli accessori


func apri():
	layer = 4
	pause_mode = Node.PAUSE_MODE_PROCESS
	get_tree().paused = true

	var velo := ColorRect.new()
	velo.color = Color(0, 0, 0, 0.55)
	velo.rect_size = Vector2(1280, 720)
	add_child(velo)
	var pannello := Panel.new()
	var stile := Stile.riquadro(Stile.LEGNO, Stile.CONTORNO, 6)
	pannello.add_stylebox_override("panel", stile)
	pannello.rect_position = Vector2(70, 50)
	pannello.rect_size = Vector2(1140, 620)
	add_child(pannello)

	var titolo := _scritta("La bancarella", FONT_TITOLO, Color("ffd84a"))
	titolo.rect_position = Vector2(110, 62)
	add_child(titolo)
	# borsellino
	var icona := TextureRect.new()
	icona.texture = CHICCO
	icona.expand = true
	icona.rect_size = Vector2(26, 33)
	icona.rect_position = Vector2(960, 76)
	add_child(icona)
	borsellino = _scritta("", FONT_TITOLO, Stile.CREMA)
	borsellino.rect_position = Vector2(994, 62)
	add_child(borsellino)

	# a sinistra: la bancarella disegnata e il pulcino che prova gli accessori
	var disegno := TextureRect.new()
	disegno.texture = BANCARELLA
	disegno.expand = true
	disegno.rect_size = Vector2(240, 200)
	disegno.rect_position = Vector2(110, 160)
	add_child(disegno)
	manichino = PULCINO.new()
	manichino.scale = Vector2(2.2, 2.2)
	manichino.position = Vector2(230, 560)
	add_child(manichino)

	# a destra: le schede degli accessori
	for i in range(ACCESSORI.ORDINE.size()):
		var nome: String = ACCESSORI.ORDINE[i]
		_scheda(nome, Vector2(400 + (i % 3) * 260, 140 + int(i / 3) * 250))

	avviso = _scritta("", FONT, Color("ffd84a"))
	avviso.rect_position = Vector2(400, 610)
	add_child(avviso)
	var chiudi := Button.new()
	chiudi.text = "Chiudi"
	chiudi.rect_position = Vector2(990, 600)
	chiudi.rect_min_size = Vector2(190, 56)
	Stile.pulsante_legno(chiudi, FONT)
	chiudi.connect("pressed", self, "chiudi")
	add_child(chiudi)
	_aggiorna()


func _scheda(nome: String, posizione: Vector2):
	var a: Dictionary = ACCESSORI.ELENCO[nome]
	var scheda := Panel.new()
	scheda.add_stylebox_override("panel", Stile.riquadro(Color("d9b07a"), Stile.CONTORNO, 4))
	scheda.rect_position = posizione
	scheda.rect_size = Vector2(240, 230)
	add_child(scheda)
	schede[nome] = scheda
	var immagine := TextureRect.new()
	immagine.texture = a["immagine"]
	immagine.expand = true
	immagine.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	immagine.rect_position = Vector2(50, 12)
	immagine.rect_size = Vector2(140, 80)
	scheda.add_child(immagine)
	var etichetta := _scritta(a["nome"], FONT, Color("3a2616"))
	etichetta.align = Label.ALIGN_CENTER
	etichetta.rect_position = Vector2(0, 96)
	etichetta.rect_size = Vector2(240, 30)
	scheda.add_child(etichetta)
	var prezzo := _scritta("%d chicchi" % a["prezzo"], FONT, Color("6a4a10"))
	prezzo.align = Label.ALIGN_CENTER
	prezzo.rect_position = Vector2(0, 128)
	prezzo.rect_size = Vector2(240, 30)
	scheda.add_child(prezzo)
	var pulsante := Button.new()
	pulsante.rect_position = Vector2(30, 166)
	pulsante.rect_min_size = Vector2(180, 50)
	Stile.pulsante_legno(pulsante, FONT)
	pulsante.connect("pressed", self, "_premuto", [nome])
	scheda.add_child(pulsante)
	pulsanti[nome] = pulsante


func _premuto(nome: String):
	var a: Dictionary = ACCESSORI.ELENCO[nome]
	var posto: String = a["posto"]
	if not Progressi.comprati.has(nome):
		if Progressi.compra(nome, a["prezzo"]):
			Progressi.indossa(nome, posto)
			Suoni.suona("fine", 0.0, -4.0)
			avviso.text = "Comprato! Ora il pulcino lo indossa."
		else:
			Suoni.suona("squittio", 0.1, -4.0)
			avviso.text = "Servono ancora %d chicchi: raccoglili nei livelli!" % (a["prezzo"] - Progressi.borsellino)
			_scuoti(schede[nome])
	elif Progressi.indossati.get(posto, "") == nome:
		Progressi.togli(posto)
		avviso.text = ""
	else:
		Progressi.indossa(nome, posto)
		Suoni.suona("becco", 0.1, -4.0)
		avviso.text = ""
	_aggiorna()


func _aggiorna():
	borsellino.text = str(Progressi.borsellino)
	for nome in pulsanti:
		var a: Dictionary = ACCESSORI.ELENCO[nome]
		if not Progressi.comprati.has(nome):
			pulsanti[nome].text = "Compra"
		elif Progressi.indossati.get(a["posto"], "") == nome:
			pulsanti[nome].text = "Togli"
		else:
			pulsanti[nome].text = "Indossa"
	if manichino and manichino.aspetto:
		manichino.aspetto.aggiorna_accessori()
	# anche il pulcino sulla mappa, sotto la bancarella
	for p in get_tree().get_nodes_in_group("pulcino_mappa"):
		p.aspetto.aggiorna_accessori()


func chiudi():
	get_tree().paused = false
	queue_free()


func _scritta(testo: String, font: Font, colore: Color) -> Label:
	var l := Label.new()
	l.text = testo
	l.add_font_override("font", font)
	l.add_color_override("font_color", colore)
	return l


func _scuoti(cosa: Control):
	var tween := Tween.new()
	tween.pause_mode = Node.PAUSE_MODE_PROCESS
	add_child(tween)
	var x := cosa.rect_position.x
	for k in range(4):
		tween.interpolate_property(cosa, "rect_position:x", x, x + (8 if k % 2 == 0 else -8), 0.05, Tween.TRANS_SINE, Tween.EASE_IN_OUT, k * 0.05)
	tween.interpolate_property(cosa, "rect_position:x", x, x, 0.01, Tween.TRANS_LINEAR, Tween.EASE_IN_OUT, 0.2)
	tween.start()
