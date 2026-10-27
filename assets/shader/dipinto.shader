// Filtro "dipinto": trasforma lo schermo in qualcosa che ricorda un quadro impressionista.
// - pennellate: ogni punto è la media di una breve pennellata, la cui direzione cambia piano sullo schermo
// - tavolozza: più luce, toni pastello, ombre velate di lilla
// - tela: una trama leggera, come la grana di una tela dipinta
shader_type canvas_item;

uniform float forza : hint_range(0.0, 1.0) = 0.9;          // quanto è forte l'effetto
uniform float lunghezza : hint_range(0.0, 0.02) = 0.0022;  // lunghezza delle pennellate (rispetto all'altezza dello schermo)
uniform float dimensione_macchie = 40.0;                   // quante zone di pennellate diverse in altezza
uniform float pastello : hint_range(0.0, 1.0) = 0.38;      // quanto i colori si schiariscono verso il pastello
uniform float grana : hint_range(0.0, 0.2) = 0.05;         // quanto si vede la trama della tela

float caso(vec2 p) {
	return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

float rumore(vec2 p) {
	vec2 i = floor(p);
	vec2 f = fract(p);
	vec2 u = f * f * (3.0 - 2.0 * f);
	return mix(mix(caso(i), caso(i + vec2(1.0, 0.0)), u.x),
			mix(caso(i + vec2(0.0, 1.0)), caso(i + vec2(1.0, 1.0)), u.x), u.y);
}

void fragment() {
	vec2 uv = SCREEN_UV;
	float proporzione = SCREEN_PIXEL_SIZE.y / SCREEN_PIXEL_SIZE.x;  // larghezza / altezza
	vec2 posto = vec2(uv.x * proporzione, uv.y);

	// direzione della pennellata in questo punto: cambia piano da una zona all'altra
	float angolo = rumore(posto * dimensione_macchie) * 6.2831;
	vec2 passo = vec2(cos(angolo) / proporzione, sin(angolo)) * lunghezza;

	// media lungo la pennellata (9 campioni)
	vec3 colore = vec3(0.0);
	for (int i = -4; i <= 4; i++) {
		colore += texture(SCREEN_TEXTURE, uv + passo * float(i)).rgb;
	}
	colore /= 9.0;

	// tavolozza impressionista
	float luce = dot(colore, vec3(0.299, 0.587, 0.114));
	colore = mix(vec3(luce), colore, 1.15);                          // un po' più vivaci
	colore = mix(colore, colore * 0.8 + vec3(0.2, 0.2, 0.24), pastello);  // verso il pastello
	colore += vec3(0.05, 0.0, 0.08) * (1.0 - luce) * pastello;        // ombre lilla

	// trama della tela, uguale su ogni schermo
	vec2 tela = floor(vec2(uv.x * 720.0 * proporzione, uv.y * 720.0) / 1.5);
	colore += (caso(tela) - 0.5) * grana;
	colore += sin(uv.x * 720.0 * proporzione * 1.3) * sin(uv.y * 720.0 * 1.3) * grana * 0.3;

	vec3 originale = texture(SCREEN_TEXTURE, uv).rgb;
	COLOR = vec4(mix(originale, colore, forza), 1.0);
}
