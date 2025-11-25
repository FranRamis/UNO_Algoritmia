import random #Importa la librería random para generar aleatoriedad.
import os #Importa la librería os para ejecutar comandos del sistema para limpiar la pantalla.
import msvcrt  # Para captura de teclas en Windows
from colorama import init, Fore, Style  #Inicializa colorama con auto-reset para que los colores no se propaguen.
import json
from datetime import datetime
init(autoreset=True)

jugadores_dic = { #Diccionario jugadores_dic con jugadores y sus puntajes actuales.
"thomas": 70, 
"vera": 70,
"fran": 65,
"augus": 55
}

def leer_archivo_json(nombre_archivo):
    '''
    Carga los datos de un archivo JSON ubicado en la carpeta 'Files'.
   
    Parámetros:
        nombre_archivo (str): Nombre del archivo a leer (ej: "ranking.json").
   
    Retorna:
        dict: El diccionario con los datos del archivo, o un diccionario vacío si falla.
    '''
    ruta = os.path.join(os.path.dirname(__file__), "FIles", nombre_archivo)
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            arch= json.load(archivo)
            print ( f"Archivo '{nombre_archivo}' leído correctamente.")
            return arch
    except Exception as e:
        print(f"Error inesperado al leer '{nombre_archivo}': {e}")
        return {}

def guardar_archivo_json(nombre_archivo, datos):
    '''
    Guarda (escribe) el diccionario de datos en un archivo JSON en la carpeta 'Files'.
   
    Parámetros:
        nombre_archivo (str): Nombre del archivo donde guardar los datos.
        datos (dict): Diccionario a serializar y escribir en el archivo.
   
    Retorna:
        None
    '''
    ruta = os.path.join(os.path.dirname(__file__), "FIles", nombre_archivo)
    
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
            print(f"Archivo '{nombre_archivo}' guardado correctamente.")
    except Exception as e:
        print(f"Error inesperado al guardar '{nombre_archivo}': {e}")

jugadores_dic = leer_archivo_json("ranking.json")

def Mazo_Uno(): #crea y devuelve el mazo completo de UNO.
    '''
    Genera y devuelve el mazo completo de cartas del juego UNO (108 cartas).
    Incluye cartas numéricas, de acción (+2, Bloqueo, Reversa) y comodines (+4, Cambio de color).
   
    Retorna:
        list: Una lista de listas, donde cada sublista es una carta [valor, color].
    '''
    colores = ["ROJO", "AMARILLO", "VERDE", "AZUL"]
    mazo = []

    for color in colores: #Define los colores de las cartas.
        for n in range(0, 10): #Inicializa la lista del mazo vacío.
            mazo.append([n, color]) #Agrega dos copias de cada carta numérica del 0 al 9 por color.
            mazo.append([n, color])

        for n in range(2): #agrega cartas especiales: Bloqueo, Reversa y +2 (dos copias por color).
            mazo.append(["BLOQUEO", color])
            mazo.append(["REVERSA", color])
            mazo.append(["+2",color])

    for n in range(4): #Agrega las cartas negras (+4 y Cambio de color).
        mazo.append(["+4", "NEGRO"])
        mazo.append(["CAMBIO_COLOR", "NEGRO"])

    return mazo #Devuelve el mazo generado.

# Nueva función de repartir con mazo de reparto y descarte
def repartir(cant, mazo_reparto, mazo_descarte):
    '''
    Reparte una cantidad específica de cartas desde el mazo de reparto.
    Si el mazo de reparto se queda vacío, recicla y baraja las cartas del mazo de descarte (manteniendo la última).
   
    Parámetros:
        cant (int): Cantidad de cartas a repartir.
        mazo_reparto (list): Lista de cartas disponibles para repartir.
        mazo_descarte (list): Lista de cartas descartadas (para reciclar si es necesario).
   
    Retorna:
        tuple: Una tupla que contiene (cartas repartidas, mazo_reparto actualizado, mazo_descarte actualizado).
    '''
    lista = []
    for i in range(cant): #reparte cartas desde el mazo de reparto.
        if len(mazo_reparto) == 0:
            # Reciclar mazo: tomar todas las cartas descartadas menos la última
            if len(mazo_descarte) > 1: #Verifica si el mazo de reparto está vacío.
                ultima_carta = mazo_descarte[-1] #Si hay cartas descartadas, recicla todas menos la última y baraja.
                mazo_reparto = mazo_descarte[:-1]
                random.shuffle(mazo_reparto)
                mazo_descarte = [ultima_carta]
            else:
                print("No hay cartas para reciclar!") #Si no hay cartas disponibles, avisa y corta.
                break
        # Sacar carta aleatoria del mazo de reparto
        carta = mazo_reparto.pop(random.randint(0, len(mazo_reparto)-1))
        lista.append(carta) #La agrega a la lista del jugador.
    return lista, mazo_reparto, mazo_descarte #Devuelve las cartas repartidas y los mazos actualizados.

