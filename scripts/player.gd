extends KinematicBody2D
# Il pulcino: camminata e salto. Tutti i valori qui sotto si regolano dall'Ispettore.

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

var velocita := Vector2.ZERO
var timer_coyote := 0.0
var timer_prenota := 0.0
var timer_invulnerabile := 0.0
var punto_sicuro := Vector2.ZERO  # da dove riparte: l'inizio, poi l'ultimo nido raggiunto

onready var aspetto := $Aspetto


func _ready():
	add_to_group("pulcino")
	punto_sicuro = position


# Toccato da un nemico: torna all'ultimo punto sicuro, senza altre punizioni
func colpito():
	if timer_invulnerabile <= 0:
		riparti()


func riparti():
	position = punto_sicuro
	velocita = Vector2.ZERO
	timer_invulnerabile = tempo_invulnerabile


func _physics_process(delta):
	# Lampeggia mentre è invulnerabile
	if timer_invulnerabile > 0:
		timer_invulnerabile -= delta
		aspetto.visible = timer_invulnerabile <= 0 or fmod(timer_invulnerabile, 0.2) > 0.1

	var a_terra := is_on_floor()

	# Camminata con accelerazione e frenata morbide
	var direzione := Input.get_action_strength("move_right") - Input.get_action_strength("move_left")
	var fattore := 1.0 if a_terra else controllo_in_aria
	if direzione != 0:
		velocita.x = move_toward(velocita.x, direzione * velocita_max, accelerazione * fattore * delta)
		aspetto.scale.x = sign(direzione)
	else:
		velocita.x = move_toward(velocita.x, 0, frenata * fattore * delta)

	# Margine coyote: resta "a terra" per un attimo dopo aver lasciato il bordo
	if a_terra:
		timer_coyote = tempo_coyote
	else:
		timer_coyote -= delta

	# Salto prenotato: ricorda la pressione per un attimo
	if Input.is_action_just_pressed("jump"):
		timer_prenota = tempo_prenota_salto
	else:
		timer_prenota -= delta

	if timer_prenota > 0 and timer_coyote > 0:
		velocita.y = -forza_salto
		timer_prenota = 0
		timer_coyote = 0

	# Salto più basso se lasci presto il tasto
	if Input.is_action_just_released("jump") and velocita.y < 0:
		velocita.y *= taglio_salto

	# Gravità: più forte in discesa
	var g := gravita if velocita.y < 0 else gravita_caduta
	velocita.y = min(velocita.y + g * delta, velocita_caduta_max)

	velocita = move_and_slide(velocita, Vector2.UP)

	# Se cade fuori dallo schermo, riparte dall'ultimo punto sicuro
	if position.y > 1000:
		riparti()
