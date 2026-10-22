extends Area2D
# Topo ciccione: cammina lentissimo avanti e indietro. Ai bordi si ferma, si gonfia offeso e si gira.
# Se vede il pulcino nella sua zona fa "!" e gli trotterella incontro, senza uscire dal suo tratto.
# Se il pulcino gli salta sopra squittisce e fa un balzo spaventato. Se lo tocca, lo manda a volare.
# La posizione è tra le zampe, appoggiato a terra.

export var velocita := 45.0  # lentezza del topo (pixel al secondo)
export var distanza := 260.0  # quanto cammina verso destra prima di girarsi (pixel)
export var pausa_offesa := 0.8  # secondi di pausa offesa prima di girarsi
export var altezza_balzo := 34.0  # quanto salta quando si spaventa (pixel)
export var raggio_vista := 240.0  # da quanto lontano si accorge del pulcino (pixel)
export var velocita_inseguimento := 85.0  # velocità quando gli va incontro: deve restare sotto quella del pulcino

const DURATA_BALZO := 0.45
const DURATA_ALLARME := 0.6

var partenza_x := 0.0
var direzione := 1.0
var timer_pausa := 0.0
var timer_balzo := 0.0
var timer_allarme := 0.0
var attesa_spavento := 0.0
var inseguendo := false
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
	timer_allarme = max(0.0, timer_allarme - delta)
	attesa_spavento = max(0.0, attesa_spavento - delta)

	if pulcino == null:
		var trovati := get_tree().get_nodes_in_group("pulcino")
		if trovati.size() > 0:
			pulcino = trovati[0]

	# Vede il pulcino nella sua zona? (a terra o poco sopra, e non mentre vola via)
	var dx_pulcino := 0.0
	var vede := false
	if pulcino and pulcino.timer_sbalzo <= 0:
		dx_pulcino = pulcino.global_position.x - global_position.x
		var dy: float = global_position.y - pulcino.global_position.y
		var px: float = pulcino.global_position.x
		vede = abs(dx_pulcino) < raggio_vista and dy > -20 and dy < 100 \
			and px > partenza_x - 60 and px < partenza_x + distanza + 60
	if vede and not inseguendo:
		timer_allarme = DURATA_ALLARME  # "!" sopra la testa
		Suoni.suona("squittio", 0.05)
	inseguendo = vede

	if timer_balzo > 0:
		pass  # in aria per lo spavento: non cammina
	elif inseguendo:
		# Gli va incontro, ma non esce mai dal suo tratto di pavimento
		timer_pausa = 0.0
		if abs(dx_pulcino) > 4:
			direzione = sign(dx_pulcino)
			position.x = clamp(position.x + direzione * velocita_inseguimento * delta, partenza_x, partenza_x + distanza)
	elif timer_pausa > 0:
		# Pausa offesa ai bordi, poi si gira
		timer_pausa -= delta
		if timer_pausa <= 0:
			direzione = -direzione
	else:
		# Camminata avanti e indietro
		position.x += direzione * velocita * delta
		if (direzione > 0 and position.x >= partenza_x + distanza) or (direzione < 0 and position.x <= partenza_x):
			timer_pausa = pausa_offesa

	# Il pulcino gli passa sopra: balzo spaventato con squittio
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
	if timer_allarme > 0:
		# "!" di sorpresa e saltino quando si accorge del pulcino
		su -= sin(PI * timer_allarme / DURATA_ALLARME) * 8.0
		var cima := Vector2(10 * d, -78 + su)
		draw_rect(Rect2(cima.x - 3, cima.y, 6, 18), Color(0.85, 0.15, 0.1))
		draw_circle(cima + Vector2(0, 26), 3.5, Color(0.85, 0.15, 0.1))
	var o := Vector2(0, su)
	var veloce := 18.0 if inseguendo else 10.0  # zampette più svelte quando insegue
	var passo := 0.0 if (offeso or spaventato) else sin(tempo * veloce) * 2.0
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
