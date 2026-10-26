extends Control
# Schermata dei crediti: chi ha fatto il gioco e le licenze di quello che usa (Godot, font Fredoka).
# Si apre dalla mappa; il testo si scorre col dito o con la rotella.

const Stile = preload("res://scripts/stile.gd")
const FONT_TITOLO = preload("res://assets/font/fredoka_messaggio.tres")
const FONT_PULSANTE = preload("res://assets/font/fredoka_piccolo.tres")
const FONT_TESTO = preload("res://assets/font/fredoka_testo.tres")

const TESTO := """IL PULCINO LIBERO

Ideato e diretto da Riccardo.

Sviluppato con l'assistenza di strumenti di intelligenza artificiale (Claude, Anthropic).

Realizzato con Godot Engine (godotengine.org).

Carattere Fredoka: Copyright 2016 The Fredoka Project Authors (https://github.com/hafontia/Fredoka-One), distribuito con licenza SIL Open Font License, versione 1.1 (scripts.sil.org/OFL).

Parti di questo software sono copyright (c) The FreeType Project (www.freetype.org). Tutti i diritti riservati.

LICENZA DI GODOT ENGINE

"""


func _ready():
	var sfondo := ColorRect.new()
	sfondo.color = Color(0.55, 0.78, 0.95)
	sfondo.anchor_right = 1.0
	sfondo.anchor_bottom = 1.0
	add_child(sfondo)

	var titolo := Label.new()
	titolo.text = "Crediti"
	titolo.add_font_override("font", FONT_TITOLO)
	titolo.add_color_override("font_color", Stile.CREMA)
	titolo.align = Label.ALIGN_CENTER
	titolo.anchor_right = 1.0
	titolo.margin_top = 18
	add_child(titolo)

	# foglio color crema con il testo che scorre
	var foglio := PanelContainer.new()
	var stile_foglio := Stile.riquadro(Color("fff6dc"), Stile.CONTORNO, 4)
	stile_foglio.content_margin_left = 24
	stile_foglio.content_margin_right = 24
	stile_foglio.content_margin_top = 16
	stile_foglio.content_margin_bottom = 16
	foglio.add_stylebox_override("panel", stile_foglio)
	foglio.rect_position = Vector2(140, 100)
	foglio.rect_size = Vector2(1000, 500)
	add_child(foglio)

	var scorrimento := ScrollContainer.new()
	scorrimento.scroll_horizontal_enabled = false
	foglio.add_child(scorrimento)

	var testo := Label.new()
	testo.autowrap = true
	testo.rect_min_size = Vector2(920, 0)
	testo.add_font_override("font", FONT_TESTO)
	testo.add_color_override("font_color", Color("4a3210"))
	testo.text = TESTO + Engine.get_license_text()
	scorrimento.add_child(testo)

	var indietro := Button.new()
	indietro.text = "Torna alla mappa"
	indietro.rect_position = Vector2(470, 618)
	indietro.rect_min_size = Vector2(340, 76)
	Stile.pulsante_legno(indietro, FONT_PULSANTE)
	indietro.connect("pressed", Progressi, "torna_alla_mappa")
	add_child(indietro)
	indietro.grab_focus()
