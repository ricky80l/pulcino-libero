tool
extends StaticBody2D
# Pezzo del livello in stile cartoon: si disegna da solo e crea la sua collisione.
# La posizione è l'angolo in alto a sinistra.
# Cassette, mangiatoie e posatoi usano un disegno vettoriale; i pezzi lunghi si disegnano da codice.

enum Tipo { PAVIMENTO, LEGNO, CASSETTA, MANGIATOIA, POSATOIO, SBARRE, PARETE, RETE, ERBA, FUORI,
		TERRA, BOTTE, CARRETTO, TETTOIA, CEPPI, ABBEVERATOIO, STECCATO, FIENILE, CANCELLO,
		TERRA_ORTO, ACQUA, INVISIBILE, CAVOLO, CARRIOLA, POMODORI, ANNAFFIATOIO, SPAVENTAPASSERI, FRAGOLE, POZZO,
		MATTONI, LAMIERA, CEMENTO, FOSSA, SOPPALCO, PILASTRO, SCATOLONE_A, SCATOLONE_B, SCATOLONE_C, BANCALE,
		CARTONI, SCAFFALE, TRANSPALLET, PORTONE, ESTINTORE, CARTELLO_USCITA, FURGONE }

const IMMAGINI := {
	Tipo.CASSETTA: preload("res://assets/grafica/pollaio/cassetta.png"),
	Tipo.MANGIATOIA: preload("res://assets/grafica/pollaio/mangiatoia.png"),
	Tipo.POSATOIO: preload("res://assets/grafica/pollaio/posatoio.png"),
	Tipo.BOTTE: preload("res://assets/grafica/cortile/botte.png"),
	Tipo.CARRETTO: preload("res://assets/grafica/cortile/carretto.png"),
	Tipo.TETTOIA: preload("res://assets/grafica/cortile/tettoia.png"),
	Tipo.CEPPI: preload("res://assets/grafica/cortile/ceppi.png"),
	Tipo.ABBEVERATOIO: preload("res://assets/grafica/cortile/abbeveratoio.png"),
	Tipo.STECCATO: preload("res://assets/grafica/cortile/steccato.png"),
	Tipo.FIENILE: preload("res://assets/grafica/cortile/fienile.png"),
	Tipo.CANCELLO: preload("res://assets/grafica/cortile/cancello.png"),
	Tipo.CAVOLO: preload("res://assets/grafica/orto/cavolo.png"),
	Tipo.CARRIOLA: preload("res://assets/grafica/orto/carriola.png"),
	Tipo.POMODORI: preload("res://assets/grafica/orto/pomodori.png"),
	Tipo.ANNAFFIATOIO: preload("res://assets/grafica/orto/annaffiatoio.png"),
	Tipo.SPAVENTAPASSERI: preload("res://assets/grafica/orto/spaventapasseri.png"),
	Tipo.FRAGOLE: preload("res://assets/grafica/orto/fragole.png"),
	Tipo.POZZO: preload("res://assets/grafica/orto/pozzo.png"),
	Tipo.SCATOLONE_A: preload("res://assets/grafica/magazzino/scatolone_a.png"),
	Tipo.SCATOLONE_B: preload("res://assets/grafica/magazzino/scatolone_b.png"),
	Tipo.SCATOLONE_C: preload("res://assets/grafica/magazzino/scatolone_c.png"),
	Tipo.BANCALE: preload("res://assets/grafica/magazzino/bancale.png"),
	Tipo.CARTONI: preload("res://assets/grafica/magazzino/cartoni_piatti.png"),
	Tipo.SCAFFALE: preload("res://assets/grafica/magazzino/scaffale.png"),
	Tipo.TRANSPALLET: preload("res://assets/grafica/magazzino/transpallet.png"),
	Tipo.PORTONE: preload("res://assets/grafica/magazzino/portone.png"),
	Tipo.ESTINTORE: preload("res://assets/grafica/magazzino/estintore.png"),
	Tipo.CARTELLO_USCITA: preload("res://assets/grafica/magazzino/uscita.png"),
	Tipo.FURGONE: preload("res://assets/grafica/magazzino/furgone.png"),
}
const MATTONI_PIASTRELLA := preload("res://assets/grafica/magazzino/mattoni.png")  # si ripete su tutta la parete

