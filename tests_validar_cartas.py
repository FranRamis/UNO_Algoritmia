from TPUno import validarCarta

assert validarCarta([7, "ROJO"], [5, "ROJO"]) == True
assert validarCarta([7, "ROJO"], [7, "ROJO"]) == True
assert validarCarta([7, "ROJO"], ["+4", "NEGRO"]) == True
assert validarCarta([7, "ROJO"], [2, "AZUL"]) == False
assert validarCarta(["+2", "VERDE"], [5, "VERDE"]) == True
assert validarCarta(["+2", "VERDE"], [5, "ROJO"]) == False
assert validarCarta(["CAMBIO", "AZUL"], ["CAMBIO", "VERDE"]) == True
assert validarCarta(["CAMBIO", "AZUL"], [3, "AZUL"]) == True
assert validarCarta(["CAMBIO", "AZUL"], [3, "ROJO"]) == False
assert validarCarta(["+4", "NEGRO"], ["+4", "NEGRO"]) == True
