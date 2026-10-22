extends Node
# Suoni del gioco, sempre disponibili come "Suoni". Esempio: Suoni.suona("salto")

const ELENCO := {
	"salto": preload("res://assets/suoni/salto.wav"),
	"atterra": preload("res://assets/suoni/atterra.wav"),
	"chicco": preload("res://assets/suoni/chicco.wav"),
	"colpito": preload("res://assets/suoni/colpito.wav"),
	"squittio": preload("res://assets/suoni/squittio.wav"),
	"nido": preload("res://assets/suoni/nido.wav"),
	"fine": preload("res://assets/suoni/fine.wav"),
}

var lettori := []


func _ready():
	randomize()
	for i in range(8):
		var lettore := AudioStreamPlayer.new()
		add_child(lettore)
		lettori.append(lettore)


# variazione: cambia un po' l'intonazione ogni volta, così non suona sempre uguale
func suona(nome: String, variazione := 0.08, volume_db := 0.0):
	for lettore in lettori:
		if not lettore.playing:
			lettore.stream = ELENCO[nome]
			lettore.pitch_scale = 1.0 + rand_range(-variazione, variazione)
			lettore.volume_db = volume_db
			lettore.play()
			return