# Función para mostrar el mazo
def mostrarMazo(mazo): #muestra las cartas del mazo con colores.
    '''
    Imprime en consola las cartas de un mazo dado, utilizando códigos de color para distinguirlas.
   
    Parámetros:
        mazo (list): La mano de cartas del jugador o cualquier lista de cartas.
   
    Retorna:
        None: Solo realiza impresión en pantalla.
    '''
    for i in range(len(mazo)): #Itera sobre todas las cartas.
        carta = mazo[i]
        numero, color = carta #Separa número y color de cada carta.
        if color == "ROJO":
            color_print = Fore.RED #Asigna un color de impresión según el color de la carta.
        elif color == "AZUL":
            color_print = Fore.LIGHTBLUE_EX
        elif color == "VERDE":
            color_print = Fore.GREEN
        elif color == "AMARILLO":
            color_print = Fore.YELLOW
        else:
            color_print = Style.RESET_ALL
        
        print(f"{i+1} -> {color_print}{numero} {color}{Style.RESET_ALL}") #Imprime la carta en pantalla con su color correspondiente.

def validarCarta(cartaEnJuego, cartaUsuario): #verifica si una carta es jugable.
    '''
    Comprueba si una carta del jugador se puede jugar legalmente sobre la carta en la pila de descarte.
   
    Parámetros:
        cartaEnJuego (list): La carta actual en la pila [valor, color].
        cartaUsuario (list): La carta que el jugador intenta jugar [valor, color].
   
    Retorna:
        bool: True si la jugada es válida, False en caso contrario.
    '''
    check = False #Inicializa check como falso.
    if cartaEnJuego[0] == cartaUsuario[0] or cartaEnJuego[1] == cartaUsuario[1]: #Valida por número o color.
        check = True  
    elif (cartaUsuario[1] == "NEGRO") : #Valida si la carta es negra (comodín).
        check = True 
    elif (cartaUsuario[0] in ["+2", "BLOQUEO", "REVERSA", "+4"]) and cartaEnJuego[0] == cartaUsuario[0]: #Valida si ambas cartas son del mismo tipo especial.
        check = True
    return check #Devuelve el resultado.

# función para selección con flechas
def seleccionar_con_flechas(mazo, msgOpcion0, cartaEnJuego): #permite elegir carta con teclado.
    '''
    Permite al usuario seleccionar una carta de su mazo (mano) usando las teclas de flecha y Enter.
   
    Parámetros:
        mazo (list): La mano de cartas del jugador.
        msgOpcion0 (str): Mensaje para la opción 0 (Tomar carta/Pasar).
        cartaEnJuego (list): La carta actual en juego para referencia visual.
   
    Retorna:
        int: El índice (1-basado) de la carta seleccionada, o 0 si elige la opción 'Tomar carta/Pasar'.
    '''
    indice = 0 #Índice de selección inicial.
    while True: #Loop infinito hasta que el jugador elija.
        os.system('cls') #Limpia pantalla.
        numero, color = cartaEnJuego #Muestra la carta en juego con color.
        if color == "ROJO":
            color_print = Fore.RED
        elif color == "AZUL":
            color_print = Fore.LIGHTBLUE_EX
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
                carta_color_print = Fore.LIGHTBLUE_EX
            elif carta_color == "VERDE":
                carta_color_print = Fore.GREEN
            elif carta_color == "AMARILLO":
                carta_color_print = Fore.YELLOW
            else:
                carta_color_print = Style.RESET_ALL
            #Muestra opciones de juego.
            prefijo = "->" if i == indice else "  "
            print(f"{prefijo} {i+1} -> {carta_color_print}{carta_num} {carta_color}{Style.RESET_ALL}")

        tecla = msvcrt.getch() #Recorre las cartas del jugador y las imprime con selector.
        if tecla == b'\xe0':  # Flechas - Detecta tecla presionada.
            flecha = msvcrt.getch()
            if flecha == b'K':  # Izquierda
                indice = (indice - 1) % len(mazo)
            elif flecha == b'M':  # Derecha
                indice = (indice + 1) % len(mazo)
        elif tecla == b'\r':  # Enter
            return indice + 1 #Mueve selección con flechas izquierda/derecha o confirma con Enter.
        elif tecla == b'0':
            return 0

