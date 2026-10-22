tool
extends StaticBody2D
# Pezzo del livello in stile cartoon: si disegna da solo e crea la sua collisione.
# La posizione è l'angolo in alto a sinistra.
# Cassette, mangiatoie e posatoi usano un disegno vettoriale; i pezzi lunghi si disegnano da codice.

enum Tipo { PAVIMENTO, LEGNO, CASSETTA, MANGIATOIA, POSATOIO, SBARRE, PARETE, RETE, ERBA, FUORI }

const IMMAGINI := {
	Tipo.CASSETTA: preload("res://assets/grafica/pollaio/cassetta.svg"),
	Tipo.MANGIATOIA: preload("res://assets/grafica/pollaio/mangiatoia.svg"),
	Tipo.POSATOIO: preload("res://assets/grafica/pollaio/posatoio.svg"),
}

# colori del pollaio
const CONTORNO := Color("5a3e14")
const LEGNO_CHIARO := Color("dda562")
const LEGNO_SCURO := Color("8f5f2a")
const METALLO := Color("8e96a3")
const METALLO_LUCE := Color("c8d0da")
const METALLO_SCURO := Color("5e6670")

export(Tipo) var tipo := Tipo.LEGNO setget _set_tipo  # aspetto del pezzo
export var dimensioni := Vector2(100, 40) setget _set_dimensioni  # larghezza e altezza in pixel
export var solido := true  # false = solo decorazione, ci si passa attraverso
export var attraversabile_da_sotto := false  # true = ci salti sopra passando da sotto

var disegno: Sprite = null


func _ready():
	_prepara_disegno()
	if Engine.editor_hint or not solido:
		return
	var rettangolo := RectangleShape2D.new()
	rettangolo.extents = dimensioni / 2
	var forma := CollisionShape2D.new()
	forma.shape = rettangolo
	forma.position = dimensioni / 2
	forma.one_way_collision = attraversabile_da_sotto
	add_child(forma)


func _set_tipo(valore):
	tipo = valore
	_prepara_disegno()
	update()


func _set_dimensioni(valore):
	dimensioni = valore
	_prepara_disegno()
	update()


# Per i pezzi con disegno vettoriale: un'immagine stirata alla misura del pezzo
func _prepara_disegno():
	if not is_inside_tree():
		return
	if IMMAGINI.has(tipo):
		if disegno == null:
			disegno = Sprite.new()
			disegno.centered = false
			add_child(disegno)
		disegno.texture = IMMAGINI[tipo]
		disegno.scale = dimensioni / disegno.texture.get_size()
		disegno.visible = true
	elif disegno:
		disegno.visible = false


# Numeri "casuali" ma sempre uguali per lo stesso pezzo, così il disegno non cambia a ogni avvio
func _caso() -> RandomNumberGenerator:
	var rng := RandomNumberGenerator.new()
	rng.seed = int(position.x * 7 + position.y * 13 + dimensioni.x * 3)
	return rng


func _draw():
	match tipo:
		Tipo.PARETE:
			_disegna_parete()
		Tipo.PAVIMENTO:
			_disegna_pavimento()
		Tipo.LEGNO:
			_disegna_legno()
		Tipo.SBARRE:
			_disegna_sbarre()
		Tipo.RETE:
			_disegna_rete()
		Tipo.ERBA:
			_disegna_erba()
		Tipo.FUORI:
			_disegna_fuori()


# Parete di assi verticali con chiodi e nodi del legno
func _disegna_parete():
	var rng := _caso()
	var larghezza_asse := 64.0
	var x := 0.0
	var i := 0
	while x < dimensioni.x:
		var w: float = min(larghezza_asse, dimensioni.x - x)
		var tono := Color("e3bf8a") if i % 2 == 0 else Color("dcb67f")
		draw_rect(Rect2(x, 0, w, dimensioni.y), tono)
		draw_line(Vector2(x + 6, 0), Vector2(x + 6, dimensioni.y), Color("ebcd9d"), 2.0)
		draw_line(Vector2(x, 0), Vector2(x, dimensioni.y), Color("b98f5c"), 3.0)
		for y in [40.0, dimensioni.y - 120.0]:
			draw_circle(Vector2(x + w / 2, y), 3.0, Color("9a7448"))
		if rng.randf() < 0.35:
			var centro := Vector2(x + rng.randf_range(16, w - 16), rng.randf_range(120, dimensioni.y - 200))
			_ellisse(centro, Vector2(7, 11), Color("c9a06b"))
			_ellisse(centro, Vector2(3, 5), Color("a87f4f"))
		x += larghezza_asse
		i += 1
	# zoccolo scuro vicino al pavimento
	draw_rect(Rect2(0, dimensioni.y - 110, dimensioni.x, 30), Color("c9a06b"))


