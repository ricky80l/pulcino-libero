extends Node2D
# L'autista del furgone del Maglificio Granada: moro, robusto, polo blu e jeans.
# Non lancia e non blocca: fa scena. Respira, si gratta la pancia, saluta, guarda l'orologio;
# quando il pulcino gli passa vicino fa un saltello di sorpresa con un "Ehi, pulcino!", poi indica il fiocco
# a maglia sul tetto del furgone ("Guarda!"): un indizio della pulcina (Tappa 24). Ogni tanto lo indica anche da solo.
# La posizione è tra i piedi, a terra; guarda verso sinistra (verso il furgone e il pulcino che arriva).

const Parti = preload("res://scripts/parti.gd")
const FONT = preload("res://assets/font/fredoka_piccolo.tres")
const Stile = preload("res://scripts/stile.gd")
const TESTA = preload("res://assets/grafica/autista/testa.png")
const CORPO = preload("res://assets/grafica/autista/corpo.png")
const BRACCIO = preload("res://assets/grafica/autista/braccio.png")
const GAMBA = preload("res://assets/grafica/autista/gamba.png")

export var verso := -1.0  # -1 = guarda a sinistra

var figura := Node2D.new()
var busto := Node2D.new()
var braccio_sx: Sprite
var braccio_dx: Sprite
var testa: Sprite
var fumetto: Label
var tempo := 0.0
var rng := RandomNumberGenerator.new()
var gesto := ""
var tempo_gesto := 0.0
var durata_gesto := 1.0
var prossimo_gesto := 1.0
var sorpreso := false  # già sorpreso per questo passaggio del pulcino
var pulcino = null


func _ready():
	rng.randomize()
	add_child(figura)
	figura.scale.x = -verso  # i disegni guardano a destra
	Parti.crea(figura, GAMBA, Vector2(24, 6), Vector2(-12, -60))
	Parti.crea(figura, GAMBA, Vector2(24, 6), Vector2(12, -60))
	busto.position = Vector2(0, -55)
	figura.add_child(busto)
	braccio_sx = Parti.crea(busto, BRACCIO, Vector2(22, 12), Vector2(-36, -52))
	braccio_dx = Parti.crea(busto, BRACCIO, Vector2(22, 12), Vector2(36, -52))
	Parti.crea(busto, CORPO, Vector2(85, 186), Vector2(0, 33))
	testa = Parti.crea(busto, TESTA, Vector2(60, 118), Vector2(0, -56))
	# le braccia davanti alla polo
	busto.move_child(braccio_sx, busto.get_child_count() - 1)
	busto.move_child(braccio_dx, busto.get_child_count() - 1)
	fumetto = Label.new()
	fumetto.text = "Ehi, pulcino!"
	fumetto.add_font_override("font", FONT)
	fumetto.add_color_override("font_color", Color("3a2616"))
	var sfondo := Stile.riquadro(Color.white, Color("3a2616"), 3)
	sfondo.set_corner_radius_all(14)
	sfondo.content_margin_left = 12
	sfondo.content_margin_right = 12
	fumetto.add_stylebox_override("normal", sfondo)
	fumetto.rect_position = Vector2(-90, -230)
	fumetto.visible = false
	add_child(fumetto)


func _process(delta):
	tempo += delta
	if pulcino == null:
		var trovati: Array = get_tree().get_nodes_in_group("pulcino")
		if not trovati.empty():
			pulcino = trovati[0]
	var sx := 0.0
	var dx := 0.0
	var su := sin(tempo * 1.5) * 1.5  # respira
	var testa_ang := 0.0
	var vicino: bool = pulcino != null and global_position.distance_to(pulcino.global_position) < 200
	if vicino and not sorpreso:
		sorpreso = true
		gesto = "sorpresa"
		durata_gesto = 1.4
		tempo_gesto = 0.0
		fumetto.visible = true
		Suoni.suona("squittio", 0.1, -6.0, 0.7)
	elif not vicino and pulcino != null and global_position.distance_to(pulcino.global_position) > 400:
		sorpreso = false
	if gesto == "":
		prossimo_gesto -= delta
		if prossimo_gesto <= 0:
			var scelte := ["pancia", "saluta", "orologio", "pancia", "indica"]
			var nuovo: String = scelte[rng.randi() % scelte.size()]
			gesto = nuovo
			durata_gesto = rng.randf_range(1.4, 2.2)
			tempo_gesto = 0.0
	else:
		tempo_gesto += delta
		var f: float = clamp(tempo_gesto / durata_gesto, 0.0, 1.0)
		var e := sin(PI * f)
		match gesto:
			"pancia":  # si gratta la pancia, soddisfatto (dopo pranzo)
				dx = 55.0 * e + sin(TAU * 4.0 * f) * 10.0 * e
				testa_ang = 4.0 * e
			"saluta":
				sx = 160.0 * e + sin(TAU * 2.0 * f) * 18.0 * e
			"orologio":
				dx = 95.0 * e
				testa_ang = 8.0 * e
			"indica":  # punta il braccio verso il furgone, dove c'è il fiocco rosa
				sx = 100.0 * min(1.0, f * 4.0) * min(1.0, (1.0 - f) * 4.0)
				testa_ang = -6.0 * e
			"sorpresa":  # saltello e braccia su
				sx = 120.0 * e
				dx = -120.0 * e
				su -= abs(sin(PI * 2.0 * f)) * 14.0
		if f >= 1.0:
			fumetto.visible = false
			if gesto == "sorpresa":
				# dopo la sorpresa indica il fiocco al pulcino
				gesto = "indica"
				durata_gesto = 2.0
				tempo_gesto = 0.0
				fumetto.text = "Guarda!"
				fumetto.visible = true
			else:
				gesto = ""
				prossimo_gesto = rng.randf_range(0.8, 2.0)
				fumetto.text = "Ehi, pulcino!"
	braccio_sx.rotation_degrees = 10.0 + sx
	braccio_dx.rotation_degrees = -10.0 + dx
	busto.position.y = -55 + su
	testa.rotation_degrees = testa_ang