def elegir_color():  # permite elegir color tras un comodín.
    '''
    Permite al jugador elegir un color después de jugar un comodín (Negro).
   
    Retorna:
        str: El color elegido ("ROJO", "AZUL", "VERDE", o "AMARILLO").
    '''
    colores = ["ROJO", "AMARILLO", "VERDE", "AZUL"]  # Lista de colores válidos.
    print("Elegí un color para el cambio:")  # Muestra mensaje.
    for i, col in enumerate(colores):  # Muestra colores numerados.
        print(f"{i+1}. {col}")
    while True:
        try:
            eleccion = int(input("Ingrese el número del color elegido: ")) - 1
            if 0 <= eleccion < len(colores):# esto es lo que estas intentando sacar
                #si por ejemplo el numero es colores[24] rompe y sale por el except y te vuelve a pedir el num 
                return colores[eleccion] 
            else:
                print("Número fuera de rango. Intente nuevamente.")
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número.")

        
def elegirColorPc(mazo): #decide color óptimo para la PC.
    '''
    Determina el color óptimo para la PC tras jugar un comodín, eligiendo el color
    que la PC tiene en mayor cantidad en su mano. Si hay empate o solo tiene negras, elige uno al azar.
   
    Parámetros:
        mazo (list): La mano de cartas de la PC.
   
    Retorna:
        str: El color elegido.
    '''
    colores_validos = ["ROJO", "AZUL", "VERDE", "AMARILLO"] #Lista de colores válidos.
    conteo = {color: 0 for color in colores_validos} #Crea conteo de colores.
    conteo["NEGRO"] = 0 

    for carta in mazo: #Cuenta cartas por color en la mano de la PC.
        color = carta[1]
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


def turnoUsuario(mazoUsuario, mazo_reparto, mazo_descarte, cartaEnJuego, historial, nombre, id_partida): #lógica del turno del jugador.
    '''
    Ejecuta la lógica completa de un turno para un jugador humano.
    Permite jugar una carta válida o tomar una carta del mazo.
   
    Parámetros:
        mazoUsuario (list): Mano actual del jugador.
        mazo_reparto (list): Mazo de donde se toman cartas.
        mazo_descarte (list): Pila de cartas descartadas.
        cartaEnJuego (list): La última carta jugada.
        historial (dict): Diccionario global donde se registran las jugadas.
        nombre (str): Nombre del jugador (clave para el historial).
        id_partida (str): Identificador único de la partida actual.
   
    Modifica:
        mazoUsuario, mazo_reparto, mazo_descarte, cartaEnJuego y historial.
   
    Retorna:
        tuple: (cartaEnJuego, mazoUsuario, mazo_reparto, mazo_descarte, msgOpcion0) actualizados.
    '''
    salir = False #Variables de control de turno.
    tomoUnaCarta = False
    opcion = -1
    msgOpcion0 = "0  -> Tomar una carta" #Mensaje inicial para opción 0.
    print("es tu turno! Elegí una opcion o carta del mazo para jugar!") #Mensaje de turno del usuario.
    if nombre not in historial:
        historial[nombre] = []
    while not salir: #Loop hasta que el jugador juegue o pase.
        opcion = seleccionar_con_flechas(mazoUsuario, msgOpcion0, cartaEnJuego) #Llama a selección con flechas.
        if opcion < 0 or opcion > len(mazoUsuario): #Valida opción fuera de rango.
            print("opcion no valida!")
        elif opcion == 0 and not tomoUnaCarta: # Si toma carta, reparte y actualiza.
            print("El usuario toma una carta")
            nueva_carta, mazo_reparto, mazo_descarte = repartir(1, mazo_reparto, mazo_descarte)
            mazoUsuario += nueva_carta
            tomoUnaCarta = True
            msgOpcion0 = "0  -> Pasar turno" #Si vuelve a elegir 0, pasa turno.
        elif opcion == 0 and tomoUnaCarta:
            salir = True
            opcion = -1
        else:
            opcion = opcion - 1
            if validarCarta(cartaEnJuego, mazoUsuario[opcion]): #Si juega una carta válida: actualiza carta en juego, pide color si comodín, descarta y registra historial.
                cartaEnJuego = mazoUsuario[opcion]
                fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if cartaEnJuego[1] == "NEGRO" :
                  cartaEnJuego[1] = elegir_color()

                mazo_descarte.append(cartaEnJuego)  # mover al mazo de descarte
                del mazoUsuario[opcion]
                historial[nombre].append({
                "turno": len(historial[nombre]) + 1,
                "carta": cartaEnJuego,
                "cartas_restantes": len(mazoUsuario),
                "mensaje": f"{nombre} jugó {cartaEnJuego[0]} {cartaEnJuego[1]}",
                "fecha_hora": fecha_hora_actual,
                "id_partida": id_partida
                })
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
    return cartaEnJuego, mazoUsuario, mazo_reparto, mazo_descarte, msgOpcion0 #Devuelve estados actualizados.


