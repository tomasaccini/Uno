import modulo_lista_circular
import modulo_jugador

CANTIDAD_CARTAS_AL_INICIO = 7

class Ronda:
	"""Representa el tablero entero con sus jugadores como nodos de una lista doblemente enlazada y circular. Servirá para llevar los turnos del partido"""

	def __init__(self):
		""" Constructor. """
		self.tablero = modulo_lista_circular.ListaCircular()
		self.j_actual = None
		self.sentido_horario = True

	def __str__(self):
		""" Representacion en cadena de una Ronda """
		return str(self.tablero)

	def __len__(self):
		""" Devuelve la cantidad de jugadores de una ronda """
		return len(self.tablero)

	def append(self,dato):
		""" Recibe un dato y lo agrega a la Ronda como nodo anterior a la mano. """
		self.tablero.append(dato)

	def jugador_actual(self):
		"""Devuelve el dato del nodo actual de la lista"""
		if self.tablero.devolver_primero() is None:
			raise ValueError("No hay mano decidida en esta ronda")
		return self.j_actual.dato

	def jugador_siguiente(self):
		"""Transforma el atributo jugador actual al siguiente en la lista"""
		if self.j_actual is None:
			self.j_actual = self.tablero.devolver_primero()
		else:
			self.j_actual = self.j_actual.prox
		return self.j_actual.dato

	def jugador_anterior(self):
		"""Transforma el atributo jugador actual al anterior en la lista"""
		if self.j_actual is None:
			self.j_actual = self.tablero.devolver_primero().ant
		else:
			self.j_actual = self.j_actual.ant
		return self.j_actual.dato

	def agregar_jugador(self,nombre):
		"""Agrega un jugador a la lista recibiendo y pasando como parámetro el nombre"""
		self.tablero.append(modulo_jugador.Jugador(nombre))

	def repartir_cartas(self,mazo):
		"""Inicializa las manos con las cartas del mazo pasadas por parámetro"""
		for i in range(CANTIDAD_CARTAS_AL_INICIO):
			for j in range(len(self)):
				self.jugador_siguiente().levantar_carta(mazo)

	def es_usuario_actual(self):
		"""devuelve un boolean indicando si el jugador actual es el mismo que la mano de la ronda, o sea, el usuario"""
		return self.j_actual == self.tablero.devolver_primero()

	def sentido_es_horario(self):
		""" Devuelve el sentido de la Ronda """
		return self.sentido_horario

	def cambiar_sentido(self):
		"""Cambia el atributo sentido horario a lo opuesto de lo que era y lo devuelve"""
		self.sentido_horario = not(self.sentido_horario)
		return self.sentido_horario
