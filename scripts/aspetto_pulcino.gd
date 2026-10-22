extends Node2D
# Aspetto del pulcino in stile cartoon: pezzi separati animati da codice.
# L'origine è tra i piedi e guarda a destra (il giocatore lo gira e lo deforma).

const Parti = preload("res://scripts/parti.gd")
const CORPO = preload("res://assets/grafica/pulcino/corpo.svg")
const ALA = preload("res://assets/grafica/pulcino/ala.svg")
const CIUFFO = preload("res://assets/grafica/pulcino/ciuffo.svg")
const OCCHIO = preload("res://assets/grafica/pulcino/occhio.svg")
const OCCHIO_CHIUSO = preload("res://assets/grafica/pulcino/occhio_chiuso.svg")
const OCCHIO_X = preload("res://assets/grafica/pulcino/occhio_x.svg")
const BECCO = preload("res://assets/grafica/pulcino/becco.svg")
const BECCO_APERTO = preload("res://assets/grafica/pulcino/becco_aperto.svg")
const ZAMPA = preload("res://assets/grafica/pulcino/zampa.svg")

var zampa_dietro: Sprite
var zampa_davanti: Sprite
var ciuffo: Sprite
var ala: Sprite
var occhio: Sprite
var becco: Sprite

var tempo := 0.0
var prossimo_battito := 2.0
var timer_becco := 0.0
var ciuffo_angolo := 0.0
var ciuffo_spinta := 0.0


func _ready():
	# l'ordine conta: i primi stanno dietro
	zampa_dietro = Parti.crea(self, ZAMPA, Vector2(12, 2), Vector2(-7, -9))
	zampa_dietro.modulate = Color(0.8, 0.8, 0.8)
	zampa_davanti = Parti.crea(self, ZAMPA, Vector2(12, 2), Vector2(6, -9))
	ciuffo = Parti.crea(self, CIUFFO, Vector2(20, 32), Vector2(-1, -47))
	Parti.crea(self, CORPO, Vector2(50, 50), Vector2(0, -28))
	ala = Parti.crea(self, ALA, Vector2(38, 12), Vector2(1, -28))
	occhio = Parti.crea(self, OCCHIO, Vector2(14, 16), Vector2(9, -35))
	becco = Parti.crea(self, BECCO, Vector2(3, 14), Vector2(19, -30))


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
