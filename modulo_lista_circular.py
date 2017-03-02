class _Nodo:
	""" Representacion de un Nodo """
	def __init__(self,dato,ant=None,prox=None):
		""" Constructor. Recibe un dato, el nodo anterior y el próximo. """
		self.dato = dato
		self.ant  = ant
		self.prox = prox

	def __str__(self):
		""" Representacion en cadena de un Nodo """
		return "{}".format(self.dato)

class ListaCircular:
	"""Representa una lista doblemente enlazada y circular"""

	def __init__(self):
		""" Constructor. """
		self.prim = None
		self.len = 0
		self.nodo_actual = None

	def __str__(self):
		""" Representacion en cadena de una lista circular doblemente enlazada """
		acumulador = "["
		n_actual = self.prim
		for i in range(self.len):
			acumulador += str(n_actual) + ","
			n_actual = n_actual.prox
		return acumulador.rstrip(",") + "]"

	def __len__(self):
		""" Devuelve la cantidad de nodos de una lista circular doblemente enlazada """
		return self.len

	def append(self,dato):
		""" Recibe un dato y lo agrega a la lista circular doblemente enlazada como nodo anterior al primer nodo. """
		if self.prim is None:
			self.prim = _Nodo(dato)
			self.prim.ant,self.prim.prox = self.prim,self.prim
		else:
			n_nuevo  = _Nodo(dato,self.prim.ant,self.prim)
			n_actual = self.prim.ant
			n_actual.prox,self.prim.ant = n_nuevo, n_nuevo
		self.len += 1

	def devolver_primero(self):
		return self.prim