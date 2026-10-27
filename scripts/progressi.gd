extends Node
# Progressi del giocatore, sempre disponibili come "Progressi".
# Ricorda i livelli sbloccati e il record di chicchi, e li salva sul telefono (anche chiudendo il browser).

const FILE := "user://progressi.json"

# I dieci luoghi del viaggio. "scena" vuota = livello non ancora costruito.
const LIVELLI := [
	{"nome": "Il pollaio", "scena": "res://scenes/livello_1.tscn"},
	{"nome": "Il cortile", "scena": "res://scenes/livello_2.tscn"},
	{"nome": "L'orto", "scena": "res://scenes/livello_3.tscn"},
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
var abilita_viste := []  # abilità di cui il giocatore ha già visto l'avviso "Nuova abilità!"


func abilita_vista(nome: String) -> bool:
	return abilita_viste.has(nome)


func segna_abilita_vista(nome: String):
	if not abilita_viste.has(nome):
		abilita_viste.append(nome)
		salva()


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


# Un luogo si può giocare se è sbloccato e il suo livello è già costruito
func giocabile(numero: int) -> bool:
	return numero >= 1 and numero <= sbloccato and LIVELLI[numero - 1]["scena"] != ""


func costruito(numero: int) -> bool:
	return numero >= 1 and numero <= LIVELLI.size() and LIVELLI[numero - 1]["scena"] != ""


# Il luogo più avanti che si può giocare
func ultimo_giocabile() -> int:
	var n := sbloccato
	while n > 1 and not giocabile(n):
		n -= 1
	return n


# Crescita del pulcino: stadio per ogni livello (vedi CLAUDE.md). Esistono già i disegni degli stadi 1 e 2.
const STADIO_DEL_LIVELLO := [1, 2, 2, 3, 3, 4, 4, 5, 5, 6]


func stadio_di(numero: int) -> int:
	return STADIO_DEL_LIVELLO[int(clamp(numero, 1, LIVELLI.size())) - 1]


# Stadio da mostrare: nella mappa quello del luogo più avanti, nei livelli quello del livello giocato
var in_mappa := true


func stadio_in_gioco() -> int:
	return stadio_di(ultimo_giocabile() if in_mappa else ultimo_giocato)


func gioca(numero: int):
	ultimo_giocato = numero
	in_mappa = false
	salva()
	get_tree().change_scene(LIVELLI[numero - 1]["scena"])


func torna_alla_mappa():
	in_mappa = true
	get_tree().change_scene("res://scenes/mappa.tscn")


func salva():
	var f := File.new()
	if f.open(FILE, File.WRITE) == OK:
		f.store_string(to_json({"sbloccato": sbloccato, "record": record,
				"ultimo_giocato": ultimo_giocato, "nebbia_vista": nebbia_vista, "abilita_viste": abilita_viste}))
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
		abilita_viste = dati.get("abilita_viste", [])
