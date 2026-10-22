extends Area2D
# Chicco di mais da raccogliere: ondeggia su e giù, sparisce con un "pop" quando il pulcino lo prende.

const Effetti = preload("res://scripts/effetti.gd")
const Parti = preload("res://scripts/parti.gd")
const IMMAGINE = preload("res://assets/grafica/oggetti/chicco.svg")

export var ampiezza_ondeggio := 4.0  # quanto sale e scende (pixel)

var tempo := 0.0
var raccolto := false
var disegno: Sprite


func _ready():
	add_to_group("chicchi")
	tempo = position.x * 0.01  # così non ondeggiano tutti insieme
	var cerchio := CircleShape2D.new()
	cerchio.radius = 16
	var forma := CollisionShape2D.new()
	forma.shape = cerchio
	add_child(forma)
	disegno = Parti.crea(self, IMMAGINE, Vector2(15, 19), Vector2.ZERO)
	connect("body_entered", self, "_on_body_entered")


func _process(delta):
	tempo += delta
	disegno.position.y = sin(tempo * 3.0) * ampiezza_ondeggio
	disegno.rotation = sin(tempo * 2.0) * 0.15


func _on_body_entered(corpo):
	if raccolto or not corpo.is_in_group("pulcino"):
		return
	raccolto = true
	get_tree().call_group("livello", "chicco_raccolto")
	Suoni.suona("chicco", 0.12)
	Effetti.sbuffo(get_parent(), position, Color(1.0, 0.9, 0.3), 10, 160.0)
	# Pop: si gonfia e svanisce
	var tween := Tween.new()
	add_child(tween)
	tween.interpolate_property(self, "scale", Vector2.ONE, Vector2(2.2, 2.2), 0.25, Tween.TRANS_BACK, Tween.EASE_OUT)
	tween.interpolate_property(self, "modulate", Color(1, 1, 1, 1), Color(1, 1, 1, 0), 0.25)
	tween.start()
	yield(tween, "tween_all_completed")
	queue_free()
