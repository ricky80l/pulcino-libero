extends Node
# Profondità e luce di un livello. Secondo il tipo:
# - all'aperto (cortile, orto): paesaggio a strati (parallasse) con cielo fermo, colline lontane che scorrono piano
#   e quelle vicine più in fretta, raggi di sole che ondeggiano e pollini nell'aria;
# - pollaio: dentro, fasci di luce dalle fessure delle assi e polvere che brilla; fuori dall'uscita, il paesaggio a strati;
# - magazzino: al chiuso, fasci di luce dai lucernari del soffitto e polvere nell'aria.
# Dappertutto: ombre morbide a terra sotto i personaggi e una luce calda ai bordi dello schermo.

const STRATO = preload("res://scripts/strato.gd")
const VIGNETTA = preload("res://assets/grafica/atmosfera/vignetta.png")

export var tipo := "cortile"  # "cortile", "orto", "pollaio" o "magazzino"

var ombre := []  # [chi la proietta, il disegno dell'ombra]
var sfondo: ParallaxBackground = null


func _ready():
	call_deferred("_prepara")


func _prepara():
	var livello := get_parent()
	if tipo != "magazzino":
		_paesaggio(livello)
	if tipo == "pollaio" or tipo == "magazzino":
		_fasci(livello)
	_particelle(livello)
	_vignetta(livello)
	var pulcino = livello.get_node_or_null("Player")
	if pulcino:
		_aggiungi_ombra(livello, pulcino, 22.0)
	for gruppo in ["Nemici", "Operatori"]:
		if livello.has_node(gruppo):
			for chi in livello.get_node(gruppo).get_children():
				if chi is KinematicBody2D:
					_aggiungi_ombra(livello, chi, 34.0)  # l'oca
				elif gruppo == "Operatori":
					_aggiungi_ombra(livello, chi, 40.0)


# Strati: [tipo di disegno, quanto si muove rispetto al livello (0 = fermo), ogni quanto si ripete (0 = mai)]
func _paesaggio(livello: Node):
	sfondo = ParallaxBackground.new()
	livello.add_child(sfondo)
	var colline: String = "campi" if tipo == "orto" else "colline"
	for s in [["cielo", 0.0, 0.0], ["sole", 0.05, 0.0], ["raggi", 0.05, 0.0], ["nuvole", 0.1, 1800.0],
			["colline_lontane", 0.2, 2048.0], [colline, 0.4, 2048.0], ["siepi", 0.65, 1536.0]]:
		var strato := ParallaxLayer.new()
		strato.motion_scale = Vector2(s[1], 1.0)  # in verticale segue il livello
		if s[2] > 0:
			strato.motion_mirroring = Vector2(s[2], 0)
		var disegno := Node2D.new()
		disegno.set_script(STRATO)
		disegno.tipo = s[0]
		if s[2] > 0:
			disegno.larghezza = s[2]
		strato.add_child(disegno)
		sfondo.add_child(strato)
		if s[0] == "nuvole":
			strato.set_meta("nuvole", true)


# Fasci di luce nel livello (davanti alle pareti): dai lucernari del magazzino o dalle fessure del pollaio
func _fasci(livello: Node):
	var fasci := Node2D.new()
	fasci.set_script(STRATO)
	fasci.tipo = "fasci_lucernari" if tipo == "magazzino" else "fasci_fessure"
	fasci.larghezza = _larghezza_livello(livello)
	fasci.z_index = 2
	livello.add_child(fasci)


func _larghezza_livello(livello: Node) -> float:
	var camera = livello.get_node_or_null("Player/Camera2D")
	return float(camera.limit_right) if camera else 4000.0


func _process(delta):
	# le nuvole passano piano da sole
	if sfondo:
		for strato in sfondo.get_children():
			if strato.has_meta("nuvole"):
				strato.motion_offset.x += 10.0 * delta
	# ombre: sul terreno sotto chi le proietta, più piccole e chiare quanto più è in alto
	var spazio: Physics2DDirectSpaceState = get_viewport().world_2d.direct_space_state
	for coppia in ombre:
		var chi = coppia[0]
		var ombra: Node2D = coppia[1]
		if not is_instance_valid(chi):
			ombra.visible = false
			continue
		var da: Vector2 = chi.global_position + Vector2(0, -10)
		var esclusi: Array = [chi] if chi is CollisionObject2D else []
		var colpo: Dictionary = spazio.intersect_ray(da, da + Vector2(0, 440), esclusi)
		if colpo.empty():
			ombra.visible = false
			continue
		var distanza: float = colpo["position"].y - da.y - 30.0
		var forza: float = clamp(1.0 - distanza / 380.0, 0.25, 1.0)
		ombra.visible = chi.visible
		ombra.global_position = colpo["position"]
		ombra.scale = Vector2(forza, forza)
		ombra.modulate.a = forza


func _aggiungi_ombra(livello: Node, chi: Node2D, larghezza: float):
	var ombra := Node2D.new()
	ombra.set_script(preload("res://scripts/ombra.gd"))
	ombra.larghezza = larghezza
	livello.add_child(ombra)
	# appena prima di chi la proietta (o del suo gruppo): sopra il terreno, sotto di lui
	var davanti: Node = chi
	while davanti.get_parent() != livello:
		davanti = davanti.get_parent()
	livello.move_child(ombra, davanti.get_index())
	ombre.append([chi, ombra])


# Pollini (all'aperto) o polvere (al chiuso) che brillano nell'aria, attorno all'inquadratura
func _particelle(livello: Node):
	var pulcino = livello.get_node_or_null("Player")
	if pulcino == null:
		return
	var al_chiuso: bool = tipo == "magazzino" or tipo == "pollaio"
	var colore: Color = Color(1, 0.93, 0.8) if al_chiuso else Color(1, 0.97, 0.75)
	var p := CPUParticles2D.new()
	p.amount = 34 if al_chiuso else 28
	p.lifetime = 9.0
	p.preprocess = 9.0
	p.local_coords = false
	p.emission_shape = CPUParticles2D.EMISSION_SHAPE_RECTANGLE
	p.emission_rect_extents = Vector2(700, 380)
	p.position = Vector2(0, -120)
	p.direction = Vector2(1, -0.3)
	p.spread = 180.0
	p.gravity = Vector2(2, 2) if al_chiuso else Vector2(4, -6)  # la polvere scende piano, i pollini salgono
	p.initial_velocity = 8.0 if al_chiuso else 12.0
	p.initial_velocity_random = 0.8
	p.scale_amount = 2.2 if al_chiuso else 3.0
	p.scale_amount_random = 0.6
	var sfumatura := Gradient.new()
	sfumatura.offsets = PoolRealArray([0.0, 0.2, 0.8, 1.0])
	sfumatura.colors = PoolColorArray([Color(colore.r, colore.g, colore.b, 0), Color(colore.r, colore.g, colore.b, 0.8),
			Color(colore.r, colore.g, colore.b, 0.8), Color(colore.r, colore.g, colore.b, 0)])
	p.color_ramp = sfumatura
	p.z_index = 5
	pulcino.add_child(p)


# Luce calda e morbida ai bordi dello schermo, sotto i pulsanti e il contatore
func _vignetta(livello: Node):
	var strato := CanvasLayer.new()
	strato.layer = 1
	var velo := TextureRect.new()
	velo.texture = VIGNETTA
	velo.expand = true
	velo.stretch_mode = TextureRect.STRETCH_SCALE
	velo.anchor_right = 1.0
	velo.anchor_bottom = 1.0
	velo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	velo.modulate.a = 0.3
	strato.add_child(velo)
	livello.add_child(strato)
