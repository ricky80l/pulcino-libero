extends KinematicBody2D
# Oca arrabbiata: passeggia beccando il terreno. Quando vede il pulcino a terra si ferma, starnazza,
# abbassa il collo e carica in linea retta. Si schiva saltando. Se sbatte contro qualcosa resta
# stordita (e intanto non fa male); se non trova niente frena e torna a passeggiare.
# La posizione è tra le zampe, appoggiata a terra.

const Parti = preload("res://scripts/parti.gd")
const Effetti = preload("res://scripts/effetti.gd")
const CORPO = preload("res://assets/grafica/oca/corpo.svg")
const ALA = preload("res://assets/grafica/oca/ala.svg")
const COLLO = preload("res://assets/grafica/oca/collo.svg")
const BECCO = preload("res://assets/grafica/oca/becco.svg")
const BECCO_APERTO = preload("res://assets/grafica/oca/becco_aperto.svg")
const OCCHIO = preload("res://assets/grafica/oca/occhio.svg")
const OCCHIO_ARRABBIATO = preload("res://assets/grafica/oca/occhio_arrabbiato.svg")
const OCCHIO_STORDITO = preload("res://assets/grafica/oca/occhio_stordito.svg")
const ZAMPA = preload("res://assets/grafica/oca/zampa.svg")

enum Stato { PASSEGGIA, ALLARME, CARICA, FRENATA, STORDITA }

export var velocita_passo := 50.0  # passeggiata tranquilla (pixel al secondo)
export var distanza := 300.0  # quanto passeggia verso destra prima di girarsi (pixel)
export var raggio_vista := 420.0  # da quanto lontano vede il pulcino
export var velocita_carica := 430.0  # quanto corre caricando: più del pulcino, che deve saltare
export var durata_allarme := 0.7  # quanto starnazza prima di partire (il tempo per prepararsi a saltare)
export var durata_stordita := 2.2  # quanto resta stordita dopo una botta
export var margine_carica := 260.0  # quanto può uscire dal suo tratto quando carica

const GRAVITA := 1800.0

var stato: int = Stato.PASSEGGIA
var partenza_x := 0.0
var direzione := 1.0
var timer := 0.0
var tempo := 0.0
var velocita := Vector2.ZERO
var pulcino = null
var pausa_becchettio := 0.0

var aspetto := Node2D.new()
var zampa_dietro: Sprite
var zampa_davanti: Sprite
var ala: Sprite
var collo: Sprite
var becco: Sprite
var occhio: Sprite
var colpitore := Area2D.new()  # la zona che fa male al pulcino


func _ready():
	partenza_x = position.x
	collision_layer = 0  # nessuno ci sbatte contro; lei invece sbatte contro muri e ostacoli
	var corpo_fisico := CollisionShape2D.new()
	var rettangolo := RectangleShape2D.new()
	rettangolo.extents = Vector2(30, 28)
	corpo_fisico.shape = rettangolo
	corpo_fisico.position = Vector2(0, -28)
	add_child(corpo_fisico)
	# zona che tocca il pulcino: un po' più piccola del disegno, per essere gentili
	var forma := CollisionShape2D.new()
	var zona := RectangleShape2D.new()
	zona.extents = Vector2(30, 26)
	forma.shape = zona
	forma.position = Vector2(4, -30)
	colpitore.add_child(forma)
	add_child(colpitore)

	# disegno a pezzi: i primi stanno dietro
	add_child(aspetto)
	zampa_dietro = Parti.crea(aspetto, ZAMPA, Vector2(20, 2), Vector2(-10, -17))
	zampa_dietro.modulate = Color(0.85, 0.85, 0.85)
	zampa_davanti = Parti.crea(aspetto, ZAMPA, Vector2(20, 2), Vector2(12, -17))
	collo = Parti.crea(aspetto, COLLO, Vector2(30, 124), Vector2(24, -44))
	Parti.crea(aspetto, CORPO, Vector2(90, 104), Vector2(0, -14))
	ala = Parti.crea(aspetto, ALA, Vector2(84, 18), Vector2(12, -46))
	# becco e occhio sono attaccati al collo, così si muovono con la testa
	becco = _pezzo_della_testa(BECCO, Vector2(4, 15), Vector2(30, -96))
	occhio = _pezzo_della_testa(OCCHIO, Vector2(14, 14), Vector2(18, -104))


func _pezzo_della_testa(immagine: Texture, perno: Vector2, posizione: Vector2) -> Sprite:
	var s := Sprite.new()
	s.texture = immagine
	s.centered = false
	s.offset = -perno
	s.position = posizione
	collo.add_child(s)
	return s


