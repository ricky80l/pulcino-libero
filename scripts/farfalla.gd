extends Node2D
# Farfalla decorativa della mappa: svolazza intorno a un punto sbattendo le ali.

export var colore := Color("ff9ec0")
export var raggio := Vector2(60, 30)  # quanto si allontana dal centro

var centro := Vector2.ZERO
var tempo := 0.0


func _ready():
	centro = position
	tempo = position.x * 0.03  # ognuna parte in un momento diverso


func _process(delta):
	tempo += delta
	position = centro + Vector2(sin(tempo * 0.9) * raggio.x, sin(tempo * 1.7) * raggio.y)
	update()


func _draw():
	var apertura: float = 0.35 + abs(sin(tempo * 14.0)) * 0.65  # ali che sbattono
	var bordo := colore.darkened(0.4)
	for lato in [-1.0, 1.0]:
		_ala(Vector2(lato * 5 * apertura, -3), Vector2(6 * apertura, 7), bordo)
		_ala(Vector2(lato * 4 * apertura, 4), Vector2(4 * apertura, 5), bordo)
	draw_line(Vector2(0, -6), Vector2(0, 6), Color("3a2a1a"), 2.0)


func _ala(c: Vector2, r: Vector2, bordo: Color):
	var punti := PoolVector2Array()
	for i in range(16):
		var a := i * TAU / 16
		punti.append(c + Vector2(cos(a) * r.x, sin(a) * r.y))
	draw_colored_polygon(punti, bordo, PoolVector2Array(), null, null, true)
	for i in range(punti.size()):
		punti[i] = c + (punti[i] - c) * 0.75
	draw_colored_polygon(punti, colore, PoolVector2Array(), null, null, true)
