import random
import modulo_carta
import modulo_mazo_cartas
import modulo_verificador_alfabetico
import modulo_verificador_numerico
import modulo_rellenar_mazo
import modulo_ronda
import modulo_juego

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

def ver_efecto_primera_carta(partida,ronda,primera_carta):
	""" Recibe la primera carta y verifica si tiene algun efecto secundario. En caso afirmativo, ejecuta dicha acción."""
	if primera_carta.valor_carta() == ESP_X2:
		partida.asignar_levantar_acumulado(partida.consultar_levantar_acumulado()+2)
	elif primera_carta.valor_carta() == ESP_X4:
		partida.asignar_levantar_acumulado(partida.consultar_levantar_acumulado()+4)
	elif primera_carta.valor_carta() == ESP_SALTEO:
		partida.asignar_estado_saltear(True)
	elif primera_carta.valor_carta() == ESP_CAMBIO_SENTIDO:
		ronda.cambiar_sentido()
	elif primera_carta.valor_carta() == ESP_NUEVA_FUNCIONALIDAD:
		partida.x2_a_todos()


def juego_usuario_con_levantar_acumulado(partida,ronda,mazo,pozo):
	""" Recibe la partida, la ronda, el mazo y el pozo. Desarrolla el turno del usuario en el caso que haya un levantar acumulado mayor que 0. """
	mensaje = "\nHay un acumulado de {} cartas para robar. Escoje una carta x2 o x4, o ingresa otra opcion para perder el turno y levantar las cartas.".format(partida.consultar_levantar_acumulado())
	pos_carta = partida.pedir_carta(mensaje)
	if ronda.jugador_actual().ver_carta(pos_carta).valor_carta() == ESP_X2:
		partida.asignar_levantar_acumulado(partida.consultar_levantar_acumulado()+2)
		partida.asignar_carta_jugada(ronda.jugador_actual().tirar_carta(pos_carta,pozo))
		partida.asignar_color_actual(partida.consultar_carta_jugada().color_carta())
		print("Tiraste la carta {}".format(partida.consultar_carta_jugada()))
	elif ronda.jugador_actual().ver_carta(pos_carta).valor_carta() == ESP_X4:
		partida.asignar_levantar_acumulado(partida.consultar_levantar_acumulado()+4)
		partida.asignar_carta_jugada(ronda.jugador_actual().tirar_carta(pos_carta,pozo))
		partida.asignar_color_actual(partida.determinar_nuevo_color())
		print("Tiraste la carta {}".format(partida.consultar_carta_jugada()))
	else:
		for i in range(partida.consultar_levantar_acumulado()):
			try:
				ronda.jugador_actual().levantar_carta(mazo)
			except ValueError:
				mazo,pozo = modulo_rellenar_mazo.rellenar_mazo(mazo,pozo)
				print("Se acabaron las cartas del mazo y se rellenaron con las del pozo")
				ronda.jugador_actual().levantar_carta(mazo)
		print("Levantaste {} cartas".format(partida.consultar_levantar_acumulado()))
		partida.asignar_levantar_acumulado(0)