func _physics_process(delta):
	tempo += delta
	timer -= delta
	if pulcino == null:
		var trovati := get_tree().get_nodes_in_group("pulcino")
		if trovati.size() > 0:
			pulcino = trovati[0]
			add_collision_exception_with(pulcino)  # non lo spinge: lo fa solo volare via

	match stato:
		Stato.PASSEGGIA:
			_passeggia(delta)
		Stato.ALLARME:
			velocita.x = 0.0
			if timer <= 0:
				stato = Stato.CARICA
		Stato.CARICA:
			velocita.x = direzione * velocita_carica
			if timer <= 0 and int(tempo * 20) % 2 == 0:
				Effetti.sbuffo(get_parent(), position, Color(0.79, 0.63, 0.42), 3, 60.0)
				timer = 0.08
			var fuori: bool = position.x < partenza_x - margine_carica or position.x > partenza_x + distanza + margine_carica
			if fuori:
				_frena()
		Stato.FRENATA:
			velocita.x = move_toward(velocita.x, 0.0, 900.0 * delta)
			if timer <= 0:
				stato = Stato.PASSEGGIA
				direzione = -direzione
		Stato.STORDITA:
			velocita.x = 0.0
			if timer <= 0:
				stato = Stato.PASSEGGIA

	velocita.y += GRAVITA * delta
	velocita = move_and_slide(velocita, Vector2.UP)

	# sbatte contro un muro o un ostacolo mentre carica: resta stordita
	if stato == Stato.CARICA and is_on_wall():
		stato = Stato.STORDITA
		timer = durata_stordita
		Suoni.suona("botta", 0.05)
		Effetti.sbuffo(get_parent(), position + Vector2(direzione * 30, -50), Color(1, 0.95, 0.6), 10, 160.0)

	# tocca il pulcino (ma non quando è stordita)
	if stato != Stato.STORDITA:
		for altro in colpitore.get_overlapping_bodies():
			if altro == pulcino and pulcino.colpito(global_position.x):
				Suoni.suona("starnazzo", 0.1, -4.0)
	_aggiorna_aspetto()
	update()


func _passeggia(delta):
	# cammina avanti e indietro nel suo tratto, ogni tanto si ferma a beccare il terreno
	pausa_becchettio -= delta
	if pausa_becchettio > 0:
		velocita.x = 0.0
	else:
		velocita.x = direzione * velocita_passo
		if (direzione > 0 and position.x >= partenza_x + distanza) or (direzione < 0 and position.x <= partenza_x):
			direzione = -direzione
		if randf() < delta * 0.25:
			pausa_becchettio = 1.0
	if _vede_il_pulcino():
		stato = Stato.ALLARME
		timer = durata_allarme
		if pulcino.global_position.x != global_position.x:
			direzione = sign(pulcino.global_position.x - global_position.x)
		Suoni.suona("starnazzo", 0.08)


func _vede_il_pulcino() -> bool:
	if pulcino == null or pulcino.timer_sbalzo > 0 or pulcino.timer_invulnerabile > 0:
		return false  # appena ripartito dal nido non lo attacca
	var dx: float = pulcino.global_position.x - global_position.x
	var dy: float = global_position.y - pulcino.global_position.y
	return abs(dx) < raggio_vista and dy > -10 and dy < 70


func _frena():
	stato = Stato.FRENATA
	timer = 0.5


func _aggiorna_aspetto():
	aspetto.scale.x = direzione
	var corre: bool = stato == Stato.CARICA or (stato == Stato.PASSEGGIA and pausa_becchettio <= 0)
	var veloce: float = 26.0 if stato == Stato.CARICA else 10.0
	var passo: float = sin(tempo * veloce) if corre else 0.0
	zampa_davanti.rotation = passo * 0.6
	zampa_dietro.rotation = -passo * 0.6
	aspetto.position.y = -abs(passo) * (4.0 if stato == Stato.CARICA else 2.0)
	aspetto.rotation = 0.0

	match stato:
		Stato.PASSEGGIA:
			# collo dritto; se si ferma, becchetta il terreno
			collo.rotation = (0.9 + sin(tempo * 12.0) * 0.25) if pausa_becchettio > 0 else sin(tempo * 3.0) * 0.08
			ala.rotation = 0.0
			becco.texture = BECCO
			occhio.texture = OCCHIO
		Stato.ALLARME:
			# collo basso e teso, ali aperte, becco spalancato, zampa che raspa
			collo.rotation = 0.75 + sin(tempo * 30.0) * 0.05
			ala.rotation = -0.6 + sin(tempo * 25.0) * 0.3
			becco.texture = BECCO_APERTO
			occhio.texture = OCCHIO_ARRABBIATO
			zampa_davanti.rotation = sin(tempo * 20.0) * 0.5
		Stato.CARICA:
			collo.rotation = 1.05
			ala.rotation = -0.5 + sin(tempo * 35.0) * 0.6
			becco.texture = BECCO_APERTO
			occhio.texture = OCCHIO_ARRABBIATO
			aspetto.rotation = 0.12 * direzione
		Stato.FRENATA:
			collo.rotation = -0.3
			ala.rotation = -0.3
			becco.texture = BECCO
			occhio.texture = OCCHIO
			aspetto.rotation = -0.15 * direzione
		Stato.STORDITA:
			collo.rotation = sin(tempo * 4.0) * 0.35
			ala.rotation = 0.2
			becco.texture = BECCO_APERTO
			occhio.texture = OCCHIO_STORDITO


func _draw():
	# stelline che girano sopra la testa quando è stordita
	if stato != Stato.STORDITA:
		return
	var centro := Vector2(28 * direzione, -118)
	for i in range(3):
		var a := tempo * 4.0 + i * TAU / 3.0
		var p := centro + Vector2(cos(a) * 24, sin(a) * 8)
		_stella(p, 7.0)


func _stella(c: Vector2, r: float):
	var punti := PoolVector2Array()
	for k in range(10):
		var raggio := r if k % 2 == 0 else r * 0.45
		var ang := -PI / 2 + k * PI / 5
		punti.append(c + Vector2(cos(ang), sin(ang)) * raggio)
	draw_colored_polygon(punti, Color("ffd84a"), PoolVector2Array(), null, null, true)
