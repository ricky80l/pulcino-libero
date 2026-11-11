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
	"becco": preload("res://assets/suoni/becco.wav"),
	"botta": preload("res://assets/suoni/botta.wav"),
	"rotto": preload("res://assets/suoni/rotto.wav"),
	"starnazzo": preload("res://assets/suoni/starnazzo.wav"),
	"doppio": preload("res://assets/suoni/doppio.wav"),
	"boing": preload("res://assets/suoni/boing.wav"),
	"traballa": preload("res://assets/suoni/traballa.wav"),
	"rotola": preload("res://assets/suoni/rotola.wav"),
	"plana": preload("res://assets/suoni/plana.wav"),
	"uovo": preload("res://assets/suoni/uovo.wav"),
	"stella": preload("res://assets/suoni/stella.wav"),
	"bu": preload("res://assets/suoni/bu.wav"),
	"scava": preload("res://assets/suoni/scava.wav"),
	"curioso": preload("res://assets/suoni/curioso.wav"),
	"piuma": preload("res://assets/suoni/piuma.wav"),
}

# La musica (Tappa 27): tre brani di Kevin MacLeod (incompetech.com), licenza CC BY 4.0, citati nei Crediti.
# Preparati da strumenti/prepara_musica.py. Si ripetono senza fine; cambiando luogo un brano sfuma nell'altro.
const MUSICHE := {
	"mappa": preload("res://assets/musica/mappa.ogg"),
	"aperto": preload("res://assets/musica/aperto.ogg"),
	"chiuso": preload("res://assets/musica/chiuso.ogg"),
}
const VOLUME_MUSICA := -9.0  # la musica sta sotto ai versi e ai suoni
const SILENZIO := -60.0
const DURATA_SFUMATURA := 1.2

# Due "canali", ognuno con il suo interruttore (nel menu di pausa e sulla mappa): Musica e Suoni
const CANALE_MUSICA := "Musica"
const CANALE_SUONI := "Suoni"

var lettori := []
var musica_attuale := ""
var musica: AudioStreamPlayer  # il brano che si sente
var musica_vecchia: AudioStreamPlayer  # quello che sta sfumando via
var sfumatura := Tween.new()


func _ready():
	randomize()
	pause_mode = Node.PAUSE_MODE_PROCESS  # la musica continua anche col gioco in pausa
	_crea_canale(CANALE_MUSICA)
	_crea_canale(CANALE_SUONI)
	for i in range(8):
		var lettore := AudioStreamPlayer.new()
		lettore.bus = CANALE_SUONI
		add_child(lettore)
		lettori.append(lettore)
	musica = AudioStreamPlayer.new()
	musica_vecchia = AudioStreamPlayer.new()
	for m in [musica, musica_vecchia]:
		m.bus = CANALE_MUSICA
		add_child(m)
	add_child(sfumatura)
	for brano in MUSICHE.values():
		brano.loop = true
	call_deferred("_applica_preferenze")  # i Progressi (con le preferenze salvate) partono dopo


func _crea_canale(nome: String):
	if AudioServer.get_bus_index(nome) >= 0:
		return
	AudioServer.add_bus()
	var indice := AudioServer.get_bus_count() - 1
	AudioServer.set_bus_name(indice, nome)
	AudioServer.set_bus_send(indice, "Master")


func _applica_preferenze():
	AudioServer.set_bus_mute(AudioServer.get_bus_index(CANALE_MUSICA), not Progressi.musica_attiva)
	AudioServer.set_bus_mute(AudioServer.get_bus_index(CANALE_SUONI), not Progressi.suoni_attivi)


# Interruttori: spengono o riaccendono un canale e il telefono se lo ricorda
func imposta_musica(attiva: bool):
	Progressi.musica_attiva = attiva
	Progressi.salva()
	_applica_preferenze()


func imposta_suoni(attivi: bool):
	Progressi.suoni_attivi = attivi
	Progressi.salva()
	_applica_preferenze()


# Fa partire un brano ("mappa", "aperto", "chiuso"): se ne suonava un altro, i due si scambiano sfumando.
# Se è già quello, resta com'è (e torna al volume normale se era stato abbassato).
func musica_di(nome: String):
	if nome == musica_attuale and musica.playing:
		sfumatura.stop_all()
		sfumatura.interpolate_property(musica, "volume_db", musica.volume_db, VOLUME_MUSICA, 0.6)
		sfumatura.start()
		return
	musica_attuale = nome
	sfumatura.stop_all()
	var vecchia := musica
	musica = musica_vecchia
	musica_vecchia = vecchia
	musica.stream = MUSICHE[nome]
	musica.volume_db = SILENZIO
	musica.play()
	sfumatura.interpolate_property(musica, "volume_db", SILENZIO, VOLUME_MUSICA, DURATA_SFUMATURA, Tween.TRANS_SINE, Tween.EASE_OUT)
	if musica_vecchia.playing:
		sfumatura.interpolate_property(musica_vecchia, "volume_db", musica_vecchia.volume_db, SILENZIO, DURATA_SFUMATURA * 0.8)
		sfumatura.interpolate_callback(musica_vecchia, DURATA_SFUMATURA * 0.8, "stop")
	sfumatura.start()


# A fine livello la musica si abbassa, così si sente la fanfara
func abbassa_musica():
	sfumatura.stop_all()
	sfumatura.interpolate_property(musica, "volume_db", musica.volume_db, VOLUME_MUSICA - 14.0, 0.5)
	sfumatura.start()


# variazione: cambia un po' l'intonazione ogni volta, così non suona sempre uguale
func suona(nome: String, variazione := 0.08, volume_db := 0.0, tono := 1.0):
	for lettore in lettori:
		if not lettore.playing:
			lettore.stream = ELENCO[nome]
			lettore.pitch_scale = tono * (1.0 + rand_range(-variazione, variazione))
			lettore.volume_db = volume_db
			lettore.play()
			return
