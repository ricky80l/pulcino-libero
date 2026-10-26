extends Node2D
# Mappa della fattoria vista dall'alto: un sentiero collega i dieci luoghi del viaggio.
# Il pulcino cammina sul sentiero; i luoghi non ancora sbloccati sono nella nebbia.
# Telefono: tocca un luogo per andarci, toccalo di nuovo per entrare. PC: frecce e spazio.

const Stile = preload("res://scripts/stile.gd")
const FONT_TITOLO = preload("res://assets/font/fredoka_messaggio.tres")
const FONT_CARTELLI = preload("res://assets/font/fredoka_piccolo.tres")
const NEBBIA = preload("res://assets/grafica/mappa/nebbia.svg")
const FARFALLA = preload("res://scripts/farfalla.gd")
const PULCINO = preload("res://scripts/pulcino_mappa.gd")

const DISEGNI := ["pollaio", "cortile", "orto", "prato", "bosco", "stagno", "collina", "grotta", "paese", "campanile"]
# dove sta ogni luogo (base del disegno, sul sentiero)
const POSIZIONI := [
	Vector2(150, 640), Vector2(380, 600), Vector2(620, 650), Vector2(860, 600), Vector2(1100, 640),
	Vector2(1130, 420), Vector2(880, 380), Vector2(630, 410), Vector2(390, 330), Vector2(640, 190),
]
const FIUME := [Vector2(1300, 110), Vector2(1235, 170), Vector2(1245, 255), Vector2(1195, 330), Vector2(1160, 380)]

const VELOCITA_PASSO := 260.0  # quanto in fretta cammina il pulcino sul sentiero

var sentiero := Curve2D.new()
var distanze := []  # punto del sentiero di ogni luogo
var cartelli := []
var nebbie := []
var alberi := []
var pulcino: Node2D
var luogo_attuale := 1
var meta := 1
var distanza_pulcino := 0.0
var nuvole := []
var tempo := 0.0


func _ready():
	# la nebbia si dirada solo sui luoghi già costruiti (gli altri sono "in arrivo")
	var ultimo := Progressi.ultimo_giocabile()
	if Progressi.nebbia_vista > ultimo:
		Progressi.nebbia_vista = ultimo
	_prepara_sentiero()
	_prepara_alberi()
	for i in range(DISEGNI.size()):
		_crea_luogo(i + 1)
	_crea_titolo_e_aiuto()
	for c in [Vector2(820, 520), Vector2(300, 470), Vector2(960, 300)]:
		var f := Node2D.new()
		f.set_script(FARFALLA)
		f.position = c
		add_child(f)
	_colora_farfalle()

	pulcino = PULCINO.new()
	add_child(pulcino)
	luogo_attuale = int(clamp(Progressi.ultimo_giocato, 1, ultimo))
	meta = luogo_attuale
	distanza_pulcino = distanze[luogo_attuale - 1]
	pulcino.position = sentiero.interpolate_baked(distanza_pulcino)

	_crea_nuvole()
	_aggiorna_cartelli()
	update()

	# Luoghi appena sbloccati e già costruiti: la nebbia si dirada e il pulcino ci va da solo
	if ultimo > Progressi.nebbia_vista:
		yield(get_tree().create_timer(0.8), "timeout")
		for n in range(Progressi.nebbia_vista + 1, ultimo + 1):
			_dirada_nebbia(n)
		Progressi.nebbia_vista = ultimo
		Progressi.salva()
		yield(get_tree().create_timer(0.9), "timeout")
		_vai_a(ultimo)


func _colora_farfalle():
	var colori := [Color("ff9ec0"), Color("ffd84a"), Color("b48cf2")]
	var i := 0
	for figlio in get_children():
		if figlio.get_script() == FARFALLA:
			figlio.colore = colori[i % colori.size()]
			i += 1


# ---------------- preparazione ----------------

func _prepara_sentiero():
	for i in range(POSIZIONI.size()):
		var p: Vector2 = POSIZIONI[i]
		var prima: Vector2 = POSIZIONI[int(max(i - 1, 0))]
		var dopo: Vector2 = POSIZIONI[int(min(i + 1, POSIZIONI.size() - 1))]
		var tangente := (dopo - prima) * 0.3
		sentiero.add_point(p, -tangente, tangente)
	sentiero.bake_interval = 6.0
	for p in POSIZIONI:
		distanze.append(sentiero.get_closest_offset(p))


