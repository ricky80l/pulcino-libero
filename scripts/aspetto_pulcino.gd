extends Node2D
# Aspetto del pulcino in stile cartoon: pezzi separati animati da codice.
# L'origine è tra i piedi e guarda a destra (il giocatore lo gira e lo deforma).
# Il pulcino cresce a stadi lungo il viaggio (vedi CLAUDE.md, "Crescita del pulcino").

const Parti = preload("res://scripts/parti.gd")
const CORPO = preload("res://assets/grafica/pulcino/corpo.svg")
const OCCHIO = preload("res://assets/grafica/pulcino/occhio.svg")
const OCCHIO_CHIUSO = preload("res://assets/grafica/pulcino/occhio_chiuso.svg")
const OCCHIO_X = preload("res://assets/grafica/pulcino/occhio_x.svg")
const BECCO = preload("res://assets/grafica/pulcino/becco.svg")
const BECCO_APERTO = preload("res://assets/grafica/pulcino/becco_aperto.svg")

# Pezzi di ogni stadio: immagine e perno. "alzata" = quanto si alza il corpo sulle zampe più lunghe.
const STADI := {
	1: {
		"zampa": [preload("res://assets/grafica/pulcino/zampa.svg"), Vector2(12, 2)],
		"ciuffo": [preload("res://assets/grafica/pulcino/ciuffo.svg"), Vector2(20, 32)],
		"ala": [preload("res://assets/grafica/pulcino/ala.svg"), Vector2(38, 12)],
		"coda": null,
		"alzata": 0.0,
	},
	2: {
		"zampa": [preload("res://assets/grafica/pulcino/stadio2/zampa.svg"), Vector2(12, 2)],
		"ciuffo": [preload("res://assets/grafica/pulcino/stadio2/ciuffo.svg"), Vector2(22, 41)],
		"ala": [preload("res://assets/grafica/pulcino/stadio2/ala.svg"), Vector2(46, 16)],
		"coda": [preload("res://assets/grafica/pulcino/stadio2/coda.svg"), Vector2(30, 28)],
		"alzata": 4.0,
	},
}

var stadio := 1
var zampa_dietro: Sprite
var zampa_davanti: Sprite
var ciuffo: Sprite
var ala: Sprite
var occhio: Sprite
var becco: Sprite
var coda: Sprite = null

var tempo := 0.0
var prossimo_battito := 2.0
var timer_becco := 0.0
var ciuffo_angolo := 0.0
var ciuffo_spinta := 0.0


func _ready():
	imposta_stadio(Progressi.stadio_in_gioco())


# Monta i pezzi dello stadio scelto (si può richiamare per farlo crescere)
func imposta_stadio(nuovo: int):
	stadio = int(clamp(nuovo, 1, STADI.size()))
	for figlio in get_children():
		figlio.queue_free()
	var s: Dictionary = STADI[stadio]
	var su: float = s["alzata"]
	# l'ordine conta: i primi stanno dietro
	zampa_dietro = Parti.crea(self, s["zampa"][0], s["zampa"][1], Vector2(-7, -9 - su))
	zampa_dietro.modulate = Color(0.8, 0.8, 0.8)
	zampa_davanti = Parti.crea(self, s["zampa"][0], s["zampa"][1], Vector2(6, -9 - su))
	coda = null
	if s["coda"] != null:
		coda = Parti.crea(self, s["coda"][0], s["coda"][1], Vector2(-17, -26 - su))
	ciuffo = Parti.crea(self, s["ciuffo"][0], s["ciuffo"][1], Vector2(-1, -47 - su))
	Parti.crea(self, CORPO, Vector2(50, 50), Vector2(0, -28 - su))
	ala = Parti.crea(self, s["ala"][0], s["ala"][1], Vector2(1, -28 - su))
	occhio = Parti.crea(self, OCCHIO, Vector2(14, 16), Vector2(9, -35 - su))
	becco = Parti.crea(self, BECCO, Vector2(3, 14), Vector2(19, -30 - su))


# Apre il becco per un attimo: "pio!"
func pigola():
	timer_becco = 0.2


func _process(delta):
	tempo += delta
	timer_becco -= delta
	var p = get_parent()
	var sbalzato: bool = p.timer_sbalzo > 0
	var a_terra: bool = p.era_a_terra
	var vx: float = abs(p.velocita.x)
	var morbido := min(1.0, 12.0 * delta)

	# Zampe: zampettano camminando, si raccolgono in aria, si agitano se sbalzato
	if sbalzato:
		zampa_davanti.rotation = sin(tempo * 30.0) * 0.9
		zampa_dietro.rotation = -sin(tempo * 30.0) * 0.9
	elif a_terra and vx > 30:
		zampa_davanti.rotation = sin(tempo * 18.0) * 0.6
		zampa_dietro.rotation = -sin(tempo * 18.0) * 0.6
	elif not a_terra:
		zampa_davanti.rotation = lerp(zampa_davanti.rotation, 0.6, morbido)
		zampa_dietro.rotation = lerp(zampa_dietro.rotation, -0.4, morbido)
	else:
		zampa_davanti.rotation = lerp(zampa_davanti.rotation, 0.0, morbido)
		zampa_dietro.rotation = lerp(zampa_dietro.rotation, 0.0, morbido)

	# Ala: sbatte forte in aria, dondola camminando
	if sbalzato or not a_terra:
		ala.rotation = -0.5 + sin(tempo * 35.0) * 0.6
	elif vx > 30:
		ala.rotation = sin(tempo * 18.0) * 0.15
	else:
		ala.rotation = lerp(ala.rotation, 0.0, morbido)

	# Ciuffo: una molla che ondeggia con la corsa e i salti
	var obiettivo: float = -vx / 300.0 * 0.35 + p.velocita.y / 900.0 * 0.4
	ciuffo_spinta += ((obiettivo - ciuffo_angolo) * 180.0 - ciuffo_spinta * 9.0) * delta
	ciuffo_angolo += ciuffo_spinta * delta
	ciuffo.rotation = ciuffo_angolo

	# Codina (dallo stadio 2): scodinzola camminando, si alza saltando
	if coda:
		if sbalzato or not a_terra:
			coda.rotation = lerp(coda.rotation, -0.4, morbido)
		elif vx > 30:
			coda.rotation = sin(tempo * 18.0) * 0.25
		else:
			coda.rotation = lerp(coda.rotation, 0.0, morbido)

	# Occhio: a X se travolto, ogni tanto sbatte le ciglia
	if sbalzato:
		occhio.texture = OCCHIO_X
	elif tempo > prossimo_battito:
		occhio.texture = OCCHIO_CHIUSO
		if tempo > prossimo_battito + 0.12:
			prossimo_battito = tempo + rand_range(2.0, 4.0)
	else:
		occhio.texture = OCCHIO

	becco.texture = BECCO_APERTO if (timer_becco > 0 or sbalzato) else BECCO