def turnoPC(mazoPC, mazo_reparto, mazo_descarte, cartaEnJuego, historial, clave_pc_actual, id_partida): #lógica del turno de la computadora.
    '''
    Ejecuta la lógica completa de un turno para la computadora (PC).
    Juega la primera carta válida que encuentra o toma una carta del mazo.
   
    Parámetros:
        mazoPC (list): Mano actual de la PC.
        mazo_reparto (list): Mazo de donde se toman cartas.
        mazo_descarte (list): Pila de cartas descartadas.
        cartaEnJuego (list): La última carta jugada.
        historial (dict): Diccionario global donde se registran las jugadas.
        clave_pc_actual (str): Clave única para el historial de la PC (ej: "PC_VS_nombre").
        id_partida (str): Identificador único de la partida actual.
   
    Modifica:
        mazoPC, mazo_reparto, mazo_descarte, cartaEnJuego y historial.
   
    Retorna:
        tuple: (cartaEnJuego, mazoPC, mazo_reparto, mazo_descarte) actualizados.
    '''
    print("\nTurno de la computadora...") #Mensaje de turno PC.
    jugada_valida = False #Bandera jugada válida.
    i = 0
    while i < len(mazoPC) and not jugada_valida:
        if validarCarta(cartaEnJuego, mazoPC[i]):
            # La PC juega mazoPC[i]
            carta_jugada = mazoPC[i]
            fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Si es comodín, elegir color
            if carta_jugada[1] == "NEGRO":
                # asignamos color al comodín (modificar una copia para no corromper la mano)
                carta_jugada = [carta_jugada[0], elegirColorPc(mazoPC)]
            # actualizar carta en juego y mover al descarte
            cartaEnJuego = carta_jugada
            mazo_descarte.append(cartaEnJuego)
            numero, color = cartaEnJuego
            color_print = {
                "ROJO": Fore.RED,
                "AZUL": Fore.BLUE,
                "VERDE": Fore.GREEN,
                "AMARILLO": Fore.YELLOW
            }.get(color, Style.RESET_ALL)
            print(f"\nLa computadora jugó: {color_print}{numero} {color}{Style.RESET_ALL}")
            del mazoPC[i]
            historial[clave_pc_actual].append({ #Si encuentra: juega, maneja comodín, actualiza mazo y registra historial
            "turno": len(historial[clave_pc_actual]) + 1,
            "carta": cartaEnJuego,
            "cartas_restantes": len(mazoPC),
            "mensaje": f"PC jugó {cartaEnJuego[0]} {cartaEnJuego[1]}",
            "fecha_hora": fecha_hora_actual,
            "id_partida": id_partida
            })
            jugada_valida = True
        else:
            i += 1 #Si no puede jugar, pasa turno.

    if not jugada_valida:
        print("La computadora no tiene cartas válidas. Toma una carta...")
        nueva_carta, mazo_reparto, mazo_descarte = repartir(1, mazo_reparto, mazo_descarte)
        carta = nueva_carta[0]
        if validarCarta(cartaEnJuego, carta):
            # juega la carta que tomó
            if carta[1] == "NEGRO":
                carta = [carta[0], elegirColorPc(mazoPC)]
            cartaEnJuego = carta
            mazo_descarte.append(carta)
            numero, color = cartaEnJuego
            color_print = {
                "ROJO": Fore.RED,
                "AZUL": Fore.BLUE,
                "VERDE": Fore.GREEN,
                "AMARILLO": Fore.YELLOW
            }.get(color, Style.RESET_ALL)
            print(f"\n¡La computadora jugó la carta que tomó! {color_print}{numero} {color}{Style.RESET_ALL}")
        else:
            mazoPC.append(carta)
            print("La computadora no pudo jugar. Pasa el turno.")

    input("\nPresione Enter para continuar...")
    return cartaEnJuego, mazoPC, mazo_reparto, mazo_descarte

