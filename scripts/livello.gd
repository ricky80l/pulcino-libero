extends Node2D
# Livello: conta i chicchi, accende i nidi e mostra il messaggio di fine quando il pulcino esce.
# A fine livello salva i progressi e, premendo salto, torna alla mappa.

export var numero := 1  # posizione del livello nel viaggio (1 = pollaio)
export var frase_fine := "Sei scappato dal pollaio!"  # cosa dice il messaggio di fine
export var beccata := false  # true se in questo livello il pulcino sa già beccare
export var doppio_salto := false  # true se in questo livello il pulcino sa già fare il doppio salto
export var planata := false  # true se in questo livello il pulcino sa già planare
export var abilita_nuova := ""  # abilità che si impara in questo livello ("beccata", "doppio_salto"): mostra l'avviso
export var salva_progressi := true  # false per le aree di prova: niente record e niente sblocchi

var completato := false
var chicchi_presi := 0
var chicchi_totali := 0
var nido_attivo = null
var uovo := false  # l'uovo d'oro segreto preso in questa partita

onready var player := $Player
onready var messaggio := $Interfaccia/Messaggio
onready var testo_fine := $Interfaccia/Messaggio/Testo
onready var contatore := $Interfaccia/Contatore
onready var numero_chicchi := $Interfaccia/Contatore/Numero


func _ready():
	add_to_group("livello")
	Pittura.entra(filename.get_file().get_basename())
	messaggio.visible = false
	$Uscita.connect("body_entered", self, "_on_uscita_body_entered")
	chicchi_totali = get_tree().get_nodes_in_group("chicchi").size()
	_aggiorna_contatore()
	player.puo_beccare = beccata
	player.puo_doppio_salto = doppio_salto
	player.puo_planare = planata
	$ControlliTouch/Becco.visible = beccata
	# avviso "Nuova abilità!" la prima volta (nelle aree di prova ogni volta)
	if abilita_nuova != "" and (not salva_progressi or not Progressi.abilita_vista(abilita_nuova)):
		var annuncio = CanvasLayer.new()
		annuncio.set_script(preload("res://scripts/annuncio.gd"))
		add_child(annuncio)
		annuncio.mostra(abilita_nuova, salva_progressi)


func uovo_preso():
	uovo = true  # si salva solo se il livello viene finito (vedi _on_uscita_body_entered)


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
		# le tre stelline: tutti i chicchi, l'uovo d'oro, mai preso dai nemici
		var stelle := [chicchi_presi == chicchi_totali, uovo, player.volte_colpito == 0]
		if salva_progressi:
			# tutto (uovo, chicchi, stelline, borsellino) conta solo arrivando all'uscita
			if uovo:
				Progressi.segna_uovo(numero)
			Progressi.livello_finito(numero, chicchi_presi, chicchi_totali, stelle)
		_mostra_stelle(stelle, player.volte_colpito)
		var testo := "\n\n\n%s\n\n" % frase_fine
		if salva_progressi and not Progressi.costruito(numero + 1):
			testo += "Per ora il viaggio si ferma qui:\nnuovi luoghi in arrivo!\n\n"
		testo_fine.text = testo + "Premi salto per tornare alla mappa"
		messaggio.visible = true
		Suoni.suona("fine", 0.0)


# Le tre stelline in cima al messaggio di fine: compaiono una alla volta, con un "ting!" sempre più acuto.
# Sotto ogni stella: un disegnino (chicco, uovo, nemico del luogo) e cosa è successo davvero in partita,
# così anche chi gioca per la prima volta capisce cosa serve per accenderla.
const STELLA = preload("res://assets/grafica/oggetti/stella.png")
const STELLA_VUOTA = preload("res://assets/grafica/oggetti/stella_vuota.png")
const FONT_STELLE = preload("res://assets/font/fredoka_piccolo.tres")
const ICONA_CHICCO = preload("res://assets/grafica/oggetti/chicco.png")
const ICONA_UOVO = preload("res://assets/grafica/oggetti/uovo_oro.png")
const ICONA_UOVO_VUOTO = preload("res://assets/grafica/oggetti/uovo_vuoto.png")
# il nemico del luogo, riconosciuto dal suo script
const ICONE_NEMICI := {
	"res://scripts/topo.gd": preload("res://assets/grafica/oggetti/icona_topo.png"),
	"res://scripts/oca.gd": preload("res://assets/grafica/oggetti/icona_oca.png"),
	"res://scripts/talpa.gd": preload("res://assets/grafica/talpa/talpa.png"),
	"res://scripts/coni.gd": preload("res://assets/grafica/magazzino/cono_in_piedi.png"),
}
const CREMA := Color(1, 0.96, 0.86)
const PASSO_STELLE := 320.0