# Terra battuta con uno strato di paglia sopra
func _disegna_pavimento():
	var rng := _caso()
	var w := dimensioni.x
	var h := dimensioni.y
	draw_rect(Rect2(0, 0, w, h), Color("9c6b35"))
	draw_rect(Rect2(0, h * 0.6, w, h * 0.4), Color("865a2b"))
	# paglia: bordo ondulato
	var punti := PoolVector2Array([Vector2(0, 16)])
	var x := 0.0
	while x <= w:
		punti.append(Vector2(x, rng.randf_range(-3, 3)))
		x += 18.0
	punti.append(Vector2(w, 0))
	punti.append(Vector2(w, 16))
	draw_colored_polygon(punti, Color("ebd27a"), PoolVector2Array(), null, null, true)
	draw_line(Vector2(0, 16), Vector2(w, 16), Color("c9a64a"), 3.0)
	# fili di paglia sparsi
	for _n in range(int(w / 14)):
		var p := Vector2(rng.randf_range(0, w), rng.randf_range(-2, 12))
		var angolo := rng.randf_range(-0.6, 0.6)
		var lungo := rng.randf_range(8, 16)
		var col := Color("f6e39a") if rng.randf() < 0.5 else Color("d9b54a")
		draw_line(p, p + Vector2(cos(angolo), sin(angolo)) * lungo, col, 2.0, true)


# Asse o palo di legno con contorno e venature
func _disegna_legno():
	var r := Rect2(Vector2.ZERO, dimensioni)
	draw_rect(r, Color("b07a3e"))
	draw_rect(Rect2(4, 0, 6, dimensioni.y), Color("c99a5c"))
	var y := 40.0
	while y < dimensioni.y:
		draw_line(Vector2(dimensioni.x * 0.3, y), Vector2(dimensioni.x * 0.7, y + 18), LEGNO_SCURO, 2.0, true)
		y += 90.0
	draw_rect(r, CONTORNO, false, 3.0)


# Sbarre di metallo della gabbia (pezzi sottili = un tubo, pezzi larghi = tante sbarre)
func _disegna_sbarre():
	var w := dimensioni.x
	var h := dimensioni.y
	if w <= 24 or h <= 24:
		draw_rect(Rect2(0, 0, w, h), METALLO)
		if w <= 24:
			draw_line(Vector2(w * 0.35, 2), Vector2(w * 0.35, h - 2), METALLO_LUCE, 3.0)
		else:
			draw_line(Vector2(2, h * 0.35), Vector2(w - 2, h * 0.35), METALLO_LUCE, 3.0)
		draw_rect(Rect2(0, 0, w, h), METALLO_SCURO, false, 3.0)
		return
	var x := 24.0
	while x < w:
		draw_line(Vector2(x, 0), Vector2(x, h), METALLO_SCURO, 7.0)
		draw_line(Vector2(x, 0), Vector2(x, h), METALLO, 4.0)
		draw_line(Vector2(x - 1, 0), Vector2(x - 1, h), METALLO_LUCE, 1.5)
		x += 24.0


