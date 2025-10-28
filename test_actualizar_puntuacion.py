from TPUno import actualizar_puntuacion, jugadores_dic

actualizar_puntuacion("vera", 10)
assert jugadores_dic["vera"] == 80  # ya que el valor inicial es 70
actualizar_puntuacion("nuevo_jugador", 20)
assert jugadores_dic["nuevo_jugador"] == 20

actualizar_puntuacion("fran", 5)
assert jugadores_dic["fran"] == 70  # ya que el valor inicial es 65