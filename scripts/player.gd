extends KinematicBody2D
# Il pulcino: camminata e salto. Tutti i valori qui sotto si regolano dall'Ispettore.

const Effetti = preload("res://scripts/effetti.gd")
const COLORE_POLVERE := Color(0.88, 0.78, 0.45)

# --- Camminata ---
export var velocita_max := 300.0  # velocità massima in orizzontale (pixel al secondo)
export var accelerazione := 1800.0  # quanto in fretta parte: più alto = scatto più deciso
export var frenata := 2400.0  # quanto in fretta si ferma quando lasci le frecce: più alto = meno scivoloso
export var controllo_in_aria := 0.7  # quanto puoi correggere la direzione in aria (1 = come a terra, 0 = per niente)

# --- Salto ---
export var forza_salto := 760.0  # spinta verso l'alto: più alto = salto più alto
export var gravita := 1800.0  # gravità mentre sale: più bassa = salto più "fluttuante"
export var gravita_caduta := 2600.0  # gravità mentre scende: più alta = ricaduta più decisa
export var taglio_salto := 0.45  # se lasci lo spazio mentre sali, la salita si accorcia (0.3 = taglia molto, 1 = non taglia)
export var velocita_caduta_max := 900.0  # velocità massima di caduta
export var tempo_coyote := 0.1  # secondi in cui puoi ancora saltare dopo essere sceso da un bordo
export var tempo_prenota_salto := 0.1  # se premi salto poco prima di atterrare, salta appena tocca terra

# --- Ripartenza ---
export var tempo_invulnerabile := 1.2  # secondi in cui lampeggia e i nemici non lo toccano, dopo essere ripartito
export var durata_sbalzo := 0.7  # secondi in cui vola via girando quando il topo lo tocca

# --- Beccata ---
export var puo_beccare := false  # il livello lo attiva quando il pulcino ha imparato la beccata
export var durata_beccata := 0.28  # quanto dura il colpo di becco (secondi)
export var pausa_beccata := 0.1  # attesa minima prima della beccata successiva
export var portata_beccata := 30.0  # quanto arriva lontano il becco davanti al pulcino (pixel)

# --- Doppio salto ---
export var puo_doppio_salto := false  # il livello lo attiva quando il pulcino ha imparato il doppio salto
export var forza_doppio_salto := 760.0  # spinta del secondo salto: sempre piena, anche con un tocco veloce

# --- Animazioni esagerate ---
export var allunga_salto := 0.35  # quanto si allunga saltando (0 = niente)
export var schiaccia_atterraggio := 0.4  # quanto si schiaccia atterrando (0 = niente)
export var dondolio_camminata := 0.15  # quanto ondeggia camminando
export var ritorno_forma := 12.0  # quanto in fretta torna alla forma normale

var velocita := Vector2.ZERO
var timer_coyote := 0.0
var timer_prenota := 0.0
var timer_invulnerabile := 0.0
var timer_sbalzo := 0.0
var punto_sicuro := Vector2.ZERO  # da dove riparte: l'inizio, poi l'ultimo nido raggiunto
var verso := 1.0  # 1 = guarda a destra, -1 = a sinistra
var deformazione := Vector2.ONE
var era_a_terra := true
var tempo := 0.0
var timer_beccata := 0.0
var attesa_beccata := 0.0
var colpiti := []  # ostacoli già colpiti in questa beccata
var doppio_usato := false  # il secondo salto si può fare una sola volta prima di toccare terra

onready var aspetto := $Aspetto


func _ready():
	add_to_group("pulcino")
	punto_sicuro = position
	aspetto.position = Vector2(0, 20)  # il disegno si deforma partendo dai piedi


# Toccato da un nemico: vola via con un "pio-pio!" e torna all'ultimo nido. Restituisce true se colpito.
func colpito(da_x := 0.0) -> bool:
	if timer_invulnerabile > 0 or timer_sbalzo > 0:
		return false
	timer_sbalzo = durata_sbalzo
	var lato := 1.0 if position.x >= da_x else -1.0
	velocita = Vector2(lato * 260, -560)
	Suoni.suona("colpito")
	aspetto.pigola()
	return true


func riparti():
	position = punto_sicuro
	velocita = Vector2.ZERO
	timer_sbalzo = 0.0
	timer_beccata = 0.0
	doppio_usato = false
	timer_invulnerabile = tempo_invulnerabile
	aspetto.rotation = 0.0
	deformazione = Vector2.ONE


