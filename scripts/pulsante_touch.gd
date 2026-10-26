extends TouchScreenButton
# Pulsante a schermo rotondo e semitrasparente. Preme la stessa azione della tastiera.

enum Simbolo { SINISTRA, DESTRA, SALTO, BECCO }

export(Simbolo) var simbolo := Simbolo.SINISTRA  # disegno sul pulsante
export var raggio := 70.0  # grandezza del cerchio disegnato
export var zona_tocco := Vector2(95, 130)  # metà larghezza e metà altezza della zona sensibile, più grande del cerchio
export var trasparenza := 0.35  # 0 = invisibile, 1 = pieno
export var trasparenza_premuto := 0.65  # quanto si illumina mentre lo tieni premuto
export var scala_telefono := 0.85  # grandezza sui telefoni (1 = com'è disegnato)
export var scala_pc := 0.6  # grandezza giocando dal PC, dove si usa la tastiera


func _ready():
	# Più piccolo su PC, un po' più piccolo su telefono; resta ancorato all'angolo più vicino in basso
	var s := scala_telefono if _e_telefono() else scala_pc
	var angolo := Vector2(0 if position.x < 640 else 1280, 720)
	position = angolo + (position - angolo) * s
	scale = Vector2(s, s)
	# Zona sensibile rettangolare: il pollice non deve centrare il cerchio
	var rettangolo := RectangleShape2D.new()
	rettangolo.extents = zona_tocco
	shape = rettangolo
	# Senza texture Godot sposterebbe la zona in basso a destra: la teniamo centrata sul cerchio
	shape_centered = false
	connect("pressed", self, "update")
	connect("released", self, "update")


static func _e_telefono() -> bool:
	# schermo touch, e non il gioco avviato direttamente sul PC
	return OS.has_touchscreen_ui_hint() and not OS.has_feature("pc")


func _draw():
	var alfa := trasparenza_premuto if is_pressed() else trasparenza
	draw_circle(Vector2.ZERO, raggio, Color(1, 1, 1, alfa))
	var s := raggio * 0.4
	var punti: PoolVector2Array
	match simbolo:
		Simbolo.SINISTRA:
			punti = PoolVector2Array([Vector2(-s, 0), Vector2(s * 0.6, -s), Vector2(s * 0.6, s)])
		Simbolo.DESTRA:
			punti = PoolVector2Array([Vector2(s, 0), Vector2(-s * 0.6, -s), Vector2(-s * 0.6, s)])
		Simbolo.SALTO:
			punti = PoolVector2Array([Vector2(0, -s), Vector2(-s, s * 0.6), Vector2(s, s * 0.6)])
		Simbolo.BECCO:
			# becco aperto che guarda a destra: due triangoli
			var col := Color(0.95, 0.5, 0.1, alfa + 0.3)
			draw_colored_polygon(PoolVector2Array([Vector2(-s * 0.8, -s * 0.7), Vector2(s, -s * 0.15), Vector2(-s * 0.8, -s * 0.05)]), col)
			draw_colored_polygon(PoolVector2Array([Vector2(-s * 0.8, s * 0.15), Vector2(s * 0.8, s * 0.45), Vector2(-s * 0.8, s * 0.7)]), col)
			return
	draw_colored_polygon(punti, Color(0.2, 0.15, 0.1, alfa + 0.2))
