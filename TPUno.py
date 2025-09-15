import random
import os
import msvcrt  # Para captura de teclas en Windows
from colorama import init, Fore, Style  
init(autoreset=True)

jugadores = [
    ["bruno", 70],
    ["mar", 65],
    ["vicky", 55],
    ["thomas", 50],
    ["vera", 45],
    ["lu", 30]
]

valores_cartas = {
    0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9,
    "+2": 20,
    "BLOQUEO": 20,
    "REVERSA": 20,
    "+4": 50,
    "CAMBIO_COLOR": 50
}
def calcular_puntaje_mano(mazo):
    total = 0
    for carta in mazo:
        valor = carta[1]  
        total += valores_cartas.get(str(valor), 0)
    return total

def Mazo_Uno():
    colores = ["ROJO", "AMARILLO", "VERDE", "AZUL"]
    mazo = []

    for color in colores:
        for n in range(0, 10):
            mazo.append([color, n])
            mazo.append([color, n])

        for n in range(2):
            mazo.append([color, "BLOQUEO"])
            mazo.append([color, "REVERSA"])
            mazo.append([color, "+2"])

    for n in range(4):
        mazo.append(["NEGRO", "+4"])
        mazo.append(["NEGRO", "CAMBIO_COLOR"])

    return mazo 

# Nueva función de repartir con mazo de reparto y descarte
def repartir(cant, mazo_reparto, mazo_descarte):
    lista = []
    for i in range(cant):
        if len(mazo_reparto) == 0:
            # Reciclar mazo: tomar todas las cartas descartadas menos la última
            if len(mazo_descarte) > 1:
                ultima_carta = mazo_descarte[-1]
                mazo_reparto = mazo_descarte[:-1]
                random.shuffle(mazo_reparto)
                mazo_descarte = [ultima_carta]
            else:
                print("No hay cartas para reciclar!")
                break
        # Sacar carta aleatoria del mazo de reparto
        carta = mazo_reparto.pop(random.randint(0, len(mazo_reparto)-1))
        lista.append(carta)
    return lista, mazo_reparto, mazo_descarte

# Función para mostrar el mazo
def mostrarMazo(mazo):
    for i in range(len(mazo)):
        carta = mazo[i]
        numero, color = carta
        if color == "ROJO":
            color_print = Fore.RED
        elif color == "AZUL":
            color_print = Fore.BLUE
        elif color == "VERDE":
            color_print = Fore.GREEN
        elif color == "AMARILLO":
            color_print = Fore.YELLOW
        else:
            color_print = Style.RESET_ALL
        
        print(f"{i+1} -> {color_print}{numero} {color}{Style.RESET_ALL}")

def validarCarta(cartaEnJuego, cartaUsuario):
    check = False
    if cartaEnJuego[0] == cartaUsuario[0] or cartaEnJuego[1] == cartaUsuario[1]:
        check = True  
    elif (cartaUsuario[0] == "NEGRO") :
        check = True 
    elif (cartaUsuario[0] in ["+2", "BLOQUEO", "REVERSA", "+4"]) and cartaEnJuego[1] == cartaUsuario[1]:
        check = True
    return check

# función para selección con flechas
def seleccionar_con_flechas(mazo, msgOpcion0, cartaEnJuego):
    indice = 0
    while True:
        os.system('cls')
        numero, color = cartaEnJuego
        if color == "ROJO":
            color_print = Fore.RED
        elif color == "AZUL":
            color_print = Fore.BLUE
        elif color == "VERDE":
            color_print = Fore.GREEN
        elif color == "AMARILLO":
            color_print = Fore.YELLOW
        else:
            color_print = Style.RESET_ALL

        print(f"\nLa carta en juego es: {color_print}{numero} {color}{Style.RESET_ALL}")
        print(msgOpcion0)
        print("0  -> Tomar carta / Pasar turno\n")

        for i in range(len(mazo)):
            carta_num, carta_color = mazo[i]
            if carta_color == "ROJO":
                carta_color_print = Fore.RED
            elif carta_color == "AZUL":
                carta_color_print = Fore.BLUE
            elif carta_color == "VERDE":
                carta_color_print = Fore.GREEN
            elif carta_color == "AMARILLO":
                carta_color_print = Fore.YELLOW
            else:
                carta_color_print = Style.RESET_ALL

            prefijo = "->" if i == indice else "  "
            print(f"{prefijo} {i+1} -> {carta_color_print}{carta_num} {carta_color}{Style.RESET_ALL}")

        tecla = msvcrt.getch()
        if tecla == b'\xe0':  # Flechas
            flecha = msvcrt.getch()
            if flecha == b'K':  # Izquierda
                indice = (indice - 1) % len(mazo)
            elif flecha == b'M':  # Derecha
                indice = (indice + 1) % len(mazo)
        elif tecla == b'\r':  # Enter
            return indice + 1
        elif tecla == b'0':
            return 0

