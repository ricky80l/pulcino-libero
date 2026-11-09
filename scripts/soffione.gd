extends StaticBody2D
# Soffione gigante del prato. Beccandolo, i semi volano via in un soffio e lì nasce per qualche secondo
# una corrente d'aria (vedi corrente.gd): planandoci dentro si sale. Dopo un po' i semi ricrescono.
# Non blocca il pulcino (sta su un livello di collisione suo): lo "sente" solo il becco.
# La posizione è la base dello stelo, a terra.

const Parti = preload("res://scripts/parti.gd")
const Effetti = preload("res://scripts/effetti.gd")
const PIENO = preload("res://assets/grafica/prato/soffione.png")
const SPOGLIO = preload("res://assets/grafica/prato/soffione_spoglio.png")
const SEME = preload("res://assets/grafica/prato/seme.png")
const CORRENTE = preload("res://scripts/corrente.gd")

export var altezza_corrente := 420.0  # quanto in alto porta la corrente che nasce
export var durata_corrente := 7.0  # quanti secondi dura
export var ricrescita := 9.0  # dopo quanti secondi i semi ricrescono

var disegno: Sprite
var pieno := true
var tempo := 0.0


func _ready():
	collision_layer = 2  # il pulcino non ci sbatte contro, ma la beccata lo trova
	collision_mask = 0
	var forma := CollisionShape2D.new()
	var rettangolo := RectangleShape2D.new()
	rettangolo.extents = Vector2(34, 75)
	forma.shape = rettangolo
	forma.position = Vector2(0, -75)
	add_child(forma)
	disegno = Parti.crea(self, PIENO, Vector2(80, 296), Vector2.ZERO)
	tempo = position.x * 0.01


func _process(delta):
	tempo += delta
	disegno.rotation = sin(tempo * 1.3) * 0.03  # ondeggia al vento


func becca(verso: float):
	if not pieno:
		return
	pieno = false
	disegno.texture = SPOGLIO
	Suoni.suona("plana", 0.05, 0.0, 1.1)
	Effetti.sbuffo(get_parent(), position + Vector2(0, -118), Color(1, 1, 1), 16, 140.0)
	_semi_al_vento(verso)
	# nasce la corrente d'aria
	var corrente := Area2D.new()
	corrente.set_script(CORRENTE)
	corrente.position = position
	corrente.larghezza = 110.0
	corrente.altezza = altezza_corrente
	corrente.durata = durata_corrente
	get_parent().add_child(corrente)
	# dopo un po' i semi ricrescono
	yield(get_tree().create_timer(ricrescita), "timeout")
	if is_inside_tree():
		disegno.texture = PIENO
		disegno.scale = Vector2.ONE * Parti.SCALA * 0.6
		var tween := Tween.new()
		add_child(tween)
		tween.interpolate_property(disegno, "scale", disegno.scale, Vector2.ONE * Parti.SCALA, 0.5, Tween.TRANS_BACK, Tween.EASE_OUT)
		tween.start()
		pieno = true
		yield(tween, "tween_all_completed")
		tween.queue_free()


# I semi volano via in alto, girando, un po' dalla parte opposta al becco
func _semi_al_vento(verso: float):
	var p := CPUParticles2D.new()
	p.position = position + Vector2(0, -118)
	p.texture = SEME
	p.one_shot = true
	p.explosiveness = 0.85
	p.amount = 26
	p.lifetime = 2.6
	p.emission_shape = CPUParticles2D.EMISSION_SHAPE_SPHERE
	p.emission_sphere_radius = 28.0
	p.direction = Vector2(verso * 0.6, -1)
	p.spread = 50.0
	p.gravity = Vector2(verso * 20.0, -30.0)
	p.initial_velocity = 110.0
	p.initial_velocity_random = 0.6
	p.angular_velocity = 90.0
	p.angular_velocity_random = 1.0
	p.scale_amount = 0.5
	p.emitting = true
	get_parent().add_child(p)
	yield(get_tree().create_timer(3.0), "timeout")
	if is_instance_valid(p):
		p.queue_free()
