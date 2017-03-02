from modulo_es_salida import es_salida

def verificador_input_alfabetico(mensaje,minimo,maximo):
	""" Recibe un mensaje (cadena), un número mínimo y un número máximo (enteros). Muestra el mensaje recibido por parametro por pantalla y espera hasta que el usuario 
	ingrese un string cuyo largo que este entre los valores mínimo y máximo (incluidos). En caso de no ingresar un string dentro del rango, vuelve a pedirlo.
	Finalmente devuelve el string ingresado por el usuario."""	
	cadena = ""
	while not(minimo <= len(cadena) <= maximo):
		cadena = input(mensaje)
		es_salida(cadena)
	return cadena