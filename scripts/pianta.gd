extends StaticBody2D
# Pianta che si piega (girasole o canna del mais): ci si atterra sopra, si piega sotto il peso
# e rilancia il pulcino in alto con un "boing", poi torna dritta ondeggiando.
# La posizione è la base della pianta, a terra. Sulla cima si atterra passando anche da sotto.

const Parti = preload("res://scripts/parti.gd")
const Effetti = preload("res://scripts/effetti.gd")

enum Tipo { GIRASOLE, MAIS }

const IMMAGINI := {
	Tipo.GIRASOLE: preload("res://assets/grafica/orto/girasole.svg"),
	Tipo.MAIS: preload("res://assets/grafica/orto/mais.svg"),
}

export(Tipo) var tipo := Tipo.GIRASOLE  # che pianta è
export var forza_rimbalzo := 780.0  # quanto rilancia in alto: circa come un salto pieno

var disegno: Sprite
var sensore := Area2D.new()  # sente quando il pulcino è appoggiato sulla cima
var attesa := 0.0
var tempo := 0.0
var oscillazione := 0.0  # quanto sta ancora ondeggiando dopo un rimbalzo
var altezza := 0.0


func _ready():
	var immagine: Texture = IMMAGINI[tipo]
	altezza = immagine.get_height() * Parti.SCALA
	disegno = Parti.crea(self, immagine, Vector2(immagine.get_width() / 2.0, immagine.get_height()), Vector2.ZERO)
	# piattaforma sottile sulla cima: ci si sale anche da sotto
	var cima := CollisionShape2D.new()
	var rettangolo := RectangleShape2D.new()
	rettangolo.extents = Vector2(30, 6)
	cima.shape = rettangolo
	cima.position = Vector2(0, -altezza + 14)
	cima.one_way_collision = true
	add_child(cima)
	# sensore appena sopra la cima
	var forma := CollisionShape2D.new()
	var zona := RectangleShape2D.new()
	zona.extents = Vector2(30, 10)
	forma.shape = zona
	forma.position = Vector2(0, -altezza + 2)
	sensore.add_child(forma)
	add_child(sensore)


func _physics_process(delta):
	tempo += delta
	attesa -= delta
	# ondeggia piano, e di più subito dopo un rimbalzo
	oscillazione = move_toward(oscillazione, 0.0, delta * 0.5)
	disegno.rotation = sin(tempo * 2.0 + position.x) * 0.02 + sin(tempo * 9.0) * oscillazione * 0.25
	if attesa > 0:
		return
	for corpo in sensore.get_overlapping_bodies():
		if corpo.is_in_group("pulcino") and corpo.velocita.y >= 0:
			_rimbalza(corpo)
			return


func _rimbalza(pulcino):
	attesa = 0.3
	oscillazione = 1.0
	pulcino.rimbalza(forza_rimbalzo)
	Suoni.suona("boing", 0.1)
	Effetti.sbuffo(get_parent(), position + Vector2(0, -altezza + 10), Color(1.0, 0.85, 0.3), 8, 120.0)
	# si piega sotto il peso e torna su come una molla
	var tween := Tween.new()
	add_child(tween)
	tween.interpolate_property(disegno, "scale", Vector2(Parti.SCALA * 1.1, Parti.SCALA * 0.82), Vector2(Parti.SCALA, Parti.SCALA), 0.6, Tween.TRANS_ELASTIC, Tween.EASE_OUT)
	tween.start()
	yield(tween, "tween_all_completed")
	tween.queue_free()
