extends CanvasLayer
# Modalità dipinto, sempre disponibile come "Dipinto": un filtro che fa sembrare il gioco un quadro impressionista.
# Sta sopra il mondo di gioco ma sotto pulsanti, contatore e messaggi, che restano nitidi.
# Si accende e si spegne dal menu di pausa e dalla mappa; la scelta resta salvata.

const SHADER = preload("res://assets/shader/dipinto.shader")

var velo := ColorRect.new()


func _ready():
	layer = 1  # sopra il mondo; i pulsanti a schermo stanno sopra (vengono dopo nell'albero)
	pause_mode = Node.PAUSE_MODE_PROCESS
	var materiale := ShaderMaterial.new()
	materiale.shader = SHADER
	velo.material = materiale
	velo.rect_size = Vector2(1280, 720)
	velo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(velo)
	velo.visible = Progressi.dipinto


func attivo() -> bool:
	return velo.visible


func alterna():
	velo.visible = not velo.visible
	Progressi.dipinto = velo.visible
	Progressi.salva()
