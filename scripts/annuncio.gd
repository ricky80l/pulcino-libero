extends CanvasLayer
# Cartello "Nuova abilità!": ferma il gioco, spiega come usare l'abilità appena imparata
# (con le istruzioni giuste per telefono o PC) e si chiude con "Ho capito!".

const Stile = preload("res://scripts/stile.gd")
const FONT_TITOLO = preload("res://assets/font/fredoka_messaggio.tres")
const FONT_TESTO = preload("res://assets/font/fredoka_piccolo.tres")

const TESTI := {
	"beccata": {
		"titolo": "Nuova abilità: la beccata!",
		"telefono": "Tocca il pulsante col becco per dare una beccata.",
		"pc": "Premi il tasto X per dare una beccata.",
		"spiegazione": "Con le beccate rompi sacchi, balle di paglia e vasi\nche ti sbarrano la strada. Funziona anche in aria!",
	},
	"doppio_salto": {
		"titolo": "Nuova abilità: il doppio salto!",
		"telefono": "Mentre sei in aria, tocca di nuovo il pulsante del salto.",
		"pc": "Mentre sei in aria, premi di nuovo Spazio.",
		"spiegazione": "Il pulcino sbatte le ali e fa un secondo salto:\ncosì superi muri alti e buche larghe.\nSi può fare una volta sola prima di toccare terra.",
	},
}

var abilita := ""
var ricorda := true  # false nelle aree di prova: l'avviso torna ogni volta


func mostra(nome: String, ricorda_vista: bool):
	abilita = nome
	ricorda = ricorda_vista
	layer = 4
	pause_mode = Node.PAUSE_MODE_PROCESS
	var t: Dictionary = TESTI[nome]
	var al_telefono: bool = OS.has_touchscreen_ui_hint() and not OS.has_feature("pc")

	var velo := ColorRect.new()
	velo.color = Color(0, 0, 0, 0.55)
	velo.rect_size = Vector2(1280, 720)
	add_child(velo)

	var pannello := PanelContainer.new()
	var stile_pannello := Stile.riquadro(Stile.LEGNO, Stile.CONTORNO, 6)
	stile_pannello.content_margin_left = 40
	stile_pannello.content_margin_right = 40
	stile_pannello.content_margin_top = 24
	stile_pannello.content_margin_bottom = 28
	pannello.add_stylebox_override("panel", stile_pannello)
	add_child(pannello)

	var colonna := VBoxContainer.new()
	colonna.add_constant_override("separation", 18)
	pannello.add_child(colonna)
	colonna.add_child(_scritta(t["titolo"], FONT_TITOLO, Color("ffd84a")))
	colonna.add_child(_scritta(t["telefono"] if al_telefono else t["pc"], FONT_TESTO, Stile.CREMA))
	colonna.add_child(_scritta(t["spiegazione"], FONT_TESTO, Color(1, 0.96, 0.86, 0.85)))

	var ok := Button.new()
	ok.text = "Ho capito!"
	ok.rect_min_size = Vector2(300, 72)
	ok.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	Stile.pulsante_legno(ok, FONT_TESTO)
	ok.add_stylebox_override("normal", Stile.riquadro(Color("8f5f2a"), Color("ffd84a"), 4))
	ok.connect("pressed", self, "chiudi")
	colonna.add_child(ok)

	# al centro dello schermo, quando il pannello ha preso le sue misure
	yield(get_tree(), "idle_frame")
	pannello.rect_position = (Vector2(1280, 720) - pannello.rect_size) / 2
	ok.grab_focus()
	get_tree().paused = true
	Suoni.suona("nido", 0.0)


func _scritta(testo: String, font: Font, colore: Color) -> Label:
	var l := Label.new()
	l.text = testo
	l.align = Label.ALIGN_CENTER
	l.add_font_override("font", font)
	l.add_color_override("font_color", colore)
	return l


func chiudi():
	get_tree().paused = false
	if ricorda:
		Progressi.segna_abilita_vista(abilita)
	queue_free()
