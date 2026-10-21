tool
extends StaticBody2D
# Pezzo segnaposto del livello: si disegna da solo e crea la sua collisione.
# La posizione è l'angolo in alto a sinistra.

enum Tipo { PAVIMENTO, LEGNO, CASSETTA, MANGIATOIA, POSATOIO, SBARRE, PARETE, RETE }

export(Tipo) var tipo := Tipo.LEGNO setget _set_tipo  # aspetto del pezzo
export var dimensioni := Vector2(100, 40) setget _set_dimensioni  # larghezza e altezza in pixel
export var solido := true  # false = solo decorazione, ci si passa attraverso
export var attraversabile_da_sotto := false  # true = ci salti sopra passando da sotto


func _ready():
	if Engine.editor_hint or not solido:
		return
	var rettangolo := RectangleShape2D.new()
	rettangolo.extents = dimensioni / 2
	var forma := CollisionShape2D.new()
	forma.shape = rettangolo
	forma.position = dimensioni / 2
	forma.one_way_collision = attraversabile_da_sotto
	add_child(forma)


func _set_tipo(valore):
	tipo = valore
	update()


func _set_dimensioni(valore):
	dimensioni = valore
	update()


func _draw():
	var r := Rect2(Vector2.ZERO, dimensioni)
	var w := dimensioni.x
	var h := dimensioni.y
	match tipo:
		Tipo.PAVIMENTO:
			draw_rect(r, Color(0.55, 0.4, 0.2))
			draw_rect(Rect2(0, 0, w, 10), Color(0.88, 0.78, 0.38))  # paglia
		Tipo.LEGNO:
			draw_rect(r, Color(0.6, 0.42, 0.22))
			draw_rect(r, Color(0.4, 0.27, 0.13), false, 3.0)
		Tipo.CASSETTA:
			draw_rect(r, Color(0.78, 0.58, 0.32))
			var scuro := Color(0.5, 0.35, 0.18)
			draw_rect(r, scuro, false, 4.0)
			draw_line(Vector2.ZERO, dimensioni, scuro, 4.0)
			draw_line(Vector2(w, 0), Vector2(0, h), scuro, 4.0)
		Tipo.MANGIATOIA:
			draw_colored_polygon(PoolVector2Array([Vector2(0, 0), Vector2(w, 0), Vector2(w - 15, h), Vector2(15, h)]), Color(0.5, 0.52, 0.55))
			draw_rect(Rect2(6, 0, w - 12, 8), Color(0.95, 0.8, 0.25))  # mangime
		Tipo.POSATOIO:
			draw_rect(r, Color(0.5, 0.33, 0.18))
			draw_line(Vector2(0, 3), Vector2(w, 3), Color(0.68, 0.48, 0.28), 3.0)
		Tipo.SBARRE:
			var grigio := Color(0.4, 0.4, 0.45)
			var x := 0.0
			while x <= w:
				draw_line(Vector2(x, 0), Vector2(x, h), grigio, 4.0)
				x += 24.0
			draw_rect(r, grigio, false, 4.0)
		Tipo.PARETE:
			draw_rect(r, Color(0.82, 0.7, 0.52))
			var y := 60.0
			while y < h:
				draw_line(Vector2(0, y), Vector2(w, y), Color(0.72, 0.6, 0.42), 2.0)
				y += 60.0
		Tipo.RETE:
			draw_rect(r, Color(0.6, 0.6, 0.62, 0.35))
			var maglia := Color(0.5, 0.5, 0.55)
			var gx := 0.0
			while gx <= w:
				draw_line(Vector2(gx, 0), Vector2(gx, h), maglia, 2.0)
				gx += 15.0
			var gy := 0.0
			while gy <= h:
				draw_line(Vector2(0, gy), Vector2(w, gy), maglia, 2.0)
				gy += 15.0
			draw_rect(r, Color(0.4, 0.4, 0.45), false, 3.0)
