extends Node2D
# Il pulcino sulla mappa: lo stesso disegno animato dei livelli, che cammina lungo il sentiero.
# La mappa lo muove; qui ci sono solo i valori che l'aspetto legge per animarsi.

var velocita := Vector2.ZERO  # in movimento le zampe zampettano
var era_a_terra := true
var timer_sbalzo := 0.0
var tempo := 0.0
var aspetto: Node2D


func _ready():
	aspetto = Node2D.new()
	aspetto.set_script(preload("res://scripts/aspetto_pulcino.gd"))
	add_child(aspetto)


func cammina(direzione_x: float):
	velocita.x = 200.0 * direzione_x
	if direzione_x != 0:
		aspetto.scale.x = sign(direzione_x)


func fermo():
	velocita.x = 0.0


func pigola():
	aspetto.pigola()


func _process(delta):
	tempo += delta
	# ondeggia camminando, come nei livelli
	if velocita.x != 0:
		aspetto.rotation = sin(tempo * 18.0) * 0.12
	else:
		aspetto.rotation = lerp(aspetto.rotation, 0.0, min(1.0, 15.0 * delta))