func _icona_nemico():
	var da_guardare := [self]
	while not da_guardare.empty():
		var nodo: Node = da_guardare.pop_back()
		var copione = nodo.get_script()
		if copione and ICONE_NEMICI.has(copione.resource_path):
			return ICONE_NEMICI[copione.resource_path]
		da_guardare += nodo.get_children()
	return null


func _mostra_stelle(stelle: Array, volte_colpito: int):
	var tween := Tween.new()
	messaggio.add_child(tween)
	var mancano := chicchi_totali - chicchi_presi
	var righe := []
	if stelle[0]:
		righe.append(["Tutti i chicchi!", "%d su %d" % [chicchi_presi, chicchi_totali]])
	else:
		righe.append(["%d su %d chicchi" % [chicchi_presi, chicchi_totali], "ne manca 1" if mancano == 1 else "ne mancano %d" % mancano])
	if stelle[1]:
		righe.append(["Uovo trovato!", "era ben nascosto"])
	else:
		righe.append(["Uovo d'oro", "non trovato: cercalo!"])
	if stelle[2]:
		righe.append(["Mai preso!", "bravissimo"])
	else:
		righe.append(["Preso 1 volta" if volte_colpito == 1 else "Preso %d volte" % volte_colpito, "prova a non farti prendere"])
	var icone := [ICONA_CHICCO, ICONA_UOVO if stelle[1] else ICONA_UOVO_VUOTO, _icona_nemico()]
	for i in range(3):
		var centro_x: float = 640 + (i - 1) * PASSO_STELLE
		var ritardo: float = 0.5 + i * 0.45
		var stella := TextureRect.new()
		stella.texture = STELLA if stelle[i] else STELLA_VUOTA
		stella.expand = true
		stella.rect_size = Vector2(96, 96)
		stella.rect_pivot_offset = Vector2(48, 48)
		stella.rect_position = Vector2(centro_x - 48, 28)
		stella.rect_scale = Vector2.ZERO
		stella.mouse_filter = Control.MOUSE_FILTER_IGNORE
		messaggio.add_child(stella)
		# riga 1: disegnino + cosa è successo
		var riga := HBoxContainer.new()
		riga.alignment = BoxContainer.ALIGN_CENTER
		riga.add_constant_override("separation", 8)
		riga.rect_size = Vector2(PASSO_STELLE, 40)
		riga.rect_position = Vector2(centro_x - PASSO_STELLE / 2, 128)
		riga.mouse_filter = Control.MOUSE_FILTER_IGNORE
		if icone[i] != null:
			var icona := TextureRect.new()
			icona.texture = icone[i]
			icona.expand = true
			icona.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
			icona.rect_min_size = Vector2(36, 36)
			icona.mouse_filter = Control.MOUSE_FILTER_IGNORE
			riga.add_child(icona)
		var nome := Label.new()
		nome.text = righe[i][0]
		nome.add_font_override("font", FONT_STELLE)
		nome.add_color_override("font_color", CREMA if stelle[i] else Color(1, 0.96, 0.86, 0.8))
		riga.add_child(nome)
		riga.modulate.a = 0.0
		messaggio.add_child(riga)
		# riga 2: un piccolo commento (cosa manca, o un complimento)
		var nota := Label.new()
		nota.text = righe[i][1]
		nota.add_font_override("font", FONT_STELLE)
		nota.add_color_override("font_color", CREMA if stelle[i] else Color("ffe08a"))
		nota.align = Label.ALIGN_CENTER
		nota.rect_size = Vector2(PASSO_STELLE / 0.8, 30)
		nota.rect_scale = Vector2(0.8, 0.8)
		nota.rect_position = Vector2(centro_x - PASSO_STELLE / 2, 168)
		nota.modulate.a = 0.0
		messaggio.add_child(nota)
		tween.interpolate_property(stella, "rect_scale", Vector2.ZERO, Vector2.ONE, 0.4, Tween.TRANS_BACK, Tween.EASE_OUT, ritardo)
		tween.interpolate_property(riga, "modulate:a", 0.0, 1.0, 0.3, Tween.TRANS_LINEAR, Tween.EASE_IN, ritardo + 0.1)
		tween.interpolate_property(nota, "modulate:a", 0.0, 0.85, 0.3, Tween.TRANS_LINEAR, Tween.EASE_IN, ritardo + 0.25)
		if stelle[i]:
			tween.interpolate_callback(self, ritardo, "_suona_stella", i)
	tween.start()


func _suona_stella(i: int):
	Suoni.suona("stella", 0.0, -2.0, 1.0 + i * 0.12)


func _process(_delta):
	# A livello finito, il tasto salto riporta alla mappa
	if completato and Input.is_action_just_pressed("jump"):
		Progressi.torna_alla_mappa()
