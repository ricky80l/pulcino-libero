extends Node2D
# Livello: conta i chicchi, accende i nidi e mostra il messaggio di fine quando il pulcino esce.
# A fine livello salva i progressi e, premendo salto, torna alla mappa.

export var numero := 1  # posizione del livello nel viaggio (1 = pollaio)
export var frase_fine := "Sei scappato dal pollaio!"  # cosa dice il messaggio di fine
export var beccata := false  # true se in questo livello il pulcino sa già beccare
export var salva_progressi := true  # false per le aree di prova: niente record e niente sblocchi

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
	player.puo_beccare = beccata
	$ControlliTouch/Becco.visible = beccata


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
		if salva_progressi:
			Progressi.livello_finito(numero, chicchi_presi, chicchi_totali)
		var testo := "%s\n\nChicchi: %d / %d\n\n" % [frase_fine, chicchi_presi, chicchi_totali]
		if salva_progressi and not Progressi.costruito(numero + 1):
			testo += "Per ora il viaggio si ferma qui:\nnuovi luoghi in arrivo!\n\n"
		testo_fine.text = testo + "Premi salto per tornare alla mappa"
		messaggio.visible = true
		Suoni.suona("fine", 0.0)


func _process(_delta):
	# A livello finito, il tasto salto riporta alla mappa
	if completato and Input.is_action_just_pressed("jump"):
		Progressi.torna_alla_mappa()
