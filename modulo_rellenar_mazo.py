import modulo_mazo_cartas

def rellenar_mazo(mazo,pozo):
	"""Recibe dos parámetros de tipo MazoCarta, mazo y pozo. Devuelve mazo y pozo modificados. Post: pierde todo el contenido de lo que tenía el mazo (pensado para cuando mazo esta vacío) 
	y lo pisa con el conenido del pozo (previamente reordenado) dejando al pozo solo con el tope."""
	ultima_carta = pozo.levantar_carta()
	pozo.mezclar()
	mazo = pozo
	pozo = modulo_mazo_cartas.MazoCartas()
	pozo.apilar(ultima_carta)
	return mazo,pozo