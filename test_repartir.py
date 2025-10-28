from TPUno import repartir

mazo_reparto = [[1, "ROJO"], [2, "AZUL"], [3, "VERDE"]]
mazo_descarte = [[5, "ROJO"]]
cartas, nuevo_mazo_reparto, nuevo_mazo_descarte = repartir(2, mazo_reparto, mazo_descarte)
assert len(cartas) == 2