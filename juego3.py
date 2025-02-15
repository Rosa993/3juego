import tkinter as tk
import random
import math
import time
import pygame

# Inicializar pygame para la música
pygame.mixer.init()

# Variables globales para la puntuación, nivel y la operación actual
puntuacion = 0
nivel = 1
operacion_actual = None  # Para almacenar la operación actual en nivel 2

# Función para generar la operación aleatoria
def generar_operacion(dificultad):
    operaciones = ['+', '-', '*', '/']
    
    # Aumentamos la dificultad con exponentes y raíces
    if dificultad > 1:
        operaciones.append('**')  # Exponentes
    if dificultad > 2:
        operaciones.append('√')  # Raíces
    
    # Seleccionamos dos números aleatorios (más grandes para mayor dificultad)
    num1 = random.randint(1, 10 * dificultad)  # Más grande según la dificultad
    num2 = random.randint(1, 10 * dificultad)
    
    # Seleccionamos una operación aleatoria
    operacion = random.choice(operaciones)
    
    # Calculamos el resultado
    if operacion == '+':
        resultado = num1 + num2
    elif operacion == '-':
        resultado = num1 - num2
    elif operacion == '*':
        resultado = num1 * num2
    elif operacion == '/':
        if num2 == 0:  # Para evitar división por cero
            num2 = 1
        resultado = round(num1 / num2, 2)
    elif operacion == '**':
        resultado = num1 ** random.randint(1, 3)  # Potencias entre 1 y 3
    elif operacion == '√':
        num1 = random.randint(1, 100)  # Número para raíz cuadrada
        resultado = round(math.sqrt(num1), 2)  # Raíz cuadrada
    
    return num1, num2, operacion, resultado

# Función para mostrar una pista
def generar_pista(operacion):
    pistas = {
        '+': "Pista: Es una operación de adición.",
        '-': "Pista: Es una operación de sustracción.",
        '*': "Pista: Es una operación de multiplicación.",
        '/': "Pista: Es una operación de división.",
        '**': "Pista: Es una operación de potenciación.",
        '√': "Pista: Es una operación de raíz cuadrada."
    }
    return pistas.get(operacion, "Pista: ¡Adivina la operación!")

# Función para verificar la respuesta
def verificar_respuesta(opcion, respuesta_correcta):
    global puntuacion, nivel
    
    if opcion == respuesta_correcta:
        puntuacion += 1  # Aumentar la puntuación al acertar
        resultado_label.config(text=f"¡Correcto! 🎉 Puntuación: {puntuacion}", fg="green")
    else:
        resultado_label.config(text=f"Incorrecto. La respuesta correcta era: {respuesta_correcta}. Puntuación: {puntuacion}", fg="red")
    
    # Aumentar el nivel después de cada respuesta correcta
    if puntuacion % 5 == 0:  # Aumentar nivel cada 5 puntos
        nivel += 1
        transition_to_new_level()
    
    # Actualizar el nivel y la puntuación en la interfaz
    nivel_label.config(text=f"Nivel: {nivel}")
    puntuacion_label.config(text=f"Puntuación: {puntuacion}")  # Actualizamos la etiqueta de puntuación
    
    # Generar una nueva operación según el nivel
    if nivel == 1:
        nueva_operacion_nivel_1()
    else:
        nueva_operacion_nivel_2()

# Función para realizar la transición de nivel
def transition_to_new_level():
    result_text = f"¡Nivel {nivel} alcanzado! 🎉"
    resultado_label.config(text=result_text, fg="blue")
    time.sleep(1)  # Hacemos una pausa antes de cambiar la operación
    nueva_operacion_nivel_1() if nivel == 1 else nueva_operacion_nivel_2()

# Función para mostrar una nueva operación en **Nivel 1** (resultado)
def nueva_operacion_nivel_1():
    num1, num2, operacion, resultado = generar_operacion(nivel)
    
    # Generar las opciones para adivinar la operación
    opciones = [operacion]
    while len(opciones) < 4:
        op = random.choice(['+', '-', '*', '/', '**', '√'])
        if op != operacion:
            opciones.append(op)
    
    random.shuffle(opciones)  # Mezclamos las opciones
    
    # Generar la pista para la operación
    pista = generar_pista(operacion)
    
    # Actualizar la etiqueta con el resultado mostrado
    resultado_label.config(text=f"Resultado: {resultado}")
    pista_label.config(text="")  # Limpiar la pista inicialmente
    
    # Asignar las opciones a los botones
    for i, boton in enumerate(opciones_botones):
        boton.config(text=f"{opciones[i]}", command=lambda op=opciones[i]: verificar_respuesta(op, operacion))

    # Asignar la pista solo cuando se presione el botón "Mostrar Pista"
    mostrar_pista_button.config(command=lambda: pista_label.config(text=pista))