def elegir_color():
    colores = ["ROJO", "AMARILLO", "VERDE", "AZUL"]
    print("Elegí un color para el cambio:")
    for i, col in enumerate(colores):
        print(f"{i+1}. {col}")
    noSalir = True
    while noSalir:
            eleccion = int(input("Ingrese el número del color elegido: ")) - 1
            if 0 <= eleccion < len(colores):
                noSalir = False
                return colores[eleccion]
               
            else:
                print("Elección no válida. Intente de nuevo.")
                noSalir = True        
def elegirColorPc(mazo):
    colores_validos = ["ROJO", "AZUL", "VERDE", "AMARILLO"]
    conteo = {color: 0 for color in colores_validos}
    conteo["NEGRO"] = 0

    for carta in mazo:
        color = carta[0]
        if color in conteo:
            conteo[color] += 1

    # Buscar el color con mayor cantidad
    max_color = max(conteo, key=lambda c: conteo[c])
    max_cantidad = conteo[max_color]

    # Verificar si hay empate o si el color más frecuente es negro
    colores_maximos = [c for c in conteo if conteo[c] == max_cantidad]
    if len(colores_maximos) > 1 or max_color == "NEGRO":
        return random.choice(colores_validos)
    else:
        return max_color        


def turnoUsuario(mazoUsuario, mazo_reparto, mazo_descarte, cartaEnJuego):
    salir = False
    tomoUnaCarta = False
    opcion = -1
    msgOpcion0 = "0  -> Tomar una carta"
    print("es tu turno! Elegí una opcion o carta del mazo para jugar!")
    while not salir:
        opcion = seleccionar_con_flechas(mazoUsuario, msgOpcion0, cartaEnJuego)
        if opcion < 0 or opcion > len(mazoUsuario):
            print("opcion no valida!")
        elif opcion == 0 and not tomoUnaCarta:
            print("El usuario toma una carta")
            nueva_carta, mazo_reparto, mazo_descarte = repartir(1, mazo_reparto, mazo_descarte)
            mazoUsuario += nueva_carta
            tomoUnaCarta = True
            msgOpcion0 = "0  -> Pasar turno"
        elif opcion == 0 and tomoUnaCarta:
            salir = True
            opcion = -1
        else:
            opcion = opcion - 1
            if validarCarta(cartaEnJuego, mazoUsuario[opcion]):
                cartaEnJuego = mazoUsuario[opcion]

                mazo_descarte.append(cartaEnJuego) 
                del mazoUsuario[opcion]
                
                if cartaEnJuego[0] == "NEGRO" :
                  cartaEnJuego[0] = elegir_color()

                mazo_descarte.append(cartaEnJuego)  # mover al mazo de descarte
                del mazoUsuario[opcion]

                salir = True
            else:
                print("No es una carta valida.")
                numero, color = cartaEnJuego
                if color == "ROJO":
                    color_print = Fore.RED
                elif color == "AZUL":
                    color_print = Fore.BLUE
                elif color == "VERDE":
                    color_print = Fore.GREEN
                elif color == "AMARILLO":
                    color_print = Fore.YELLOW
                else:
                    color_print = Style.RESET_ALL
                print(f"\nLa carta en juego es: {color_print}{numero} {color}{Style.RESET_ALL}")

                input("\nPresione Enter para continuar...")
    return cartaEnJuego, mazoUsuario, mazo_reparto, mazo_descarte, msgOpcion0

    return cartaEnJuego, mazoUsuario, mazo_reparto, mazo_descarte


