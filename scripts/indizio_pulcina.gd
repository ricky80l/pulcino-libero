extends Node2D
# Indizio della pulcina misteriosa (Tappa 24): la sua piuma, le sue impronte, il suo filo rosa o il suo fiocco a maglia.
# Tutto quello che è suo è crema e rosa e luccica piano di rosa: così si capisce che non è messo lì a caso.
# Quando il pulcino ci passa vicino la prima volta, frena un attimo, gli spunta un «?» rosa e fa un «pio?» curioso.
# La piuma si trova sempre vicino all'uscita: toccandola vola via in un luccichio (conta solo finendo il livello).
# La posizione è la base dell'indizio (per le impronte: la prima orma, a terra).

const Parti = preload("res://scripts/parti.gd")
const Effetti = preload("res://scripts/effetti.gd")
const PIUMA = preload("res://assets/grafica/pulcina/piuma.png")
const IMPRONTA = preload("res://assets/grafica/pulcina/impronta.png")
const FILO = preload("res://assets/grafica/pulcina/filo.png")
const FIOCCO = preload("res://assets/grafica/pulcina/fiocco_maglia.png")
const BAGLIORE = preload("res://assets/grafica/oggetti/bagliore.png")
const FONT = preload("res://assets/font/fredoka_messaggio.tres")

const ROSA := Color(1.0, 0.62, 0.76)

export var cosa := "piuma"  # "piuma", "impronte", "filo" o "fiocco"
export var grandezza := 1.0  # la piuma è sempre più grande di luogo in luogo
export var numero_impronte := 6
export var passo_impronte := 46.0
export var raggio_curiosita := 190.0  # da quanto vicino il pulcino se ne accorge

var disegno: Node2D = Node2D.new()  # tutto il disegno dell'indizio (dondola, nel caso della piuma)
var alone: Sprite
var centro := Vector2.ZERO  # dove sta il cuore del disegno, rispetto alla base
var tempo := 0.0
var prossima_scintilla := 0.5
var pulcino = null
var presa := false


func _ready():
	add_to_group("indizio_pulcina")
	if cosa == "piuma":
		add_to_group("piuma_pulcina")
	tempo = position.x * 0.01
	alone = Parti.crea(self, BAGLIORE, Vector2(BAGLIORE.get_width() / 2.0, BAGLIORE.get_height() / 2.0), Vector2.ZERO)
	alone.modulate = Color(ROSA.r, ROSA.g, ROSA.b, 0.6)
	add_child(disegno)
	match cosa:
		"piuma":
			Parti.crea(disegno, PIUMA, Vector2(35, 146), Vector2.ZERO)
			disegno.scale = Vector2(grandezza, grandezza)
			centro = Vector2(0, -40 * grandezza)
		"impronte":  # stampate nella terra davanti, in fila verso destra
			for k in range(numero_impronte):
				var orma: Sprite = Parti.crea(disegno, IMPRONTA, Vector2(18, 15), Vector2(k * passo_impronte, -4 if k % 2 == 0 else 4))
				orma.scale *= 0.85
			centro = Vector2((numero_impronte - 1) * passo_impronte / 2.0, -6)
			alone.scale = Vector2(numero_impronte * 0.6, 0.5) * Parti.SCALA
		"filo":
			Parti.crea(disegno, FILO, Vector2(70, 22), Vector2.ZERO)
			disegno.scale = Vector2(grandezza, grandezza)
		"fiocco":
			Parti.crea(disegno, FIOCCO, Vector2(60, 40), Vector2.ZERO)
			disegno.scale = Vector2(grandezza, grandezza)
	alone.position = centro


