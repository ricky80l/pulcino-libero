extends Node
# Progressi del giocatore, sempre disponibili come "Progressi".
# Ricorda i livelli sbloccati e il record di chicchi, e li salva sul telefono (anche chiudendo il browser).

const FILE := "user://progressi.json"

# Gli undici luoghi del viaggio. "scena" vuota = livello non ancora costruito.
const LIVELLI := [
	{"nome": "Il pollaio", "scena": "res://scenes/livello_1.tscn"},
	{"nome": "Il cortile", "scena": "res://scenes/livello_2.tscn"},
	{"nome": "L'orto", "scena": "res://scenes/livello_3.tscn"},
	{"nome": "Maglificio Granada", "scena": "res://scenes/livello_4.tscn", "senza_nuovo": true},  # nome lungo: niente «nuovo!» sul cartello
	{"nome": "Il prato", "scena": "res://scenes/livello_5.tscn"},
	{"nome": "Il bosco", "scena": ""},
	{"nome": "Lo stagno", "scena": ""},
	{"nome": "La collina", "scena": ""},
	{"nome": "La grotta", "scena": ""},
	{"nome": "Il paese", "scena": ""},
	{"nome": "Il campanile", "scena": ""},
]

const LUOGHI_CON_PIUMA := [1, 2, 3, 4, 5]  # luoghi che hanno già gli indizi della pulcina (Tappa 24)

var sbloccato := 1  # numero del livello più avanti che si può giocare
var record := {}  # numero livello (come testo) -> {"presi": n, "totale": n}
var ultimo_giocato := 1  # dove sta il pulcino sulla mappa
var nebbia_vista := 1  # fin dove la mappa ha già mostrato la nebbia che si dirada
var abilita_viste := []  # abilità di cui il giocatore ha già visto l'avviso "Nuova abilità!"
var dipinto := false  # true = modalità dipinta accesa (vedi Pittura)
var uova := []  # numeri dei luoghi dove l'uovo d'oro segreto è stato trovato
var stelle := {}  # numero livello (come testo) -> [tutti i chicchi, uovo d'oro, mai preso]: le migliori ottenute
var borsellino := 0  # chicchi da spendere alla bancarella: tutti quelli raccolti nelle partite finite
var comprati := []  # accessori comprati (vedi scripts/accessori.gd)
var indossati := {}  # posto ("testa", "occhi", "collo") -> accessorio indossato
var piume := []  # luoghi finiti in cui il pulcino ha trovato la piuma misteriosa (Tappa 24)
var piume_viste := []  # luoghi di cui la mappa ha già mostrato la scena della piuma


func compra(nome: String, prezzo: int) -> bool:
	if comprati.has(nome) or borsellino < prezzo:
		return false
	borsellino -= prezzo
	comprati.append(nome)
	salva()
	return true


func indossa(nome: String, posto: String):
	indossati[posto] = nome
	salva()


func togli(posto: String):
	indossati.erase(posto)
	salva()


func uovo_trovato_in(numero: int) -> bool:
	return uova.has(numero)


func segna_uovo(numero: int):
	if not uova.has(numero):
		uova.append(numero)
		salva()


func segna_piuma(numero: int):
	if not piume.has(numero):
		piume.append(numero)
		salva()


func segna_piuma_vista(numero: int):
	if not piume_viste.has(numero):
		piume_viste.append(numero)
		salva()


func abilita_vista(nome: String) -> bool:
	return abilita_viste.has(nome)


func segna_abilita_vista(nome: String):
	if not abilita_viste.has(nome):
		abilita_viste.append(nome)
		salva()


func _ready():
	carica()


func livello_finito(numero: int, presi: int, totale: int, nuove_stelle := [false, false, false]):
	var chiave := str(numero)
	borsellino += presi
	var vecchie: Array = stelle.get(chiave, [false, false, false])
	stelle[chiave] = [bool(vecchie[0]) or nuove_stelle[0], bool(vecchie[1]) or nuove_stelle[1], bool(vecchie[2]) or nuove_stelle[2]]
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


# Crescita del pulcino: stadio per ogni livello (vedi CLAUDE.md). Esistono già i disegni degli stadi 1, 2 e 3.
const STADIO_DEL_LIVELLO := [1, 2, 2, 2, 3, 3, 4, 4, 5, 5, 6]


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
				"ultimo_giocato": ultimo_giocato, "nebbia_vista": nebbia_vista, "abilita_viste": abilita_viste, "dipinto": dipinto, "uova": uova, "stelle": stelle,
				"borsellino": borsellino, "comprati": comprati, "indossati": indossati,
				"piume": piume, "piume_viste": piume_viste}))
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
		dipinto = bool(dati.get("dipinto", false))
		stelle = dati.get("stelle", {})
		comprati = dati.get("comprati", [])
		indossati = dati.get("indossati", {})
		if dati.has("borsellino"):
			borsellino = int(dati["borsellino"])
		else:
			# primo avvio con la bancarella: nel borsellino i chicchi dei record già fatti
			borsellino = 0
			for r in record.values():
				borsellino += int(r["presi"])
		uova = []
		for n in dati.get("uova", []):
			uova.append(int(n))  # nel file i numeri tornano decimali
		piume = []
		for n in dati.get("piume", []):
			piume.append(int(n))
		if not dati.has("piume"):
			# primo avvio con le piume: i luoghi già finiti (con gli indizi) danno la loro piuma, e la mappa ne mostra le scene
			for chiave in record.keys():
				if LUOGHI_CON_PIUMA.has(int(chiave)):
					piume.append(int(chiave))
		piume_viste = []
		for n in dati.get("piume_viste", []):
			piume_viste.append(int(n))