# colori del magazzino
const AZZURRO := Color("2f6db5")
const AZZURRO_SCURO := Color("1c4a80")
const GRIGIO := Color("a9b0b8")
const GRIGIO_SCURO := Color("6e757d")

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

const MARGINE_DIPINTO := 16  # i pezzi dipinti sono fotografati con un po' di bordo intorno (vedi ridipingi.py)

var disegno: Sprite = null
var dipinto: Node2D = null  # versione dipinta dei pezzi disegnati da codice (modalità dipinta)


func _ready():
	_prepara_disegno()
	if not Engine.editor_hint:
		Pittura.connect("cambiata", self, "_mostra_dipinto")
		_mostra_dipinto()
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


# Modalità dipinta: al posto del disegno da codice si vedono le strisce ridipinte di questo pezzo
func _mostra_dipinto():
	if dipinto:
		dipinto.queue_free()
		dipinto = null
	if Pittura.attiva and not IMMAGINI.has(tipo):
		var strisce: Array = Pittura.strisce(name)
		if not strisce.empty():
			var margine := 0.0 if tipo == Tipo.FUORI else float(MARGINE_DIPINTO)
			dipinto = Node2D.new()
			dipinto.position = Vector2(-margine, -margine)
			add_child(dipinto)
			var x := 0.0
			for immagine in strisce:
				var s := Sprite.new()
				s.texture = immagine
				s.centered = false
				s.position.x = x
				dipinto.add_child(s)
				x += immagine.get_width()
	update()


# Numeri "casuali" ma sempre uguali per lo stesso pezzo, così il disegno non cambia a ogni avvio
func _caso() -> RandomNumberGenerator:
	var rng := RandomNumberGenerator.new()
	rng.seed = int(position.x * 7 + position.y * 13 + dimensioni.x * 3)
	return rng


func _draw():
	if dipinto:
		return
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
		Tipo.TERRA:
			_disegna_terra()
		Tipo.TERRA_ORTO:
			_disegna_terra_orto()
		Tipo.ACQUA:
			_disegna_acqua()
		Tipo.MATTONI:
			_disegna_mattoni()
		Tipo.LAMIERA:
			_disegna_lamiera()
		Tipo.CEMENTO:
			_disegna_cemento()
		Tipo.FOSSA:
			_disegna_fossa()
		Tipo.SOPPALCO:
			_disegna_soppalco()
		Tipo.PILASTRO:
			_disegna_pilastro()


