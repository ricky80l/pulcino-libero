extends Node2D
# Operatore del magazzino filati, in camice blu: aspetta con le mani unite davanti come uno scalino.
# Se il pulcino ci atterra sopra, lo tiene un attimo, carica la sua mossa e lo lancia, poi esulta.
# Ognuno ha la sua mossa (vedi CLAUDE.md, livello 4). La posizione è tra i piedi, a terra.

const Parti = preload("res://scripts/parti.gd")
const Effetti = preload("res://scripts/effetti.gd")
const Stile = preload("res://scripts/stile.gd")
const FONT = preload("res://assets/font/fredoka_piccolo.tres")
const CORPO = preload("res://assets/grafica/operatori/corpo.svg")
const GAMBA = preload("res://assets/grafica/operatori/gamba.svg")

enum Chi { MORO, BIONDO, INDIANO, MAROCCHINO }
enum Stato { PRONTO, CARICA, LANCIO, ESULTA }

const NOMI := ["moro", "biondo", "indiano", "marocchino"]
const BATTUTE := ["Su!", "Vai!", "Op-là!", "Volaaa!"]
# Lancio di ogni mossa (pixel al secondo; x verso dove guarda l'operatore):
# bagher dritto in alto, canestro ad arco in avanti, catapulta in diagonale, giravolta lontanissimo in orizzontale
const LANCI := [Vector2(0, -1090), Vector2(460, -900), Vector2(430, -1000), Vector2(1100, -600)]

# Pose: angolo delle braccia (sinistro e destro sullo schermo), quanto si abbassa il busto,
# quanto si inclina in avanti, quanto apre le gambe
const PRONTO := {"sx": -38.0, "dx": 38.0, "abbassa": 4.0, "inclina": 0.0, "gambe": 6.0}
const ESULTA := {"sx": 165.0, "dx": -165.0, "abbassa": 0.0, "inclina": 0.0, "gambe": 4.0}
const CARICHE := [
	{"sx": -30.0, "dx": 30.0, "abbassa": 16.0, "inclina": 0.0, "gambe": 12.0},
	{"sx": -55.0, "dx": 55.0, "abbassa": 10.0, "inclina": -6.0, "gambe": 8.0},
	{"sx": -20.0, "dx": 20.0, "abbassa": 22.0, "inclina": -14.0, "gambe": 14.0},
	{"sx": 95.0, "dx": -95.0, "abbassa": 4.0, "inclina": 0.0, "gambe": 6.0},
]
const LANCIATE := [
	{"sx": -75.0, "dx": 75.0, "abbassa": -6.0, "inclina": 0.0, "gambe": 0.0},
	{"sx": 172.0, "dx": -150.0, "abbassa": -4.0, "inclina": 6.0, "gambe": 4.0},
	{"sx": -95.0, "dx": -125.0, "abbassa": 8.0, "inclina": 14.0, "gambe": 10.0},
	{"sx": 95.0, "dx": -95.0, "abbassa": 0.0, "inclina": 0.0, "gambe": 6.0},
]

export(Chi) var chi := Chi.MORO  # quale operatore è (e quindi quale mossa fa)
export var verso := 1.0  # 1 = lancia verso destra, -1 = verso sinistra
export var potenza := 1.0  # moltiplica la forza del lancio, per regolarlo nel livello
export var durata_carica := 0.3  # quanto tiene il pulcino prima di lanciarlo (secondi)

var figura := Node2D.new()  # tutto il disegno: si specchia e gira su se stesso
var busto := Node2D.new()  # camice, testa e braccia: si abbassa e si inclina sui fianchi
var braccio_sx: Sprite
var braccio_dx: Sprite
var testa: Sprite
var gamba_sx: Sprite
var gamba_dx: Sprite
var fumetto: Label

var stato: int = Stato.PRONTO
var timer := 0.0
var tempo := 0.0
var attesa := 0.0  # dopo un lancio non riprende subito il pulcino
var pulcino = null
var posa: Dictionary = PRONTO.duplicate()
var posa_da: Dictionary = PRONTO.duplicate()
var posa_a: Dictionary = PRONTO.duplicate()
var durata_posa := 0.2
# gesti da fermo, ogni tanto e a caso, per non sembrare tutti uguali e ripetitivi
var rng := RandomNumberGenerator.new()
var gesto := ""
var tempo_gesto := 0.0
var durata_gesto := 1.0
var prossimo_gesto := 2.0


