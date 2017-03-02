import modulo_pila
import modulo_sottolo

class MazoCartas:
	"""Representa un mazo de cartas, tanto usado en el mazo como en el pozo donde se jugarán las cartas"""
	
	def __init__(self):
		""" Constructor. """
		self.pila = modulo_pila.Pila()

	def __str__(self):
		""" Representacion en cadena de un Mazo de Cartas """
		return str(self.pila)

	def __len__(self):
		""" Devuelve la cantidad de elementos que tiene el Mazo de Cartas """
		return len(self.pila)

	def apilar(self,carta):
		""" Recibe una carta y la apila """
		self.pila.apilar(carta)

	def esta_vacio(self):
		""" Devuelve un booleano indicando si el Mazo de Cartas está vacío """
		return self.pila.esta_vacia()

	def levantar_carta(self):
		"""Desapila una carta y la devuelve. De no haber más cartas que levantar, levanta una excepción de tipo ValueError"""
		if self.esta_vacio():
			raise ValueError("El mazo de cartas no tiene mas cartas")
		return self.pila.desapilar()

	def ver_tope(self):
		""" Devuelve la última carta del Mazo de Cartas """
		return self.pila.ver_tope()

	def mezclar(self):
		"""Modifica el orden en el que están las cartas. Post: sin agregar ni quitar cartas"""
		lista_auxiliar = []
		while not(self.esta_vacio()):
			lista_auxiliar.append(self.levantar_carta())
		#Ya tengo la pila de cartas vacia y la lista con todos los elementos ordenados, ahora desordeno
		#Aplico el algoritmo de Sottolo
		modulo_sottolo.algoritmo_Sottolo(lista_auxiliar)
		#Tengo la lista desordenada, ahora apilo todos los elementos de la lista a la pila de cartas.
		for i in range(len(lista_auxiliar)):
			self.pila.apilar(lista_auxiliar[i])