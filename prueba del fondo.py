import pygame
from pygame.locals import *

pygame.init()

# Dimensiones de la ventana del juego
WIDTH = 800
HEIGHT = 600

# Crear la ventana del juego
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Cargar la imagen del fondo
background = pygame.image.load("nebula.png").convert()

# Ajustar la imagen del fondo al tamaño de la ventana
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Obtener la altura de la imagen del fondo
background_height = background.get_height()

# Posición inicial del fondo
background_y = 0

# Bucle principal del juego
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Dibujar el fondo en la pantalla
    screen.blit(background, (0, background_y))
    screen.blit(background, (0, background_y - background_height))

    # Mover el fondo en forma vertical
    background_y += 1
    if background_y >= background_height:
        background_y = 0

    pygame.display.update()
    clock.tick(60)

pygame.quit()