# Parete di assi verticali con chiodi e nodi del legno
func _disegna_parete():
	var rng := _caso()
	var larghezza_asse := 64.0
	var x := 0.0
	var i := 0
	var tondi := []
	while x < dimensioni.x:
		var w: float = min(larghezza_asse, dimensioni.x - x)
		var tono := Color("e3bf8a") if i % 2 == 0 else Color("dcb67f")
		# solo rettangoli e poligoni: la scheda video li disegna tutti insieme in un colpo solo
		# (righe spesse e cerchi andrebbero disegnati uno per uno, e la parete è lunga quanto il livello)
		draw_rect(Rect2(x, 0, w, dimensioni.y), tono)
		draw_rect(Rect2(x + 5, 0, 2, dimensioni.y), Color("ebcd9d"))
		draw_rect(Rect2(x - 1.5, 0, 3, dimensioni.y), Color("b98f5c"))
		for y in [40.0, dimensioni.y - 120.0]:
			tondi.append([Vector2(x + w / 2, y), Vector2(3, 3), Color("9a7448")])
		if rng.randf() < 0.35:
			var centro := Vector2(x + rng.randf_range(16, w - 16), rng.randf_range(120, dimensioni.y - 200))
			tondi.append([centro, Vector2(7, 11), Color("c9a06b")])
			tondi.append([centro, Vector2(3, 5), Color("a87f4f")])
		x += larghezza_asse
		i += 1
	# zoccolo scuro vicino al pavimento
	draw_rect(Rect2(0, dimensioni.y - 110, dimensioni.x, 30), Color("c9a06b"))
	# chiodi e nodi del legno tutti insieme, dopo i rettangoli (alternarli spezzerebbe il gruppo)
	for t in tondi:
		_ovale(t[0], t[1], t[2])


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
	# solo rettangoli e poligoni, raggruppati: la scheda video li disegna in pochi colpi
	var r := Rect2(Vector2.ZERO, dimensioni)
	draw_rect(r, Color("b07a3e"))
	draw_rect(Rect2(4, 0, 6, dimensioni.y), Color("c99a5c"))
	_cornice(r, CONTORNO, 3.0)
	var y := 40.0
	while y < dimensioni.y:
		_striscia(Vector2(dimensioni.x * 0.3, y), Vector2(dimensioni.x * 0.7, y + 18), 2.0, LEGNO_SCURO)
		y += 90.0


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
	var fili := []
	while c < w + h:
		# diagonale che scende verso destra: y = x - c
		var x1: float = max(0.0, c)
		var x2: float = min(w, h + c)
		if x2 > x1:
			fili.append([Vector2(x1, x1 - c), Vector2(x2, x2 - c)])
		# diagonale che sale verso destra: y = c - x
		var x3: float = max(0.0, c - h)
		var x4: float = min(w, c)
		if x4 > x3:
			fili.append([Vector2(x3, c - x3), Vector2(x4, c - x4)])
		c += passo
	# i fili come strisce sottili (poligoni): la scheda video li disegna tutti insieme;
	# prima un alone più largo e trasparente, poi il filo, così i bordi restano morbidi
	var alone := Color(filo.r, filo.g, filo.b, 0.35)
	for f in fili:
		_striscia(f[0], f[1], 3.2, alone)
	for f in fili:
		_striscia(f[0], f[1], 1.6, filo)
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


# Terra battuta del cortile, con sassolini e ciuffi d'erba
func _disegna_terra():
	var rng := _caso()
	var w := dimensioni.x
	var h := dimensioni.y
	draw_rect(Rect2(0, 0, w, h), Color("c9a06a"))
	draw_rect(Rect2(0, h * 0.55, w, h * 0.45), Color("b08650"))
	draw_line(Vector2(0, 2), Vector2(w, 2), Color("a8834e"), 4.0)
	# sassolini
	for _n in range(int(w / 40)):
		var c := Vector2(rng.randf_range(4, w - 4), rng.randf_range(10, h - 10))
		var r := rng.randf_range(3, 6)
		_ellisse(c, Vector2(r * 1.4, r), Color("8e877c"))
		_ellisse(c + Vector2(-1, -1), Vector2(r * 1.1, r * 0.7), Color("b5afa4"))
	# ciuffi d'erba sul bordo
	for _n in range(int(w / 90)):
		var x := rng.randf_range(10, w - 10)
		var ciuffo := PoolVector2Array([Vector2(x - 9, 2), Vector2(x - 6, -10), Vector2(x - 2, 0), Vector2(x + 1, -14),
				Vector2(x + 4, 0), Vector2(x + 8, -9), Vector2(x + 10, 2)])
		draw_colored_polygon(ciuffo, Color("6dbe45"), PoolVector2Array(), null, null, true)


# Terra scura dell'orto, con i solchi e le piantine appena spuntate
func _disegna_terra_orto():
	var rng := _caso()
	var w := dimensioni.x
	var h := dimensioni.y
	draw_rect(Rect2(0, 0, w, h), Color("7a5230"))
	# bordo ondulato più chiaro
	var punti := PoolVector2Array([Vector2(0, 12)])
	var x := 0.0
	while x <= w:
		punti.append(Vector2(x, -2 + sin(x * 0.08) * 3))
		x += 10.0
	punti.append(Vector2(w, 12))
	draw_colored_polygon(punti, Color("8a5e36"), PoolVector2Array(), null, null, true)
	# solchi
	for y in [28.0, 50.0]:
		if y < h:
			draw_line(Vector2(0, y), Vector2(w, y), Color("5e3e20"), 5.0)
	# piantine appena spuntate
	for _n in range(int(w / 80)):
		var c := Vector2(rng.randf_range(10, w - 10), 2)
		_ellisse(c + Vector2(-4, -3), Vector2(5, 3), Color("6dbe45"))
		_ellisse(c + Vector2(4, -3), Vector2(5, 3), Color("6dbe45"))
		draw_line(c, c + Vector2(0, -4), Color("3e7a22"), 2.0)


