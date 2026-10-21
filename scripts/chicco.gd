extends Area2D
# Chicco di mais da raccogliere: ondeggia su e giù, sparisce con un "pop" quando il pulcino lo prende.

export var ampiezza_ondeggio := 4.0  # quanto sale e scende (pixel)

var tempo := 0.0
var raccolto := false


func _ready():
	add_to_group("chicchi")
	tempo = position.x * 0.01  # così non ondeggiano tutti insieme
	var cerchio := CircleShape2D.new()
	cerchio.radius = 16
	var forma := CollisionShape2D.new()
	forma.shape = cerchio
	add_child(forma)
	connect("body_entered", self, "_on_body_entered")


func _process(delta):
	tempo += delta
	update()


func _draw():
	var y := sin(tempo * 3.0) * ampiezza_ondeggio
	draw_set_transform(Vector2(0, y), 0, Vector2(0.75, 1.0))
	draw_circle(Vector2.ZERO, 11, Color(0.95, 0.75, 0.1))
	draw_circle(Vector2(-3, -4), 4, Color(1.0, 0.92, 0.55))  # riflesso
	draw_set_transform(Vector2.ZERO, 0, Vector2.ONE)


func _on_body_entered(corpo):
	if raccolto or not corpo.is_in_group("pulcino"):
		return
	raccolto = true
	get_tree().call_group("livello", "chicco_raccolto")
	# Pop: si gonfia e svanisce
	var tween := Tween.new()
	add_child(tween)
	tween.interpolate_property(self, "scale", Vector2.ONE, Vector2(2.2, 2.2), 0.25, Tween.TRANS_BACK, Tween.EASE_OUT)
	tween.interpolate_property(self, "modulate", Color(1, 1, 1, 1), Color(1, 1, 1, 0), 0.25)
	tween.start()
	yield(tween, "tween_all_completed")
	queue_free()
