extends Area2D
# Nido di paglia: punto sicuro. Quando il pulcino ci passa si illumina e diventa il punto di ripartenza.
# La posizione è il centro del nido, appoggiato a terra.

var acceso := false


func _ready():
	add_to_group("nidi")
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
	update()


func spegni():
	acceso = false
	update()


func _draw():
	if acceso:
		draw_circle(Vector2(0, -14), 44, Color(1.0, 0.95, 0.5, 0.45))  # bagliore
	var paglia := Color(0.95, 0.8, 0.35) if acceso else Color(0.75, 0.6, 0.3)
	var scuro := Color(0.6, 0.45, 0.2) if acceso else Color(0.5, 0.38, 0.18)
	# conca del nido: mezza ellisse
	draw_set_transform(Vector2(0, -10), 0, Vector2(1.0, 0.45))
	draw_circle(Vector2.ZERO, 32, scuro)
	draw_set_transform(Vector2.ZERO, 0, Vector2.ONE)
	draw_rect(Rect2(-32, -24, 64, 14), paglia)
	# fili di paglia
	for i in range(7):
		var x := -28 + i * 9
		draw_line(Vector2(x, -26), Vector2(x + 6, -12), scuro, 2.0)
