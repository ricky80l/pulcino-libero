extends Area2D
# Nido di paglia: punto sicuro. Quando il pulcino ci passa si illumina e diventa il punto di ripartenza.
# La posizione è il centro del nido, appoggiato a terra.

const Parti = preload("res://scripts/parti.gd")
const NIDO = preload("res://assets/grafica/oggetti/nido.svg")
const NIDO_ACCESO = preload("res://assets/grafica/oggetti/nido_acceso.svg")
const BAGLIORE = preload("res://assets/grafica/oggetti/bagliore.svg")

var acceso := false
var tempo := 0.0
var bagliore: Sprite
var disegno: Sprite


func _ready():
	add_to_group("nidi")
	bagliore = Parti.crea(self, BAGLIORE, Vector2(80, 80), Vector2(0, -14))
	bagliore.visible = false
	disegno = Parti.crea(self, NIDO, Vector2(70, 56), Vector2.ZERO)
	var rettangolo := RectangleShape2D.new()
	# Zona alta: vale anche se il pulcino ci passa sopra saltando
	rettangolo.extents = Vector2(32, 220)
	var forma := CollisionShape2D.new()
	forma.shape = rettangolo
	forma.position = Vector2(0, -220)
	add_child(forma)
	connect("body_entered", self, "_on_body_entered")


func _on_body_entered(corpo):
	if corpo.is_in_group("pulcino") and not acceso:
		get_tree().call_group("livello", "nido_raggiunto", self)


func accendi():
	acceso = true
	_aggiorna()
	Suoni.suona("nido", 0.0)
	# piccolo saltello di gioia del nido
	var tween := Tween.new()
	add_child(tween)
	tween.interpolate_property(self, "scale", Vector2(1.4, 0.7), Vector2.ONE, 0.5, Tween.TRANS_ELASTIC, Tween.EASE_OUT)
	tween.start()
	yield(tween, "tween_all_completed")
	tween.queue_free()


func spegni():
	acceso = false
	_aggiorna()


func _aggiorna():
	disegno.texture = NIDO_ACCESO if acceso else NIDO
	bagliore.visible = acceso


func _process(delta):
	# il bagliore del nido acceso "respira"
	if acceso:
		tempo += delta
		var r := 0.5 * (1.0 + sin(tempo * 3.0) * 0.08)
		bagliore.scale = Vector2(r, r)