def registrar_usuario(): #pide nombre del jugador.
    '''
    Pide y valida el nombre del jugador principal.
   
    Retorna:
        str: El nombre del usuario en minúsculas y sin espacios iniciales/finales.
    '''
    print("\n=== REGISTRO DE USUARIO ===") #Muestra mensaje.
    nombre = input("Ingrese su nombre: ") #Pide nombre.
    while len(nombre.strip()) == 0: #Valida que no esté vacío.
        print("El nombre no puede estar vacío")
        nombre = input("Ingrese su nombre: ")
    return nombre.strip().lower() #Devuelve nombre.
def registrar_oponente(nombre_primer_jugador):
    '''
    Pide y valida el nombre del oponente (Jugador 2) para el modo 1v1.
    Asegura que el nombre no esté vacío y que no sea el mismo que el Jugador 1.
   
    Parámetros:
        nombre_primer_jugador (str): El nombre del Jugador 1 (para evitar duplicados).
   
    Retorna:
        str: El nombre del oponente en minúsculas.
    '''
    print("\n=== REGISTRO/SELECCIÓN DE OPONENTE ===")
    while True:
        nombre2 = input("Ingrese el nombre del oponente: ").strip().lower()
        if len(nombre2) == 0:
            print("El nombre no puede estar vacío.")
            continue
        if nombre2 == nombre_primer_jugador:
            print("El oponente no puede ser el mismo que el jugador 1. Ingrese otro nombre.")
            continue
        return nombre2

def reglas(): #imprime las reglas básicas del UNO.
    '''
    Muestra las reglas del juego leyendo el contenido del archivo 'FIles/reglas.txt'.
   
    Retorna:
        None: Solo realiza impresión en pantalla.
    '''
    try: 
        reglas = open("FIles/reglas.txt", "r") #Abre archivo de reglas.
        for linea in reglas:
            print(linea)
        reglas.close() #Cierra archivo.
        input("\nPresione Enter para continuar...") #Pausa para continuar.
    except FileNotFoundError:
        print("Archivo de reglas no encontrado.")
        input("\nPresione Enter para continuar...")
    
def ranking(): #muestra el ranking de jugadores.
    '''
    Imprime el ranking de jugadores ordenados por puntuación de forma descendente.
    Utiliza la variable global jugadores_dic.
   
    Retorna:
        None: Solo realiza impresión en pantalla.
    '''
    print("\n=== RANKING DE JUGADORES ===") #Título.
    ranking_ordenado = sorted(jugadores_dic.items(), key=lambda x: x[1], reverse=True) #Ordena diccionario por puntaje descendente.
    for i in range(len(ranking_ordenado)): #Recorre y muestra jugadores.
        nombre, puntos = ranking_ordenado[i]
        print(f"{i+1}. {nombre}: {puntos} puntos")
    input("\nPresione Enter para continuar...") #Pausa.

def actualizar_puntuacion(nombre, puntos): #actualiza puntaje de un jugador.
    '''
    Actualiza la puntuación de un jugador sumando o estableciendo nuevos puntos.
    Guarda el ranking actualizado en "ranking.json".
   
    Parámetros:
        nombre (str): Nombre del jugador a actualizar.
        puntos (int): Puntos a sumar (puede ser positivo o negativo).
   
    Modifica:
        El diccionario global jugadores_dic y el archivo ranking.json.
   
    Retorna:
        None
    '''
    nombre_lower = nombre.lower() 
    try:
        jugadores_dic[nombre_lower] += puntos 
    except KeyError:
        jugadores_dic[nombre_lower] = puntos
    guardar_archivo_json("ranking.json", jugadores_dic)

def historial_partidas(historial, nombre, clave_pc_actual):
    '''
    Muestra el historial completo de jugadas de las partidas del jugador principal.
    Recolecta y ordena cronológicamente las jugadas del jugador y de sus oponentes (PC o J2)
    que pertenecen a las mismas partidas.
   
    Parámetros:
        historial (dict): Diccionario cargado desde Logs.json con todos los registros de juego.
        nombre (str): Nombre del jugador principal.
        clave_pc_actual (str): Clave usada para el historial del modo VS PC (ej: "PC_VS_nombre").
   
    Retorna:
        None: Solo realiza impresión en pantalla.
    '''
    if historial.get(nombre) or historial.get(clave_pc_actual):
        print("\n=== HISTORIAL DE JUGADAS ===")
        log_total = []
        for jugada in historial.get(nombre, []):
            if 'id_partida' in jugada:
                log_total.append((nombre, jugada))
        for clave_oponente, jugadas in historial.items():
            if clave_oponente != nombre:
                for jugada in jugadas:
                    if 'id_partida' in jugada and jugada['id_partida'] in [j['id_partida'] for j in historial.get(nombre, [])]:
                        log_total.append((clave_oponente, jugada))
        log_total.sort(key=lambda x: x[1]['fecha_hora']) 
        id_partida_anterior = None
        for jugador, jugada in log_total:
            id_partida_actual = jugada['id_partida']
            if id_partida_anterior is not None and id_partida_actual != id_partida_anterior:
                print("-------------------- FIN DE PARTIDA --------------------")
            print(f"{jugada['fecha_hora']} - {jugada['mensaje']} | Cartas restantes: {jugada['cartas_restantes']}")
            id_partida_anterior = id_partida_actual
    else:
        print(f"\nNo hay historial de partidas de {nombre} todavía.")
    
    input("\nPresione Enter para continuar...")


