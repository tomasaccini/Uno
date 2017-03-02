import modulo_rellenar_mazo
#Tengo que importar las constantes para el metodo puedo_tirar
ROJO = "Rojo"
AZUL = "Azul"
VERDE = "Verde"
AMARILLO = "Amarillo"
ESP_X2 = "X2"
ESP_X4 = "X4"
ESP_CAMBIO_SENTIDO = " -><- "
ESP_CAMBIO_COLOR = "COLOR"
ESP_SALTEO = "SALTEO"
ESP_NUEVA_FUNCIONALIDAD = "X2 A TODOS"

class Jugador:
	"""Representa a un jugador y sus cartas"""
	
	def __init__(self,nombre):
		"""Constructor. Recibe nombre como un str"""
		self.cartas = []
		self.nombre = nombre

	def __str__(self):
		""" Representacion en cadena de un Jugador """
		acumulador = "[ "
		for i in range(len(self.cartas)):
			acumulador += "  " + str(i+1) + "-" + str(self.cartas[i])
		return self.nombre + ":" + acumulador + " ]"

	def tirar_carta(self,posicion_carta,pozo):
		"""Recibe la posicion de la carta eliminar y la apila en el pozo"""
		carta_tirada = self.cartas.pop(posicion_carta)
		pozo.apilar(carta_tirada)
		return carta_tirada

	def ver_carta(self,posicion_carta):
		"""Recibe la posición de la carta en la mano del jugador y la devuelve"""
		return self.cartas[posicion_carta]

	def levantar_carta(self,mazo):
		""" Recibe un mazo y se levanta una carta del mismo. """
		self.cartas.append(mazo.levantar_carta())

	def puedo_tirar(self,posicion_carta,pozo_tope,color_actual):
		"""Recibe la posición de la carta en la mano, el tope del pozo junto con el color de la ultima carta y devuelve un boolean que determina si es válido o no tirar la carta """
		carta = self.cartas[posicion_carta]
	
		if carta.valor in (ESP_X4,ESP_CAMBIO_COLOR,ESP_NUEVA_FUNCIONALIDAD):
			return True
		if pozo_tope.valor in (ESP_X2,ESP_X4) and (carta.valor in (ESP_X2,ESP_X4)):
			return True
		if carta.color == color_actual:
			return True
		if carta.valor == pozo_tope.valor:
			return True
		return False
		
	def nombre_jugador(self):
		""" Devuelve el nombre del jugador """
		return self.nombre

	def cant_cartas(self):
		""" Devuelve la cantidad de cartas de un jugador """
		return len(self.cartas)

	def ia_jugar_carta(self,mazo,pozo,levantar_acumulado,color_actual):
		""" Recibe el mazo, el pozo, el acumulado para levantar cartas y el color de la última carta, y devuelve una carta tirada, o None si no hubo ninguna opcion correcta para tirar """
		if levantar_acumulado > 0:
			for pos_actual in range(self.cant_cartas()):
				if self.ver_carta(pos_actual).valor_carta() in (ESP_X2,ESP_X4):
					return (self.tirar_carta(pos_actual,pozo))
			return None
		else:	
			for pos_actual in range(len(self.cartas)):
				if self.puedo_tirar(pos_actual,pozo.ver_tope(),color_actual):
					return (self.tirar_carta(pos_actual,pozo))
			try:
				self.levantar_carta(mazo)
			except ValueError:
				mazo,pozo = modulo_rellenar_mazo.rellenar_mazo(mazo,pozo)
				print("Se acabaron las cartas del mazo y se rellenaron con las del pozo")
				self.levantar_carta(mazo)
			if self.puedo_tirar(self.cant_cartas() - 1,pozo.ver_tope(),color_actual):
				return self.tirar_carta(self.cant_cartas() - 1,pozo)
			else:
				return None