# Acqua del canale d'irrigazione: ci si cade dentro e si riparte dal nido
func _disegna_acqua():
	var w := dimensioni.x
	var h := dimensioni.y
	draw_rect(Rect2(0, 0, w, h), Color("5db4e3"))
	draw_rect(Rect2(0, 0, w, 6), Color("8fd0f2"))
	var x := 10.0
	while x < w - 20:
		draw_line(Vector2(x, 14), Vector2(x + 16, 14), Color("8fd0f2"), 3.0, true)
		x += 46.0


# Parete del magazzino: mattoni a due colori (una piastrella ripetuta) e gli oblò in alto
func _disegna_mattoni():
	draw_set_transform(Vector2.ZERO, 0, Vector2(0.5, 0.5))  # la piastrella è disegnata al doppio
	draw_texture_rect(MATTONI_PIASTRELLA, Rect2(Vector2.ZERO, dimensioni * 2), true)
	draw_set_transform(Vector2.ZERO, 0, Vector2.ONE)
	# oblò: solo poligoni, così la scheda video li disegna tutti insieme (la parete è lunga quanto il livello)
	var x := 330.0
	while x < dimensioni.x - 30:
		var c := Vector2(x, 160)
		_ovale(c, Vector2(24, 24), Color("8c9096"), 28)
		_ovale(c, Vector2(20, 20), Color("5e646a"), 28)
		_ovale(c, Vector2(17, 17), Color("eaf4fa"), 28)
		_spicchio(c, 9.5, 12.5, -2.4, -1.2, Color.white)
		x += 650.0


# Soffitto di lamiera ondulata con i lucernari, la trave e le lampade
func _disegna_lamiera():
	var w := dimensioni.x
	var h := dimensioni.y
	# solo rettangoli pieni (anche le cornici): la scheda video li disegna tutti insieme
	draw_rect(Rect2(0, 0, w, h - 12), Color("c9cccf"))
	var x := 0.0
	while x < w:
		draw_rect(Rect2(x, 0, 6, h - 12), Color("b5babf"))
		x += 12.0
	# raggruppati per colore (prima tutti i vetri, poi tutte le cornici): ogni cambio di colore spezza il gruppo
	var lucernari := []
	x = 180.0
	while x < w - 150:
		lucernari.append(Rect2(x, 8, 150, h - 30))
		x += 460.0
	for r in lucernari:
		draw_rect(r, Color("eef6fb"))
	for r in lucernari:
		_cornice(r, Color("9da3a8"), 3.0)
	draw_rect(Rect2(0, h - 14, w, 12), Color("a8adb3"))
	draw_rect(Rect2(0, h - 3, w, 2), Color("7e848a"))
	var lampade := []
	x = 100.0
	while x < w - 80:
		lampade.append(Rect2(x, h - 2, 80, 6))
		x += 260.0
	for r in lampade:
		draw_rect(r, Color("f5f8fa"))
	for r in lampade:
		_cornice(r, Color("9da3a8"), 1.5)


# Pavimento di cemento grigio chiaro con i giunti
func _disegna_cemento():
	var w := dimensioni.x
	var h := dimensioni.y
	draw_rect(Rect2(0, 0, w, h), Color("d8dcd8"))
	draw_line(Vector2(0, 2), Vector2(w, 2), Color("a9aeaa"), 4.0)
	draw_line(Vector2(0, 24), Vector2(w, 24), Color("c7ccc8"), 2.0)
	var x := 160.0
	while x < w:
		draw_line(Vector2(x, 4), Vector2(x - 30, h), Color("c3c8c4"), 2.0)
		x += 320.0