func _prepara_alberi():
	# alberi sparsi lontano dal sentiero, dai luoghi, dal fiume e dal titolo
	var rng := RandomNumberGenerator.new()
	rng.seed = 2024
	var punti := sentiero.get_baked_points()
	var tentativi := 0
	while alberi.size() < 24 and tentativi < 600:
		tentativi += 1
		var a := Vector2(rng.randf_range(30, 1250), rng.randf_range(110, 700))
		if a.x < 480 and a.y < 110:  # sotto il titolo
			continue
		var libero := true
		for p in punti:
			if a.distance_to(p) < 60:
				libero = false
				break
		for p in POSIZIONI:
			if libero and (a.distance_to(p + Vector2(0, -45)) < 110):
				libero = false
		for p in FIUME:
			if libero and a.distance_to(p) < 70:
				libero = false
		for b in alberi:
			if libero and a.distance_to(b) < 70:
				libero = false
		if libero:
			alberi.append(a)
	alberi.sort_custom(self, "_piu_in_alto")


func _piu_in_alto(a, b):
	return a.y < b.y


func _crea_luogo(numero: int):
	var base: Vector2 = POSIZIONI[numero - 1]
	var disegno := Sprite.new()
	disegno.texture = load("res://assets/grafica/mappa/%s.svg" % DISEGNI[numero - 1])
	disegno.centered = false
	disegno.offset = Vector2(-120, -190)
	disegno.scale = Vector2(0.5, 0.5)
	disegno.position = base
	add_child(disegno)

	var cartello := Label.new()
	cartello.add_font_override("font", FONT_CARTELLI)
	cartello.add_color_override("font_color", Stile.CREMA)
	cartello.align = Label.ALIGN_CENTER
	cartello.rect_size = Vector2(200, 0)
	cartello.rect_position = base + Vector2(-100, -186)
	add_child(cartello)
	cartelli.append(cartello)

	var nebbia := Sprite.new()
	nebbia.texture = NEBBIA
	nebbia.scale = Vector2(0.62, 0.62)
	nebbia.position = base + Vector2(0, -52)
	nebbia.visible = numero > Progressi.nebbia_vista or not Progressi.costruito(numero)
	add_child(nebbia)
	nebbie.append(nebbia)


func _crea_titolo_e_aiuto():
	var titolo := Label.new()
	titolo.text = "Il Pulcino Libero"
	titolo.add_font_override("font", FONT_TITOLO)
	titolo.add_color_override("font_color", Stile.CREMA)
	titolo.add_stylebox_override("normal", _tavola(Stile.CONTORNO, 4))
	titolo.rect_position = Vector2(20, 14)
	add_child(titolo)

	var aiuto := Label.new()
	aiuto.text = "Tocca un luogo per andarci, toccalo di nuovo per entrare"
	aiuto.add_font_override("font", FONT_CARTELLI)
	aiuto.add_color_override("font_color", Stile.CREMA)
	aiuto.add_stylebox_override("normal", _tavola(Stile.CONTORNO, 3))
	aiuto.rect_position = Vector2(270, 672)
	add_child(aiuto)

	var crediti := Button.new()
	crediti.text = "Crediti"
	crediti.focus_mode = Control.FOCUS_NONE  # non ruba le frecce al pulcino
	crediti.rect_position = Vector2(1120, 16)
	crediti.rect_min_size = Vector2(140, 56)
	Stile.pulsante_legno(crediti, FONT_CARTELLI)
	crediti.connect("pressed", get_tree(), "change_scene", ["res://scenes/crediti.tscn"])
	add_child(crediti)


func _crea_nuvole():
	for i in range(3):
		var n := Sprite.new()
		n.texture = NEBBIA
		n.scale = Vector2(0.4, 0.4)
		n.modulate = Color(1, 1, 1, 0.7)
		n.position = Vector2(200 + i * 480, 70 + i * 40)
		add_child(n)
		nuvole.append(n)


func _tavola(bordo: Color, spessore: int) -> StyleBoxFlat:
	var s := Stile.riquadro(Stile.LEGNO, bordo, spessore)
	s.set_corner_radius_all(12)
	s.content_margin_left = 12
	s.content_margin_right = 12
	s.content_margin_top = 4
	s.content_margin_bottom = 6
	return s