def menu(historial, nombre, clave_pc_actual): #menú principal del juego.
    '''
    Muestra el menú principal del juego y maneja la navegación.
   
    Parámetros:
        historial (dict): Diccionario de historial de partidas.
        nombre (str): Nombre del jugador actual.
        clave_pc_actual (str): Clave para el historial VS PC.
   
    Retorna:
        int/bool: 1 (vs PC), 2 (1v1), o False (Salir del juego).
    '''
    if nombre not in historial:
        historial[nombre] = []
    while True:
        os.system('cls') #Limpia pantalla y muestra título.
        print("\n=== MENÚ PRINCIPAL ===") #Muestra opciones del menú.
        print("1. Iniciar partida")
        print("2. Reglas del juego")
        print("3. Ranking de jugadores")
        print("4. Historial")
        print("5. Salir del juego")
        try:
            opcion = int(input("\nSeleccione una opción: "))
            
            if opcion == 1:
                  # Elegir modo de juego
                while True:
                    os.system('cls')
                    print("Elegí modo de juego:")
                    print("1. vs PC")
                    print("2. 1v1 (Jugador vs Jugador)")
                    print("3. Volver")
                    try:
                        modo = int(input("Seleccione: "))
                        if modo in (1,2):
                            return modo
                        elif modo == 3:
                            break
                        else:
                            print("Opción inválida.")
                            input("Presione Enter para continuar...")
                    except ValueError:
                        print("Ingrese un número válido.")
                        input("Presione Enter para continuar...")
            elif opcion == 2:
                reglas()
            elif opcion == 3:
                ranking()
            elif opcion == 4:
                historial_partidas(historial, nombre, clave_pc_actual)
            elif opcion == 5:
                print("\n¡Gracias por jugar!")
                return False
            else:
                print("\nNumero Incorrecto! Por favor, ingrese un número del 1 al 5.") 
                input("\nPresione Enter para continuar...")
            
        except ValueError:
            print("\nSolo se permiten numero! Por favor, ingrese un número del 1 al 5.")
            input("Presione Enter para continuar...")