def juego_usuario_sin_levantar_acumulado(partida,ronda,mazo,pozo):
	""" Recibe la partida, la ronda, el mazo y el pozo. Desarrolla el turno del usuario en el caso que no haya un levantar acumulado. """
	mensaje = "\nIngrese la posición de la carta que quiere jugar (0 para levantar): "
	pos_carta = partida.pedir_carta(mensaje)
	if pos_carta == -1:
		try:
			ronda.jugador_actual().levantar_carta(mazo)
		except ValueError:
			mazo,pozo = modulo_rellenar_mazo.rellenar_mazo(mazo,pozo)
			print("Se acabaron las cartas del mazo y se rellenaron con las del pozo")
			ronda.jugador_actual().levantar_carta(mazo)
		print("\n" + str(ronda.jugador_actual()))
		mensaje = "\nIngrese la posición de la carta que quiere jugar (0 para pasar): "
		pos_carta = partida.pedir_carta(mensaje)
	if pos_carta != -1:
		partida.asignar_carta_jugada(ronda.jugador_actual().tirar_carta(pos_carta,pozo))
		print("Tiraste la carta {}".format(partida.consultar_carta_jugada()))
		#Casos que el sea una carta que acumula robos
		if partida.consultar_carta_jugada().valor_carta() == ESP_X2:
			partida.asignar_levantar_acumulado(partida.consultar_levantar_acumulado()+2)
		elif partida.consultar_carta_jugada().valor_carta() == ESP_X4:
			partida.asignar_levantar_acumulado(partida.consultar_levantar_acumulado()+4)
		#El color actual sera None si es una carta x4 o cambio de color
		elif partida.consultar_carta_jugada().valor_carta() == ESP_CAMBIO_SENTIDO:
			ronda.cambiar_sentido()
			print("El sentido de la ronda ahora es ",end = "")
			if ronda.sentido_es_horario():
				print("horario")
			else:
				print("antihorario")
		elif partida.consultar_carta_jugada().valor_carta() == ESP_SALTEO:
			partida.asignar_estado_saltear(True)
		elif partida.consultar_carta_jugada().valor_carta() == ESP_NUEVA_FUNCIONALIDAD:
			partida.x2_a_todos()
		partida.asignar_color_actual(partida.consultar_carta_jugada().color_carta())

def juego_pc(partida,ronda,mazo,pozo):
	""" Recibe la partida, la ronda, el mazo y el pozo. Desarrolla el turno de la pc. """
	nombre_jugador_actual = ronda.jugador_actual().nombre_jugador()
	print("\nTurno del jugador {}".format(nombre_jugador_actual))	
	partida.asignar_carta_jugada(ronda.jugador_actual().ia_jugar_carta(mazo,pozo,partida.consultar_levantar_acumulado(),partida.consultar_color_actual()))
	if not(partida.consultar_carta_jugada() is None):
		print("El jugador {} jugo la carta {}".format(nombre_jugador_actual, partida.consultar_carta_jugada()))
		if partida.consultar_carta_jugada().valor_carta() == ESP_X2:
			partida.asignar_levantar_acumulado(partida.consultar_levantar_acumulado()+2)
		elif partida.consultar_carta_jugada().valor_carta() == ESP_X4:
			partida.asignar_levantar_acumulado(partida.consultar_levantar_acumulado()+4)
		elif partida.consultar_carta_jugada().valor_carta() == ESP_CAMBIO_SENTIDO:
			ronda.cambiar_sentido()
			print("\nEl sentido de la ronda ahora es ",end = "")
			if ronda.sentido_es_horario():
				print("horario")
			else:
				print("antihorario")
		elif partida.consultar_carta_jugada().valor_carta() == ESP_SALTEO:
			partida.asignar_estado_saltear(True)
		elif partida.consultar_carta_jugada().valor_carta() == ESP_NUEVA_FUNCIONALIDAD:
			partida.x2_a_todos()
		#El color actual sera None si es una carta x4 o cambio de color
		partida.asignar_color_actual(partida.consultar_carta_jugada().color_carta())
	else:
		if partida.consultar_levantar_acumulado() > 0:
			for i in range(partida.consultar_levantar_acumulado()):
				try:
					ronda.jugador_actual().levantar_carta(mazo)
				except ValueError:
					mazo,pozo = modulo_rellenar_mazo.rellenar_mazo(mazo,pozo)
					print("Se acabaron las cartas del mazo y se rellenaron con las del pozo")
					ronda.jugador_actual().levantar_carta(mazo)
			print("El jugador {} levanto {} cartas.".format(nombre_jugador_actual, partida.consultar_levantar_acumulado()))
			partida.asignar_levantar_acumulado(0)
		else:
			print("El jugador {} agarró una carta y pasó el turno".format(nombre_jugador_actual))
	print("Le quedan {} cartas".format(ronda.jugador_actual().cant_cartas()))

