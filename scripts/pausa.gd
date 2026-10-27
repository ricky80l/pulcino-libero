extends CanvasLayer
# Pulsante di pausa in alto a destra e menu di pausa: Continua, Ricomincia, Torna alla mappa.
# Sul PC la pausa si apre e si chiude anche con il tasto Esc.

const Stile = preload("res://scripts/stile.gd")
const FONT_PICCOLO = preload("res://assets/font/fredoka_contatore.tres")
const FONT_GRANDE = preload("res://assets/font/fredoka_messaggio.tres")

var pulsante_pausa := Button.new()
var pannello := Control.new()
var primo_pulsante: Button


func _ready():
	layer = 3
	pause_mode = Node.PAUSE_MODE_PROCESS  # deve funzionare anche a gioco fermo

	pulsante_pausa.text = "II"
	pulsante_pausa.rect_position = Vector2(1280 - 16 - 72, 12)
	pulsante_pausa.rect_size = Vector2(72, 60)
	pulsante_pausa.focus_mode = Control.FOCUS_NONE
	Stile.pulsante_legno(pulsante_pausa, FONT_PICCOLO)
	pulsante_pausa.connect("pressed", self, "apri")
	add_child(pulsante_pausa)

	# menu: velo scuro, titolo e tre pulsanti
	pannello.anchor_right = 1.0
	pannello.anchor_bottom = 1.0
	pannello.visible = false
	add_child(pannello)
	var velo := ColorRect.new()
	velo.color = Color(0, 0, 0, 0.55)
	velo.anchor_right = 1.0
	velo.anchor_bottom = 1.0
	pannello.add_child(velo)
	var colonna := VBoxContainer.new()
	colonna.rect_position = Vector2(440, 140)
	colonna.rect_min_size = Vector2(400, 0)
	colonna.add_constant_override("separation", 22)
	pannello.add_child(colonna)
	var titolo := Label.new()
	titolo.text = "Pausa"
	titolo.align = Label.ALIGN_CENTER
	titolo.add_font_override("font", FONT_GRANDE)
	titolo.add_color_override("font_color", Stile.CREMA)
	colonna.add_child(titolo)
	primo_pulsante = _voce(colonna, "Continua", "chiudi")
	_voce(colonna, "Ricomincia", "_ricomincia")
	_voce(colonna, "Torna alla mappa", "_mappa")


func _voce(colonna: Control, testo: String, metodo: String) -> Button:
	var b := Button.new()
	b.text = testo
	b.rect_min_size = Vector2(400, 84)
	Stile.pulsante_legno(b, FONT_PICCOLO)
	b.connect("pressed", self, metodo)
	colonna.add_child(b)
	return b


func apri():
	get_tree().paused = true
	pannello.visible = true
	pulsante_pausa.visible = false
	primo_pulsante.grab_focus()


func chiudi():
	get_tree().paused = false
	pannello.visible = false
	pulsante_pausa.visible = true


func _ricomincia():
	get_tree().paused = false
	get_tree().reload_current_scene()


func _mappa():
	get_tree().paused = false
	Progressi.torna_alla_mappa()


func _unhandled_input(evento):
	if evento.is_action_pressed("ui_cancel"):
		if pannello.visible:
			chiudi()
		else:
			apri()
		get_tree().set_input_as_handled()
