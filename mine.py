import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from formulas import (
    altura_misil_enemigo,
    tiempo_caida_libre,
    calcular_intercepcion,
    simulacion_intercepcion_completa
)

def solicitar_parametros():
    """
    Solicita al usuario los parámetros iniciales de la simulación.
    """
    print("\n=== Parámetros de la Simulación ===")
    while True:
        try:
            h_enemigo = float(input("Ingrese la altura inicial del misil enemigo (m) [10000]: ") or "10000")
            if h_enemigo <= 0:
                print("La altura debe ser mayor que 0.")
                continue
                
            d_enemigo = float(input("Ingrese la distancia horizontal al misil enemigo (m) [30000]: ") or "30000")
            if d_enemigo <= 0:
                print("La distancia debe ser mayor que 0.")
                continue
                
            return h_enemigo, d_enemigo
            
        except ValueError:
            print("Por favor, ingrese un número válido.")

try:
    # Solicitar parámetros al usuario
    h_enemigo, d_enemigo = solicitar_parametros()
    
    # Otros parámetros
    g = 9.81  # Gravedad (m/s^2)
    dt = 0.01  # Paso de tiempo para la simulación (s)
    y_min_intercept = 5000  # Altura mínima deseada para la intercepción (m)

    # Calcular los parámetros de intercepción
    v0, theta_deg, t_intercept, coords_intercept = calcular_intercepcion(h_enemigo, d_enemigo, y_min_intercept, g)

    # Imprimir información sobre los parámetros calculados
    print(f"\nParámetros de intercepción calculados:")
    print(f"Velocidad inicial del antimisil: {v0:.2f} m/s")
    print(f"Ángulo de lanzamiento: {theta_deg:.2f}°")
    print(f"Tiempo de intercepción: {t_intercept:.2f} s")
    print(f"Coordenadas de intercepción: ({coords_intercept[0]:.2f}, {coords_intercept[1]:.2f}) m")

    # Simulación completa de intercepción
    resultado, trayectoria_antimisil, trayectoria_misil = simulacion_intercepcion_completa(
        h_enemigo, d_enemigo, v0, theta_deg, g, dt=dt
    )

    # Crear la figura y el eje
    fig, ax = plt.subplots(figsize=(12, 7))
    plt.subplots_adjust(bottom=0.25)  # Ajustar espacio para la barra deslizadora

    ax.set_xlim(0, d_enemigo + 1000)  # Ampliar un poco más allá de la distancia del misil
    ax.set_ylim(0, h_enemigo + 1000)  # Ampliar un poco más allá de la altura inicial

    # Graficar las trayectorias calculadas
    ax.plot(trayectoria_misil[0], trayectoria_misil[1], label="Trayectoria del misil enemigo", color="red", linestyle="--")
    ax.plot(trayectoria_antimisil[0], trayectoria_antimisil[1], label="Trayectoria del antimisil", color="blue")

    # Agregar detalles
    ax.set_title("Simulación de Intercepción de Misiles", fontsize=14, pad=49)
    ax.set_xlabel("Distancia horizontal (m)", fontsize=12)
    ax.set_ylabel("Altura (m)", fontsize=12)
    ax.axhline(y=0, color="black", linewidth=0.8, linestyle="--")  # Línea del suelo
    ax.legend(fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.7)

    # Agregar puntos móviles para el misil enemigo y el antimisil
    misil_point, = ax.plot([], [], 'ro', label="Misil enemigo (punto móvil)")
    antimisil_point, = ax.plot([], [], 'o', color="#00FFFF", label="Antimisil (punto móvil)")  # Punto azul neón
    inicio_misil_point, = ax.plot([d_enemigo], [h_enemigo], 'o', color="#FF6666", markersize=8, label="Inicio del misil enemigo")
    intercept_point, = ax.plot([], [], 'go', label="Punto de intersección", zorder=5)

    # Crear el label para las coordenadas de intersección (inicialmente vacío)
    inter_label = ax.text(0, 0, '', color='green', fontsize=10, fontweight='bold',
                         bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='green', alpha=0.7),
                         visible=False)

    # Crear el label para el mensaje de éxito (inicialmente invisible)
    exito_label = ax.text(0.5, 1.02, '', color='green', fontsize=14, fontweight='bold',
                         ha='center', va='bottom', transform=ax.transAxes, visible=False)

    # Agregar cuadro de texto con los parámetros
    info_text = (
        f"Parámetros de la simulación:\n"
        f"Altura inicial del misil: {h_enemigo:.0f} m\n"
        f"Distancia al misil: {d_enemigo:.0f} m\n"
        f"Velocidad inicial del antimisil: {v0:.2f} m/s\n"
        f"Ángulo de lanzamiento: {theta_deg:.2f}°\n"
        f"Tiempo de intercepción: {t_intercept:.2f} s"
    )
    
    # Crear el cuadro de texto en la esquina superior izquierda, debajo de la leyenda
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.02, 0.90, info_text,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='top',
            horizontalalignment='left',
            bbox=props)

    # Barra deslizadora
    ax_slider = plt.axes([0.2, 0.1, 0.65, 0.03])  # Posición [izquierda, abajo, ancho, alto]
    slider = Slider(ax_slider, 'Tiempo (s)', 0, t_intercept, valinit=0, valstep=dt)

    # Función para actualizar los puntos basado en la barra deslizadora
    def update(val):
        time = slider.val  # Obtener el valor actual de la barra deslizadora

        # Actualizar posición del misil enemigo
        x_misil = [d_enemigo]  # El misil enemigo solo se mueve verticalmente
        y_misil = [altura_misil_enemigo(time, h_enemigo, g)]
        misil_point.set_data(x_misil, y_misil)

        # Actualizar posición del antimisil
        if time <= t_intercept:
            index = int(time / dt)  # Convertir tiempo a índice usando el mismo dt
            if index < len(trayectoria_antimisil[0]):  # Verificar que el índice sea válido
                x_antimisil = [trayectoria_antimisil[0][index]]
                y_antimisil = [trayectoria_antimisil[1][index]]
                antimisil_point.set_data(x_antimisil, y_antimisil)

        # Actualizar punto de intersección y label
        if resultado and time == t_intercept:  # Cuando se alcanza el tiempo de intersección
            x_intercept, y_intercept = coords_intercept
            intercept_point.set_data([x_intercept], [y_intercept])
            # Calcular desplazamiento de 5 cm en unidades del eje x
            ancho_figura_cm = fig.get_size_inches()[0] * 2.54
            rango_x = ax.get_xlim()[1] - ax.get_xlim()[0]
            desplazamiento_x = (5 / ancho_figura_cm) * rango_x  # 5 cm a la izquierda
            # Mostrar el label con las coordenadas
            inter_label.set_text(f"({x_intercept:.2f}, {y_intercept:.2f}) m")
            inter_label.set_position((x_intercept - desplazamiento_x, y_intercept + 200))
            inter_label.set_visible(True)
            # Mostrar mensaje de éxito en la gráfica
            exito_label.set_text("¡Misil interceptado con éxito!")
            exito_label.set_visible(True)
            # Imprimir en consola solo la primera vez
            if not hasattr(update, 'mensaje_mostrado'):
                print("\n¡Misil interceptado con éxito!")
                update.mensaje_mostrado = True
        else:
            intercept_point.set_data([], [])  # Ocultar el punto de intersección
            inter_label.set_visible(False)
            exito_label.set_visible(False)
            if hasattr(update, 'mensaje_mostrado'):
                del update.mensaje_mostrado

        fig.canvas.draw_idle()  # Actualizar la figura

    # Conectar la barra deslizadora con la función de actualización
    slider.on_changed(update)

    # Mostrar la gráfica
    plt.show()

except ValueError as e:
    print(f"Error en los parámetros: {str(e)}")
except Exception as e:
    print(f"Error inesperado: {str(e)}")