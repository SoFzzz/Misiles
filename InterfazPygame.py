import pygame
import sys
import math
import numpy as np
from formulas import calcular_trayectorias, calcular_intercepcion
from sys import exit

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
ANCHO = 800
ALTO = 600
ESCALA = 50  # Píxeles por unidad de distancia
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Simulador de Intercepción de Misiles')
clock = pygame.time.Clock()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)

# Fuente
try:
    test_font = pygame.font.Font('font/PixeloidSans-Bold.ttf', 30)
except:
    test_font = pygame.font.SysFont('Arial', 30)

# Clase para el misil
class Misil:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radio = 5

    def dibujar(self, superficie):
        pygame.draw.circle(superficie, self.color, (int(self.x), int(self.y)), self.radio)

# Función para convertir coordenadas del mundo real a coordenadas de pantalla
def mundo_a_pantalla(x, y):
    return (int(x * ESCALA + ANCHO/2), int(ALTO - y * ESCALA))

# Función para dibujar la cuadrícula
def dibujar_cuadricula():
    for x in range(0, ANCHO, 50):
        pygame.draw.line(screen, (100, 100, 100), (x, 0), (x, ALTO))
    for y in range(0, ALTO, 50):
        pygame.draw.line(screen, (100, 100, 100), (0, y), (ANCHO, y))

# Parámetros de la simulación
h_misil = 10  # altura inicial del misil enemigo
d_ciudad = 15  # distancia a la ciudad
dt = 0.01  # paso de tiempo

# Calcular trayectorias
tiempos, misil_x, misil_y, parab_x, parab_y = calcular_trayectorias(h_misil, d_ciudad, dt=dt)

# Crear objetos misil
misil_enemigo = Misil(0, 0, ROJO)
misil_interceptor = Misil(0, 0, AZUL)

# Variables para la animación
indice_actual = 0
ejecutando = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ejecutando = not ejecutando
            elif event.key == pygame.K_r:
                indice_actual = 0

    # Limpiar pantalla
    screen.fill(BLANCO)
    
    # Dibujar cuadrícula
    dibujar_cuadricula()

    # Actualizar posición de los misiles si la simulación está en ejecución
    if ejecutando and indice_actual < len(tiempos):
        # Actualizar posición del misil enemigo
        x_enemigo, y_enemigo = mundo_a_pantalla(misil_x[indice_actual], misil_y[indice_actual])
        misil_enemigo.x = x_enemigo
        misil_enemigo.y = y_enemigo

        # Actualizar posición del misil interceptor
        x_interceptor, y_interceptor = mundo_a_pantalla(parab_x[indice_actual], parab_y[indice_actual])
        misil_interceptor.x = x_interceptor
        misil_interceptor.y = y_interceptor

        indice_actual += 1

    # Dibujar trayectorias
    for i in range(indice_actual):
        # Trayectoria del misil enemigo
        x1, y1 = mundo_a_pantalla(misil_x[i], misil_y[i])
        if i > 0:
            x2, y2 = mundo_a_pantalla(misil_x[i-1], misil_y[i-1])
            pygame.draw.line(screen, ROJO, (x1, y1), (x2, y2), 2)

        # Trayectoria del misil interceptor
        x1, y1 = mundo_a_pantalla(parab_x[i], parab_y[i])
        if i > 0:
            x2, y2 = mundo_a_pantalla(parab_x[i-1], parab_y[i-1])
            pygame.draw.line(screen, AZUL, (x1, y1), (x2, y2), 2)

    # Dibujar misiles
    misil_enemigo.dibujar(screen)
    misil_interceptor.dibujar(screen)

    # Dibujar información
    tiempo_texto = test_font.render(f'Tiempo: {tiempos[indice_actual-1]:.2f}s', True, NEGRO)
    screen.blit(tiempo_texto, (10, 10))

    # Instrucciones
    instrucciones = test_font.render('Espacio: Pausar/Reanudar  R: Reiniciar', True, NEGRO)
    screen.blit(instrucciones, (10, ALTO - 40))

    pygame.display.flip()
    clock.tick(60)  # 60 FPS