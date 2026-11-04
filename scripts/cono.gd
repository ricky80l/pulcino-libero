extends KinematicBody2D
# Cono di filato che rotola: cade dal ripiano, rotola dritto srotolando il filo dietro di sé
# e si ferma sbattendo contro un ostacolo (o cade in una fossa). Se tocca il pulcino, lui riparte dal nido.
# Lo crea coni.gd; si salta.

const Parti = preload("res://scripts/parti.gd")
const Effetti = preload("res://scripts/effetti.gd")
const CONO_ROTOLA = preload("res://assets/grafica/magazzino/cono_rotola.png")
const RAGGIO := 15.0

var verso := 1.0  # da che parte rotola
var colore := Color.white
var velocita_rotola := 230.0  # più lento del pulcino, così si può sempre scappare o saltarlo
var gravita := 2200.0
var velocita := Vector2.ZERO
var a_terra := false
var vita := 0.0
var finito := false
var disegno: Sprite
var filo := Line2D.new()  # il filo srotolato, lasciato sul pavimento
var pulcino = null


func _ready():
	collision_layer = 0  # nessuno ci sbatte contro; lui invece sbatte contro muri e ostacoli
	var forma := CollisionShape2D.new()
	var cerchio := CircleShape2D.new()
	cerchio.radius = RAGGIO
	forma.shape = cerchio
	add_child(forma)
	disegno = Parti.crea(self, CONO_ROTOLA, Vector2(32, 32), Vector2.ZERO)
	disegno.modulate = colore
	# il filo sta nel livello, dietro al cono, così resta dove è stato srotolato
	filo.width = 3.0
	filo.default_color = colore.darkened(0.1)
	filo.z_index = -1
	get_parent().call_deferred("add_child", filo)
	velocita = Vector2(verso * 60.0, -120.0)  # si ribalta giù dal ripiano
	var trovati: Array = get_tree().get_nodes_in_group("pulcino")
	if not trovati.empty():
		pulcino = trovati[0]
		add_collision_exception_with(pulcino)  # non lo spinge: lo fa solo ripartire dal nido


func _physics_process(delta):
	if finito:
		return
	vita += delta
	velocita.y = min(velocita.y + gravita * delta, 900.0)
	if a_terra:
		velocita.x = verso * velocita_rotola
	var cadeva := not a_terra
	velocita = move_and_slide(velocita, Vector2.UP)
	a_terra = is_on_floor()
	if a_terra and cadeva:
		_suona("rotola", -6.0)
		Effetti.sbuffo(get_parent(), position + Vector2(0, RAGGIO), Color(0.85, 0.85, 0.82), 5, 70.0)
	# gira come una ruota e srotola il filo
	disegno.rotation += velocita.x / RAGGIO * delta
	if a_terra:
		var punto := position + Vector2(0, RAGGIO - 1)
		if filo.get_point_count() == 0 or filo.get_point_position(filo.get_point_count() - 1).distance_to(punto) > 12:
			filo.add_point(punto)
	elif filo.get_point_count() > 0:
		filo.add_point(position)  # cadendo dal bordo il filo scende con lui
	# tocca il pulcino?
	if pulcino and position.distance_to(pulcino.global_position + Vector2(0, 4)) < RAGGIO + 18:
		pulcino.colpito(position.x)
	if a_terra and is_on_wall():
		_fine(true)
	elif position.y > 900 or vita > 12.0:
		_fine(false)


# Il cono sbatte e si sfascia in un batuffolo di filo; il filo sul pavimento svanisce piano
func _fine(sbatte: bool):
	finito = true
	if sbatte:
		_suona("botta", -8.0)
		Effetti.sbuffo(get_parent(), position, colore, 10, 140.0)
	var tween := Tween.new()
	get_parent().add_child(tween)
	tween.interpolate_property(filo, "modulate:a", 1.0, 0.0, 1.5, Tween.TRANS_LINEAR, Tween.EASE_IN, 0.8)
	tween.start()
	tween.connect("tween_all_completed", filo, "queue_free")
	tween.connect("tween_all_completed", tween, "queue_free")
	queue_free()


func _suona(nome: String, volume_base: float):
	if pulcino == null:
		return
	var distanza: float = global_position.distance_to(pulcino.global_position)
	if distanza < 650:
		Suoni.suona(nome, 0.15, volume_base - distanza / 650.0 * 14.0)
