import random

def algoritmo_Sottolo(lista):
	"""Algoritmo para ordenar azarosamente una lista"""
	i = len(lista)
	while i > 1:
		i = i - 1
		j = random.randrange(i) # 0 <= j <= i-1
		lista[j], lista[i] = lista[i], lista[j]