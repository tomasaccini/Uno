import random
import modulo_carta
import modulo_mazo_cartas
import modulo_verificador_alfabetico
import modulo_verificador_numerico
import modulo_rellenar_mazo
import modulo_ronda

ROJO = "Rojo"
AZUL = "Azul"
VERDE = "Verde"
AMARILLO = "Amarillo"
ESP_X2 = "X2"
ESP_X4 = "X4"
ESP_CAMBIO_SENTIDO = " -><- "
ESP_CAMBIO_COLOR = "COLOR"
ESP_SALTEO = "SALTEO"
#La carta especial es un x2 a todos sin excepcion (no se puede acumular, ni se puede tirar en caso que haya un acumulado para levantar), y cambia el color al que el que la tiró quiera (random en caso que la tire la pc)
ESP_NUEVA_FUNCIONALIDAD = "X2 A TODOS"
CANTIDAD_CARTAS_AL_INICIO = 7

class Juego:
	""" Representa una partida del juego Uno. """
	def __init__(self,mazo,pozo,ronda):
		""" Constructor. """
		self.mazo = mazo
		self.pozo = pozo
		self.ronda = ronda
		self.levantar_acumulado = 0
		self.saltear = False
		self.color_actual = None
		self.carta_jugada = None


		
	def consultar_levantar_acumulado(self):
		""" Devuelve el acumulado de cartas a levantar como un entero. """
		return self.levantar_acumulado

	def asignar_levantar_acumulado(self,acumulado):
		""" Recibe un nuevo pozo acumulado, y lo asigna al atributo levantar_acumulado. """
		self.levantar_acumulado = acumulado

	def consultar_estado_saltear(self):
		""" Devuelve un booleano indicando si se debe saltear el turno o no """
		return self.saltear

	def asignar_estado_saltear(self,estado):
		""" Recibe un booleano y lo asigna al atributo saltear """
		self.saltear = estado

	def consultar_color_actual(self):
		""" Devuelve el color actual """
		return self.color_actual

	def asignar_color_actual(self,color):
		""" Recibe una de los 4 posibles colores dentro del juego como cadena y lo asigna al atributo color_actual. """
		self.color_actual = color

	def consultar_carta_jugada(self):
		""" Devuelve la carta jugada """
		return self.carta_jugada

	def asignar_carta_jugada(self,carta):
		""" Recibe una carta. Asigna al atributo carta jugada la ultima carta jugada en la partida. """
		self.carta_jugada = carta

	def completar_mazo_cartas_iniciales(self):
		"""Agrega las cartas iniciales al mazo, con ciclos."""
		#Ciclo de 4 para los 4 colores
		for i in range(4):
			if i == 0:
				color_actual = VERDE
			elif i == 1:
				color_actual = AMARILLO
			elif i == 2:
				color_actual = ROJO
			else:
				color_actual =  AZUL
			#Ciclo de 10 para las cartas numericas
			for j in range(0,10):
				cantidad_cartas_por_numero = 1
				if j != 0:
					cantidad_cartas_por_numero = 2
				for k in range(cantidad_cartas_por_numero):
					self.mazo.apilar(modulo_carta.Carta(j,color_actual))
			#Ahora las cartas especiales con dos cartas por color
			for l in range(2):
				self.mazo.apilar(modulo_carta.Carta(ESP_X2,color_actual))
				self.mazo.apilar(modulo_carta.Carta(ESP_CAMBIO_SENTIDO,color_actual))
				self.mazo.apilar(modulo_carta.Carta(ESP_SALTEO,color_actual))
		#Ciclo de 4 para las 4 cartas de cada uno de los tipos sin color
		for m in range(4):
			self.mazo.apilar(modulo_carta.Carta(ESP_X4))
			self.mazo.apilar(modulo_carta.Carta(ESP_CAMBIO_COLOR))
			self.mazo.apilar(modulo_carta.Carta(ESP_NUEVA_FUNCIONALIDAD))

	def pedir_carta(self,mensaje):
		"""Recibe un mensaje en forma de string. Se le pide al usuario que seleccione una carta valida. Devuelve la posición de la carta que se jugará"""
		pos_carta = modulo_verificador_numerico.verificador_input_numerico(mensaje, 0, self.ronda.jugador_actual().cant_cartas()) - 1
		if self.levantar_acumulado == 0:
			while pos_carta != -1 and not(self.ronda.jugador_actual().puedo_tirar(pos_carta,self.pozo.ver_tope(),self.color_actual)):
				print("\nNo puede tirar esa carta. Eliga otra")
				pos_carta = modulo_verificador_numerico.verificador_input_numerico("\nIngrese la posición de la carta que quiere jugar: ", 0, self.ronda.jugador_actual().cant_cartas()) - 1
		return pos_carta

	def determinar_nuevo_color(self):
		""" Si el jugador actual es el usuario, el pide un color. Si el jugador actual es la maquina, selecciona un color aleatorio. Devuelve un color en forma de string"""
		if self.ronda.es_usuario_actual():
			mensaje = "Cambio de color. \nIngrese un 1 para cambiar a Rojo. \nIngrese un 2 para cambiar a Azul. \nIngrese un 3 para cambiar a Verde. \nIngrese un 4 para cambiar a Amarillo."
			opcion_elegida = modulo_verificador_numerico.verificador_input_numerico(mensaje, 1, 4)
		else:
			opcion_elegida = random.randrange(1,5)
		if opcion_elegida == 1:
			return ROJO
		elif opcion_elegida == 2:
			return AZUL
		elif opcion_elegida == 3:
			return VERDE
		elif opcion_elegida == 4:
			return AMARILLO

	def x2_a_todos(self):
		"""Agrega dos cartas a las manos de todos los jugadores excepto el que tira la carta."""
		cartas_a_levantar = 2
		print("\nTodos levantan dos cartas menos {}".format(self.ronda.jugador_actual().nombre_jugador()))
		for i in range(len(self.ronda)-1):
			self.ronda.jugador_siguiente()
			for i in range(cartas_a_levantar):
				try:
					self.ronda.jugador_actual().levantar_carta(self.mazo)
				except ValueError:
					self.mazo,self.pozo = modulo_rellenar_mazo.rellenar_mazo(self.mazo,self.pozo)
					print("Se acabaron las cartas del mazo y se rellenaron con las del pozo")
					self.ronda.jugador_actual().levantar_carta(self.mazo)
			print("El jugador {} agarró 2 cartas".format(self.ronda.jugador_actual().nombre_jugador()))
		self.ronda.jugador_siguiente()