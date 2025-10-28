from TPUno import elegir_Color
from unittest.mock import patch #agrego esta libreria que me pertmite simular inputs

mazo = [[1, "ROJO"], [2, "AZUL"], [3, "VERDE"], [4, "AMARILLO"], ["+4", "NEGRO"]]
color = elegir_Color(mazo)
assert color in ["ROJO", "AZUL", "VERDE", "AMARILLO"] == True

with patch('builtins.input', return_value='2'):
    color = elegir_Color()
    assert color == "AMARILLO"