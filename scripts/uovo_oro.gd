extends Area2D
# Uovo d'oro segreto: uno per luogo, nascosto bene. Brilla piano e ogni tanto scintilla, per incuriosire.
# Preso: festa di scintille, "dlin-dlin!", la scritta "Uovo d'oro trovato!" e il telefono se lo ricorda.
# Se era già stato trovato in un'altra partita si vede trasparente, ma si può riprendere (vale per le stelline).
# La posizione è la base dell'uovo, appoggiato.

const Parti = preload("res://scripts/parti.gd")
const Effetti = preload("res://scripts/effetti.gd")
const IMMAGINE = preload("res://assets/grafica/oggetti/uovo_oro.png")
const BAGLIORE = preload("res://assets/grafica/oggetti/bagliore.png")
const FONT = preload("res://assets/font/fredoka_messaggio.tres")

var disegno: Sprite
var alone: Sprite
var tempo := 0.0
var preso := false
var prossima_scintilla := 1.0


func _ready():
	var forma := CollisionShape2D.new()
	var cerchio := CircleShape2D.new()
	cerchio.radius = 18.0
	forma.shape = cerchio
	forma.position = Vector2(0, -18)
	add_child(forma)
	alone = Parti.crea(self, BAGLIORE, Vector2(BAGLIORE.get_width() / 2.0, BAGLIORE.get_height() / 2.0), Vector2(0, -18))
	alone.modulate = Color(1, 0.85, 0.3, 0.5)
	disegno = Parti.crea(self, IMMAGINE, Vector2(30, 72), Vector2.ZERO)
	connect("body_entered", self, "_on_body_entered")
	call_deferred("_gia_trovato")  # il livello si presenta dopo i suoi figli: si controlla un attimo dopo


func _gia_trovato():
	if Progressi.uovo_trovato_in(_numero_livello()):
		modulate.a = 0.45  # già trovato in un'altra partita


func _numero_livello() -> int:
	var livelli: Array = get_tree().get_nodes_in_group("livello")
	return livelli[0].numero if not livelli.empty() else 0


func _process(delta):
	if preso:
		return
	tempo += delta
	disegno.position.y = sin(tempo * 2.5) * 3.0  # dondola piano
	alone.scale = Vector2.ONE * Parti.SCALA * (1.0 + sin(tempo * 3.0) * 0.12)
	prossima_scintilla -= delta
	if prossima_scintilla <= 0:
		prossima_scintilla = rand_range(0.8, 1.6)
		Effetti.sbuffo(get_parent(), position + Vector2(rand_range(-14, 14), -30), Color(1, 0.95, 0.6), 3, 40.0)


func _on_body_entered(corpo):
	if preso or not corpo.is_in_group("pulcino"):
		return
	preso = true
	Suoni.suona("uovo", 0.0)
	Effetti.sbuffo(get_parent(), position + Vector2(0, -20), Color(1, 0.85, 0.25), 24, 260.0)
	Effetti.sbuffo(get_parent(), position + Vector2(0, -20), Color(1, 1, 0.85), 14, 160.0)
	var livelli: Array = get_tree().get_nodes_in_group("livello")
	if not livelli.empty():
		livelli[0].uovo_preso()
	_scritta()
	# l'uovo sale ruotando e svanisce
	var tween := Tween.new()
	add_child(tween)
	tween.interpolate_property(self, "position:y", position.y, position.y - 60, 0.6, Tween.TRANS_BACK, Tween.EASE_OUT)
	tween.interpolate_property(self, "modulate:a", modulate.a, 0.0, 0.4, Tween.TRANS_LINEAR, Tween.EASE_IN, 0.4)
	tween.interpolate_property(disegno, "scale", disegno.scale, disegno.scale * 1.6, 0.6, Tween.TRANS_BACK, Tween.EASE_OUT)
	tween.start()
	yield(tween, "tween_all_completed")
	visible = false


# "Uovo d'oro trovato!" in grande, che compare e poi svanisce
func _scritta():
	var strato := CanvasLayer.new()
	strato.layer = 3
	var scritta := Label.new()
	scritta.text = "Uovo d'oro trovato!"
	scritta.add_font_override("font", FONT)
	scritta.add_color_override("font_color", Color("ffd84a"))
	scritta.add_color_override("font_color_shadow", Color("6a4a10"))
	scritta.add_constant_override("shadow_offset_x", 3)
	scritta.add_constant_override("shadow_offset_y", 4)
	scritta.align = Label.ALIGN_CENTER
	scritta.rect_size = Vector2(1280, 80)
	scritta.rect_position = Vector2(0, 150)
	strato.add_child(scritta)
	get_parent().add_child(strato)
	var tween := Tween.new()
	strato.add_child(tween)
	tween.interpolate_property(scritta, "rect_scale", Vector2(0.6, 0.6), Vector2.ONE, 0.35, Tween.TRANS_BACK, Tween.EASE_OUT)
	tween.interpolate_property(scritta, "modulate:a", 1.0, 0.0, 0.6, Tween.TRANS_LINEAR, Tween.EASE_IN, 1.6)
	scritta.rect_pivot_offset = Vector2(640, 40)
	tween.start()
	yield(tween, "tween_all_completed")
	strato.queue_free()
