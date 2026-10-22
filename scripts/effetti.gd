extends Reference
# Piccoli effetti riutilizzabili: sbuffi di polvere, scintille.


# Uno sbuffo di particelle che si spegne e si cancella da solo
static func sbuffo(genitore: Node, posizione: Vector2, colore: Color, quantita := 8, velocita := 120.0):
	var p := CPUParticles2D.new()
	p.position = posizione
	p.one_shot = true
	p.amount = quantita
	p.lifetime = 0.45
	p.explosiveness = 1.0
	p.direction = Vector2(0, -1)
	p.spread = 75.0
	p.initial_velocity = velocita
	p.initial_velocity_random = 0.5
	p.gravity = Vector2(0, 350)
	p.scale_amount = 6.0
	p.scale_amount_random = 0.5
	var sfumatura := Gradient.new()
	sfumatura.colors = PoolColorArray([colore, Color(colore.r, colore.g, colore.b, 0)])
	p.color_ramp = sfumatura
	genitore.add_child(p)
	p.emitting = true
	genitore.get_tree().create_timer(1.0).connect("timeout", p, "queue_free")
