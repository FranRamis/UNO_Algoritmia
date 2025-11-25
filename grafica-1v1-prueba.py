import random
import os
import sys
import json
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk

# --- Configuración Inicial ---
# Intentamos importar colorama por si se usa en consola, aunque en GUI no es vital
try:
    from colorama import init
    init(autoreset=True)
except ImportError:
    pass

# --- Constantes de Color y Diseño ---
AMARILLO_FONDO = '#F8DB22'
ROJO_UNO = "#EE161F"
VERDE_BTN = "#94EC57"
AZUL_BTN = "#0092CB"
ROJO_BTN = "#EC1A23"
GRIS_NEUTRO = "#DDDDDD"

# Diccionario de colores para las cartas visuales (Estilo Original)
COLORES_CARTA = {
    "ROJO": "#EC1A23",
    "AZUL": "#0092CB",
    "VERDE": "#94EC57",
    "AMARILLO": "#F3CF09",
    "NEGRO": "#555555"
}

# --- Variables Globales ---
jugadores_dic = {
    "thomas": 70, 
    "vera": 70,
    "fran": 65,
    "augus": 55
}
nombre_global = "Jugador"
ventana_principal = None

# --- Gestión de Archivos ---

def leer_archivo_json(nombre_archivo):
    ruta = os.path.join(os.path.dirname(__file__), "FIles", nombre_archivo)
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except:
        return {}

def guardar_archivo_json(nombre_archivo, datos):
    ruta = os.path.join(os.path.dirname(__file__), "FIles", nombre_archivo)
    # Crear carpeta si no existe
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error guardando {nombre_archivo}: {e}")

# Carga inicial del ranking
jugadores_dic = leer_archivo_json("ranking.json") or jugadores_dic

def cargar_historial():
    data = leer_archivo_json("Logs.json")
    return data if data else {}

def guardar_historial(historial):
    guardar_archivo_json("Logs.json", historial)

def actualizar_puntuacion(nombre, puntos):
    global jugadores_dic
    nombre = nombre.lower()
    jugadores_dic[nombre] = jugadores_dic.get(nombre, 0) + puntos
    guardar_archivo_json("ranking.json", jugadores_dic)

# --- Lógica del Juego (Mazos y Cartas) ---

def generar_mazo():
    colores = ["ROJO", "AMARILLO", "VERDE", "AZUL"]
    mazo = []
    for color in colores:
        mazo.append([0, color]) # Un 0
        for n in range(1, 10): # Dos del 1 al 9
            mazo.append([n, color])
            mazo.append([n, color])
        # Especiales de color (2 de cada uno)
        for _ in range(2):
            mazo.append(["BLOQUEO", color])
            mazo.append(["REVERSA", color])
            mazo.append(["+2", color])
    
    # Especiales Negros (4 de cada uno)
    for _ in range(4):
        mazo.append(["+4", "NEGRO"])
        mazo.append(["CAMBIO_COLOR", "NEGRO"])
    
    random.shuffle(mazo)
    return mazo

def repartir_cartas(cantidad, mazo_origen, mazo_descarte):
    mano = []
    for _ in range(cantidad):
        if not mazo_origen:
            if len(mazo_descarte) > 1:
                # Reciclar descarte
                ultima = mazo_descarte.pop()
                mazo_origen = mazo_descarte[:]
                random.shuffle(mazo_origen)
                mazo_descarte = [ultima]
            else:
                break # No hay más cartas
        mano.append(mazo_origen.pop())
    return mano, mazo_origen, mazo_descarte

def es_jugada_valida(carta_mesa, carta_jugador):
    # [valor, color]
    val_mesa, col_mesa = carta_mesa
    val_jug, col_jug = carta_jugador
    
    if col_jug == "NEGRO": return True
    if col_jug == col_mesa: return True
    if val_jug == val_mesa: return True
    
    return False