def turnoPC(mazoPC, mazo_reparto, mazo_descarte, cartaEnJuego):
    print("\nTurno de la computadora...")
    jugada_valida = False
    i = 0

    while i < len(mazoPC) and not jugada_valida:
        if validarCarta(cartaEnJuego, mazoPC[i]):

            mazo_descarte.append(cartaEnJuego)
            if mazoPC[i][0] == "NEGRO":
                cartaEnJuego = mazoPC[i]
                cartaEnJuego[0] = elegirColorPc(mazoPC)
            else:
                cartaEnJuego = mazoPC[i]


            cartaEnJuego = mazoPC[i]
            mazo_descarte.append(cartaEnJuego)

            numero, color = cartaEnJuego
            if color == "ROJO":
                color_print = Fore.RED
            elif color == "AZUL":
                color_print = Fore.BLUE
            elif color == "VERDE":
                color_print = Fore.GREEN
            elif color == "AMARILLO":
                color_print = Fore.YELLOW
            else:
                color_print = Style.RESET_ALL
            print(f"\nLa computadora jugó: {color_print}{numero} {color}{Style.RESET_ALL}")
            del mazoPC[i]
            jugada_valida = True
        else:
            i += 1

    if not jugada_valida:
        print("La computadora no tiene cartas válidas. Toma una carta...")
        nueva_carta, mazo_reparto, mazo_descarte = repartir(1, mazo_reparto, mazo_descarte)
        carta = nueva_carta[0]
        if validarCarta(cartaEnJuego, carta):
            cartaEnJuego = carta
            mazo_descarte.append(carta)
            print("¡La computadora jugó la carta que tomó! ", cartaEnJuego[0], cartaEnJuego[1])
        else:
            mazoPC.append(carta)
            print("La computadora no pudo jugar. Pasa el turno.")

    input("\nPresione Enter para continuar...")
    return cartaEnJuego, mazoPC, mazo_reparto, mazo_descarte

def registrar_usuario():
    print("\n=== REGISTRO DE USUARIO ===")
    nombre = input("Ingrese su nombre: ")
    while len(nombre.strip()) == 0:
        print("El nombre no puede estar vacío")
        nombre = input("Ingrese su nombre: ")
    return nombre

def reglas():
    print("\n=== REGLAS DEL UNO ===")
    print("1. Cada jugador recibe 7 cartas al inicio")
    print("2. Se juega por turnos")
    print("3. Se puede jugar una carta si coincide con el número o color de la carta en juego")
    print("4. Si no tenes una carta válida, tenes que tomar una carta del mazo")
    print("5. La carta de bloqueo le roba el turno al jugador contrincante")
    print("6. La carta +2 indica que el jugador contrincante deberá tomar dos cartas del mazo y perderá el turno")
    print("7. La carta +4 indica que el jugador contrincante deberá tomar cuatro cartas del mazo y perderá el turno")
    print("8. El primer jugador en quedarse sin cartas gana")
    input("\nPresione Enter para continuar...")

def ranking():
    print("\n=== RANKING DE JUGADORES ===")
    ranking_ordenado = sorted(jugadores, key=lambda x: x[1], reverse=True)
    for i, j in enumerate(ranking_ordenado):
        print(f"{i+1}. {j[0]}: {j[1]} puntos")
    input("\nPresione Enter para continuar...")

def actualizar_puntuacion(nombre, puntos):
    for i in range(len(jugadores)):
        if jugadores[i][0].lower() == nombre.lower():
            jugadores[i][1] += puntos
            return
    jugadores.append([nombre.lower(), puntos])

def menu():
    while True:
        os.system('cls')
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Iniciar partida")
        print("2. Reglas del juego")
        print("3. Ranking de jugadores")
        print("4. Salir del juego")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            return True
        elif opcion == "2":
            reglas()
        elif opcion == "3":
            ranking()
        elif opcion == "4":
            print("\n¡Gracias por jugar!")
            return False
        else:
            print("\nOpción no válida")
            input("Presione Enter para continuar...")

