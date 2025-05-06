import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from formulas import pos_vertical, tiempo_caida_libre, tiro_parabolico, verificar_intercepcion

# Función para actualizar las trayectorias y graficarlas
def actualizar_grafica():
    try:
        # Obtener valores de los sliders
        h_misil = altura_misil_slider.get()
        distancia_ciudad = distancia_ciudad_slider.get()
        velocidad_proyectil = velocidad_proyectil_slider.get()
        angulo_proyectil = angulo_proyectil_slider.get()

        # Calcular trayectoria del misil enemigo
        tiempo_total_misil = tiempo_caida_libre(0, h_misil)
        tiempos_misil = np.arange(0, tiempo_total_misil, 0.01)
        misil_x = [distancia_ciudad for _ in tiempos_misil]  # Movimiento vertical
        misil_y = [pos_vertical(h_misil, 0, t) for t in tiempos_misil]

        # Calcular trayectoria del misil antiaéreo
        parab_x, parab_y = tiro_parabolico(angulo_proyectil, velocidad_proyectil)

        # Ajustar posición inicial del lanzamisiles
        parab_x = [x for x in parab_x]

        # Verificar intercepción
        intercepcion = verificar_intercepcion(misil_x, misil_y, parab_x, parab_y)

        # Crear figura para graficar
        fig.clear()
        ax = fig.add_subplot(111)
        ax.plot(misil_x, misil_y, label="Trayectoria Misil Enemigo (C)")
        ax.plot(parab_x, parab_y, label="Trayectoria Misil Antiaéreo (A)")
        if intercepcion[0]:
            ax.scatter(intercepcion[1], intercepcion[2], color="red", label="Intercepción Exitosa", zorder=5)
        ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
        ax.set_title("Simulación de Intercepción de Misil")
        ax.set_xlabel("Distancia (m)")
        ax.set_ylabel("Altura (m)")
        ax.legend()
        ax.grid(True)

        # Actualizar Canvas
        canvas.draw()

    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {e}")

# Crear ventana principal
root = tk.Tk()
root.title("Simulación de Intercepción de Misiles")

# Crear sliders y etiquetas
frame_controles = tk.Frame(root)
frame_controles.pack(side=tk.LEFT, padx=10, pady=10)

tk.Label(frame_controles, text="Altura Inicial del Misil (m)").pack()
altura_misil_slider = ttk.Scale(frame_controles, from_=100, to=1000, orient="horizontal")
altura_misil_slider.set(500)
altura_misil_slider.pack()

tk.Label(frame_controles, text="Distancia Ciudad-Misil (m)").pack()
distancia_ciudad_slider = ttk.Scale(frame_controles, from_=100, to=1000, orient="horizontal")
distancia_ciudad_slider.set(500)
distancia_ciudad_slider.pack()

tk.Label(frame_controles, text="Velocidad Inicial del Proyectil (m/s)").pack()
velocidad_proyectil_slider = ttk.Scale(frame_controles, from_=10, to=300, orient="horizontal")
velocidad_proyectil_slider.set(100)
velocidad_proyectil_slider.pack()

tk.Label(frame_controles, text="Ángulo de Lanzamiento del Proyectil (°)").pack()
angulo_proyectil_slider = ttk.Scale(frame_controles, from_=10, to=80, orient="horizontal")
angulo_proyectil_slider.set(45)
angulo_proyectil_slider.pack()

# Botón para actualizar la gráfica
boton_actualizar = tk.Button(frame_controles, text="Actualizar Gráfica", command=actualizar_grafica)
boton_actualizar.pack(pady=10)

# Crear área para la gráfica
frame_grafica = tk.Frame(root)
frame_grafica.pack(side=tk.RIGHT, padx=10, pady=10)

fig = plt.Figure(figsize=(8, 6), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
canvas.get_tk_widget().pack()

# Ejecutar la aplicación
root.mainloop()