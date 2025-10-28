from TPUno import menu
from unittest.mock import patch #agrego esta libreria que me pertmite simular inputs

historial = {"Usuario": [], "PC": []}

with patch('builtins.input', return_value='5'):
    resultado = menu(historial)
    assert resultado == False  # Opción 5 es salir