# Rete da pollaio: maglie a rombo, con i fili rotti in fondo dove c'è la buca
func _disegna_rete():
	var w := dimensioni.x
	var h := dimensioni.y
	draw_rect(Rect2(0, 0, w, h), Color(0.6, 0.62, 0.66, 0.25))
	var filo := Color("7d858f")
	var passo := 14.0
	var c := -h
	while c < w + h:
		# diagonale che scende verso destra: y = x - c
		var x1: float = max(0.0, c)
		var x2: float = min(w, h + c)
		if x2 > x1:
			draw_line(Vector2(x1, x1 - c), Vector2(x2, x2 - c), filo, 2.0, true)
		# diagonale che sale verso destra: y = c - x
		var x3: float = max(0.0, c - h)
		var x4: float = min(w, c)
		if x4 > x3:
			draw_line(Vector2(x3, c - x3), Vector2(x4, c - x4), filo, 2.0, true)
		c += passo
	# cornice di legno ai lati e fili spezzati in fondo
	draw_rect(Rect2(0, 0, 5, h), Color("b07a3e"))
	draw_rect(Rect2(w - 5, 0, 5, h), Color("b07a3e"))
	for i in range(4):
		var bx := 4.0 + i * 7.0
		draw_line(Vector2(bx, h), Vector2(bx + 3, h + 10), filo, 2.0, true)


# Prato fuori dal pollaio
func _disegna_erba():
	var rng := _caso()
	var w := dimensioni.x
	var h := dimensioni.y
	draw_rect(Rect2(0, 0, w, h), Color("7a5230"))
	draw_rect(Rect2(0, 0, w, 18), Color("6dbe45"))
	# fili d'erba a punta
	var punti := PoolVector2Array([Vector2(0, 2)])
	var x := 0.0
	while x < w:
		punti.append(Vector2(x + 5, -rng.randf_range(6, 12)))
		punti.append(Vector2(x + 10, 2))
		x += 10.0
	punti.append(Vector2(w, 18))
	punti.append(Vector2(0, 18))
	draw_colored_polygon(punti, Color("6dbe45"), PoolVector2Array(), null, null, true)
	draw_line(Vector2(0, 18), Vector2(w, 18), Color("4e9a2e"), 3.0)
	for _n in range(int(w / 70)):
		var fiore := Vector2(rng.randf_range(10, w - 10), rng.randf_range(-4, 8))
		var petali := Color("ffffff") if rng.randf() < 0.5 else Color("ffd84a")
		for a in range(5):
			var ang := a * TAU / 5
			draw_circle(fiore + Vector2(cos(ang), sin(ang)) * 4, 3, petali)
		draw_circle(fiore, 2.5, Color("f29e1f"))


# Paesaggio fuori: colline, sole e nuvole (il cielo è il colore di sfondo)
func _disegna_fuori():
	var w := dimensioni.x
	var h := dimensioni.y
	# sole con raggi
	var sole := Vector2(w * 0.65, 120)
	for a in range(12):
		var ang := a * TAU / 12
		draw_line(sole + Vector2(cos(ang), sin(ang)) * 58, sole + Vector2(cos(ang), sin(ang)) * 78, Color("ffd84a"), 5.0, true)
	draw_circle(sole, 50, Color("f2b705"))
	draw_circle(sole, 45, Color("ffe066"))
	# nuvole
	for centro in [Vector2(w * 0.2, 170), Vector2(w * 0.8, 260)]:
		for d in [Vector2(-30, 6), Vector2(0, -10), Vector2(30, 4), Vector2(55, 10)]:
			draw_circle(centro + d, 26, Color("e6f2fb"))
		for d in [Vector2(-30, 2), Vector2(0, -14), Vector2(30, 0), Vector2(55, 6)]:
			draw_circle(centro + d, 24, Color("ffffff"))
	# colline: lontana più chiara, vicina più scura
	_collina(h - 200, 70.0, 0.006, Color("a8d977"))
	_collina(h - 140, 50.0, 0.011, Color("7cc24e"))


func _collina(base: float, altezza: float, frequenza: float, colore: Color):
	var punti := PoolVector2Array()
	var x := 0.0
	while x <= dimensioni.x:
		punti.append(Vector2(x, base - sin(x * frequenza + 1.0) * altezza * 0.5 - altezza * 0.5))
		x += 20.0
	punti.append(Vector2(dimensioni.x, dimensioni.y))
	punti.append(Vector2(0, dimensioni.y))
	draw_colored_polygon(punti, colore, PoolVector2Array(), null, null, true)


func _ellisse(centro: Vector2, raggi: Vector2, colore: Color):
	draw_set_transform(centro, 0, Vector2(raggi.x / raggi.y, 1.0))
	draw_circle(Vector2.ZERO, raggi.y, colore)
	draw_set_transform(Vector2.ZERO, 0, Vector2.ONE)
