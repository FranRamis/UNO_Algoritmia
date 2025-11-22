import random #Importa la librería random para generar aleatoriedad.
import os #Importa la librería os para ejecutar comandos del sistema para limpiar la pantalla.
import msvcrt
from tkinter import simpledialog  # Para captura de teclas en Windows
from colorama import init, Fore, Style  #Inicializa colorama con auto-reset para que los colores no se propaguen.
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
from datetime import datetime
init(autoreset=True)

AMARILLO =  '#F8DB22'
ROJO = "#EE161F"
ROJOCARTA = "#EC1A23"
VERDECARTA = "#94EC57"
AMARILLOCARTA = "#F3CF09"
AZULCARTA = "#0092CB"

# Funciones del juego (se definen antes de crear la ventana)
def leer_archivo_json(nombre_archivo):
    ruta = os.path.join(os.path.dirname(__file__), "FIles", nombre_archivo)
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            arch = json.load(archivo)
            print(f"Archivo '{nombre_archivo}' leído correctamente.")
            return arch
    except Exception as e:
        print(f"Error inesperado al leer '{nombre_archivo}': {e}")
        return {}

def guardar_archivo_json(nombre_archivo, datos):
    ruta = os.path.join(os.path.dirname(__file__), "FIles", nombre_archivo)
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
            print(f"Archivo '{nombre_archivo}' guardado correctamente.")
    except Exception as e:
        print(f"Error inesperado al guardar '{nombre_archivo}': {e}")





def leer_archivo_json(nombre_archivo):
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
    ruta = os.path.join(os.path.dirname(__file__), "FIles", nombre_archivo)
    
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
            print(f"Archivo '{nombre_archivo}' guardado correctamente.")
    except Exception as e:
        print(f"Error inesperado al guardar '{nombre_archivo}': {e}")

jugadores_dic = leer_archivo_json("ranking.json")

def guardar_historial_json(historial):
    ruta = os.path.join(os.path.dirname(__file__), "FIles", "Logs.json")

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(historial, archivo, indent=4, ensure_ascii=False)

    print("\nArchivo 'Logs.json' actualizado correctamente.")

def cargar_historial_json():
    ruta = os.path.join(os.path.dirname(__file__), "FIles", "Logs.json")

    with open(ruta, "r", encoding="utf-8") as archivo:
        try:
            data = json.load(archivo)
            if "PC" not in data:
                data["PC"] = []
            return data
        except json.JSONDecodeError:
            return {"PC": []}




def Mazo_Uno(): #crea y devuelve el mazo completo de UNO.
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
    check = False 
    if cartaEnJuego[0] == cartaUsuario[0] or cartaEnJuego[1] == cartaUsuario[1]: #Valida por número o color.
        check = True  
    elif (cartaUsuario[1] == "NEGRO") : #Valida si la carta es negra (comodín).
        check = True 
    elif (cartaUsuario[1] in ["+2", "BLOQUEO", "REVERSA", "+4"]) and cartaEnJuego[1] == cartaUsuario[1]: #Valida si ambas cartas son del mismo tipo especial.
        check = True
    return check 

# función para selección con flechas
def seleccionar_con_flechas(mazo, msgOpcion0, cartaEnJuego): #permite elegir carta con teclado.
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
            print(f"\nLa computadora jugó: {cartaEnJuego[0]} {cartaEnJuego[1]}")
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
            print("¡La computadora jugó la carta que tomó! ", cartaEnJuego[0], cartaEnJuego[1])
        else:
            mazoPC.append(carta)
            print("La computadora no pudo jugar. Pasa el turno.")

    input("\nPresione Enter para continuar...")
    return cartaEnJuego, mazoPC, mazo_reparto, mazo_descarte

def registrar_usuario(): #pide nombre del jugador.
    print("\n=== REGISTRO DE USUARIO ===") #Muestra mensaje.
    nombre = input("Ingrese su nombre: ") #Pide nombre.
    while len(nombre.strip()) == 0: #Valida que no esté vacío.
        print("El nombre no puede estar vacío")
        nombre = input("Ingrese su nombre: ")
    return nombre.strip().lower() #Devuelve nombre.

