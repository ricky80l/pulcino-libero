extends Area2D
# Talpa dispettosa: vive in una buca nel terreno. Ogni tanto il mucchietto di terra trema (avviso),
# poi spunta con un "bu!", resta fuori un attimo e si rintana. Fa male solo quando è fuori:
# si passa quando è sotto terra, oppure le si salta sopra.
# La posizione è il centro della buca, al livello del terreno.

const Parti = preload("res://scripts/parti.gd")
const Effetti = preload("res://scripts/effetti.gd")
const TALPA = preload("res://assets/grafica/talpa/talpa.svg")
const TALPA_BU = preload("res://assets/grafica/talpa/talpa_bu.svg")
const ZAMPA = preload("res://assets/grafica/talpa/zampa.svg")

enum Stato { SOTTO, AVVISO, SU, GIU }

export var attesa_minima := 2.5  # quanto resta sotto terra tra una spuntata e l'altra: cambia ogni volta
export var attesa_massima := 4.0
export var distanza_udibile := 650.0  # oltre questa distanza dal pulcino la talpa non si sente
export var durata_avviso := 0.9  # quanto trema la terra prima che spunti: il tempo per fermarsi
export var durata_su := 1.1  # quanto resta fuori

const PROFONDITA := 72.0  # quanto scende per sparire sotto terra
const COLORE_TERRA := Color("7a5230")

var stato: int = Stato.SOTTO
var timer := 0.0
var tempo := 0.0
var su := 0.0  # 0 = tutta sotto terra, 1 = tutta fuori
var pulcino = null

var talpa: Node2D = Node2D.new()  # la talpa con le zampe, dietro al terreno
var disegno: Sprite
var zampa_sx: Sprite
var zampa_dx: Sprite
var mucchio: Polygon2D  # il bordo di terra davanti, che trema prima che spunti


func _ready():
	z_index = 1  # il bordo davanti sta sopra il terreno
	timer = rand_range(0.5, attesa_massima)  # le talpe non spuntano tutte insieme
	# buio della buca, dietro a tutto
	var buio := _ellisse(Vector2(0, 0), Vector2(32, 9), Color("2a1a10"))
	buio.z_index = -3
	add_child(buio)
	# la talpa sta dietro al terreno, così la parte sotto terra non si vede
	talpa.z_index = -2
	add_child(talpa)
	disegno = Parti.crea(talpa, TALPA, Vector2(60, 134), Vector2(0, 0))
	# mucchietto di terra davanti alla buca
	mucchio = _ellisse(Vector2(0, 4), Vector2(40, 8), COLORE_TERRA)
	add_child(mucchio)
	# zampe aggrappate al bordo, davanti al terreno
	zampa_sx = Parti.crea(self, ZAMPA, Vector2(22, 30), Vector2(-24, 2))
	zampa_dx = Parti.crea(self, ZAMPA, Vector2(22, 30), Vector2(24, 2))
	# zona che tocca il pulcino: la parte della talpa fuori dalla buca
	var forma := CollisionShape2D.new()
	var rettangolo := RectangleShape2D.new()
	rettangolo.extents = Vector2(22, 26)
	forma.shape = rettangolo
	forma.position = Vector2(0, -28)
	add_child(forma)
	_aggiorna_disegno()


func _ellisse(centro: Vector2, raggi: Vector2, colore: Color) -> Polygon2D:
	var p := Polygon2D.new()
	var punti := PoolVector2Array()
	for i in range(24):
		var a := i * TAU / 24
		punti.append(centro + Vector2(cos(a) * raggi.x, sin(a) * raggi.y))
	p.polygon = punti
	p.color = colore
	p.antialiased = true
	return p


func _physics_process(delta):
	tempo += delta
	timer -= delta
	match stato:
		Stato.SOTTO:
			if timer <= 0:
				stato = Stato.AVVISO
				timer = durata_avviso
				_suona("scava", -8.0)
		Stato.AVVISO:
			if int(tempo * 10) != int((tempo - delta) * 10):
				Effetti.sbuffo(get_parent(), position + Vector2(0, -4), COLORE_TERRA, 3, 110.0)
			if timer <= 0:
				stato = Stato.SU
				timer = durata_su
				_suona("bu", -2.0)
		Stato.SU:
			su = move_toward(su, 1.0, delta * 7.0)  # spunta di scatto
			if timer <= 0:
				stato = Stato.GIU
		Stato.GIU:
			su = move_toward(su, 0.0, delta * 5.0)
			if su <= 0:
				stato = Stato.SOTTO
				timer = rand_range(attesa_minima, attesa_massima)

	if pulcino == null:
		var trovati := get_tree().get_nodes_in_group("pulcino")
		if trovati.size() > 0:
			pulcino = trovati[0]
	# fa male solo quando è fuori per più di metà
	if su > 0.5:
		for altro in get_overlapping_bodies():
			if altro == pulcino:
				pulcino.colpito(global_position.x)
	_aggiorna_disegno()


# Si sente solo se il pulcino è vicino, e più piano quanto più è lontano
func _suona(nome: String, volume_base: float):
	if pulcino == null:
		return
	var distanza: float = global_position.distance_to(pulcino.global_position)
	if distanza > distanza_udibile:
		return
	Suoni.suona(nome, 0.15, volume_base - distanza / distanza_udibile * 14.0)


func _aggiorna_disegno():
	talpa.position.y = (1.0 - su) * PROFONDITA
	# la terra trema durante l'avviso
	mucchio.position.x = sin(tempo * 60.0) * 3.0 if stato == Stato.AVVISO else 0.0
	# appena spuntata fa "bu!" a bocca aperta, poi si guarda intorno
	var appena_spuntata: bool = stato == Stato.SU and timer > durata_su - 0.45
	disegno.texture = TALPA_BU if appena_spuntata else TALPA
	disegno.rotation = sin(tempo * 4.0) * 0.08 if (stato == Stato.SU and not appena_spuntata) else 0.0
	# le zampe si aggrappano al bordo quando è fuori
	zampa_sx.visible = su > 0.7
	zampa_dx.visible = su > 0.7