def elegir_color_pc(mano_pc):
    colores = ["ROJO", "AZUL", "VERDE", "AMARILLO"]
    conteo = {c: 0 for c in colores}
    for c in mano_pc:
        if c[1] in conteo:
            conteo[c[1]] += 1
    # Devuelve el color más frecuente
    return max(conteo, key=conteo.get)

# --- Lógica de la Interfaz Gráfica (Juego) ---

class PartidaGUI:
    def __init__(self, master, jugador1_nombre, modo_juego, jugador2_nombre="PC"):
        self.master = master
        self.ventana = tk.Toplevel(master)
        self.ventana.title(f"Partida UNO: {modo_juego}")
        self.ventana.geometry("1000x750") # Un poco más grande para las cartas altas
        self.ventana.configure(bg=AMARILLO_FONDO)
        
        # Datos de la partida
        self.modo = modo_juego # "VS_PC" o "1V1"
        self.j1_nombre = jugador1_nombre
        self.j2_nombre = jugador2_nombre
        self.historial = cargar_historial()
        self.id_partida = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Inicializar claves de historial si no existen
        if self.j1_nombre not in self.historial: self.historial[self.j1_nombre] = []
        clave_oponente = self.j2_nombre if self.modo == "1V1" else f"PC_VS_{self.j1_nombre}"
        if clave_oponente not in self.historial: self.historial[clave_oponente] = []

        # Preparar mazos
        self.mazo_robo = generar_mazo()
        self.mazo_descarte = []
        self.mano_j1, self.mazo_robo, self.mazo_descarte = repartir_cartas(7, self.mazo_robo, self.mazo_descarte)
        self.mano_j2, self.mazo_robo, self.mazo_descarte = repartir_cartas(7, self.mazo_robo, self.mazo_descarte)
        
        # Carta inicial (evitar negra al inicio para simplificar)
        carta_ini, self.mazo_robo, self.mazo_descarte = repartir_cartas(1, self.mazo_robo, self.mazo_descarte)
        while carta_ini[0][1] == "NEGRO":
            self.mazo_robo.append(carta_ini[0])
            random.shuffle(self.mazo_robo)
            carta_ini, self.mazo_robo, self.mazo_descarte = repartir_cartas(1, self.mazo_robo, self.mazo_descarte)
        
        self.carta_mesa = carta_ini[0]
        self.mazo_descarte.append(self.carta_mesa)
        
        # Estado del juego
        self.turno_actual = 0 # 0 = J1, 1 = J2 (o PC)
        self.ha_tomado_carta = False # Para controlar si ya robó en este turno
        
        # Elementos GUI
        self.crear_elementos_ui()
        self.actualizar_pantalla()
        
        # Si empieza la PC (en caso de implementar sorteo, aquí forzamos J1 empieza)
        self.log_evento(f"¡Inicia la partida! {self.j1_nombre} vs {self.j2_nombre}")

    def crear_elementos_ui(self):
        # Panel Superior (Oponente)
        self.frame_top = tk.Frame(self.ventana, bg=AMARILLO_FONDO)
        self.frame_top.pack(pady=10)
        self.lbl_oponente = tk.Label(self.frame_top, text=f"Oponente: {self.j2_nombre}", font=("Arial", 14, "bold"), bg=AMARILLO_FONDO)
        self.lbl_oponente.pack()
        self.lbl_cartas_oponente = tk.Label(self.frame_top, text="Cartas: 7", font=("Arial", 12), bg=AMARILLO_FONDO)
        self.lbl_cartas_oponente.pack()

        # Panel Central (Mesa)
        self.frame_mesa = tk.Frame(self.ventana, bg="#FFFFFF", bd=5, relief="ridge")
        self.frame_mesa.pack(pady=20, padx=20, fill="x")
        
        self.lbl_estado = tk.Label(self.frame_mesa, text="Estado: Iniciando...", font=("Arial", 12, "italic"), fg="blue", bg="white")
        self.lbl_estado.pack(pady=5)

        self.lbl_carta_mesa = tk.Label(self.frame_mesa, text="", font=("Arial", 24, "bold"), width=10, height=4, relief="solid")
        self.lbl_carta_mesa.pack(pady=10)
        
        # Botón para pasar turno o robar
        self.btn_accion = tk.Button(self.frame_mesa, text="Robar Carta", font=("Arial", 12, "bold"), bg=AZUL_BTN, fg="white", command=self.accion_boton_central)
        self.btn_accion.pack(pady=5)

        # Panel Inferior (Jugador Actual)
        self.frame_bottom = tk.Frame(self.ventana, bg=AMARILLO_FONDO)
        self.frame_bottom.pack(pady=10, fill="both", expand=True)
        
        self.lbl_jugador_actual = tk.Label(self.frame_bottom, text=f"Tu turno: {self.j1_nombre}", font=("Arial", 14, "bold"), bg=AMARILLO_FONDO, fg="black")
        self.lbl_jugador_actual.pack()
        
        # Scrollbar para las cartas si son muchas
        self.canvas_cartas = tk.Canvas(self.frame_bottom, bg=AMARILLO_FONDO, height=220) # Altura aumentada para cartas grandes
        self.scroll_cartas = tk.Scrollbar(self.frame_bottom, orient="horizontal", command=self.canvas_cartas.xview)
        self.frame_mis_cartas = tk.Frame(self.canvas_cartas, bg=AMARILLO_FONDO)
        
        self.frame_mis_cartas.bind("<Configure>", lambda e: self.canvas_cartas.configure(scrollregion=self.canvas_cartas.bbox("all")))
        self.canvas_cartas.create_window((0, 0), window=self.frame_mis_cartas, anchor="nw")
        self.canvas_cartas.configure(xscrollcommand=self.scroll_cartas.set)
        
        self.canvas_cartas.pack(side="top", fill="x", padx=10)
        self.scroll_cartas.pack(side="top", fill="x", padx=10)

    def actualizar_pantalla(self):
        # Actualizar datos oponente
        mano_op = self.mano_j2 if self.turno_actual == 0 else self.mano_j1
        # Lógica de visualización:
        if self.modo == "VS_PC":
            mano_visual = self.mano_j1
            nombre_visual = self.j1_nombre
            cant_oponente = len(self.mano_j2)
            nombre_oponente = "PC"
            es_mi_turno = (self.turno_actual == 0)
        else:
            # Modo 1v1
            if self.turno_actual == 0:
                mano_visual = self.mano_j1
                nombre_visual = self.j1_nombre
                cant_oponente = len(self.mano_j2)
                nombre_oponente = self.j2_nombre
            else:
                mano_visual = self.mano_j2
                nombre_visual = self.j2_nombre
                cant_oponente = len(self.mano_j1)
                nombre_oponente = self.j1_nombre
            es_mi_turno = True # En 1v1 local, siempre es turno del humano activo

        # Actualizar carta mesa
        texto_carta = f"{self.carta_mesa[0]}\n{self.carta_mesa[1]}"
        color_bg = COLORES_CARTA.get(self.carta_mesa[1], "#FFFFFF")
        # La mesa la dejamos con texto visible (negro o blanco según fondo)
        fg_mesa = "white" if self.carta_mesa[1] != "AMARILLO" else "black"
        self.lbl_carta_mesa.config(text=texto_carta, bg=color_bg, fg=fg_mesa)

        # Actualizar labels
        self.lbl_oponente.config(text=f"Oponente: {nombre_oponente}")
        self.lbl_cartas_oponente.config(text=f"Cartas: {cant_oponente}")
        
        if self.modo == "VS_PC" and self.turno_actual == 1:
            self.lbl_jugador_actual.config(text=f"Turno de: {nombre_oponente} (Pensando...)", fg="gray")
            self.btn_accion.config(state="disabled")
        else:
            self.lbl_jugador_actual.config(text=f"Turno de: {nombre_visual}", fg="black")
            self.btn_accion.config(state="normal")
            
        if self.ha_tomado_carta:
            self.btn_accion.config(text="Pasar Turno")
        else:
            self.btn_accion.config(text="Robar Carta")

        # Renderizar cartas abajo (Estilo original solicitado)
        for widget in self.frame_mis_cartas.winfo_children():
            widget.destroy()

        if es_mi_turno:
            for idx, carta in enumerate(mano_visual):
                val, col = carta
                c_bg = COLORES_CARTA.get(col, "gray")
                # Estilo restaurado: Más altas, fuente grande, texto blanco, solo valor
                btn = tk.Button(self.frame_mis_cartas, text=f"{val}", bg=c_bg, fg="white",
                                width=8, height=10, font=("Arial", 12, "bold"),
                                command=lambda i=idx: self.intentar_jugar_carta(i))
                btn.pack(side="left", padx=5, pady=5)
        else:
            lbl = tk.Label(self.frame_mis_cartas, text="Esperando al oponente...", bg=AMARILLO_FONDO)
            lbl.pack()

    def log_evento(self, mensaje):
        self.lbl_estado.config(text=mensaje)
        # print(mensaje) # Opcional para debug

    def accion_boton_central(self):
        # Lógica para el botón Robar/Pasar
        if self.ha_tomado_carta:
            # Pasar turno
            self.finalizar_turno_jugador()
        else:
            # Robar carta
            nuevas, self.mazo_robo, self.mazo_descarte = repartir_cartas(1, self.mazo_robo, self.mazo_descarte)
            carta_robada = nuevas[0]
            
            mano_actual = self.mano_j1 if self.turno_actual == 0 else self.mano_j2
            mano_actual.append(carta_robada)
            
            self.ha_tomado_carta = True
            self.log_evento(f"Robaste: {carta_robada[0]} {carta_robada[1]}")
            
            # Si la carta es jugable, permitir jugarla, si no, el usuario debe dar a "Pasar"
            if es_jugada_valida(self.carta_mesa, carta_robada):
                # No forzamos jugada, solo actualizamos UI para que vea la carta
                pass 
            
            self.actualizar_pantalla()

    def intentar_jugar_carta(self, indice):
        mano_actual = self.mano_j1 if self.turno_actual == 0 else self.mano_j2
        carta = mano_actual[indice]
        
        if es_jugada_valida(self.carta_mesa, carta):
            # Jugarla
            if carta[1] == "NEGRO":
                nuevo_color = simpledialog.askstring("Comodín", "Elige color (ROJO, AZUL, VERDE, AMARILLO):", parent=self.ventana)
                if not nuevo_color or nuevo_color.upper() not in ["ROJO", "AZUL", "VERDE", "AMARILLO"]:
                    nuevo_color = "ROJO" # Default
                carta = [carta[0], nuevo_color.upper()]
            
            # Registrar log
            nombre_jug = self.j1_nombre if self.turno_actual == 0 else self.j2_nombre
            clave_historial = nombre_jug
            if self.modo == "VS_PC" and self.turno_actual == 1: clave_historial = f"PC_VS_{self.j1_nombre}"
            
            self.historial[clave_historial].append({
                "id_partida": self.id_partida,
                "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "mensaje": f"{nombre_jug} jugó {carta[0]} {carta[1]}",
                "cartas_restantes": len(mano_actual) - 1
            })

            # Actualizar mesa
            self.carta_mesa = carta
            self.mazo_descarte.append(carta)
            mano_actual.pop(indice)
            
            # Verificar victoria
            if len(mano_actual) == 0:
                self.game_over(nombre_jug)
                return

            # Aplicar efectos especiales
            siguiente_turno = 1 - self.turno_actual
            mano_siguiente = self.mano_j2 if siguiente_turno == 1 else self.mano_j1
            nombre_siguiente = self.j2_nombre if siguiente_turno == 1 else self.j1_nombre
            
            efecto_aplicado = False
            
            if carta[0] == "+2":
                nuevas, self.mazo_robo, self.mazo_descarte = repartir_cartas(2, self.mazo_robo, self.mazo_descarte)
                mano_siguiente.extend(nuevas)
                messagebox.showinfo("Efecto +2", f"¡{nombre_siguiente} come 2 cartas y pierde turno!")
                efecto_aplicado = True
                
            elif carta[0] == "+4":
                nuevas, self.mazo_robo, self.mazo_descarte = repartir_cartas(4, self.mazo_robo, self.mazo_descarte)
                mano_siguiente.extend(nuevas)
                messagebox.showinfo("Efecto +4", f"¡{nombre_siguiente} come 4 cartas y pierde turno!")
                efecto_aplicado = True
                
            elif carta[0] == "BLOQUEO" or carta[0] == "REVERSA":
                # En 1v1, reversa actúa como bloqueo
                messagebox.showinfo("Bloqueo", f"¡{nombre_siguiente} pierde el turno!")
                efecto_aplicado = True

            self.ha_tomado_carta = False # Reset para el prox turno
            
            if efecto_aplicado:
                # El turno NO cambia (vuelve al mismo jugador)
                # Pero debemos refrescar la pantalla
                self.actualizar_pantalla()
            else:
                # Cambio de turno normal
                self.cambiar_turno()

        else:
            messagebox.showerror("Jugada Inválida", "Esa carta no coincide con la mesa.")

    def finalizar_turno_jugador(self):
        self.ha_tomado_carta = False
        self.cambiar_turno()

    def cambiar_turno(self):
        self.turno_actual = 1 - self.turno_actual
        
        if self.modo == "1V1":
            nombre_sig = self.j1_nombre if self.turno_actual == 0 else self.j2_nombre
            messagebox.showinfo("Cambio de Turno", f"Es el turno de {nombre_sig}.\n(Cierra los ojos el otro jugador)")
            self.actualizar_pantalla()
        
        elif self.modo == "VS_PC":
            self.actualizar_pantalla()
            if self.turno_actual == 1:
                # Turno PC con un pequeño delay para que se note
                self.ventana.after(1000, self.rutina_pc)

    def rutina_pc(self):
        # Lógica simple de la PC
        posibles = []
        for i, c in enumerate(self.mano_j2):
            if es_jugada_valida(self.carta_mesa, c):
                posibles.append(i)
        
        if posibles:
            # Jugar carta
            idx = posibles[0] # Juega la primera que encuentra
            carta = self.mano_j2[idx]
            
            if carta[1] == "NEGRO":
                nuevo_color = elegir_color_pc(self.mano_j2)
                carta = [carta[0], nuevo_color]
            
            self.carta_mesa = carta
            self.mazo_descarte.append(carta)
            self.mano_j2.pop(idx)
            
            # Log PC
            clave_pc = f"PC_VS_{self.j1_nombre}"
            self.historial[clave_pc].append({
                "id_partida": self.id_partida,
                "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "mensaje": f"PC jugó {carta[0]} {carta[1]}",
                "cartas_restantes": len(self.mano_j2)
            })
            
            self.log_evento(f"PC jugó {carta[0]} {carta[1]}")

            if len(self.mano_j2) == 0:
                self.game_over("PC")
                return

            # Efectos PC
            salta_turno_humano = False
            if carta[0] == "+2":
                nuevas, self.mazo_robo, self.mazo_descarte = repartir_cartas(2, self.mazo_robo, self.mazo_descarte)
                self.mano_j1.extend(nuevas)
                messagebox.showwarning("PC Ataca", "¡La PC tiró +2! Comes 2 cartas y pierdes turno.")
                salta_turno_humano = True
            elif carta[0] == "+4":
                nuevas, self.mazo_robo, self.mazo_descarte = repartir_cartas(4, self.mazo_robo, self.mazo_descarte)
                self.mano_j1.extend(nuevas)
                messagebox.showwarning("PC Ataca", "¡La PC tiró +4! Comes 4 cartas y pierdes turno.")
                salta_turno_humano = True
            elif carta[0] in ["BLOQUEO", "REVERSA"]:
                messagebox.showwarning("PC Ataca", "¡La PC te bloqueó! Pierdes turno.")
                salta_turno_humano = True
            
            if salta_turno_humano:
                # PC vuelve a jugar
                self.actualizar_pantalla()
                self.ventana.after(1000, self.rutina_pc)
            else:
                self.turno_actual = 0
                self.actualizar_pantalla()

        else:
            # Robar carta
            nuevas, self.mazo_robo, self.mazo_descarte = repartir_cartas(1, self.mazo_robo, self.mazo_descarte)
            robada = nuevas[0]
            self.mano_j2.append(robada)
            self.log_evento("PC robó una carta")
            
            # Intentar jugar la robada
            if es_jugada_valida(self.carta_mesa, robada):
                # La juega inmediatamente (recursividad simple)
                # NOTA: En una IA más compleja, esto debería ser más limpio, pero aquí funciona
                self.actualizar_pantalla()
                self.ventana.after(500, self.rutina_pc)
            else:
                self.turno_actual = 0
                self.actualizar_pantalla()

    def game_over(self, ganador):
        messagebox.showinfo("Fin del Juego", f"¡El ganador es {ganador.upper()}!")
        
        # Calcular puntos
        puntos_ganador = 0
        mano_perdedora = self.mano_j2 if ganador == self.j1_nombre else self.mano_j1
        
        # Sistema simple de puntos: 10 por carta restante del oponente
        puntos_ganador = len(mano_perdedora) * 10
        
        actualizar_puntuacion(ganador, puntos_ganador)
        if ganador != "PC": # Restar puntos al perdedor si es humano
            perdedor = self.j2_nombre if ganador == self.j1_nombre else self.j1_nombre
            if perdedor != "PC":
                actualizar_puntuacion(perdedor, -5)
        
        guardar_historial(self.historial)
        self.ventana.destroy()

