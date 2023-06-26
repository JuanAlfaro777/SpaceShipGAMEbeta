import random 
import pygame
from pygame.locals import *

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Esquiva los meteoritos')

# Cargar la imagen del fondo
background_image = pygame.image.load("nebula.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Dimensiones de la imagen del fondo
background_height = background_image.get_height()

# Colores
WHITE = (255, 255, 255)

# Clase de la nave espacial
class SpaceShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('cohete.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))  # Ajusta el tamaño de la imagen
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.centery = HEIGHT // 2
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

# Clase de los meteoritos
class Meteor(pygame.sprite.Sprite):
    def __init__(self, meteor_type):
        super().__init__()
        self.meteor_type = meteor_type
        self.image = pygame.image.load(f"meteorito{meteor_type}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))  # Ajusta el tamaño de la imagen
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(2, 4)  # Ajusta el rango de velocidad
        self.vida = 4  # Cantidad de veces que aparecerá el meteorito

    def update(self):
        self.rect.y += self.speed_y

        # Comportamiento según el tipo de meteorito
        if self.meteor_type == 1:
            # Comportamiento del tipo 1
            pass
        elif self.meteor_type == 2:
            # Comportamiento del tipo 2
            pass
        elif self.meteor_type == 3:
            # Comportamiento del tipo 3
            pass
        elif self.meteor_type == 4:
            # Comportamiento del tipo 4
            pass

        # Verificar si el meteorito salió de la pantalla
        if self.rect.top > HEIGHT:
            self.vida -= 1
            if self.vida > 0:
                self.rect.x = random.randint(0, WIDTH - self.rect.width)
                self.rect.y = random.randint(-100, -40)
                self.speed_y = random.randint(2, 4)

# Grupos de sprites
all_sprites = pygame.sprite.Group()
meteors = pygame.sprite.Group()

# Crear nave espacial
spaceship = SpaceShip()
all_sprites.add(spaceship)

# Crear meteoritos
for _ in range(8):
    meteor_type = random.randint(1, 4)
    meteor = Meteor(meteor_type)
    all_sprites.add(meteor)
    meteors.add(meteor)

# Reloj para controlar la velocidad de actualización
clock = pygame.time.Clock()

# Puntaje
score = 0

# Fuente del puntaje
font = pygame.font.Font(None, 36)

# Función para renderizar el puntaje en pantalla
def render_score():
    score_text = font.render("Score: " + str(score), True, WHITE)
    window.blit(score_text, (50, 50))

# Función para mostrar el menú
def show_menu():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return None
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return "start"
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    return None

        # Dibujar el fondo
        window.blit(background_image, (0, 0))

        # Renderizar el título y las opciones del menú
        title_font = pygame.font.Font(None, 64)
        title_text = title_font.render("Esquiva los meteoritos", True, WHITE)
        window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 200))

        menu_font = pygame.font.Font(None, 36)
        start_text = menu_font.render("Presiona ESPACIO para comenzar", True, WHITE)
        quit_text = menu_font.render("Presiona ESC para salir", True, WHITE)
        window.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 300))
        window.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 350))

        pygame.display.flip()

# Función para el bucle principal del juego
def game_loop():
    global score, background_y

    # Reiniciar variables
    score = 0
    background_y = 0
    game_started = True

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

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

        # Actualizar solo si el juego ha comenzado
        if game_started:
            score += int(dt * 60)  # Ajusta el factor de incremento según tus necesidades

        # Actualizar
        all_sprites.update()

        # Mover el fondo de forma infinita
        background_y += 1
        if background_y >= background_height:
            background_y = 0

        # Dibujar el fondo
        window.blit(background_image, (0, background_y))
        window.blit(background_image, (0, background_y - background_height))

        # Dibujar todos los sprites
        all_sprites.draw(window)

        # Verificar colisión entre la nave espacial y los meteoritos
        collisions = pygame.sprite.spritecollide(spaceship, meteors, False)
        if collisions:
            running = False

        # Renderizar el puntaje en pantalla
        render_score()

        pygame.display.flip()
# Mostrar la pantalla de fin de juego
    show_game_over()

# Función para mostrar la pantalla de fin de juego
def show_game_over():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return None
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return "start"
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    return None

        # Dibujar el fondo
        window.blit(background_image, (0, 0))

        # Renderizar el mensaje de fin de juego
        game_over_font = pygame.font.Font(None, 64)
        game_over_text = game_over_font.render("¡Fin del juego!", True, WHITE)
        window.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 200))

        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render("Puntaje final: " + str(score), True, WHITE)
        window.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 300))

        restart_text = score_font.render("Presiona ESPACIO para reiniciar", True, WHITE)
        quit_text = score_font.render("Presiona ESC para salir", True, WHITE)
        window.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 400))
        window.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 450))

        pygame.display.flip()
        
# Bucle principal del programa
while True:
    choice = show_menu()
    if choice == "start":
        game_loop()
    else:
        break
pygame.quit()
