extends Node2D
# Pezzi che volano via quando un ostacolo si rompe: chicchi e brandelli di sacco, oppure fili di paglia.
# Cadono, girano, svaniscono e poi si cancellano da soli.

const GRAVITA := 1300.0
const DURATA := 1.1

var pezzi := []  # ognuno: posizione, velocità, angolo, giro, colore, forma
var tempo := 0.0


func lancia(tipo: int, verso: float, quanti: int, misura: Vector2):
	var rng := RandomNumberGenerator.new()
	rng.randomize()
	for i in range(quanti):
		var p := {
			"pos": Vector2(rng.randf_range(-misura.x, misura.x) * 0.4, rng.randf_range(-misura.y, misura.y) * 0.4),
			"vel": Vector2(verso * rng.randf_range(60, 340) + rng.randf_range(-140, 140), rng.randf_range(-560, -180)),
			"ang": rng.randf_range(0, TAU),
			"giro": rng.randf_range(-12, 12),
		}
		if tipo == 0:  # sacco: chicchi di mangime e brandelli di tela
			if i % 3 == 0:
				p["forma"] = "brandello"
				p["colore"] = Color("c9a46a")
			else:
				p["forma"] = "chicco"
				p["colore"] = Color("f2c230")
		else:  # balla: fili di paglia
			p["forma"] = "filo"
			p["colore"] = Color("ebc85a") if i % 2 == 0 else Color("d9b04a")
		pezzi.append(p)


func _process(delta):
	tempo += delta
	if tempo > DURATA:
		queue_free()
		return
	for p in pezzi:
		var vel: Vector2 = p["vel"]
		vel.y += GRAVITA * delta
		p["vel"] = vel
		p["pos"] = p["pos"] + vel * delta
		p["ang"] = p["ang"] + p["giro"] * delta
	update()


func _draw():
	var alfa: float = clamp((DURATA - tempo) / 0.4, 0.0, 1.0)  # svaniscono alla fine
	for p in pezzi:
		var col: Color = p["colore"]
		col.a = alfa
		var bordo := Color(0.35, 0.22, 0.08, alfa)
		draw_set_transform(p["pos"], p["ang"], Vector2.ONE)
		match p["forma"]:
			"chicco":
				draw_circle(Vector2.ZERO, 5, bordo)
				draw_circle(Vector2.ZERO, 3.5, col)
			"brandello":
				draw_rect(Rect2(-7, -5, 14, 10), bordo)
				draw_rect(Rect2(-5.5, -3.5, 11, 7), col)
			"filo":
				draw_line(Vector2(-10, 0), Vector2(10, 0), col, 3.0, true)
	draw_set_transform(Vector2.ZERO, 0, Vector2.ONE)
