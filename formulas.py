import math
import numpy as np

# Función para calcular la posición vertical del misil
def pos_vertical(h_0, v_0, t):
    return h_0 + v_0 * t - 4.9 * (t ** 2)

# Función para calcular el tiempo de caída libre
def tiempo_caida_libre(v_0, h_0):
    t1 = (-v_0 + math.sqrt(v_0 ** 2 - 4 * (-4.9) * h_0)) / (-9.8)
    t2 = (-v_0 - math.sqrt(v_0 ** 2 - 4 * (-4.9) * h_0)) / (-9.8)
    return max(t1, t2)

# Función para simular el tiro parabólico
def tiro_parabolico(angulo_deg, velocidad, g=9.81, dt=0.01):
    angulo_rad = np.radians(angulo_deg)
    v0x = velocidad * np.cos(angulo_rad)
    v0y = velocidad * np.sin(angulo_rad)

    x_list, y_list = [], []
    x, y = 0.0, 0.0
    vx, vy = v0x, v0y

    while y >= 0.0:
        x_list.append(x)
        y_list.append(y)
        x += vx * dt
        y += vy * dt
        vy -= g * dt

    return x_list, y_list

# Función para verificar si un proyectil intercepta al misil
def verificar_intercepcion(misil_x, misil_y, parab_x, parab_y, tolerancia=1.0):
    for i in range(len(parab_x)):
        for j in range(len(misil_x)):
            distancia = math.sqrt((parab_x[i] - misil_x[j]) ** 2 + (parab_y[i] - misil_y[j]) ** 2)
            if distancia <= tolerancia:
                return True, parab_x[i], parab_y[i]
    return False, None, None