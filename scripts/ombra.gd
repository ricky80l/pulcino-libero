extends Node2D
# Ombra morbida a terra sotto un personaggio (la sposta atmosfera.gd).

var larghezza := 22.0


func _draw():
	for i in range(3):
		var k := 1.0 - i * 0.22
		draw_set_transform(Vector2.ZERO, 0, Vector2(1.0, 0.28))
		draw_circle(Vector2.ZERO, larghezza * k, Color(0.12, 0.2, 0.05, 0.12))
	draw_set_transform(Vector2.ZERO, 0, Vector2.ONE)
