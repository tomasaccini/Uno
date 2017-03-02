def es_salida(cadena):
	"""Recibe una cadena y levanta un SystemExit error en el caso que sea igual a la cadena 'salir' """
	if cadena.lower() == "salir" and input("¿Seguro que desea salir? S/N: ").lower() == "s":
		raise SystemExit