# ================== Juego principal ==================
def iniciar_partida_vs_pc(nombre_usuario, historial):
    '''
    Inicializa y ejecuta una partida de UNO en el modo Jugador vs PC.
   
    Parámetros:
        nombre_usuario (str): Nombre del jugador humano.
        historial (dict): Diccionario para registrar el log de jugadas.
   
    Modifica:
        Actualiza el historial con las jugadas y el ranking con el resultado final.
   
    Retorna:
        None
    '''
    clave_pc_actual = f"PC_VS_{nombre_usuario}"
    id_partida = datetime.now().strftime("%Y%m%d%H%M%S")
    if nombre_usuario not in historial:
        historial[nombre_usuario] = []
    if clave_pc_actual not in historial:
        historial[clave_pc_actual] = []

    mazo_general = Mazo_Uno()
    mazo_reparto = mazo_general.copy()
    random.shuffle(mazo_reparto)
    mazo_descarte = []

    mazoUsuario, mazo_reparto, mazo_descarte = repartir(7, mazo_reparto, mazo_descarte)
    mazoPC, mazo_reparto, mazo_descarte = repartir(7, mazo_reparto, mazo_descarte)
    cartaEnJuego_list, mazo_reparto, mazo_descarte = repartir(1, mazo_reparto, mazo_descarte)
    while cartaEnJuego_list and cartaEnJuego_list[0][1] == "NEGRO":
        cartaEnJuego_list, mazo_reparto, mazo_descarte = repartir(1, mazo_reparto, mazo_descarte)
    cartaEnJuego = cartaEnJuego_list[0]

    turno = 0  # 0 = Usuario, 1 = PC
    efecto_pendiente = None
    prev_carta = None

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

        # Efectos pendientes (igual que antes)
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
            prev_carta = cartaEnJuego[:]
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
            prev_carta = cartaEnJuego[:]
            continue

        if efecto_pendiente == "BLOQUEO":
            print("¡BLOQUEO! Se salta un turno.")
            turno = 1 - turno
            efecto_pendiente = None
            input("\nPresione Enter para continuar...")
            prev_carta = cartaEnJuego[:]
            continue

        if efecto_pendiente == "REVERSA":
            print("¡Reversa! Se invierte el turno (en dos jugadores equivale a saltar turno).")
            turno = 1 - turno
            efecto_pendiente = None
            input("\nPresione Enter para continuar...")
            prev_carta = cartaEnJuego[:]
            continue

        # Turnos
        if turno == 0:
            cartaEnJuego, mazoUsuario, mazo_reparto, mazo_descarte, msgOpcion0 = turnoUsuario(
                mazoUsuario, mazo_reparto, mazo_descarte, cartaEnJuego, historial, nombre_usuario, id_partida)
            turno = 1
        else:
            cartaEnJuego, mazoPC, mazo_reparto, mazo_descarte = turnoPC(
                mazoPC, mazo_reparto, mazo_descarte, cartaEnJuego, historial, f"PC_VS_{nombre_usuario}", id_partida)
            turno = 0

        if prev_carta is None or cartaEnJuego != prev_carta:
            if cartaEnJuego[0] == "+2":
                efecto_pendiente = "MAS2"
            elif cartaEnJuego[0] == "+4":
                efecto_pendiente = "MAS4"
            elif cartaEnJuego[0] == "BLOQUEO":
                efecto_pendiente = "BLOQUEO"
            elif cartaEnJuego[0] == "REVERSA":
                efecto_pendiente = "REVERSA"
            else:
                efecto_pendiente = None
        else:
            efecto_pendiente = None

        prev_carta = cartaEnJuego[:]

    # Fin del juego
    if len(mazoUsuario) == 0:
        print("¡Ganaste!")
        puntuacion=10*len(mazoPC)
        actualizar_puntuacion(nombre_usuario, puntuacion)
    else:
        print("¡Ganó la computadora!")
        actualizar_puntuacion(nombre_usuario, -5)
    guardar_archivo_json("Logs.json", historial)
    input("\nPresione Enter para continuar...")

