extends StaticBody2D
# Ostacolo che si rompe a beccate: sacco di mangime o balla di paglia.
# La posizione è il centro della base, appoggiata a terra.
# Ogni beccata toglie un punto di resistenza: finché resiste traballa, poi va in pezzi.

const Parti = preload("res://scripts/parti.gd")
const PEZZI = preload("res://scripts/pezzi.gd")

enum Tipo { SACCO, BALLA }

const IMMAGINI := {
	Tipo.SACCO: preload("res://assets/grafica/ostacoli/sacco.svg"),
	Tipo.BALLA: preload("res://assets/grafica/ostacoli/balla.svg"),
}
const MISURE := {Tipo.SACCO: Vector2(60, 70), Tipo.BALLA: Vector2(90, 60)}

export(Tipo) var tipo := Tipo.SACCO  # che ostacolo è
export var resistenza := 1  # quante beccate servono per romperlo

var disegno: Sprite


func _ready():
	var misura: Vector2 = MISURE[tipo]
	var rettangolo := RectangleShape2D.new()
	rettangolo.extents = misura / 2
	var forma := CollisionShape2D.new()
	forma.shape = rettangolo
	forma.position = Vector2(0, -misura.y / 2)
	add_child(forma)
	var immagine: Texture = IMMAGINI[tipo]
	disegno = Parti.crea(self, immagine, Vector2(immagine.get_width() / 2.0, immagine.get_height()), Vector2.ZERO)


# Chiamata dal pulcino quando lo becca; verso = da che parte arriva il colpo
func becca(verso: float):
	resistenza -= 1
	if resistenza > 0:
		_traballa(verso)
	else:
		_rompi(verso)


func _traballa(verso: float):
	Suoni.suona("botta", 0.1)
	_sbriciola(verso, 5)
	var tween := Tween.new()
	add_child(tween)
	tween.interpolate_property(disegno, "scale", Vector2(0.58, 0.44), Vector2(0.5, 0.5), 0.4, Tween.TRANS_ELASTIC, Tween.EASE_OUT)
	tween.interpolate_property(disegno, "rotation", verso * 0.12, 0.0, 0.4, Tween.TRANS_ELASTIC, Tween.EASE_OUT)
	tween.start()
	yield(tween, "tween_all_completed")
	tween.queue_free()


func _rompi(verso: float):
	Suoni.suona("rotto", 0.1)
	_sbriciola(verso, 22)
	# non blocca più il passaggio
	collision_layer = 0
	collision_mask = 0
	queue_free()


func _sbriciola(verso: float, quanti: int):
	var pezzi = Node2D.new()
	pezzi.set_script(PEZZI)
	pezzi.position = position + Vector2(0, -MISURE[tipo].y / 2)
	get_parent().add_child(pezzi)
	pezzi.lancia(tipo, verso, quanti, MISURE[tipo])