func _aggiorna_cartelli():
	for i in range(cartelli.size()):
		var numero := i + 1
		var cartello: Label = cartelli[i]
		cartello.visible = numero <= Progressi.sbloccato and not nebbie[i].visible
		var testo: String = Progressi.LIVELLI[i]["nome"]
		if Progressi.finito(numero):
			var r: Dictionary = Progressi.record[str(numero)]
			testo += "\n%d / %d" % [int(r["presi"]), int(r["totale"])]
		else:
			testo += "\nnuovo!"
		cartello.text = testo
		# il cartello del luogo dove sta il pulcino è evidenziato
		if numero == luogo_attuale:
			cartello.add_stylebox_override("normal", _tavola(Color("ffd84a"), 5))
		else:
			cartello.add_stylebox_override("normal", _tavola(Stile.CONTORNO, 3))
		# ricalcola l'altezza: con due righe il cartello deve crescere
		cartello.rect_size = Vector2(200, 0)


# ---------------- disegno del paesaggio ----------------

func _draw():
	var rng := RandomNumberGenerator.new()
	rng.seed = 7
	draw_rect(Rect2(0, 0, 1280, 720), Color("a8d977"))
	# chiazze di prato più chiare e più scure
	for i in range(18):
		var c := Vector2(rng.randf_range(0, 1280), rng.randf_range(0, 720))
		var col := Color("b6e086") if i % 2 == 0 else Color("97cb66")
		_ellisse(c, Vector2(rng.randf_range(60, 140), rng.randf_range(25, 50)), col)
	# fiorellini
	for i in range(70):
		var c := Vector2(rng.randf_range(0, 1280), rng.randf_range(100, 720))
		var col: Color = [Color("ffffff"), Color("ffd84a"), Color("ff9ec0")][i % 3]
		draw_circle(c, 2.5, col)
	# fiume che finisce nello stagno
	var fiume := PoolVector2Array(FIUME)
	draw_polyline(fiume, Color("2f7faf"), 34.0, true)
	draw_polyline(fiume, Color("5db4e3"), 26.0, true)
	draw_polyline(fiume, Color("8fd0f2"), 6.0, true)
	# sentiero: la parte già sbloccata è piena, il resto più pallido
	var punti := sentiero.get_baked_points()
	var fine_sbloccata: float = distanze[Progressi.ultimo_giocabile() - 1]
	var aperto := PoolVector2Array()
	var chiuso := PoolVector2Array()
	for i in range(punti.size()):
		if i * sentiero.bake_interval <= fine_sbloccata + 1:
			aperto.append(punti[i])
		else:
			if chiuso.size() == 0 and aperto.size() > 0:
				chiuso.append(aperto[aperto.size() - 1])
			chiuso.append(punti[i])
	if chiuso.size() > 1:
		draw_polyline(chiuso, Color(0.79, 0.65, 0.42, 0.45), 30.0, true)
		draw_polyline(chiuso, Color(0.91, 0.8, 0.56, 0.45), 20.0, true)
	if aperto.size() > 1:
		draw_polyline(aperto, Color("c9a76a"), 30.0, true)
		draw_polyline(aperto, Color("e8cb8e"), 20.0, true)
	# alberi tondi
	for a in alberi:
		draw_rect(Rect2(a.x - 5, a.y - 6, 10, 22), Color("7a4e22"))
		_ellisse(a + Vector2(0, -18), Vector2(27, 27), Color("2f6b1a"))
		_ellisse(a + Vector2(0, -18), Vector2(23, 23), Color("4e9a2e"))
		_ellisse(a + Vector2(-7, -25), Vector2(8, 8), Color("7cc24e"))


func _ellisse(c: Vector2, r: Vector2, colore: Color):
	var punti := PoolVector2Array()
	for i in range(28):
		var a := i * TAU / 28
		punti.append(c + Vector2(cos(a) * r.x, sin(a) * r.y))
	draw_colored_polygon(punti, colore, PoolVector2Array(), null, null, true)


# ---------------- movimento e comandi ----------------

func _process(delta):
	tempo += delta
	# la nebbia ondeggia piano, le nuvole passano
	for i in range(nebbie.size()):
		var n: Sprite = nebbie[i]
		n.position.x = POSIZIONI[i].x + sin(tempo * 0.8 + i) * 4
	for n in nuvole:
		n.position.x += 14 * delta
		if n.position.x > 1400:
			n.position.x = -120

	# cammino verso la meta lungo il sentiero
	var obiettivo: float = distanze[meta - 1]
	if abs(obiettivo - distanza_pulcino) > 1.0:
		var verso := sign(obiettivo - distanza_pulcino)
		var prima: Vector2 = pulcino.position
		distanza_pulcino = move_toward(distanza_pulcino, obiettivo, VELOCITA_PASSO * delta)
		pulcino.position = sentiero.interpolate_baked(distanza_pulcino)
		pulcino.cammina(sign(pulcino.position.x - prima.x) if pulcino.position.x != prima.x else verso)
		if abs(obiettivo - distanza_pulcino) <= 1.0:
			_arrivato()
	else:
		pulcino.fermo()

	# tastiera: frecce per spostarsi, salto per entrare
	if Input.is_action_just_pressed("move_right"):
		_vai_a(meta + 1)
	elif Input.is_action_just_pressed("move_left"):
		_vai_a(meta - 1)
	elif Input.is_action_just_pressed("jump") or Input.is_action_just_pressed("ui_accept"):
		if meta == luogo_attuale and not _in_cammino():
			_entra(luogo_attuale)