# --- Interfaz del Menú Principal ---

def mostrar_reglas():
    v = tk.Toplevel()
    v.title("Reglas")
    v.geometry("600x400")
    txt = tk.Text(v, font=("Arial", 12))
    txt.pack(fill="both", expand=True)
    try:
        with open(os.path.join(os.path.dirname(__file__), "FIles", "reglas.txt"), "r", encoding="utf-8") as f:
            txt.insert("1.0", f.read())
    except:
        txt.insert("1.0", "No se encontró el archivo de reglas.\nBásicamente: Tira una carta del mismo color o número. Usa cartas negras para cambiar color.")
    txt.config(state="disabled")

def mostrar_ranking():
    v = tk.Toplevel()
    v.title("Ranking")
    v.geometry("400x500")
    v.configure(bg=AMARILLO_FONDO)
    
    tk.Label(v, text="🏆 Ranking Global", font=("Arial", 18, "bold"), bg=AMARILLO_FONDO).pack(pady=10)
    
    ranking_ord = sorted(jugadores_dic.items(), key=lambda x: x[1], reverse=True)
    
    for i, (nom, ptos) in enumerate(ranking_ord):
        tk.Label(v, text=f"{i+1}. {nom.upper()} - {ptos} pts", font=("Arial", 12), bg=AMARILLO_FONDO).pack()