# Fossa nel pavimento (la rampa di carico): ci si cade dentro e si riparte dal nido
func _disegna_fossa():
	var w := dimensioni.x
	var h := dimensioni.y
	draw_rect(Rect2(0, 0, w, h), Color("3a3d42"))
	draw_rect(Rect2(0, 0, w, 10), Color("2a2c30"))
	# bordi a strisce gialle e nere, come quelli di sicurezza
	for lato in [0.0, w - 12.0]:
		var y := 0.0
		while y < h:
			draw_rect(Rect2(lato, y, 12, 10), Color("f2c230"))
			draw_rect(Rect2(lato, y + 10, 12, 10), Color("2a2a2a"))
			y += 20.0


# Soppalco azzurro: piano di grigliato, trave azzurra e la ringhiera
func _disegna_soppalco():
	var w := dimensioni.x
	draw_rect(Rect2(0, 0, w, 6), GRIGIO)
	draw_rect(Rect2(0, 6, w, dimensioni.y - 6), AZZURRO)
	draw_rect(Rect2(0, 0, w, dimensioni.y), AZZURRO_SCURO, false, 2.5)
	for y in [-52.0, -28.0]:
		draw_line(Vector2(2, y), Vector2(w - 2, y), AZZURRO, 5.0)
	var x := 3.0
	while x < w:
		draw_line(Vector2(x, 0), Vector2(x, -52), AZZURRO, 4.0)
		x += 40.0
	draw_line(Vector2(w - 3, 0), Vector2(w - 3, -52), AZZURRO, 4.0)


# Pilastro azzurro del soppalco, con i bulloni
func _disegna_pilastro():
	draw_rect(Rect2(Vector2.ZERO, dimensioni), AZZURRO)
	draw_rect(Rect2(Vector2.ZERO, dimensioni), AZZURRO_SCURO, false, 2.5)
	var y := 20.0
	while y < dimensioni.y:
		draw_circle(Vector2(dimensioni.x / 2, y), 2.0, AZZURRO_SCURO)
		y += 60.0


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


# Ovale pieno fatto con un poligono a 16 lati (si disegna insieme agli altri pezzi, a differenza dei cerchi)
func _ovale(centro: Vector2, raggi: Vector2, colore: Color, lati := 16):
	var punti := PoolVector2Array()
	for k in range(lati):
		var a := TAU * k / float(lati)
		punti.append(centro + Vector2(cos(a) * raggi.x, sin(a) * raggi.y))
	draw_colored_polygon(punti, colore)


# Segmento spesso fatto con un poligono a quattro lati (si disegna insieme agli altri, a differenza delle righe)
func _striscia(da: Vector2, a: Vector2, spessore: float, colore: Color):
	var lato := (a - da).normalized().tangent() * spessore * 0.5
	draw_colored_polygon(PoolVector2Array([da + lato, a + lato, a - lato, da - lato]), colore)


# Cornice di un rettangolo fatta con quattro rettangoli pieni (come draw_rect vuoto, ma si disegna insieme agli altri)
func _cornice(r: Rect2, colore: Color, spessore: float):
	var m := spessore * 0.5
	draw_rect(Rect2(r.position.x - m, r.position.y - m, r.size.x + spessore, spessore), colore)
	draw_rect(Rect2(r.position.x - m, r.end.y - m, r.size.x + spessore, spessore), colore)
	draw_rect(Rect2(r.position.x - m, r.position.y + m, spessore, r.size.y - spessore), colore)
	draw_rect(Rect2(r.end.x - m, r.position.y + m, spessore, r.size.y - spessore), colore)


# Spicchio di anello (un riflesso curvo) fatto con un poligono
func _spicchio(centro: Vector2, raggio_dentro: float, raggio_fuori: float, da: float, a: float, colore: Color):
	var punti := PoolVector2Array()
	for k in range(9):
		var ang: float = lerp(da, a, k / 8.0)
		punti.append(centro + Vector2(cos(ang), sin(ang)) * raggio_fuori)
	for k in range(8, -1, -1):
		var ang: float = lerp(da, a, k / 8.0)
		punti.append(centro + Vector2(cos(ang), sin(ang)) * raggio_dentro)
	draw_colored_polygon(punti, colore)
