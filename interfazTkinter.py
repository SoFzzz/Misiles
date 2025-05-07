import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from formulas import calcular_intercepcion, simulacion_intercepcion_completa


class InterfazSimulacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Intercepción de Misiles")
        
        # Variables para los parámetros
        self.altura_misil = tk.DoubleVar(value="")  # Altura inicial del misil enemigo (vacío)
        self.distancia_ciudad = tk.DoubleVar(value="")  # Distancia del punto azul al cuadrado verde (vacío)
        self.simulacion_pausada = False
        self.animacion = None
        
        # Crear campos para ingresar parámetros
        tk.Label(root, text="Altura inicial del misil enemigo (m):").pack(pady=5)
        self.altura_entry = tk.Entry(root, textvariable=self.altura_misil)
        self.altura_entry.pack(pady=5)
        
        tk.Label(root, text="Distancia del antimisil a la ciudad (m):").pack(pady=5)
        self.distancia_entry = tk.Entry(root, textvariable=self.distancia_ciudad)
        self.distancia_entry.pack(pady=5)
        
        # Botones de control
        self.start_button = tk.Button(root, text="Iniciar Simulación", command=self.iniciar_simulacion)
        self.start_button.pack(pady=10)
        
        self.pause_button = tk.Button(root, text="Pausar Simulación", command=self.pausar_simulacion, state=tk.DISABLED)
        self.pause_button.pack(pady=10)
        
        self.reset_button = tk.Button(root, text="Nueva Simulación", command=self.reiniciar_simulacion, state=tk.DISABLED)
        self.reset_button.pack(pady=10)
        
        # Espacio para mostrar resultados de cálculos
        self.resultados_label = tk.Label(root, text="Resultados de los cálculos:", font=("Arial", 12, "bold"))
        self.resultados_label.pack(pady=10)
        self.resultados_text = tk.Text(root, height=5, width=60, state=tk.DISABLED, font=("Arial", 11, "bold"))
        self.resultados_text.pack(pady=10)
        
        # Espacio para el gráfico
        self.figure, self.ax = plt.subplots(figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def mostrar_resultados(self, resultados):
        """Muestra los resultados de los cálculos en el cuadro de texto."""
        self.resultados_text.config(state=tk.NORMAL)
        self.resultados_text.delete(1.0, tk.END)  # Limpiar texto anterior
        self.resultados_text.insert(tk.END, f"Ángulo de lanzamiento: {resultados['angulo_interceptor']:.2f}°\n")
        self.resultados_text.insert(tk.END, f"Velocidad inicial del antimisil: {resultados['v0_interceptor']:.2f} m/s\n")
        self.resultados_text.insert(tk.END, f"Tiempo de intercepción: {resultados['t_caida']:.2f} s\n")
        self.resultados_text.insert(
            tk.END,
            f"Coordenadas de intercepción: ({resultados['x_intercept']:.2f}, {resultados['y_intercept']:.2f}) m\n"
        )
        self.resultados_text.config(state=tk.DISABLED)  # Desactivar edición
    
    def iniciar_simulacion(self):
        """Inicia la simulación y grafica los resultados."""
        try:
            h_misil = self.altura_misil.get()
            d_ciudad = self.distancia_ciudad.get()
            g = 9.81
            y_min_intercept = 5000
            dt = 0.01

            # Validar entradas
            if h_misil <= 0 or d_ciudad <= 0:
                raise ValueError("La altura y la distancia deben ser números positivos mayores a 0.")

            # Calcular los parámetros óptimos igual que en mine.py
            v0, theta_deg, t_intercept, coords_intercept = calcular_intercepcion(
                h_misil, d_ciudad, y_min_intercept, g
            )

            # Simular y graficar
            resultado, (trayectoria_x_antimisil, trayectoria_y_antimisil), (trayectoria_x_enemigo, trayectoria_y_enemigo) = simulacion_intercepcion_completa(
                h_enemigo=h_misil,
                d_enemigo=d_ciudad,
                v0_interceptor=v0,
                angulo_interceptor=theta_deg,
                g=g,
                dt=dt
            )

            # Mostrar resultados de cálculos
            self.mostrar_resultados({
                "angulo_interceptor": theta_deg,
                "v0_interceptor": v0,
                "t_caida": t_intercept,
                "x_intercept": coords_intercept[0],
                "y_intercept": coords_intercept[1]
            })

            self.ax.clear()

            # Graficar las trayectorias
            self.ax.plot(trayectoria_x_enemigo, trayectoria_y_enemigo, 'r--', label='Misil enemigo')
            self.ax.plot(trayectoria_x_antimisil, trayectoria_y_antimisil, 'b-', label='Antimisil')

            # Agregar puntos móviles
            self.punto_rojo, = self.ax.plot([], [], 'ro', label='Misil enemigo (punto móvil)')
            self.punto_azul, = self.ax.plot([], [], 'o', color='#00FFFF', label='Antimisil (punto móvil)')
            self.intercept_point, = self.ax.plot([], [], 'go', label='Punto de intersección', zorder=5)

            # Etiquetas y leyenda
            self.ax.set_title("Simulación de Intercepción de Misiles")
            self.ax.set_xlabel("Distancia horizontal (m)")
            self.ax.set_ylabel("Altura (m)")
            self.ax.axhline(0, color='black', linewidth=0.8, linestyle='--')  # Línea del suelo
            self.ax.grid(True, linestyle='--', alpha=0.7)
            self.ax.legend()

            self.canvas.draw()

            
            
            self.animacion_terminada = False

            # Animar los puntos
            def actualizar(frame):
                if self.animacion_terminada:
                    return  # No hacer nada si la animación ya se detuvo

                epsilon = 0.02  # Margen de tolerancia para el tiempo
                current_time = frame * dt

                # Actualizar posición del misil enemigo
                if frame < len(trayectoria_x_enemigo):
                    self.punto_rojo.set_data([trayectoria_x_enemigo[frame]], [trayectoria_y_enemigo[frame]])

                # Actualizar posición del antimisil
                if frame < len(trayectoria_x_antimisil):
                    self.punto_azul.set_data([trayectoria_x_antimisil[frame]], [trayectoria_y_antimisil[frame]])
                
                # Mostrar el punto de intersección solo cuando ambos llegan
                if resultado and abs(current_time - t_intercept) < epsilon:
                    x_intercept, y_intercept = coords_intercept
                    self.intercept_point.set_data([x_intercept], [y_intercept])

                    # Detener la animación automáticamente
                    if self.animacion and not self.animacion_terminada:
                        self.animacion.event_source.stop()
                        self.animacion_terminada = True  # Marcar la animación como terminada
                        self.pause_button.config(state=tk.DISABLED)
                        self.start_button.config(state=tk.NORMAL)  # Habilitar el botón de inicio
                return self.punto_rojo, self.punto_azul, self.intercept_point

            total_frames = int(t_intercept / dt) + 1
            self.animacion = FuncAnimation(self.figure, actualizar, frames=total_frames, interval=20, blit=True)

        except ValueError as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")
    
    def pausar_simulacion(self):
        """Pausa la simulación."""
        if not self.simulacion_pausada:
            self.simulacion_pausada = True
            self.animacion.event_source.stop()
            self.pause_button.config(text="Reanudar Simulación")
        else:
            self.simulacion_pausada = False
            self.animacion.event_source.start()
            self.pause_button.config(text="Pausar Simulación")
    
    def reiniciar_simulacion(self):
        """Reinicia la simulación."""
        self.altura_misil.set(10000)
        self.distancia_ciudad.set(50000)
        self.ax.clear()
        self.ax.set_title("Simulación de Intercepción: Antimisil vs Misil enemigo")
        self.ax.set_xlabel("Distancia horizontal (m)")
        self.ax.set_ylabel("Altura (m)")
        self.canvas.draw()
        self.resultados_text.config(state=tk.NORMAL)
        self.resultados_text.delete(1.0, tk.END)
        self.resultados_text.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.DISABLED, text="Pausar Simulación")
        self.reset_button.config(state=tk.DISABLED)
        if self.animacion:
            self.animacion.event_source.stop()
            self.animacion = None


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazSimulacion(root)
    root.mainloop()