func _physics_process(delta):
	tempo += delta

	# Sbalzato dal topo: vola girando, poi riparte dal nido
	if timer_sbalzo > 0:
		timer_sbalzo -= delta
		velocita.y += gravita * delta
		velocita = move_and_slide(velocita, Vector2.UP)
		aspetto.rotation += 18.0 * delta * verso
		if timer_sbalzo <= 0:
			riparti()
		return

	# Lampeggia mentre è invulnerabile
	if timer_invulnerabile > 0:
		timer_invulnerabile -= delta
		aspetto.visible = timer_invulnerabile <= 0 or fmod(timer_invulnerabile, 0.2) > 0.1

	var a_terra := is_on_floor()

	if puo_beccare:
		_gestisci_beccata(delta)

	# Camminata con accelerazione e frenata morbide
	var direzione := Input.get_action_strength("move_right") - Input.get_action_strength("move_left")
	var fattore := 1.0 if a_terra else controllo_in_aria
	if direzione != 0:
		velocita.x = move_toward(velocita.x, direzione * velocita_max, accelerazione * fattore * delta)
		verso = sign(direzione)
	else:
		velocita.x = move_toward(velocita.x, 0, frenata * fattore * delta)

	# Margine coyote: resta "a terra" per un attimo dopo aver lasciato il bordo
	if a_terra:
		timer_coyote = tempo_coyote
		doppio_usato = false
	else:
		timer_coyote -= delta

	# Salto prenotato: ricorda la pressione per un attimo
	if Input.is_action_just_pressed("jump"):
		timer_prenota = tempo_prenota_salto
		# in aria (e oltre il margine coyote): secondo salto con un battito d'ali
		if puo_doppio_salto and timer_coyote <= 0 and not doppio_usato:
			_doppio_salto()
			timer_prenota = 0
	else:
		timer_prenota -= delta

	if timer_prenota > 0 and timer_coyote > 0:
		velocita.y = -forza_salto
		timer_prenota = 0
		timer_coyote = 0
		deformazione = Vector2(1.0 - allunga_salto * 0.6, 1.0 + allunga_salto)
		Suoni.suona("salto")
		aspetto.pigola()
		Effetti.sbuffo(get_parent(), position + Vector2(0, 20), COLORE_POLVERE, 6, 90.0)

	# Salto più basso se lasci presto il tasto (non vale per il doppio salto, che è sempre pieno)
	if Input.is_action_just_released("jump") and velocita.y < 0 and not doppio_usato:
		velocita.y *= taglio_salto

	# Gravità: più forte in discesa
	var g := gravita if velocita.y < 0 else gravita_caduta
	velocita.y = min(velocita.y + g * delta, velocita_caduta_max)

	var caduta := velocita.y
	velocita = move_and_slide(velocita, Vector2.UP)

	# Atterraggio: si schiaccia, solleva polvere, "puf"
	var a_terra_ora := is_on_floor()
	if a_terra_ora and not era_a_terra and caduta > 200:
		var forza := clamp(caduta / velocita_caduta_max, 0.3, 1.0)
		deformazione = Vector2(1.0 + schiaccia_atterraggio * forza, 1.0 - schiaccia_atterraggio * forza)
		Suoni.suona("atterra", 0.15, -4.0)
		Effetti.sbuffo(get_parent(), position + Vector2(0, 20), COLORE_POLVERE, int(6 + 8 * forza), 80.0 + 100.0 * forza)
	era_a_terra = a_terra_ora

	# Torna piano piano alla forma normale; ondeggia camminando
	deformazione = deformazione.linear_interpolate(Vector2.ONE, min(1.0, ritorno_forma * delta))
	if timer_beccata > 0:
		# beccata: si sbilancia in avanti col becco e torna su
		var fase := sin((1.0 - timer_beccata / durata_beccata) * PI)
		aspetto.rotation = verso * fase * 0.6
		aspetto.position.x = verso * fase * 8.0
	elif a_terra_ora and abs(velocita.x) > 30:
		aspetto.rotation = sin(tempo * 18.0) * dondolio_camminata
		aspetto.position.x = 0.0
	else:
		aspetto.rotation = lerp(aspetto.rotation, 0.0, min(1.0, 15.0 * delta))
		aspetto.position.x = 0.0
	aspetto.scale = Vector2(verso * deformazione.x, deformazione.y)

	# Se cade fuori dallo schermo, riparte dall'ultimo punto sicuro
	if position.y > 1000:
		riparti()


# Rilanciato in alto da una pianta che si piega: dopo il rimbalzo si può di nuovo fare il doppio salto
func rimbalza(forza: float):
	velocita.y = -forza
	doppio_usato = false
	timer_coyote = 0
	deformazione = Vector2(1.0 - allunga_salto * 0.6, 1.0 + allunga_salto)
	aspetto.pigola()


func _doppio_salto():
	doppio_usato = true
	velocita.y = -forza_doppio_salto
	deformazione = Vector2(1.0 + allunga_salto * 0.5, 1.0 - allunga_salto * 0.3)  # si gonfia come per spiccare il volo
	Suoni.suona("doppio", 0.08)
	aspetto.sbatti_ali()
	Effetti.sbuffo(get_parent(), position + Vector2(0, 10), Color(1.0, 0.93, 0.62), 10, 140.0)


# Beccata: col tasto X (o il pulsante col becco) colpisce quello che ha davanti, anche in aria
func _gestisci_beccata(delta):
	attesa_beccata -= delta
	if timer_beccata > 0:
		timer_beccata -= delta
		if timer_beccata > durata_beccata * 0.4:  # il becco colpisce nella prima parte del movimento
			_colpisci()
	elif attesa_beccata <= 0 and Input.is_action_just_pressed("peck"):
		timer_beccata = durata_beccata
		attesa_beccata = durata_beccata + pausa_beccata
		colpiti = []
		deformazione = Vector2(1.2, 0.88)
		Suoni.suona("becco", 0.1)
		aspetto.pigola()
		_colpisci()


func _colpisci():
	var zona := RectangleShape2D.new()
	zona.extents = Vector2(portata_beccata * 0.5 + 6, 16)
	var domanda := Physics2DShapeQueryParameters.new()
	domanda.set_shape(zona)
	domanda.transform = Transform2D(0, global_position + Vector2(verso * (20 + portata_beccata * 0.5), -4))
	domanda.exclude = [self]
	for risultato in get_world_2d().direct_space_state.intersect_shape(domanda, 8):
		var cosa = risultato["collider"]
		if cosa.has_method("becca") and not colpiti.has(cosa):
			colpiti.append(cosa)
			cosa.becca(verso)
