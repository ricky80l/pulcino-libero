extends Node2D
# Pulcino segnaposto: quadrato giallo con occhi e becco. Lo sostituiremo nella Tappa 6.
# L'origine è tra i piedi, così si schiaccia e si allunga "da terra".

var tempo := 0.0
var prossimo_battito := 2.0


func _process(delta):
	tempo += delta
	update()


func _draw():
	var pulcino = get_parent()
	draw_rect(Rect2(-20, -40, 40, 40), Color(1.0, 0.85, 0.2))
	# becco
	draw_colored_polygon(PoolVector2Array([Vector2(20, -20), Vector2(28, -16), Vector2(20, -12)]), Color(1.0, 0.5, 0.1))
	if pulcino.timer_sbalzo > 0:
		# occhi a X: è stato travolto dal topo
		for cx in [6, 16]:
			draw_line(Vector2(cx - 4, -30), Vector2(cx + 4, -22), Color.black, 2.0)
			draw_line(Vector2(cx + 4, -30), Vector2(cx - 4, -22), Color.black, 2.0)
		return
	# battito di ciglia ogni tanto
	if tempo > prossimo_battito:
		if tempo > prossimo_battito + 0.12:
			prossimo_battito = tempo + rand_range(2.0, 4.0)
		draw_line(Vector2(0, -26), Vector2(20, -26), Color.black, 2.0)
		return
	draw_circle(Vector2(4, -26), 5, Color.white)
	draw_circle(Vector2(14, -26), 5, Color.white)
	draw_circle(Vector2(6, -26), 2.5, Color.black)
	draw_circle(Vector2(16, -26), 2.5, Color.black)