func _ready():
	tempo = position.x * 0.01  # così non respirano tutti insieme
	rng.randomize()
	prossimo_gesto = rng.randf_range(1.0, 3.0)
	var nome: String = NOMI[chi]
	var immagine_braccio: Texture = load("res://assets/grafica/operatori/braccio_%s.svg" % nome)
	add_child(figura)
	figura.scale.x = verso
	gamba_sx = Parti.crea(figura, GAMBA, Vector2(22, 6), Vector2(-10, -60))
	gamba_dx = Parti.crea(figura, GAMBA, Vector2(22, 6), Vector2(10, -60))
	busto.position = Vector2(0, -55)  # il busto ruota sui fianchi
	figura.add_child(busto)
	Parti.crea(busto, CORPO, Vector2(75, 176), Vector2(0, 27))
	testa = Parti.crea(busto, load("res://assets/grafica/operatori/testa_%s.svg" % nome), Vector2(56, 116), Vector2(0, -58))
	braccio_sx = Parti.crea(busto, immagine_braccio, Vector2(20, 12), Vector2(-30, -55))
	braccio_dx = Parti.crea(busto, immagine_braccio, Vector2(20, 12), Vector2(30, -55))
	_crea_fumetto()
	_applica_posa()


func _crea_fumetto():
	fumetto = Label.new()
	fumetto.text = BATTUTE[chi]
	fumetto.add_font_override("font", FONT)
	fumetto.add_color_override("font_color", Color("3a2616"))
	var sfondo := Stile.riquadro(Color.white, Color("3a2616"), 3)
	sfondo.set_corner_radius_all(14)
	sfondo.content_margin_left = 12
	sfondo.content_margin_right = 12
	sfondo.content_margin_top = 2
	sfondo.content_margin_bottom = 4
	fumetto.add_stylebox_override("normal", sfondo)
	fumetto.visible = false
	add_child(fumetto)


func _physics_process(delta):
	tempo += delta
	timer += delta
	attesa -= delta
	if pulcino == null:
		var trovati: Array = get_tree().get_nodes_in_group("pulcino")
		if not trovati.empty():
			pulcino = trovati[0]

	match stato:
		Stato.PRONTO:
			if attesa <= 0 and _pulcino_sulle_mani():
				_afferra()
		Stato.CARICA:
			_tieni_pulcino()
			if chi == Chi.MAROCCHINO:
				# giravolta: un giro completo su se stesso
				figura.scale.x = verso * cos(min(timer / durata_carica, 1.0) * TAU)
			if timer >= durata_carica:
				_lancia()
		Stato.LANCIO:
			if timer >= 0.25:
				_vai(Stato.ESULTA, ESULTA, 0.15)
				fumetto.visible = true
				var larghezza: float = FONT.get_string_size(fumetto.text).x + 24
				fumetto.rect_position = Vector2(-larghezza / 2, -215)
		Stato.ESULTA:
			if timer >= 0.8:
				fumetto.visible = false
				_vai(Stato.PRONTO, PRONTO, 0.3)

	# la posa si avvicina a quella voluta; da fermo respira piano e ogni tanto fa un gesto
	var t: float = clamp(timer / durata_posa, 0.0, 1.0)
	t = t * t * (3.0 - 2.0 * t)
	for k in posa:
		posa[k] = lerp(posa_da[k], posa_a[k], t)
	var extra := {"sx": 0.0, "dx": 0.0, "abbassa": 0.0, "x": 0.0, "inclina": 0.0, "testa": 0.0}
	if stato == Stato.PRONTO:
		extra["abbassa"] = sin(tempo * 1.6) * 1.2
		_gesti(delta, extra)
	elif stato == Stato.ESULTA:
		extra["abbassa"] = -abs(sin(timer * 12.0)) * 8.0
	_applica_posa(extra)


func _applica_posa(extra := {}):
	braccio_sx.rotation_degrees = posa["sx"] + extra.get("sx", 0.0)
	braccio_dx.rotation_degrees = posa["dx"] + extra.get("dx", 0.0)
	busto.position = Vector2(extra.get("x", 0.0), -55 + posa["abbassa"] + extra.get("abbassa", 0.0))
	busto.rotation_degrees = posa["inclina"] + extra.get("inclina", 0.0)
	gamba_sx.rotation_degrees = posa["gambe"]
	gamba_dx.rotation_degrees = -posa["gambe"]
	testa.rotation_degrees = -posa["inclina"] * 0.4 + extra.get("testa", 0.0)


