extends Area2D
# Topo ciccione: cammina lentissimo avanti e indietro. Ai bordi si ferma, si gonfia offeso e si gira.
# Se tocca il pulcino, lo rimanda all'ultimo nido. La posizione è tra le zampe, appoggiato a terra.

export var velocita := 45.0  # lentezza del topo (pixel al secondo)
export var distanza := 260.0  # quanto cammina verso destra prima di girarsi (pixel)
export var pausa_offesa := 0.8  # secondi di pausa offesa prima di girarsi

var partenza_x := 0.0
var direzione := 1.0
var timer_pausa := 0.0
var tempo := 0.0


func _ready():
	partenza_x = position.x
	var rettangolo := RectangleShape2D.new()
	rettangolo.extents = Vector2(28, 16)
	var forma := CollisionShape2D.new()
	forma.shape = rettangolo
	forma.position = Vector2(0, -18)
	add_child(forma)


func _physics_process(delta):
	tempo += delta
	if timer_pausa > 0:
		timer_pausa -= delta
		if timer_pausa <= 0:
			direzione = -direzione
	else:
		position.x += direzione * velocita * delta
		if (direzione > 0 and position.x >= partenza_x + distanza) or (direzione < 0 and position.x <= partenza_x):
			timer_pausa = pausa_offesa
	for corpo in get_overlapping_bodies():
		if corpo.is_in_group("pulcino"):
			corpo.colpito()
	update()


func _draw():
	var d := direzione
	var offeso := timer_pausa > 0
	var passo := 0.0 if offeso else sin(tempo * 10.0) * 2.0
	var gonfio := 1.18 if offeso else 1.0
	var grigio := Color(0.58, 0.56, 0.6)
	var rosa := Color(0.95, 0.68, 0.72)
	# coda
	draw_line(Vector2(-28 * d, -10), Vector2(-52 * d, -24 + passo * 2), rosa, 3.0)
	# zampette
	draw_circle(Vector2(-14 + passo, -2), 5, rosa)
	draw_circle(Vector2(14 - passo, -2), 5, rosa)
	# pancione: ellisse
	draw_set_transform(Vector2(0, -20), 0, Vector2(1.6 * gonfio, 1.0 * gonfio))
	draw_circle(Vector2.ZERO, 20, grigio)
	draw_set_transform(Vector2.ZERO, 0, Vector2.ONE)
	# orecchio
	draw_circle(Vector2(12 * d, -40), 10, grigio)
	draw_circle(Vector2(12 * d, -40), 6, rosa)
	# occhio e naso
	draw_circle(Vector2(22 * d, -26), 3, Color.black)
	draw_circle(Vector2(34 * d, -18), 4, rosa)
	# baffi
	draw_line(Vector2(32 * d, -18), Vector2(44 * d, -22), Color(0.3, 0.3, 0.3), 1.0)
	draw_line(Vector2(32 * d, -18), Vector2(44 * d, -14), Color(0.3, 0.3, 0.3), 1.0)
	# sopracciglio offeso
	if offeso:
		draw_line(Vector2(17 * d, -34), Vector2(27 * d, -30), Color.black, 2.0)
