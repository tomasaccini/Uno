class Carta:
	"""Representa a las cartas con su respectivo valor(que será un int entre 0 y 9 o un valor especial) y color(rojo, azul, verde o amarillo)"""
	
	def __init__(self,valor,color=None):
		self.valor = valor
		self.color = color

	def __str__(self):
		if self.color:
			return ("({},{})".format(self.color,self.valor))
		return ("({})".format(self.valor))

	def valor_carta(self):
		return self.valor

	def color_carta(self):
		return self.color