def reglas(): #imprime las reglas básicas del UNO.
    ventana_reglas = tk.Toplevel(ventana)
    ventana_reglas.title("Reglas del Juego")
    ventana_reglas.geometry("600x582")
    ventana_reglas.configure(bg=AMARILLO)
    
    text_widget = tk.Text(ventana_reglas, font=("Arial", 12), wrap=tk.WORD, bg=AMARILLO)
    text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    try: 
        with open("FIles/reglas.txt", "r", encoding="utf-8") as archivo:
            text_widget.insert("1.0", archivo.read())
    except FileNotFoundError:
        text_widget.insert("1.0", "Archivo de reglas no encontrado.")
    
    text_widget.config(state=tk.DISABLED)
    
def ranking(): #muestra el ranking de jugadores.
    print("\n=== RANKING DE JUGADORES ===") #Título.
    ranking_ordenado = sorted(jugadores_dic.items(), key=lambda x: x[1], reverse=True) #Ordena diccionario por puntaje descendente.
    ventana_reglas = tk.Toplevel(ventana)
    ventana_reglas.title("Reglas del Juego")
    ventana_reglas.geometry("600x582")
    ventana_reglas.configure(bg=AMARILLO)
    rankingtxt = ""
    text_widget = tk.Text(ventana_reglas, font=("Arial", 20), wrap=tk.WORD, bg=AMARILLO, spacing1=5, spacing3=5)
    text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    for i in range(len(ranking_ordenado)): #Recorre y muestra jugadores.
        nombre, puntos = ranking_ordenado[i]
        rankingtxt = rankingtxt + str(i+1) +  ". " + nombre + ": " + str(puntos) + "\n"
    text_widget.insert("1.0", rankingtxt)
    
    
    text_widget.config(state=tk.DISABLED)



  
    for i in range(len(ranking_ordenado)): #Recorre y muestra jugadores.
        nombre, puntos = ranking_ordenado[i]
        rankingtxt = rankingtxt + str(i +  nombre + ":"+ puntos )
   
  
def actualizar_puntuacion(nombre, puntos): #actualiza puntaje de un jugador.
    nombre_lower = nombre.lower() 
    try:
        jugadores_dic[nombre_lower] += puntos 
    except KeyError:
        jugadores_dic[nombre_lower] = puntos
    guardar_archivo_json("ranking.json", jugadores_dic)



