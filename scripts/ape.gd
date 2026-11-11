extends Area2D
# Ape ronzante del prato: vola avanti e indietro tra i fiori lungo il suo giro, ondeggiando su e giù.
# Il giro si vede bene: una scia di puntini di polline. Ronza: il "bzzz" si sente solo da vicino.
# Non insegue il pulcino: si passa sotto o sopra quando è lontana. Se lo tocca, lui riparte dall'ultimo nido.
# Ai capi del giro si ferma un attimo ad annusare l'aria e si gira; se prende il pulcino fa una giravolta contenta.
# La posizione è il capo sinistro del giro, a metà dell'onda.

const Parti = preload("res://scripts/parti.gd")
const Effetti = preload("res://scripts/effetti.gd")
const CORPO = preload("res://assets/grafica/ape/corpo.png")
const ALA = preload("res://assets/grafica/ape/ala.png")
const RONZIO = preload("res://assets/suoni/ronzio.wav")

export var larghezza_giro := 320.0  # quanto è lungo il suo giro, verso destra (pixel)
export var onda := 40.0  # quanto sale e scende
export var onde_nel_giro := 2.0  # quante volte sale e scende lungo il giro
export var velocita := 115.0  # pixel al secondo: lenta, si vede arrivare
export var pausa_ai_capi := 0.7  # secondi in cui annusa l'aria prima di girarsi

var partenza := Vector2.ZERO
var x := 0.0  # dove sta lungo il giro (0 = capo sinistro)
var direzione := 1.0
var pausa := 0.0
var tempo := 0.0
var contenta := 0.0  # dopo aver preso il pulcino: giravolta
var aspetto := Node2D.new()
var ala_dietro: Sprite
var ala_davanti: Sprite
var voce: AudioStreamPlayer2D
var scia := Node2D.new()


func _ready():
	add_to_group("api")
	partenza = position
	tempo = position.x * 0.013
	var cerchio := CircleShape2D.new()
	cerchio.radius = 19.0
	var forma := CollisionShape2D.new()
	forma.shape = cerchio
	add_child(forma)
	add_child(aspetto)
	ala_dietro = Parti.crea(aspetto, ALA, Vector2(8, 38), Vector2(-4, -12))
	Parti.crea(aspetto, CORPO, Vector2(56, 58), Vector2.ZERO)
	ala_davanti = Parti.crea(aspetto, ALA, Vector2(8, 38), Vector2(2, -14))
	ala_dietro.modulate = Color(0.85, 0.9, 0.95, 0.8)
	# il ronzio: si ripete senza fine e si sente solo da vicino
	voce = AudioStreamPlayer2D.new()
	var suono: AudioStreamSample = RONZIO.duplicate()
	suono.loop_mode = AudioStreamSample.LOOP_FORWARD
	suono.loop_begin = 0
	suono.loop_end = int(suono.data.size() / 2)  # campioni a 16 bit
	voce.stream = suono
	voce.max_distance = 560.0
	voce.attenuation = 2.0
	voce.volume_db = -3.0
	voce.bus = "Suoni"  # si spegne con l'interruttore Suoni
	add_child(voce)
	voce.play(rand_range(0.0, 0.9))
	# la scia di polline che mostra il suo giro, disegnata una volta sola nel livello
	scia.position = partenza
	scia.z_index = -1
	scia.connect("draw", self, "_disegna_scia")
	get_parent().call_deferred("add_child", scia)
	connect("body_entered", self, "_on_body_entered")


func _altezza(xx: float) -> float:
	return -sin(xx / larghezza_giro * onde_nel_giro * TAU) * onda


func _process(delta):
	tempo += delta
	# ali che sbattono velocissime
	var battito: float = abs(sin(tempo * 52.0))
	ala_dietro.scale.y = Parti.SCALA * (0.3 + 0.7 * abs(sin(tempo * 52.0 + 0.8)))
	ala_davanti.scale.y = Parti.SCALA * (0.3 + 0.7 * battito)
	var inclinazione := 0.0
	if pausa > 0:
		# annusa l'aria: dondola il muso
		pausa -= delta
		inclinazione = sin(tempo * 14.0) * 0.18
		if pausa <= 0:
			direzione = -direzione
	else:
		x += direzione * velocita * delta
		if x >= larghezza_giro or x <= 0.0:
			x = clamp(x, 0.0, larghezza_giro)
			pausa = pausa_ai_capi
		# si inclina seguendo la salita o la discesa dell'onda
		var pendenza := (_altezza(x + direzione * 6.0) - _altezza(x)) / 6.0
		inclinazione = clamp(pendenza * direzione, -0.5, 0.5) * 0.6
	position = partenza + Vector2(x, _altezza(x) + sin(tempo * 7.0) * 3.0)
	# si gira piano (per un attimo è di profilo stretto: sembra una piroetta)
	aspetto.scale.x = move_toward(aspetto.scale.x, direzione, delta * 6.0)
	aspetto.rotation = lerp(aspetto.rotation, inclinazione, min(1.0, delta * 8.0))
	if contenta > 0:
		contenta -= delta
		aspetto.rotation = (1.0 - contenta / 0.7) * TAU
		aspetto.position.y = -sin(contenta / 0.7 * PI) * 14.0
	else:
		aspetto.position.y = 0.0
	voce.pitch_scale = 1.0 if pausa > 0 else 1.08


func _on_body_entered(altro):
	if altro.is_in_group("pulcino") and altro.colpito(global_position.x):
		contenta = 0.7
		Effetti.sbuffo(get_parent(), position, Color(1.0, 0.9, 0.4), 8, 90.0)


# Puntini di polline lungo tutto il giro
func _disegna_scia():
	var xx := 0.0
	while xx <= larghezza_giro:
		var c := Vector2(xx, _altezza(xx))
		var punti := PoolVector2Array()
		for k in range(6):
			var a := TAU * k / 6.0
			punti.append(c + Vector2(cos(a), sin(a)) * 2.6)
		scia.draw_colored_polygon(punti, Color(1.0, 0.9, 0.45, 0.5))
		xx += 22.0