def terminar_juego(ronda,cantidad_contrincantes):
	""" Recibe la ronda y la cantidad de contrincantes (entero). Finaliza el juego indicando quien es el ganador y mostrando las manos del resto de los jugadores."""
	print("\n¡El jugador {} es el Ganador!\n\nLas cartas de los jugadores restantes son: ".format(ronda.jugador_actual().nombre_jugador()))
	if ronda.sentido_es_horario():
		ronda.jugador_siguiente()
	else:
		ronda.jugador_anterior()
	for i in range(cantidad_contrincantes):
		print("Con {} cartas, {}".format(ronda.jugador_actual().cant_cartas(),ronda.jugador_actual()))
		if ronda.sentido_es_horario():
			ronda.jugador_siguiente()
		else:
			ronda.jugador_anterior()

def juego(cantidad_contrincantes):
	"""Recibe la cantidad de contrincantes que tendrá el usuario y turno a turno hará tanto al usuario como a las inteligencias artificiales jugar al Uno hasta que uno llegue a la victoria"""
	mazo = modulo_mazo_cartas.MazoCartas()
	pozo = modulo_mazo_cartas.MazoCartas()
	ronda = modulo_ronda.Ronda()
	partida = modulo_juego.Juego(mazo,pozo,ronda)
	partida.completar_mazo_cartas_iniciales()
	mazo.mezclar()
	ronda.agregar_jugador(modulo_verificador_alfabetico.verificador_input_alfabetico("\nIngrese su nombre (entre 1 y 6 caracteres): ",1,6)) #por ser el 1ro en ser agregado es mano
	for i in range(cantidad_contrincantes):
		ronda.agregar_jugador("PC "+str(i+1))
	ronda.repartir_cartas(mazo)
	pozo.apilar(mazo.levantar_carta())
	primera_carta = pozo.ver_tope()
	print("Empieza el juego\n\nEl pozo empieza con la carta {}".format(primera_carta))
	ver_efecto_primera_carta(partida,ronda,primera_carta)
	partida.asignar_color_actual(primera_carta.color_carta())
	if partida.consultar_color_actual() is None:
		partida.asignar_color_actual(partida.determinar_nuevo_color())
	victoria = False
	while not(victoria):
		print("\n-----------------------------------------------------------------------------\n")
		if ronda.sentido_es_horario():
			ronda.jugador_siguiente()
		else:
			ronda.jugador_anterior()
		if partida.consultar_estado_saltear():
			partida.asignar_estado_saltear(False)
			print("\nTurno de {} salteado\n".format(ronda.jugador_actual().nombre_jugador()))
			continue
		partida.asignar_carta_jugada(None)
		if ronda.es_usuario_actual():
			#Caso en el que la carta inicial sea un +4 o cambio de color, elije un color al azar
			if partida.consultar_color_actual() is None:
				partida.asignar_color_actual(partida.determinar_nuevo_color())
			print("\nColor actual: {}".format(partida.consultar_color_actual()))
			print("\nPozo tope: {}.\n".format(pozo.ver_tope()))
			print(ronda.jugador_actual())
			#Caso que haya un acumulado para robar
			if partida.consultar_levantar_acumulado() > 0:
				juego_usuario_con_levantar_acumulado(partida,ronda,mazo,pozo)
			#Caso en el que no lo haya
			else:
				juego_usuario_sin_levantar_acumulado(partida,ronda,mazo,pozo)
		#Juego de la pc
		else:
			juego_pc(partida,ronda,mazo,pozo)
		#En el caso que el color_actual sea None, pido el color a cambiar al usuario o elijo uno random por la pc
		if partida.consultar_color_actual() is None:
			partida.asignar_color_actual(partida.determinar_nuevo_color())
		if ronda.jugador_actual().cant_cartas() == 0:
			victoria = True
			terminar_juego(ronda,cantidad_contrincantes)

def menu_principal():
	""" Funcion de presentacion del juego. Imprime un mensaje de bienvenida, y pide al usuario que ingrese la cantidad de contrinantes. """
	while True:
		
		print("\n\nBienvenido al juego de cartas UNO!.\n\nPara salir del juego ingrese salir en cualquier instancia")
		cantidad_contrincantes = modulo_verificador_numerico.verificador_input_numerico("\nIngrese el numero de contrincantes (1 a 3)\n\r", 1, 3)
		if cantidad_contrincantes == 0:
			break
		else:
			juego(cantidad_contrincantes)

menu_principal()