# Gesti da fermo: uno alla volta, ogni pochi secondi, con un movimento morbido che parte e torna.
# Se il pulcino è vicino, l'operatore si prepara: piega le ginocchia e abbassa le mani per riceverlo.
func _gesti(delta: float, extra: Dictionary):
	if gesto == "":
		prossimo_gesto -= delta
		if prossimo_gesto > 0:
			return
		var vicino: bool = pulcino != null and attesa <= 0 and abs(pulcino.global_position.x - global_position.x) < 260
		if vicino:
			gesto = "invita"
			durata_gesto = 1.1
		else:
			var scelte := ["sistema", "guarda", "stiracchia", "peso", "guarda"]
			gesto = scelte[rng.randi() % scelte.size()]
			durata_gesto = {"sistema": 1.2, "guarda": 2.2, "stiracchia": 1.8, "peso": 2.6}[gesto]
		tempo_gesto = 0.0
	tempo_gesto += delta
	var f: float = clamp(tempo_gesto / durata_gesto, 0.0, 1.0)
	var e := sin(PI * f)  # da 0 sale a 1 e torna a 0, senza scatti
	match gesto:
		"invita":  # si prepara a ricevere il pulcino
			extra["abbassa"] += 7.0 * e
			extra["sx"] += 10.0 * e
			extra["dx"] -= 10.0 * e
		"sistema":  # si aggiusta il camice: abbassa le mani e le riunisce
			extra["sx"] += 32.0 * e
			extra["dx"] -= 32.0 * e
			extra["testa"] = 5.0 * e
		"guarda":  # si guarda intorno, da una parte e dall'altra
			extra["testa"] = 8.0 * sin(TAU * f)
		"stiracchia":  # si stiracchia con le braccia in alto
			var su := e * e
			extra["sx"] += 190.0 * su
			extra["dx"] -= 190.0 * su
			extra["abbassa"] -= 4.0 * su
		"peso":  # sposta il peso da un piede all'altro
			extra["x"] = 3.0 * sin(TAU * f)
			extra["inclina"] = 2.5 * sin(TAU * f)
	if f >= 1.0:
		gesto = ""
		prossimo_gesto = rng.randf_range(1.5, 4.5)


func _vai(nuovo: int, verso_posa: Dictionary, durata: float):
	stato = nuovo
	timer = 0.0
	posa_da = posa.duplicate()
	posa_a = verso_posa
	durata_posa = durata


# Punto delle mani: in mezzo alle due mani, oppure la mano davanti nella giravolta
func _mani() -> Vector2:
	var destra := braccio_dx.to_global(Vector2(0, 108))
	if chi == Chi.MAROCCHINO and stato != Stato.PRONTO:
		return destra
	return (braccio_sx.to_global(Vector2(0, 108)) + destra) / 2.0


func _pulcino_sulle_mani() -> bool:
	if pulcino == null or pulcino.tenuto or pulcino.timer_sbalzo > 0 or pulcino.velocita.y <= 0:
		return false
	var mani := _mani()
	var piedi: Vector2 = pulcino.global_position + Vector2(0, 20)
	return abs(piedi.x - mani.x) < 34 and piedi.y > mani.y - 24 and piedi.y < mani.y + 14


func _afferra():
	gesto = ""
	prossimo_gesto = rng.randf_range(1.5, 3.0)
	pulcino.afferra()
	_vai(Stato.CARICA, CARICHE[chi], durata_carica * 0.8)
	Suoni.suona("atterra", 0.1, -4.0)


func _tieni_pulcino():
	pulcino.global_position = _mani() - Vector2(0, 26)


func _lancia():
	figura.scale.x = verso
	_vai(Stato.LANCIO, LANCIATE[chi], 0.08)
	_applica_posa()
	var spinta: Vector2 = LANCI[chi] * potenza
	pulcino.lancia(Vector2(spinta.x * verso, spinta.y))
	attesa = 0.8
	Suoni.suona("boing", 0.1)
	Effetti.sbuffo(get_parent(), _mani(), Color(1.0, 0.93, 0.62), 10, 160.0)
