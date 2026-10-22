extends Node
# Progressi del giocatore, sempre disponibili come "Progressi".
# Ricorda i livelli sbloccati e il record di chicchi, e li salva sul telefono (anche chiudendo il browser).

const FILE := "user://progressi.json"

# I dieci luoghi del viaggio. "scena" vuota = livello non ancora costruito.
const LIVELLI := [
	{"nome": "Il pollaio", "scena": "res://scenes/livello_1.tscn"},
	{"nome": "Il cortile", "scena": ""},
	{"nome": "L'orto", "scena": ""},
	{"nome": "Il prato", "scena": ""},
	{"nome": "Il bosco", "scena": ""},
	{"nome": "Lo stagno", "scena": ""},
	{"nome": "La collina", "scena": ""},
	{"nome": "La grotta", "scena": ""},
	{"nome": "Il paese", "scena": ""},
	{"nome": "Il campanile", "scena": ""},
]

var sbloccato := 1  # numero del livello più avanti che si può giocare
var record := {}  # numero livello (come testo) -> {"presi": n, "totale": n}
var ultimo_giocato := 1  # dove sta il pulcino sulla mappa
var nebbia_vista := 1  # fin dove la mappa ha già mostrato la nebbia che si dirada


func _ready():
	carica()


func livello_finito(numero: int, presi: int, totale: int):
	var chiave := str(numero)
	if not record.has(chiave) or presi > record[chiave]["presi"]:
		record[chiave] = {"presi": presi, "totale": totale}
	sbloccato = int(max(sbloccato, min(numero + 1, LIVELLI.size())))
	salva()


func finito(numero: int) -> bool:
	return record.has(str(numero))


func gioca(numero: int):
	ultimo_giocato = numero
	salva()
	get_tree().change_scene(LIVELLI[numero - 1]["scena"])


func torna_alla_mappa():
	get_tree().change_scene("res://scenes/mappa.tscn")


func salva():
	var f := File.new()
	if f.open(FILE, File.WRITE) == OK:
		f.store_string(to_json({"sbloccato": sbloccato, "record": record,
				"ultimo_giocato": ultimo_giocato, "nebbia_vista": nebbia_vista}))
		f.close()


func carica():
	var f := File.new()
	if not f.file_exists(FILE) or f.open(FILE, File.READ) != OK:
		return
	var dati = parse_json(f.get_as_text())
	f.close()
	if typeof(dati) == TYPE_DICTIONARY:
		sbloccato = int(dati.get("sbloccato", 1))
		record = dati.get("record", {})
		ultimo_giocato = int(dati.get("ultimo_giocato", 1))
		nebbia_vista = int(dati.get("nebbia_vista", 1))
