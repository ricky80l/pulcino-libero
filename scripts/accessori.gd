extends Reference
# Gli accessori del pulcino che si comprano alla bancarella con i chicchi (vedi strumenti/disegni_accessori.py).
# Per ognuno: dove si indossa (uno per posto), prezzo, nome, immagine, perno nel disegno,
# punto del pulcino dove si aggancia (misure al doppio, stadio 1, origine tra i piedi) e inclinazione.

const ELENCO := {
	"fiocco": {"posto": "testa", "prezzo": 40, "nome": "Fiocco rosa",
			"immagine": preload("res://assets/grafica/accessori/fiocco.png"), "perno": Vector2(27, 19), "punto": Vector2(-16, -96), "angolo": -15},
	"occhiali": {"posto": "occhi", "prezzo": 60, "nome": "Occhiali tondi",
			"immagine": preload("res://assets/grafica/accessori/occhiali.png"), "perno": Vector2(20, 17), "punto": Vector2(18, -70), "angolo": 0},
	"sciarpa": {"posto": "collo", "prezzo": 80, "nome": "Sciarpa a righe",
			"immagine": preload("res://assets/grafica/accessori/sciarpa.png"), "perno": Vector2(52, 18), "punto": Vector2(0, -34), "angolo": 0},
	"berretto": {"posto": "testa", "prezzo": 100, "nome": "Berretto rosso",
			"immagine": preload("res://assets/grafica/accessori/berretto.png"), "perno": Vector2(42, 46), "punto": Vector2(4, -90), "angolo": -6},
	"cappello": {"posto": "testa", "prezzo": 120, "nome": "Cappello di paglia",
			"immagine": preload("res://assets/grafica/accessori/cappello.png"), "perno": Vector2(60, 50), "punto": Vector2(2, -88), "angolo": -8},
}
const ORDINE := ["fiocco", "occhiali", "sciarpa", "berretto", "cappello"]