def menu(historial, nombre, clave_pc_actual): #menú principal del juego.
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
                return True
            elif opcion == 2:
                reglas()
            elif opcion == 3:
                ranking()
            elif opcion == 4:
                if historial[nombre] or historial["PC"]:
                    print("\n=== HISTORIAL DE JUGADAS ===") #Muestra historial de jugadas.

                    log_total = []
                    for jugada in historial[nombre]:
                        if 'id_partida' in jugada:
                            log_total.append((nombre, jugada)) 
                    for jugada in historial.get(clave_pc_actual,[]):
                        if 'id_partida' in jugada:
                            log_total.append(("PC", jugada))

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
def iniciar_juego(): #controla todo el flujo del juego.
    nombre_usuario = registrar_usuario() #Registra usuario.
    print(f"\n¡Bienvenido {nombre_usuario}!") #Mensaje de bienvenida.
    input("Presione Enter para continuar...") #Pausa.
    historial = cargar_historial_json() #Cargo historial de partidas
    clave_pc_actual = f"PC_VS_{nombre_usuario}" 
    while True: #Loop principal del juego.
        opcion = menu(historial, nombre_usuario, clave_pc_actual)
        if opcion == False:
            guardar_historial_json(historial)
            break
        elif opcion == True: #Si usuario elige jugar: prepara mazos, reparte y elige carta inicial.
            id_partida = datetime.now().strftime("%Y%m%d%H%M%S") 

            if nombre_usuario not in historial:
                historial[nombre_usuario] = []

            if clave_pc_actual not in historial:
                historial[clave_pc_actual] = []

            mazo_general = Mazo_Uno() # Mazo original
            mazo_reparto = mazo_general.copy() # Copio el original para modificarlo
            random.shuffle(mazo_reparto) # Barajo el mazo a repartir
            mazo_descarte = [] #genero un mazo para descartar cartas vacio.

            mazoUsuario, mazo_reparto, mazo_descarte = repartir(7, mazo_reparto, mazo_descarte)
            mazoPC, mazo_reparto, mazo_descarte = repartir(7, mazo_reparto, mazo_descarte)
            cartaEnJuego, mazo_reparto, mazo_descarte = repartir(1, mazo_reparto, mazo_descarte)
            mazoUsuario = [[10,"ROJO"]]      
            cartaEnJuego = [[10,"ROJO"]]  
            while cartaEnJuego[0][1] == "NEGRO":
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
                elif efecto_pendiente == "REVERSA":
                    print("¡Reversa! Se invierte el turno (en dos jugadores equivale a saltar turno).")
                    turno = 1 - turno
                    efecto_pendiente = None
                    input("\nPresione Enter para continuar...")
                    continue

                # Lógica del turno usuario.
                if turno == 0:

                    cartaEnJuego, mazoUsuario, mazo_reparto, mazo_descarte, msgOpcion0 = turnoUsuario(
                        mazoUsuario, mazo_reparto, mazo_descarte, cartaEnJuego, historial, nombre_usuario, id_partida)
                    turno = 1
                #Lógica del turno PC.
                else:
                    cartaEnJuego, mazoPC, mazo_reparto, mazo_descarte = turnoPC(
                        mazoPC, mazo_reparto, mazo_descarte, cartaEnJuego, historial, clave_pc_actual, id_partida)
                    turno = 0

                # Detectar efecto de la última carta jugada

                if msgOpcion0 != "0  -> Pasar turno":
                    if cartaEnJuego[0] == "+2":
                            efecto_pendiente = "MAS2"
                    elif cartaEnJuego[0] == "+4":
                            efecto_pendiente = "MAS4"
                    elif cartaEnJuego[0] == "BLOQUEO":
                            efecto_pendiente = "BLOQUEO"
                    elif cartaEnJuego[0] == "REVERSA":
                            efecto_pendiente = "REVERSA"
                else:
                    efecto_pendiente=None


            # Fin del juego: declara ganador y actualiza puntuación.
            if len(mazoUsuario) == 0:
                print("¡Ganaste!")
                actualizar_puntuacion(nombre_usuario, 15)
            else:
                print("¡Ganó la computadora!")
                actualizar_puntuacion(nombre_usuario, -5)
            guardar_historial_json(historial)
            input("\nPresione Enter para continuar...") #Pausa.

#iniciar_juego() 
# Crear ventana principal
ventana = tk.Tk()
ventana.title("UNO - Algoritmos y estructuras de datos")
ventana.geometry("600x500")
ventana.configure(bg=AMARILLO)
ruta_logo = os.path.join(os.path.dirname(__file__), "FIles", "Imgs", "logo.png")
icono_pequeño = Image.open(ruta_logo).resize((16, 16))
ventana.iconphoto(True, ImageTk.PhotoImage(icono_pequeño))


nombre_input = simpledialog.askstring("Input", "¿Cómo te llamas?")
 
titulo = tk.Label(
    ventana,
    text="UNO - Algoritmos y estructuras de datos",
    font=("Arial", 20, "bold"),
    bg=AMARILLO,
    fg=ROJO
)
titulo.pack(pady=10)

btn_iniciar = tk.Button(ventana, text="🎯 Iniciar Partida", font=("Arial", 14, "bold"), 
                        bg=VERDECARTA, fg="black", width=25, height=2)
btn_iniciar.pack(pady=10)

btn_reglas = tk.Button(ventana, text="📖 Reglas del Juego", font=("Arial", 14, "bold"),
                       bg=AZULCARTA, fg="white", width=25, height=2, command=reglas )
btn_reglas.pack(pady=10)

btn_ranking = tk.Button(ventana, text="🏆 Ranking", font=("Arial", 14, "bold"),
                        bg=AZULCARTA, fg="white", width=25, height=2, command=ranking)
btn_ranking.pack(pady=10)

btn_historial = tk.Button(ventana, text="🕑 Historial", font=("Arial", 14, "bold"),
                          bg=AZULCARTA, fg="white", width=25, height=2)
btn_historial.pack(pady=10)

btn_salir = tk.Button(ventana, text="❌ Salir", font=("Arial", 14, "bold"),
                      bg=ROJO, fg="white", width=25, height=2)
btn_salir.pack(pady=10)
ventana.mainloop()