extends Area2D
# Corrente d'aria del prato: una colonna d'aria chiara con riccioli, petali e semi che salgono.
# Se il pulcino ci entra in volo tenendo premuto salto (cioè planando), la corrente lo solleva: così arriva in alto.
# Può essere fissa, oppure nascere da un soffione beccato e durare pochi secondi.
# La posizione è la base della colonna, al centro.

export var larghezza := 100.0  # quanto è larga la colonna
export var altezza := 400.0  # quanto è alta: fin lassù solleva
export var forza_salita := 270.0  # velocità con cui sale il pulcino dentro la corrente (pixel al secondo)
export var durata := 0.0  # 0 = sempre; altrimenti secondi di vita (le correnti dei soffioni)

const COLORI_PETALI := [Color("ff9ec0"), Color("ffd84a"), Color("ffffff"), Color("b48cf2")]

var tempo := 0.0
var forza_visibile := 0.0  # 0..1: compare e scompare piano
var particelle: CPUParticles2D


func _ready():
	add_to_group("correnti")
	var forma := CollisionShape2D.new()
	var rettangolo := RectangleShape2D.new()
	rettangolo.extents = Vector2(larghezza / 2.0, altezza / 2.0)
	forma.shape = rettangolo
	forma.position = Vector2(0, -altezza / 2.0)
	add_child(forma)
	z_index = -2  # davanti al paesaggio, dietro al pulcino
	particelle = CPUParticles2D.new()
	particelle.amount = int(clamp(altezza / 22.0, 8, 30))
	particelle.lifetime = altezza / 150.0
	particelle.preprocess = particelle.lifetime
	particelle.emission_shape = CPUParticles2D.EMISSION_SHAPE_RECTANGLE
	particelle.emission_rect_extents = Vector2(larghezza * 0.4, 6)
	particelle.direction = Vector2(0, -1)
	particelle.spread = 12.0
	particelle.gravity = Vector2.ZERO
	particelle.initial_velocity = 150.0
	particelle.initial_velocity_random = 0.3
	particelle.angular_velocity = 180.0
	particelle.angular_velocity_random = 1.0
	particelle.scale_amount = 4.0
	particelle.scale_amount_random = 0.5
	particelle.color = COLORI_PETALI[int(abs(position.x)) % COLORI_PETALI.size()]
	add_child(particelle)
	forza_visibile = 0.0 if durata > 0 else 1.0


func _process(delta):
	tempo += delta
	if durata > 0:
		# compare in fretta, poi svanisce verso la fine
		var resta := durata - tempo
		forza_visibile = min(1.0, tempo * 3.0) * clamp(resta / 1.2, 0.0, 1.0)
		if resta <= 0:
			queue_free()
			return
	particelle.modulate.a = forza_visibile
	update()


func _physics_process(delta):
	if forza_visibile < 0.3:
		return
	for corpo in get_overlapping_bodies():
		if corpo.is_in_group("pulcino") and corpo.get("puo_planare") and not corpo.is_on_floor() \
				and Input.is_action_pressed("jump"):
			corpo.velocita.y = move_toward(corpo.velocita.y, -forza_salita, 1800.0 * delta)
			corpo.in_corrente = 0.1  # per un attimo niente gravità né frenata della planata: sale ad ali aperte


func _draw():
	# la colonna d'aria e i riccioli che salgono (solo rettangoli e poligoni: leggeri per il telefono)
	var a := forza_visibile
	draw_rect(Rect2(-larghezza / 2.0, -altezza, larghezza, altezza), Color(1, 1, 1, 0.13 * a))
	draw_rect(Rect2(-larghezza * 0.3, -altezza, larghezza * 0.6, altezza), Color(1, 1, 1, 0.07 * a))
	var passo := 70.0
	for corsia in range(3):
		var x: float = (corsia - 1) * larghezza * 0.28
		var y := -fmod(tempo * 120.0 + corsia * 23.0, passo)
		while y > -altezza + 10:
			_ricciolo(Vector2(x + sin(tempo * 2.0 + y * 0.05) * 6.0, y), Color(1, 1, 1, 0.55 * a))
			y -= passo
	# in cima, una freccina che dice "si va su"
	var cima := Vector2(0, -altezza + 14)
	draw_colored_polygon(PoolVector2Array([cima + Vector2(-11, 10), cima + Vector2(0, -6), cima + Vector2(11, 10)]),
			Color(1, 1, 1, 0.75 * a))


# Un ricciolo: mezzaluna sottile
func _ricciolo(c: Vector2, colore: Color):
	var punti := PoolVector2Array()
	for k in range(7):
		var ang := PI + k * PI / 6.0
		punti.append(c + Vector2(cos(ang), sin(ang) * 0.6) * 13.0)
	for k in range(6, -1, -1):
		var ang := PI + k * PI / 6.0
		punti.append(c + Vector2(cos(ang), sin(ang) * 0.6) * 9.5 + Vector2(0, 1.5))
	draw_colored_polygon(punti, colore)