def mostrar_historial_menu(nombre):
    v = tk.Toplevel()
    v.title("Historial")
    v.geometry("600x500")
    txt = tk.Text(v, font=("Consolas", 10))
    txt.pack(fill="both", expand=True)
    
    historial = cargar_historial()
    logs = []
    
    # Buscar logs del jugador y de la PC contra él
    if nombre in historial:
        for jugada in historial[nombre]:
            if isinstance(jugada, dict): jugada['autor'] = nombre
            logs.append(jugada)
            
    clave_pc = f"PC_VS_{nombre}"
    if clave_pc in historial:
        for jugada in historial[clave_pc]:
            if isinstance(jugada, dict): jugada['autor'] = "PC"
            logs.append(jugada)
            
    # Ordenar
    logs.sort(key=lambda x: x.get('fecha_hora', ''))
    
    last_id = ""
    for log in logs:
        if 'id_partida' in log and log['id_partida'] != last_id:
            txt.insert("end", "\n" + "-"*40 + "\n")
            last_id = log['id_partida']
        
        if 'mensaje' in log:
            txt.insert("end", f"{log.get('fecha_hora','')} | {log['mensaje']}\n")
            
    txt.config(state="disabled")

def iniciar_app():
    global nombre_global, ventana_principal
    
    # 1. Ventana Login simple
    root_login = tk.Tk()
    root_login.withdraw() # Ocultar raíz
    nombre_global = simpledialog.askstring("Login", "Ingrese su nombre de usuario:")
    
    if not nombre_global:
        sys.exit()
    
    nombre_global = nombre_global.strip().lower()
    root_login.destroy()

    # 2. Ventana Principal
    ventana_principal = tk.Tk()
    ventana_principal.title("UNO - Menú Principal")
    ventana_principal.geometry("500x600")
    ventana_principal.configure(bg=AMARILLO_FONDO)
    
    # Cargar Logo si existe
    try:
        img = Image.open(os.path.join(os.path.dirname(__file__), "FIles", "Imgs", "logo.png"))
        img = img.resize((100, 100))
        logo = ImageTk.PhotoImage(img)
        lbl_logo = tk.Label(ventana_principal, image=logo, bg=AMARILLO_FONDO)
        lbl_logo.image = logo
        lbl_logo.pack(pady=10)
        ventana_principal.iconphoto(True, logo)
    except:
        pass

    tk.Label(ventana_principal, text=f"Bienvenido, {nombre_global.upper()}", 
             font=("Arial", 20, "bold"), bg=AMARILLO_FONDO, fg=ROJO_UNO).pack(pady=10)

    # Botones
    estilo_btn = {"font": ("Arial", 12, "bold"), "width": 25, "height": 2, "bd": 3, "relief": "raised"}
    
    def btn_vs_pc():
        ventana_principal.withdraw()
        PartidaGUI(ventana_principal, nombre_global, "VS_PC")
        
    def btn_1v1():
        oponente = simpledialog.askstring("1v1", "Nombre del Oponente:")
        if oponente and oponente.strip().lower() != nombre_global:
            ventana_principal.withdraw()
            PartidaGUI(ventana_principal, nombre_global, "1V1", oponente.strip().lower())
        else:
            messagebox.showerror("Error", "Nombre inválido o igual al jugador 1")

    tk.Button(ventana_principal, text="🎮 Jugar vs PC", bg=VERDE_BTN, fg="black", command=btn_vs_pc, **estilo_btn).pack(pady=5)
    tk.Button(ventana_principal, text="👥 Jugar 1 vs 1", bg=VERDE_BTN, fg="black", command=btn_1v1, **estilo_btn).pack(pady=5)
    tk.Button(ventana_principal, text="📜 Reglas", bg=AZUL_BTN, fg="white", command=mostrar_reglas, **estilo_btn).pack(pady=5)
    tk.Button(ventana_principal, text="🏆 Ranking", bg=AZUL_BTN, fg="white", command=mostrar_ranking, **estilo_btn).pack(pady=5)
    tk.Button(ventana_principal, text="🕒 Historial", bg=AZUL_BTN, fg="white", command=lambda: mostrar_historial_menu(nombre_global), **estilo_btn).pack(pady=5)
    tk.Button(ventana_principal, text="❌ Salir", bg=ROJO_BTN, fg="white", command=ventana_principal.quit, **estilo_btn).pack(pady=20)

    ventana_principal.mainloop()

if __name__ == "__main__":
    iniciar_app()