func _in_cammino() -> bool:
	return abs(distanze[meta - 1] - distanza_pulcino) > 1.0


func _vai_a(numero: int):
	# si può andare solo dove la nebbia è (o sta per essere) diradata
	if not Progressi.giocabile(numero) or numero > Progressi.nebbia_vista:
		return
	meta = numero


func _arrivato():
	luogo_attuale = meta
	pulcino.fermo()
	pulcino.pigola()
	Suoni.suona("salto", 0.1, -6.0)
	_aggiorna_cartelli()


func _unhandled_input(evento):
	# tocco o clic su un luogo: vale il disegno e anche il suo cartello
	if evento is InputEventMouseButton and evento.pressed and evento.button_index == BUTTON_LEFT:
		var punto := get_global_mouse_position()
		for i in range(POSIZIONI.size()):
			var zona := Rect2(POSIZIONI[i] + Vector2(-75, -120), Vector2(150, 150))
			var cartello: Label = cartelli[i]
			var sul_cartello: bool = cartello.visible and cartello.get_global_rect().has_point(punto)
			if not zona.has_point(punto) and not sul_cartello:
				continue
			var numero := i + 1
			if nebbie[i].visible:
				_scuoti(nebbie[i])
			elif numero == luogo_attuale and not _in_cammino():
				_entra(numero)
			else:
				_vai_a(numero)
			get_tree().set_input_as_handled()
			return


func _entra(numero: int):
	if Progressi.LIVELLI[numero - 1]["scena"] == "":
		_scuoti(cartelli[numero - 1])  # il livello non c'è ancora
		Suoni.suona("squittio", 0.1, -4.0)
		return
	set_process(false)
	pulcino.pigola()
	Suoni.suona("salto")
	var tween := Tween.new()
	add_child(tween)
	tween.interpolate_property(pulcino, "position:y", pulcino.position.y, pulcino.position.y - 30, 0.15, Tween.TRANS_QUAD, Tween.EASE_OUT)
	tween.interpolate_property(pulcino, "position:y", pulcino.position.y - 30, pulcino.position.y, 0.15, Tween.TRANS_QUAD, Tween.EASE_IN, 0.15)
	tween.start()
	yield(tween, "tween_all_completed")
	Progressi.gioca(numero)


# piccola scossa: per la nebbia che non si apre e per i livelli che non ci sono ancora
func _scuoti(cosa):
	var tween := Tween.new()
	add_child(tween)
	var proprieta := "rect_position:x" if cosa is Control else "position:x"
	var x: float = cosa.rect_position.x if cosa is Control else cosa.position.x
	for k in range(4):
		var spinta := 6.0 if k % 2 == 0 else -6.0
		tween.interpolate_property(cosa, proprieta, x, x + spinta, 0.05, Tween.TRANS_SINE, Tween.EASE_IN_OUT, k * 0.05)
	tween.interpolate_property(cosa, proprieta, x, x, 0.01, Tween.TRANS_LINEAR, Tween.EASE_IN_OUT, 0.2)
	tween.start()
	yield(tween, "tween_all_completed")
	tween.queue_free()


func _dirada_nebbia(numero: int):
	var nebbia: Sprite = nebbie[numero - 1]
	Suoni.suona("nido", 0.0)
	var tween := Tween.new()
	add_child(tween)
	tween.interpolate_property(nebbia, "modulate:a", 1.0, 0.0, 1.2)
	tween.interpolate_property(nebbia, "scale", nebbia.scale, nebbia.scale * 1.6, 1.2, Tween.TRANS_QUAD, Tween.EASE_OUT)
	tween.start()
	yield(tween, "tween_all_completed")
	nebbia.visible = false
	nebbia.modulate.a = 1.0
	_aggiorna_cartelli()
	tween.queue_free()
