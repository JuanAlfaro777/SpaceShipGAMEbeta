import random
import pygame
from pygame.locals import *

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Esquiva los meteoritos')
# Dimensiones de la ventana del juego
WIDTH = 800
HEIGHT = 600

# Crear la ventana del juego
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Variables para el movimiento del fondo
background_x = 0


# Colores
WHITE = (255, 255, 255)

# Clase de la nave espacial
class SpaceShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('cohete.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))  # Ajusta el tamaño de la imagen
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.centery = height // 2
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > width:
            self.rect.right = width
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > height:
            self.rect.bottom = height
            # Controlar la velocidad de movimiento del cohete
        spaceship.speed_x = -10 if pygame.key.get_pressed()[K_LEFT] else 10 if pygame.key.get_pressed()[K_RIGHT] else 0
        spaceship.speed_y = -10 if pygame.key.get_pressed()[K_UP] else 10 if pygame.key.get_pressed()[K_DOWN] else 0

# Clase de los meteoritos
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('meteorito.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))  # Ajusta el tamaño de la imagen
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(4, 6) # Ajusta el rango de velocidad

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > height:
            self.rect.x = random.randint(0, width - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed_y = random.randint(4, 6) # Ajusta el rango de velocidad
            

# Grupos de sprites
all_sprites = pygame.sprite.Group()
meteors = pygame.sprite.Group()

# Crear nave espacial
spaceship = SpaceShip()
all_sprites.add(spaceship)

# Crear meteoritos
for _ in range(8):
    meteor = Meteor()
    all_sprites.add(meteor)
    meteors.add(meteor)

# Reloj para controlar la velocidad de actualización
clock = pygame.time.Clock()

# Puntaje
score = 0

# Tiempo de juego en segundos
game_time = 0

# Fuente del puntaje
font = pygame.font.Font(None, 36)
   
# Función para renderizar el puntaje en pantalla
def render_score():
    score_text = font.render("Score: " + str(score), True, WHITE)
    window.blit(score_text, (50, 50))
running = True
while running:
    # Obtener el tiempo transcurrido desde el último fotograma en segundos
    dt = clock.tick(20) / 1000.0
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                spaceship.speed_x = -5
            elif event.key == K_RIGHT:
                spaceship.speed_x = 5
            elif event.key == K_UP:
                spaceship.speed_y = -5
            elif event.key == K_DOWN:
                spaceship.speed_y = 5
        elif event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                spaceship.speed_x = 0
            elif event.key == K_UP or event.key == K_DOWN:
                spaceship.speed_y = 0
    
    # Actualizar
    all_sprites.update()

    # Incrementar el puntaje basado en el tiempo transcurrido
    score += int(dt * 20)  # Ajusta el factor de incremento según tus necesidades

    # Colisiones
    if pygame.sprite.spritecollide(spaceship, meteors, False):
        running = False

    # Renderizar
    window.fill(BLEND_RGB_ADD)
    all_sprites.draw(window)
    render_score()
    pygame.display.flip()

    # Controlar la velocidad de fotogramas
    clock.tick(60)

pygame.quit()