func _process(delta):
	if presa:
		return
	tempo += delta
	if cosa == "piuma":
		# la piuma ondeggia come se ci soffiasse un filo d'aria
		disegno.rotation = sin(tempo * 1.7) * 0.18
		disegno.position.y = sin(tempo * 2.3) * 2.0
	if cosa != "impronte":
		alone.scale = Vector2.ONE * Parti.SCALA * (0.9 + sin(tempo * 2.6) * 0.12)
	prossima_scintilla -= delta
	if prossima_scintilla <= 0:
		prossima_scintilla = rand_range(0.7, 1.4)
		var dove := position + centro + Vector2(rand_range(-16, 16), rand_range(-14, 6))
		if cosa == "impronte":
			dove = position + Vector2(rand_range(0, (numero_impronte - 1) * passo_impronte), -10)
		Effetti.sbuffo(get_parent(), dove, ROSA.lightened(0.3), 3, 36.0)
	if pulcino == null or not is_instance_valid(pulcino):
		var trovati: Array = get_tree().get_nodes_in_group("pulcino")
		if trovati.empty():
			return
		pulcino = trovati[0]
	var vicino: Vector2 = pulcino.global_position - (global_position + centro)
	if vicino.length() < raggio_curiosita:
		_curiosita()
	if cosa == "piuma" and vicino.length() < 46:
		_prendi()


# «?» rosa sopra la testa del pulcino e un «pio?» curioso: una volta sola per livello
func _curiosita():
	var livello = get_parent()
	while livello and not livello.is_in_group("livello"):
		livello = livello.get_parent()
	if livello == null or livello.has_meta("curiosita_pulcina"):
		return
	livello.set_meta("curiosita_pulcina", true)
	Suoni.suona("curioso", 0.04, -3.0)
	if pulcino.get("aspetto") != null:
		pulcino.aspetto.pigola()
	if pulcino.is_on_floor() and pulcino.get("velocita") != null:
		pulcino.velocita.x *= 0.15  # frena un istante, come per guardare meglio
	mostra_domanda(pulcino, Vector2(0, -78))


# Il «?» rosa: lo usa anche la mappa
static func mostra_domanda(sopra: Node, dove: Vector2):
	var porta := Node2D.new()
	porta.position = dove
	porta.z_index = 10
	var punto := Label.new()
	punto.text = "?"
	punto.add_font_override("font", FONT)
	punto.add_color_override("font_color", Color(1.0, 0.58, 0.74))
	punto.rect_position = Vector2(-16, -34)
	punto.rect_pivot_offset = Vector2(16, 34)
	porta.add_child(punto)
	sopra.add_child(porta)
	var tween := Tween.new()
	porta.add_child(tween)
	tween.interpolate_property(punto, "rect_scale", Vector2(0.2, 0.2), Vector2.ONE, 0.35, Tween.TRANS_BACK, Tween.EASE_OUT)
	tween.interpolate_property(punto, "rect_rotation", -18.0, 8.0, 0.35, Tween.TRANS_BACK, Tween.EASE_OUT)
	tween.interpolate_property(porta, "position:y", dove.y, dove.y - 10, 1.0, Tween.TRANS_SINE, Tween.EASE_IN_OUT, 0.35)
	tween.interpolate_property(punto, "modulate:a", 1.0, 0.0, 0.4, Tween.TRANS_LINEAR, Tween.EASE_IN, 1.3)
	tween.start()
	tween.connect("tween_all_completed", porta, "queue_free")


# La piuma vola via in un luccichio rosa (il livello la conta solo arrivando all'uscita)
func _prendi():
	presa = true
	_curiosita()
	Suoni.suona("piuma", 0.0, -2.0)
	Effetti.sbuffo(get_parent(), position + centro, ROSA, 18, 170.0)
	Effetti.sbuffo(get_parent(), position + centro, Color(1, 0.95, 0.88), 10, 110.0)
	var tween := Tween.new()
	add_child(tween)
	tween.interpolate_property(disegno, "position", disegno.position, Vector2(0, -70), 0.9, Tween.TRANS_SINE, Tween.EASE_OUT)
	tween.interpolate_property(disegno, "rotation", disegno.rotation, 2.6, 0.9, Tween.TRANS_SINE, Tween.EASE_OUT)
	tween.interpolate_property(self, "modulate:a", 1.0, 0.0, 0.5, Tween.TRANS_LINEAR, Tween.EASE_IN, 0.45)
	tween.start()
	yield(tween, "tween_all_completed")
	visible = false
