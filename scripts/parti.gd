extends Reference
# Aiuto per montare i personaggi a pezzi: ogni pezzo è un'immagine con il suo punto di rotazione.
# Le immagini sono disegnate al doppio della grandezza, per restare nitide sugli schermi fini.

const SCALA := 0.5


# perno: punto di rotazione nell'immagine (in pixel dell'immagine); posizione: dove va nel personaggio
static func crea(genitore: Node, immagine: Texture, perno: Vector2, posizione: Vector2) -> Sprite:
	var s := Sprite.new()
	s.texture = immagine
	s.centered = false
	s.offset = -perno
	s.scale = Vector2(SCALA, SCALA)
	s.position = posizione
	genitore.add_child(s)
	return s
