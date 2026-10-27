extends Node
# Modalità dipinta, sempre disponibile come "Pittura".
# Scambia i disegni cartoon con le versioni ridipinte a pennellate (in assets/dipinto/, create da
# strumenti/ridipingi.py). Si accende e si spegne dal menu di pausa; il telefono ricorda la scelta.
# Si vede solo nei luoghi che hanno anche il paesaggio dipinto (assets/dipinto/livelli/<scena>).

signal cambiata

const CARTELLA := "res://assets/dipinto/"

var luogo := ""  # scena in corso, per esempio "livello_2"
var attiva := false  # true quando si vede la versione dipinta
var coppie := {}  # disegno cartoon -> immagine dipinta
var originali := {}  # disegno cartoon -> file dell'immagine cartoon (per tornare indietro)


func _ready():
	_cerca(CARTELLA + "grafica")


# Trova le immagini dipinte e le collega ai disegni cartoon con lo stesso nome
func _cerca(cartella: String):
	var dir := Directory.new()
	if dir.open(cartella) != OK:
		return
	dir.list_dir_begin(true, true)
	var f := dir.get_next()
	while f != "":
		if dir.current_is_dir():
			_cerca(cartella + "/" + f)
		else:
			# nel gioco esportato i file compaiono come "nome.png.import"
			var nome := f.trim_suffix(".import")
			if nome.ends_with(".png"):
				var cartoon := (cartella + "/" + nome).replace(CARTELLA + "grafica/", "res://assets/grafica/").replace(".png", ".svg")
				if ResourceLoader.exists(cartoon):
					coppie[cartoon] = cartella + "/" + nome
		f = dir.get_next()
	dir.list_dir_end()


# Da chiamare all'ingresso di ogni scena con disegni (livelli e mappa)
func entra(scena: String):
	luogo = scena
	_aggiorna()


# Il luogo in corso ha la versione dipinta?
func disponibile() -> bool:
	return luogo != "" and Directory.new().dir_exists(CARTELLA + "livelli/" + luogo)


func imposta(acceso: bool):
	Progressi.dipinto = acceso
	Progressi.salva()
	_aggiorna()


# Le strisce dipinte di un pezzo disegnato da codice (pavimenti, pareti, paesaggio), da sinistra a destra
func strisce(nome_pezzo: String) -> Array:
	var risultato := []
	var i := 0
	while ResourceLoader.exists("%slivelli/%s/%s_%d.png" % [CARTELLA, luogo, nome_pezzo, i]):
		risultato.append(load("%slivelli/%s/%s_%d.png" % [CARTELLA, luogo, nome_pezzo, i]))
		i += 1
	return risultato


func _aggiorna():
	attiva = Progressi.dipinto and disponibile()
	# ogni disegno cartoon carica al suo posto l'immagine dipinta (o torna quella di prima):
	# così cambia ovunque sia usato, anche nei personaggi a pezzi, senza toccare il resto del gioco
	for cartoon in coppie:
		var immagine: StreamTexture = load(cartoon)
		if not originali.has(cartoon):
			originali[cartoon] = immagine.load_path
		var file: String = load(coppie[cartoon]).load_path if attiva else originali[cartoon]
		if immagine.load_path != file:
			immagine.load(file)
	emit_signal("cambiata")