def iniciar_partida_1v1(nombre_usuario, historial):
    '''
    Inicializa y ejecuta una partida de UNO en el modo Jugador vs Jugador (1v1).
   
    Parámetros:
        nombre_usuario (str): Nombre del Jugador 1.
        historial (dict): Diccionario para registrar el log de jugadas.
   
    Modifica:
        Actualiza el historial con las jugadas y el ranking con el resultado final.
   
    Retorna:
        None
    '''
    jugador1 = nombre_usuario
    jugador2 = registrar_oponente(nombre_usuario)

    # Crear claves en historial si no existen
    if jugador1 not in historial:
        historial[jugador1] = []
    if jugador2 not in historial:
        historial[jugador2] = []

    id_partida = datetime.now().strftime("%Y%m%d%H%M%S")

    mazo_general = Mazo_Uno()
    mazo_reparto = mazo_general.copy()
    random.shuffle(mazo_reparto)
    mazo_descarte = []

    mazoJ1, mazo_reparto, mazo_descarte = repartir(7, mazo_reparto, mazo_descarte)
    mazoJ2, mazo_reparto, mazo_descarte = repartir(7, mazo_reparto, mazo_descarte)
    cartaEnJuego_list, mazo_reparto, mazo_descarte = repartir(1, mazo_reparto, mazo_descarte)
    while cartaEnJuego_list and cartaEnJuego_list[0][1] == "NEGRO":
        cartaEnJuego_list, mazo_reparto, mazo_descarte = repartir(1, mazo_reparto, mazo_descarte)
    cartaEnJuego = cartaEnJuego_list[0]

    # turno: 0 = jugador1, 1 = jugador2
    turno = 0
    efecto_pendiente = None
    prev_carta = None

    while len(mazoJ1) > 0 and len(mazoJ2) > 0:
        os.system('cls')
        print(f"\nJugador 1: {jugador1} - cartas: {len(mazoJ1)}")
        print(f"Jugador 2: {jugador2} - cartas: {len(mazoJ2)}")
        numero, color = cartaEnJuego
        color_print = {
            "ROJO": Fore.RED,
            "AZUL": Fore.BLUE,
            "VERDE": Fore.GREEN,
            "AMARILLO": Fore.YELLOW
        }.get(color, Style.RESET_ALL)
        print(f"\nLa carta en juego es: {color_print}{numero} {color}{Style.RESET_ALL}")

        # Efectos pendientes
        if efecto_pendiente == "MAS2":
            if turno == 0:
                print(f"¡Efecto +2! {jugador1} toma 2 cartas y pierde el turno.")
                nuevas, mazo_reparto, mazo_descarte = repartir(2, mazo_reparto, mazo_descarte)
                mazoJ1 += nuevas
                turno = 1
            else:
                print(f"¡Efecto +2! {jugador2} toma 2 cartas y pierde el turno.")
                nuevas, mazo_reparto, mazo_descarte = repartir(2, mazo_reparto, mazo_descarte)
                mazoJ2 += nuevas
                turno = 0
            efecto_pendiente = None
            input("\nPresione Enter para continuar...")
            prev_carta = cartaEnJuego[:]
            continue

        if efecto_pendiente == "MAS4":
            if turno == 0:
                print(f"¡Efecto +4! {jugador1} toma 4 cartas y pierde el turno.")
                nuevas, mazo_reparto, mazo_descarte = repartir(4, mazo_reparto, mazo_descarte)
                mazoJ1 += nuevas
                turno = 1
            else:
                print(f"¡Efecto +4! {jugador2} toma 4 cartas y pierde el turno.")
                nuevas, mazo_reparto, mazo_descarte = repartir(4, mazo_reparto, mazo_descarte)
                mazoJ2 += nuevas
                turno = 0
            efecto_pendiente = None
            input("\nPresione Enter para continuar...")
            prev_carta = cartaEnJuego[:]
            continue

        if efecto_pendiente == "BLOQUEO":
            print("¡BLOQUEO! Se salta un turno.")
            turno = 1 - turno
            efecto_pendiente = None
            input("\nPresione Enter para continuar...")
            prev_carta = cartaEnJuego[:]
            continue

        if efecto_pendiente == "REVERSA":
            print("¡Reversa! Se invierte el turno (en dos jugadores equivale a saltar turno).")
            turno = 1 - turno
            efecto_pendiente = None
            input("\nPresione Enter para continuar...")
            prev_carta = cartaEnJuego[:]
            continue

        if turno == 0:
            cartaEnJuego, mazoJ1, mazo_reparto, mazo_descarte, msgOpcion0 = turnoUsuario(
                mazoJ1, mazo_reparto, mazo_descarte, cartaEnJuego, historial, jugador1, id_partida)
            turno = 1
        else:
            cartaEnJuego, mazoJ2, mazo_reparto, mazo_descarte, msgOpcion0 = turnoUsuario(
                mazoJ2, mazo_reparto, mazo_descarte, cartaEnJuego, historial, jugador2, id_partida)
            turno = 0

        if prev_carta is None or cartaEnJuego != prev_carta:
            if cartaEnJuego[0] == "+2":
                efecto_pendiente = "MAS2"
            elif cartaEnJuego[0] == "+4":
                efecto_pendiente = "MAS4"
            elif cartaEnJuego[0] == "BLOQUEO":
                efecto_pendiente = "BLOQUEO"
            elif cartaEnJuego[0] == "REVERSA":
                efecto_pendiente = "REVERSA"
            else:
                efecto_pendiente = None
        else:
            efecto_pendiente = None

        prev_carta = cartaEnJuego[:]

    # Fin del juego 1v1
    if len(mazoJ1) == 0:
        print(f"¡Ganó {jugador1}!")
        actualizar_puntuacion(jugador1, 10*len(mazoJ2))
        actualizar_puntuacion(jugador2, -5)
    else:
        print(f"¡Ganó {jugador2}!")
        actualizar_puntuacion(jugador2, 10*len(mazoJ1))
        actualizar_puntuacion(jugador1, -5)

    guardar_archivo_json("Logs.json", historial)
    input("\nPresione Enter para continuar...")

# ================== Juego principal ==================
def iniciar_juego():
    '''
    Función principal que inicializa el juego: registra al usuario, carga el historial
    y entra en el bucle del menú principal.
   
    Retorna:
        None
    '''
    nombre_usuario = registrar_usuario()
    print(f"\n¡Bienvenido {nombre_usuario}!")
    input("Presione Enter para continuar...")
    historial = leer_archivo_json("Logs.json") or {}

    while True:
        modo = menu(historial, nombre_usuario, f"PC_VS_{nombre_usuario}")
        if modo == False:
            guardar_archivo_json("Logs.json", historial)
            break
        elif modo == 1:
            iniciar_partida_vs_pc(nombre_usuario, historial)
        elif modo == 2:
            iniciar_partida_1v1(nombre_usuario, historial)
        else:
            continue

iniciar_juego()
