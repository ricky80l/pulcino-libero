extends Node2D
# Pulcino segnaposto: quadrato giallo con occhi e becco. Lo sostituiremo nella Tappa 6.


func _draw():
	draw_rect(Rect2(-20, -20, 40, 40), Color(1.0, 0.85, 0.2))
	# occhi
	draw_circle(Vector2(4, -6), 5, Color.white)
	draw_circle(Vector2(14, -6), 5, Color.white)
	draw_circle(Vector2(6, -6), 2.5, Color.black)
	draw_circle(Vector2(16, -6), 2.5, Color.black)
	# becco
	draw_colored_polygon(PoolVector2Array([Vector2(20, 0), Vector2(28, 4), Vector2(20, 8)]), Color(1.0, 0.5, 0.1))
