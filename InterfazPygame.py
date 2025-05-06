import pygame
import sys
from sys import exit

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Simulacion de Tiro Parabolico')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/PixeloidSans-Bold.ttf', 50)

sky_surface = pygame.image.load("graphics/Sky.png")
sky_surface = pygame.transform.scale(sky_surface, (800, 500))

spritesheet = pygame.image.load("graphics/Ground.png").convert_alpha()
''# Función para extraer un sprite de la spritesheet #''
def get_sprite(sheet, x, y, width, height):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    return sprite

# Extrae algunos sprites (ajusta las coordenadas y tamaños según tu imagen)
sprite_4 = get_sprite(spritesheet, 16 * 17, 16 * 0, 16, 16)
sprite_4_escalado = pygame.transform.scale(sprite_4, (800, 100))
sprite_5 = get_sprite(spritesheet, 16 * 6, 16 * 10, 16, 16)
sprite_5_escalado = pygame.transform.scale(sprite_4, (800, 100))

text_surface = test_font.render('Simulador Antimisil', False, 'White') 


while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_surface,(0,0))

    for i in range(0, 800, 16):  # Repite horizontalmente
        screen.blit(sprite_4, (i, 500))
    for i in range(0, 800, 16):  # Repite horizontalmente
        screen.blit(sprite_4, (i, 517))
    for i in range(0, 800, 16):  # Repite horizontalmente
        screen.blit(sprite_5, (i, 534))
    for i in range(0, 800, 16):  # Repite horizontalmente
        screen.blit(sprite_5, (i, 551))
    for i in range(0, 800, 16):  # Repite horizontalmente
        screen.blit(sprite_5, (i, 568))
    for i in range(0, 800, 16):  # Repite horizontalmente
        screen.blit(sprite_5, (i, 585))

    screen.blit(text_surface,(80,90))
    
    pygame.display.update()
    clock.tick(30)