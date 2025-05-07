import math
import numpy as np

# Función para calcular la posición vertical del misil enemigo
def altura_misil_enemigo(t, h_0, g=9.81):
    """
    Calcula la altura del misil enemigo en caída libre en un tiempo t.
    Si el misil ya tocó el suelo, retorna 0.
    """
    if t < 0:
        raise ValueError("El tiempo no puede ser negativo.")
    y = h_0 - 0.5 * g * t**2
    return max(0, y)  # La altura no puede ser menor que 0

# Función para calcular el tiempo de caída libre del misil enemigo
def tiempo_caida_libre(h_0, g=9.81):
    """
    Calcula el tiempo que tarda un objeto en caer desde una altura h sin velocidad inicial.
    """
    if h_0 <= 0:
        raise ValueError("La altura debe ser mayor que 0.")
    return math.sqrt(2 * h_0 / g)

# Función para calcular los parámetros de intercepción del antimisil
def calcular_intercepcion(h_0, d, y_intercept=5000, g=9.81):
    """
    Ajusta los cálculos para interceptar al misil enemigo a una altura y_intercept >= 5000 m.
    Devuelve los parámetros de lanzamiento del antimisil ajustados.
    """
    if h_0 <= 0 or d <= 0 or y_intercept <= 0 or y_intercept >= h_0:
        raise ValueError("Los parámetros deben ser mayores que 0 y y_intercept debe ser menor que h_0.")

    # Tiempo de caída ajustado basado en la altura deseada de intercepción
    t_intercept = math.sqrt(2 * (h_0 - y_intercept) / g)

    # Componentes de velocidad del antimisil
    v0x = d / t_intercept
    v0y = (y_intercept + 0.5 * g * t_intercept**2) / t_intercept

    # Velocidad inicial total y ángulo de lanzamiento
    v0 = math.sqrt(v0x**2 + v0y**2)
    theta_rad = math.atan2(v0y, v0x)
    theta_deg = math.degrees(theta_rad)

    return v0, theta_deg, t_intercept, (d, y_intercept)

# Función para calcular el momento óptimo de disparo y simular la trayectoria
def calcular_disparo_y_trayectoria(h_0, d, g=9.81, dt=0.01):
    """
    Calcula el momento óptimo para disparar el antimisil, simula su trayectoria parabólica,
    y devuelve tanto los parámetros de disparo como las trayectorias.
    """
    # Calcular tiempo de caída del misil enemigo
    t_enemigo = tiempo_caida_libre(h_0, g)

    # Calcular componentes de velocidad inicial del antimisil
    v0x = d / t_enemigo
    v0y = h_0 / t_enemigo
    v0 = math.sqrt(v0x**2 + v0y**2)
    theta_rad = math.atan2(v0y, v0x)
    theta_deg = math.degrees(theta_rad)

    # Simular la trayectoria parabólica del antimisil
    x, y = 0.0, 0.0
    vx, vy = v0 * math.cos(theta_rad), v0 * math.sin(theta_rad)
    x_list, y_list = [], []

    while y >= 0.0:
        x_list.append(x)
        y_list.append(y)
        x += vx * dt
        y += vy * dt
        vy -= g * dt

    return {
        "v0": v0,
        "theta_deg": theta_deg,
        "t_disparo": 0,
        "trayectoria_x": x_list,
        "trayectoria_y": y_list,
        "t_enemigo": t_enemigo
    }



# Función principal para simular la intercepción completa
def simulacion_intercepcion_completa(h_enemigo, d_enemigo, v0_interceptor, angulo_interceptor, g=9.81, dt=0.001, tolerancia=5.0):
    """
    Simula la intercepción de un misil enemigo por un antimisil, calcula las trayectorias,
    y verifica si se logra la intercepción.
    """
     # Validación de entradas
    if h_enemigo <= 0 or d_enemigo <= 0 or v0_interceptor <= 0 or angulo_interceptor < 0 or angulo_interceptor > 90:
        raise ValueError("Los parámetros deben ser positivos y el ángulo debe estar entre 0 y 90 grados.")

    # Paso 1: Calcular la trayectoria del misil enemigo
    t_caida = tiempo_caida_libre(h_enemigo, g)  # Tiempo total de caída del misil enemigo
    tiempos = np.arange(0, t_caida + dt, dt)  # Vector de tiempos
    misil_x = [d_enemigo] * len(tiempos)  # El misil enemigo se mueve solo en la dirección vertical
    misil_y = [altura_misil_enemigo(t, h_enemigo, g) for t in tiempos]  # Altura del misil enemigo en cada instante

    # Paso 2: Calcular la trayectoria del antimisil
    angle_rad = math.radians(angulo_interceptor)  # Convertir ángulo a radianes
    v0x = v0_interceptor * math.cos(angle_rad)  # Componente horizontal de la velocidad inicial
    v0y = v0_interceptor * math.sin(angle_rad)  # Componente vertical de la velocidad inicial

    x, y = 0.0, 0.0  # Posición inicial del antimisil
    vx, vy = v0x, v0y  # Velocidades iniciales
    parab_x, parab_y = [], []  # Listas para almacenar la trayectoria del antimisil

    while y >= 0.0:  # Simular hasta que el antimisil toque el suelo
        parab_x.append(x)
        parab_y.append(y)
        x += vx * dt
        y += vy * dt
        vy -= g * dt  # Actualizar la velocidad vertical debido a la gravedad

    # Paso 3: Verificar intercepción
    n = min(len(misil_x), len(parab_x))  # Asegurar que las listas tengan la misma longitud
    for i in range(n):
        distancia = math.sqrt((parab_x[i] - misil_x[i])**2 + (parab_y[i] - misil_y[i])**2)
        if distancia <= tolerancia:
            print(f"Intercepción detectada en el índice {i}: (x = {parab_x[i]:.2f}, y = {parab_y[i]:.2f})")
            return True, (parab_x, parab_y), (misil_x, misil_y)

    # Mensaje de intercepción fallida
    print("Intercepción fallida. El antimisil no alcanzó al objetivo.")
    return False, (parab_x, parab_y), (misil_x, misil_y)