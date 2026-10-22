extends Reference
# Stile comune dei pulsanti di legno (mappa, pausa).

const LEGNO := Color("b07a3e")
const LEGNO_CHIARO := Color("c99a5c")
const CONTORNO := Color("5a3e14")
const BLOCCATO := Color("9a9a96")
const CREMA := Color(1, 0.96, 0.86)


static func pulsante_legno(b: Button, font: Font):
	b.add_font_override("font", font)
	b.add_color_override("font_color", CREMA)
	b.add_color_override("font_color_hover", Color(1, 1, 1))
	b.add_color_override("font_color_focus", Color(1, 1, 1))
	b.add_color_override("font_color_pressed", Color(1, 1, 1))
	b.add_color_override("font_color_disabled", Color(0.95, 0.95, 0.93))
	b.add_stylebox_override("normal", riquadro(LEGNO, CONTORNO, 4))
	b.add_stylebox_override("hover", riquadro(LEGNO_CHIARO, CONTORNO, 4))
	b.add_stylebox_override("pressed", riquadro(CONTORNO, CONTORNO, 4))
	b.add_stylebox_override("focus", riquadro(Color(0, 0, 0, 0), Color("ffd84a"), 8))
	b.add_stylebox_override("disabled", riquadro(BLOCCATO, Color("6b6b68"), 4))


static func riquadro(sfondo: Color, bordo: Color, spessore: int) -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = sfondo
	s.border_color = bordo
	s.set_border_width_all(spessore)
	s.set_corner_radius_all(18)
	return s
