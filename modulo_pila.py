class Pila:
	""" Representa una pila de elementos """
	def __init__(self):
		""" Constructor. """
		self.elementos = []
		self.len = 0

	def __str__(self):
		""" Representacion en cadena de la clase Pila """
		acumulador = "["
		for x in self.elementos:
			acumulador += str(x) + ","
		return acumulador.rstrip(",")+"]"

	def ver_tope(self):
		""" Devuelve el último elemento de la Pila """
		if self.esta_vacia():
			return None
		else:
			return self.elementos[-1]

	def esta_vacia(self):
		""" Devuelve un booleano indicando si la Pila esta vacía """
		return self.len == 0

	def apilar(self,dato):
		""" Recibe un elemento y lo apila """
		self.elementos.append(dato)
		self.len += 1

	def desapilar(self):
		""" Devuelve el último elemento de la Pila. En caso que esté vacía, lanza una excepción """
		if self.esta_vacia():
			raise ValueError("La pila esta vacia")
		else:
			self.len -= 1
			return self.elementos.pop()
