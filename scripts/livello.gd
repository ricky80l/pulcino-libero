extends Node2D
# Livello: conta i chicchi, accende i nidi e mostra il messaggio di fine quando il pulcino esce.

var completato := false
var chicchi_presi := 0
var chicchi_totali := 0
var nido_attivo = null

onready var player := $Player
onready var messaggio := $Interfaccia/Messaggio
onready var testo_fine := $Interfaccia/Messaggio/Testo
onready var contatore := $Interfaccia/Contatore
onready var numero_chicchi := $Interfaccia/Contatore/Numero


func _ready():
	add_to_group("livello")
	messaggio.visible = false
	$Uscita.connect("body_entered", self, "_on_uscita_body_entered")
	chicchi_totali = get_tree().get_nodes_in_group("chicchi").size()
	_aggiorna_contatore()


func chicco_raccolto():
	chicchi_presi += 1
	_aggiorna_contatore()
	# il contatore fa un piccolo "boing"
	var tween := Tween.new()
	add_child(tween)
	tween.interpolate_property(contatore, "rect_scale", Vector2(1.3, 1.3), Vector2.ONE, 0.3, Tween.TRANS_BACK, Tween.EASE_OUT)
	tween.start()
	yield(tween, "tween_all_completed")
	tween.queue_free()


func nido_raggiunto(nido):
	if nido_attivo:
		nido_attivo.spegni()
	nido_attivo = nido
	nido.accendi()
	player.punto_sicuro = nido.global_position + Vector2(0, -30)


func _aggiorna_contatore():
	numero_chicchi.text = "%d / %d" % [chicchi_presi, chicchi_totali]


func _on_uscita_body_entered(corpo):
	if corpo == player and not completato:
		completato = true
		player.set_physics_process(false)
		testo_fine.text = "Sei scappato dal pollaio!\n\nChicchi: %d / %d\n\nPremi salto per rigiocare" % [chicchi_presi, chicchi_totali]
		messaggio.visible = true
		Suoni.suona("fine", 0.0)


func _process(_delta):
	# A livello finito, il tasto salto fa ricominciare
	if completato and Input.is_action_just_pressed("jump"):
		get_tree().reload_current_scene()
