from modulo_es_salida import es_salida

def verificador_input_numerico(mensaje, minimo, maximo):
	""" Recibe un mensaje (cadena), un número mínimo y un número máximo (enteros). Muestra el mensaje recibido por parametro por pantalla y espera hasta que el usuario 
	ingrese un número entero que este entre los valores mínimo y máximo (incluidos). En caso de no ingresar un número, o que el ingresado este fuera del rango, vuelve a pedirlo.
	Finalmente devuelve el numero ingresado por el usuario."""
	numero = ""
	while not numero.isdigit() and numero != "-1":
		numero = input(mensaje)
		es_salida(numero)
		if numero.isdigit() or numero == "-1":
			if int(numero) < minimo or int(numero) > maximo:
				numero = ""
	return int(numero)