# Función para mostrar una nueva operación en **Nivel 2** (operación)
def nueva_operacion_nivel_2():
    global operacion_actual
    num1, num2, operacion, resultado = generar_operacion(nivel)
    operacion_actual = f"{num1} {operacion} {num2}"
    
    # Generar las opciones para adivinar el resultado
    opciones = [resultado]
    while len(opciones) < 4:
        resultado_incorrecto = round(random.uniform(1, 100), 2)
        if resultado_incorrecto != resultado:
            opciones.append(resultado_incorrecto)
    
    random.shuffle(opciones)  # Mezclamos las opciones
    
    # Mostrar la operación que el jugador debe resolver
    resultado_label.config(text=f"Operación: {operacion_actual}")
    
    # Asignar las opciones a los botones
    for i, boton in enumerate(opciones_botones):
        boton.config(text=f"{opciones[i]}", command=lambda op=opciones[i]: verificar_respuesta(op, resultado))

    # Limpiar la pista cuando se cambie de nivel
    pista_label.config(text="")

# Función para reproducir música de fondo
def reproducir_musica():
    pygame.mixer.music.load("me_ss.musi.mp3")  # Cargar la música en formato mp3
    pygame.mixer.music.play(loops=-1, start=0.0)  # Reproducir música en bucle

# Función para mostrar la portada del juego
def mostrar_portada():
    portada = tk.Toplevel(root)  # Crear una nueva ventana para la portada
    portada.title("Portada - Adivina la Operación")
    portada.configure(bg="#D8A7D1")

    # Etiqueta de bienvenida
    bienvenida_label = tk.Label(portada, text="¡Bienvenido al Juego!", font=("Helvetica", 24, "bold"), bg="#D8A7D1", fg="black")
    bienvenida_label.pack(pady=30)

    # Botón "Siguiente" que abre la pantalla principal
    siguiente_button = tk.Button(portada, text="Siguiente", font=("Helvetica", 18), bg="#3D85C6", fg="white", relief="raised", command=lambda: iniciar_juego(portada))
    siguiente_button.pack(pady=20)

# Función para iniciar el juego
def iniciar_juego(portada):
    portada.destroy()  # Cerrar la ventana de la portada
    # Crear la interfaz principal
    global root, resultado_label, nivel_label, puntuacion_label, opciones_botones, pista_label, mostrar_pista_button
    
    root = tk.Tk()
    root.title("Juego: Adivina la Operación")
    root.configure(bg="#D8A7D1")  # Fondo lila suave

    # Etiqueta para mostrar el resultado
    resultado_label = tk.Label(root, text="¿Cuál es la operación?", font=("Helvetica", 18, "bold"), bg="#D8A7D1", fg="black")
    resultado_label.pack(pady=20)

    # Etiqueta para mostrar el nivel
    nivel_label = tk.Label(root, text=f"Nivel: {nivel}", font=("Helvetica", 16), bg="#D8A7D1", fg="blue")
    nivel_label.pack()

    # Caja de puntuación
    puntuacion_label = tk.Label(root, text=f"Puntuación: {puntuacion}", font=("Helvetica", 16), bg="#D8A7D1", fg="green")
    puntuacion_label.pack(pady=10)

    # Botones para las opciones
    opciones_botones = []
    for i in range(4):
        boton = tk.Button(root, text="", width=15, height=2, font=("Arial", 14), bg="#FFDD57", fg="black", relief="sunken", bd=3, borderwidth=2)
        boton.pack(pady=5)
        opciones_botones.append(boton)

    # Caja de pistas
    pista_label = tk.Label(root, text="Pista: ", font=("Helvetica", 14), bg="#D8A7D1", fg="purple", relief="solid", width=40, height=3)
    pista_label.pack(pady=20)

    # Botón para mostrar la pista
    mostrar_pista_button = tk.Button(root, text="Mostrar Pista", font=("Helvetica", 14), bg="#3D85C6", fg="white", relief="raised")
    mostrar_pista_button.pack(pady=10)

    # Generar la primera operación en el nivel 1
    nueva_operacion_nivel_1()

    # Reproducir música de fondo
    reproducir_musica()

    # Iniciar el bucle principal de la aplicación
    root.mainloop()

# Crear la ventana de portada al iniciar
root = tk.Tk()
root.withdraw()  # Ocultar la ventana principal

# Mostrar la portada
mostrar_portada()

# Iniciar el bucle principal
root.mainloop()
