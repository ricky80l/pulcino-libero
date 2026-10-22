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

const Parti = preload("res://scripts/parti.gd")
const CORPO = preload("res://assets/grafica/topo/corpo.svg")
const ORECCHIO = preload("res://assets/grafica/topo/orecchio.svg")
const CODA = preload("res://assets/grafica/topo/coda.svg")
const ZAMPA = preload("res://assets/grafica/topo/zampa.svg")
const OCCHIO = preload("res://assets/grafica/topo/occhio.svg")
const OCCHIO_SPAVENTATO = preload("res://assets/grafica/topo/occhio_spaventato.svg")
const SOPRACCIGLIO = preload("res://assets/grafica/topo/sopracciglio.svg")
const ESCLAMATIVO = preload("res://assets/grafica/topo/esclamativo.svg")

# pezzi del disegno, dentro "aspetto" che si gira verso la direzione di marcia
var aspetto := Node2D.new()
var coda: Sprite
var zampa_dietro: Sprite
var zampa_davanti: Sprite
var corpo: Sprite
var orecchio: Sprite
var occhio: Sprite
var sopracciglio: Sprite
var esclamativo: Sprite


func _ready():
	partenza_x = position.x
	var rettangolo := RectangleShape2D.new()
	rettangolo.extents = Vector2(28, 16)
	var forma := CollisionShape2D.new()
	forma.shape = rettangolo
	forma.position = Vector2(0, -18)
	add_child(forma)
	# monta il disegno: i primi pezzi stanno dietro
	add_child(aspetto)
	coda = Parti.crea(aspetto, CODA, Vector2(66, 50), Vector2(-28, -12))
	zampa_dietro = Parti.crea(aspetto, ZAMPA, Vector2(11, 7), Vector2(-14, -3))
	zampa_davanti = Parti.crea(aspetto, ZAMPA, Vector2(11, 7), Vector2(14, -3))
	orecchio = Parti.crea(aspetto, ORECCHIO, Vector2(20, 34), Vector2(12, -36))
	corpo = Parti.crea(aspetto, CORPO, Vector2(66, 96), Vector2.ZERO)
	occhio = Parti.crea(aspetto, OCCHIO, Vector2(10, 10), Vector2(22, -27))
	sopracciglio = Parti.crea(aspetto, SOPRACCIGLIO, Vector2(15, 7), Vector2(22, -36))
	esclamativo = Parti.crea(aspetto, ESCLAMATIVO, Vector2(11, 56), Vector2(6, -58))


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

	for altro in get_overlapping_bodies():
		if altro.is_in_group("pulcino") and altro.colpito(global_position.x):
			Suoni.suona("squittio", 0.05, -3.0)
	_aggiorna_aspetto()


# Muove i pezzi del disegno secondo l'umore del topo
func _aggiorna_aspetto():
	var offeso := timer_pausa > 0
	var spaventato := timer_balzo > 0
	var su := 0.0
	if spaventato:
		su = -sin(PI * (1.0 - timer_balzo / DURATA_BALZO)) * altezza_balzo
	if timer_allarme > 0:
		su -= sin(PI * timer_allarme / DURATA_ALLARME) * 8.0  # saltino di sorpresa
	aspetto.position.y = su
	aspetto.scale.x = direzione

	var veloce := 18.0 if inseguendo else 10.0  # zampette più svelte quando insegue
	var passo := 0.0 if (offeso or spaventato) else sin(tempo * veloce)
	zampa_dietro.position.x = -14 + passo * 3
	zampa_davanti.position.x = 14 - passo * 3
	aspetto.position.y -= abs(passo) * 2  # sobbalza camminando
	zampa_dietro.position.y = -3 + abs(passo) * 2  # le zampe restano a terra
	zampa_davanti.position.y = -3 + abs(passo) * 2

	# si gonfia offeso ai bordi
	var gonfio := 1.15 if offeso else 1.0
	corpo.scale = Vector2(0.5 * gonfio, 0.5 * gonfio)

	# coda: dritta e tesa se spaventato, altrimenti scodinzola
	coda.rotation = 0.9 if spaventato else sin(tempo * 4.0) * 0.15
	orecchio.rotation = sin(tempo * 7.0) * 0.08

	occhio.texture = OCCHIO_SPAVENTATO if spaventato else OCCHIO
	occhio.offset = Vector2(-16, -16) if spaventato else Vector2(-10, -10)
	sopracciglio.visible = offeso
	esclamativo.visible = timer_allarme > 0