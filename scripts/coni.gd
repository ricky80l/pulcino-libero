extends Node2D
# Punto da cui cadono i coni di filato (in cima a uno scaffale o sul soppalco).
# Ogni tanto un cono in piedi traballa ("tic-tic-tic"): è l'avviso. Poi si ribalta, cade
# e rotola nella direzione scelta srotolando il filo. Funziona solo quando il pulcino è vicino.
# La posizione è la base del cono in piedi, sul ripiano.

const Parti = preload("res://scripts/parti.gd")
const CONO_IN_PIEDI = preload("res://assets/grafica/magazzino/cono_in_piedi.png")
const CONO = preload("res://scripts/cono.gd")
const COLORI := [Color("f4a7b9"), Color("f2f0ea"), Color("5a5a62"), Color("6bbf8a"), Color("d9c29a"),
		Color("e0584a"), Color("8fb8e8"), Color("f2c14e")]

enum Stato { ATTESA, TRABALLA }

export var verso := 1.0  # da che parte rotola: 1 = destra, -1 = sinistra
export var attesa_minima := 2.5  # secondi minimi tra un cono e l'altro
export var attesa_massima := 4.5  # secondi massimi tra un cono e l'altro
export var durata_avviso := 0.9  # quanto traballa prima di cadere (secondi)
export var distanza_attiva := 900.0  # lancia coni solo se il pulcino è più vicino di così (pixel)

var stato: int = Stato.ATTESA
var timer := 0.0
var tempo := 0.0
var rng := RandomNumberGenerator.new()
var cono: Sprite  # il prossimo cono, in piedi sul ripiano
var pulcino = null


func _ready():
	rng.randomize()
	timer = rng.randf_range(attesa_minima, attesa_massima)
	cono = Parti.crea(self, CONO_IN_PIEDI, Vector2(30, 98), Vector2.ZERO)
	_nuovo_colore()


func _nuovo_colore():
	cono.modulate = COLORI[rng.randi() % COLORI.size()]


func _physics_process(delta):
	tempo += delta
	if pulcino == null:
		var trovati: Array = get_tree().get_nodes_in_group("pulcino")
		if not trovati.empty():
			pulcino = trovati[0]
	if pulcino == null or global_position.distance_to(pulcino.global_position) > distanza_attiva:
		cono.rotation = 0.0
		return
	timer -= delta
	match stato:
		Stato.ATTESA:
			cono.rotation = 0.0
			if timer <= 0:
				stato = Stato.TRABALLA
				timer = durata_avviso
				_suona("traballa", -2.0)
		Stato.TRABALLA:
			# traballa sempre più forte, poi si ribalta
			var forza := 1.0 - timer / durata_avviso
			cono.rotation = sin(tempo * 28.0) * (0.08 + 0.12 * forza)
			if timer <= 0:
				_cade()
				stato = Stato.ATTESA
				timer = rng.randf_range(attesa_minima, attesa_massima)


func _cade():
	var c := KinematicBody2D.new()
	c.set_script(CONO)
	c.verso = verso
	c.colore = cono.modulate
	c.position = position + Vector2(verso * 14, -16)
	get_parent().add_child(c)
	# il cono sul ripiano ricompare dopo un attimo, di un altro colore
	cono.visible = false
	yield(get_tree().create_timer(0.6), "timeout")
	_nuovo_colore()
	cono.visible = true


func _suona(nome: String, volume_base: float):
	var distanza: float = global_position.distance_to(pulcino.global_position)
	if distanza < 650:
		Suoni.suona(nome, 0.15, volume_base - distanza / 650.0 * 14.0)