# ================== Juego principal ==================
def iniciar_juego():
    nombre_usuario = registrar_usuario()
    print(f"\n¡Bienvenido {nombre_usuario}!")
    input("Presione Enter para continuar...")

    while menu():
        mazo_general = Mazo_Uno() # Mazo original
        mazo_reparto = mazo_general.copy() # Copio el original para modificarlo
        random.shuffle(mazo_reparto) # Barajo el mazo a repartir
        mazo_descarte = [] #genero un mazo para descartar cartas vacio.

        mazoUsuario, mazo_reparto, mazo_descarte = repartir(7, mazo_reparto, mazo_descarte)
        mazoPC, mazo_reparto, mazo_descarte = repartir(7, mazo_reparto, mazo_descarte)
        cartaEnJuego, mazo_reparto, mazo_descarte = repartir(1, mazo_reparto, mazo_descarte)
        cartaEnJuego = cartaEnJuego[0]
        
        turno = 0  # 0 = Usuario, 1 = PC
        efecto_pendiente = None

        while len(mazoPC) > 0 and len(mazoUsuario) > 0:
            os.system('cls')
            print(f"\nJugador: {nombre_usuario}")
            print("\nLa cantidad de cartas que tiene la computadora es: ", len(mazoPC))
            numero, color = cartaEnJuego
            color_print = {
                "ROJO": Fore.RED,
                "AZUL": Fore.BLUE,
                "VERDE": Fore.GREEN,
                "AMARILLO": Fore.YELLOW
            }.get(color, Style.RESET_ALL)
            print(f"\nLa carta en juego es: {color_print}{numero} {color}{Style.RESET_ALL}")

            # Aplicar efectos pendientes
            if efecto_pendiente == "MAS2":
                if turno == 0:
                    print("¡Efecto +2! El jugador toma 2 cartas y pierde el turno.")
                    nuevas, mazo_reparto, mazo_descarte = repartir(2, mazo_reparto, mazo_descarte)
                    mazoUsuario += nuevas
                    turno = 1
                else:
                    print("¡Efecto +2! La computadora toma 2 cartas y pierde el turno.")
                    nuevas, mazo_reparto, mazo_descarte = repartir(2, mazo_reparto, mazo_descarte)
                    mazoPC += nuevas
                    turno = 0
                efecto_pendiente = None
                input("\nPresione Enter para continuar...")
                continue
            if efecto_pendiente == "MAS4":
                if turno == 0:
                    print("¡Efecto +4! El jugador toma 4 cartas y pierde el turno.")
                    nuevas, mazo_reparto, mazo_descarte = repartir(4, mazo_reparto, mazo_descarte)
                    mazoUsuario += nuevas
                    turno = 1
                else:
                    print("¡Efecto +4! La computadora toma 4 cartas y pierde el turno.")
                    nuevas, mazo_reparto, mazo_descarte = repartir(4, mazo_reparto, mazo_descarte)
                    mazoPC += nuevas
                    turno = 0
                efecto_pendiente = None
                input("\nPresione Enter para continuar...")
                continue
            elif efecto_pendiente == "BLOQUEO":
                print("¡BLOQUEO! Se salta un turno.")
                turno = 1 - turno
                efecto_pendiente = None
                input("\nPresione Enter para continuar...")
                continue
            elif efecto_pendiente == "Reversa":
                print("¡Reversa! Se invierte el turno (en dos jugadores equivale a saltar turno).")
                turno = 1 - turno
                efecto_pendiente = None
                input("\nPresione Enter para continuar...")
                continue

            # Turno normal
            if turno == 0:

                cartaEnJuego, mazoUsuario, mazo_reparto, mazo_descarte, msgOpcion0 = turnoUsuario(
                    mazoUsuario, mazo_reparto, mazo_descarte, cartaEnJuego)

                cartaEnJuego, mazoUsuario, mazo_reparto, mazo_descarte = turnoUsuario(
                    mazoUsuario, mazo_reparto, mazo_descarte, cartaEnJuego)
                turno = 1
            else:
                cartaEnJuego, mazoPC, mazo_reparto, mazo_descarte = turnoPC(
                    mazoPC, mazo_reparto, mazo_descarte, cartaEnJuego)
                turno = 0

            # Detectar efecto de la última carta jugada


            if msgOpcion0 != "0  -> Pasar turno":
                if cartaEnJuego[1] == "+2":
                        efecto_pendiente = "MAS2"
                elif cartaEnJuego[1] == "+4":
                        efecto_pendiente = "MAS4"
                elif cartaEnJuego[1] == "BLOQUEO":
                        efecto_pendiente = "BLOQUEO"
                elif cartaEnJuego[1] == "Reversa":
                        efecto_pendiente = "Reversa"
            else:
                efecto_pendiente=None


            if cartaEnJuego[1] == "+2":
                efecto_pendiente = "MAS2"
            elif cartaEnJuego[1] == "+4":
                efecto_pendiente = "MAS4"
            elif cartaEnJuego[1] == "BLOQUEO":
                efecto_pendiente = "BLOQUEO"
            elif cartaEnJuego[1] == "Reversa":
                efecto_pendiente = "Reversa"


        # Final del juego
        if len(mazoUsuario) == 0:
            print("¡Ganaste!")
            actualizar_puntuacion(nombre_usuario, 15)
        else:
            print("¡Ganó la computadora!")
            actualizar_puntuacion(nombre_usuario, -5)
        
        input("\nPresione Enter para continuar...")

iniciar_juego()


'''
def Reparto() #Descuento las cartas del mazo, solucionar el tema probabilistica.
def Cambio_de_jugador() #Agrega la funcion de la carta que cambia la el orden de juego invirtiendolo.
def sistema_juego_mas2_mas4(): #Aplica el efecto de las cartas especiales +2 y +4. Obliga al jugador rival a tomar cartas y perder su turno
'''
