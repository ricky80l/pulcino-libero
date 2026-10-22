extends Control
# Mappa provvisoria: una tavoletta per ogni luogo del viaggio. Verrà sostituita dalla mappa disegnata (Tappa 8).
# Si sceglie col dito, oppure con le frecce e il salto.

const FONT_TITOLO = preload("res://assets/font/fredoka_messaggio.tres")
const FONT_TAVOLETTE = preload("res://assets/font/fredoka_contatore.tres")

const LEGNO := Color("b07a3e")
const LEGNO_CHIARO := Color("c99a5c")
const CONTORNO := Color("5a3e14")
const BLOCCATO := Color("9a9a96")


func _ready():
	var sfondo := ColorRect.new()
	sfondo.color = Color(0.55, 0.78, 0.95)
	sfondo.anchor_right = 1.0
	sfondo.anchor_bottom = 1.0
	add_child(sfondo)

	var titolo := Label.new()
	titolo.text = "Il Pulcino Libero"
	titolo.add_font_override("font", FONT_TITOLO)
	titolo.add_color_override("font_color", Color(1, 0.96, 0.86))
	titolo.align = Label.ALIGN_CENTER
	titolo.anchor_right = 1.0
	titolo.margin_top = 40
	add_child(titolo)

	var griglia := GridContainer.new()
	griglia.columns = 5
	griglia.add_constant_override("hseparation", 20)
	griglia.add_constant_override("vseparation", 20)
	griglia.rect_position = Vector2(80, 190)
	add_child(griglia)

	# Evidenzia l'ultimo livello giocato (o il primo giocabile), così si sceglie anche con le frecce
	var da_selezionare: Button = null
	for i in range(Progressi.LIVELLI.size()):
		var numero := i + 1
		var tavoletta := _crea_tavoletta(numero)
		griglia.add_child(tavoletta)
		if tavoletta.disabled:
			continue
		if da_selezionare == null or numero == Progressi.ultimo_giocato:
			da_selezionare = tavoletta
	if da_selezionare:
		da_selezionare.grab_focus()


func _crea_tavoletta(numero: int) -> Button:
	var livello: Dictionary = Progressi.LIVELLI[numero - 1]
	var b := Button.new()
	b.rect_min_size = Vector2(208, 150)
	b.add_font_override("font", FONT_TAVOLETTE)
	b.add_color_override("font_color", Color(1, 0.96, 0.86))
	b.add_color_override("font_color_hover", Color(1, 1, 1))
	b.add_color_override("font_color_focus", Color(1, 1, 1))
	b.add_color_override("font_color_disabled", Color(0.95, 0.95, 0.93))

	var sbloccato := numero <= Progressi.sbloccato
	var costruito: bool = livello["scena"] != ""
	var testo := "%d\n%s\n" % [numero, livello["nome"]]
	if not sbloccato:
		testo = "%d\n???\n" % numero
	elif not costruito:
		testo += "presto!"
	elif Progressi.finito(numero):
		var r: Dictionary = Progressi.record[str(numero)]
		testo += "%d / %d" % [int(r["presi"]), int(r["totale"])]
	else:
		testo += "nuovo!"
	b.text = testo
	b.disabled = not (sbloccato and costruito)

	b.add_stylebox_override("normal", _stile(LEGNO, CONTORNO, 4))
	b.add_stylebox_override("hover", _stile(LEGNO_CHIARO, CONTORNO, 4))
	b.add_stylebox_override("pressed", _stile(CONTORNO, CONTORNO, 4))
	b.add_stylebox_override("focus", _stile(Color(0, 0, 0, 0), Color("ffd84a"), 8))
	b.add_stylebox_override("disabled", _stile(BLOCCATO, Color("6b6b68"), 4))
	b.connect("pressed", Progressi, "gioca", [numero])
	return b


func _stile(sfondo: Color, bordo: Color, spessore: int) -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = sfondo
	s.border_color = bordo
	s.set_border_width_all(spessore)
	s.set_corner_radius_all(18)
	return s
