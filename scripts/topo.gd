extends Area2D
# Topo ciccione: cammina lentissimo avanti e indietro. Ai bordi si ferma, si gonfia offeso e si gira.
# Se il pulcino gli salta sopra squittisce e fa un balzo spaventato. Se lo tocca, lo manda a volare.
# La posizione è tra le zampe, appoggiato a terra.

export var velocita := 45.0  # lentezza del topo (pixel al secondo)
export var distanza := 260.0  # quanto cammina verso destra prima di girarsi (pixel)
export var pausa_offesa := 0.8  # secondi di pausa offesa prima di girarsi
export var altezza_balzo := 34.0  # quanto salta quando si spaventa (pixel)

const DURATA_BALZO := 0.45

var partenza_x := 0.0
var direzione := 1.0
var timer_pausa := 0.0
var timer_balzo := 0.0
var attesa_spavento := 0.0
var tempo := 0.0
var pulcino = null


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
	timer_balzo = max(0.0, timer_balzo - delta)
	attesa_spavento = max(0.0, attesa_spavento - delta)

	# Camminata avanti e indietro, con pausa offesa ai bordi
	if timer_pausa > 0:
		timer_pausa -= delta
		if timer_pausa <= 0:
			direzione = -direzione
	elif timer_balzo <= 0:
		position.x += direzione * velocita * delta
		if (direzione > 0 and position.x >= partenza_x + distanza) or (direzione < 0 and position.x <= partenza_x):
			timer_pausa = pausa_offesa

	# Il pulcino gli passa sopra: balzo spaventato con squittio
	if pulcino == null:
		var trovati := get_tree().get_nodes_in_group("pulcino")
		if trovati.size() > 0:
			pulcino = trovati[0]
	if pulcino and attesa_spavento <= 0:
		var dx: float = abs(pulcino.global_position.x - global_position.x)
		var sopra: bool = pulcino.global_position.y < global_position.y - 60
		if dx < 45 and sopra:
			timer_balzo = DURATA_BALZO
			attesa_spavento = 1.5
			Suoni.suona("squittio")

	for corpo in get_overlapping_bodies():
		if corpo.is_in_group("pulcino") and corpo.colpito(global_position.x):
			Suoni.suona("squittio", 0.05, -3.0)
	update()


func _draw():
	var d := direzione
	var offeso := timer_pausa > 0
	var spaventato := timer_balzo > 0
	var su := 0.0
	if spaventato:
		su = -sin(PI * (1.0 - timer_balzo / DURATA_BALZO)) * altezza_balzo
	var o := Vector2(0, su)
	var passo := 0.0 if (offeso or spaventato) else sin(tempo * 10.0) * 2.0
	var gonfio := 1.18 if offeso else 1.0
	var grigio := Color(0.58, 0.56, 0.6)
	var rosa := Color(0.95, 0.68, 0.72)
	# coda: dritta e tesa se spaventato
	var punta_coda := Vector2(-56 * d, -44) if spaventato else Vector2(-52 * d, -24 + passo * 2)
	draw_line(o + Vector2(-28 * d, -10), o + punta_coda, rosa, 3.0)
	# zampette
	draw_circle(o + Vector2(-14 + passo, -2), 5, rosa)
	draw_circle(o + Vector2(14 - passo, -2), 5, rosa)
	# pancione: ellisse
	draw_set_transform(o + Vector2(0, -20), 0, Vector2(1.6 * gonfio, 1.0 * gonfio))
	draw_circle(Vector2.ZERO, 20, grigio)
	draw_set_transform(Vector2.ZERO, 0, Vector2.ONE)
	# orecchio
	draw_circle(o + Vector2(12 * d, -40), 10, grigio)
	draw_circle(o + Vector2(12 * d, -40), 6, rosa)
	# occhio: enorme quando è spaventato
	if spaventato:
		draw_circle(o + Vector2(22 * d, -27), 7, Color.white)
		draw_circle(o + Vector2(23 * d, -27), 3, Color.black)
	else:
		draw_circle(o + Vector2(22 * d, -26), 3, Color.black)
	# naso e baffi
	draw_circle(o + Vector2(34 * d, -18), 4, rosa)
	draw_line(o + Vector2(32 * d, -18), o + Vector2(44 * d, -22), Color(0.3, 0.3, 0.3), 1.0)
	draw_line(o + Vector2(32 * d, -18), o + Vector2(44 * d, -14), Color(0.3, 0.3, 0.3), 1.0)
	# sopracciglio offeso
	if offeso:
		draw_line(o + Vector2(17 * d, -34), o + Vector2(27 * d, -30), Color.black, 2.0)
