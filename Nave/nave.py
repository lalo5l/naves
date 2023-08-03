import pygame
import sys
import random
from pygame.locals import *

# Dimensiones de la pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

# Configuración de la nave espacial
NAVE_ANCHO = 50
NAVE_ALTO = 50
NAVE_VELOCIDAD = 8

# Configuración del asteroide
ASTEROIDE_ANCHO = 50
ASTEROIDE_ALTO = 50
ASTEROIDE_VELOCIDAD = 5

# Configuración del proyectil
PROYECTIL_ANCHO = 10
PROYECTIL_ALTO = 30
PROYECTIL_VELOCIDAD = 10

# Inicializar Pygame
pygame.init()

# Crear la pantalla
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Juego de Disparos")

# Cargar imágenes

nave_imagen = pygame.image.load("imagenes/nave.png").convert_alpha()
nave_imagen = pygame.transform.scale(nave_imagen, (NAVE_ANCHO, NAVE_ALTO))
asteroide_imagen = pygame.image.load("imagenes/asteroide.png").convert_alpha()
asteroide_imagen = pygame.transform.scale(asteroide_imagen, (ASTEROIDE_ANCHO, ASTEROIDE_ALTO))

# Clase para representar la nave espacial
class NaveEspacial(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = nave_imagen
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO_PANTALLA // 2
        self.rect.bottom = ALTO_PANTALLA - 10
        self.velocidad_x = 0

    def update(self):
        self.rect.x += self.velocidad_x

        # Mantener la nave dentro de la pantalla horizontalmente
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO_PANTALLA:
            self.rect.right = ANCHO_PANTALLA

    def mover_izquierda(self):
        self.velocidad_x = -NAVE_VELOCIDAD

    def mover_derecha(self):
        self.velocidad_x = NAVE_VELOCIDAD

    def detener(self):
        self.velocidad_x = 0

    def disparar(self):
        proyectil = Proyectil(self.rect.centerx, self.rect.top)
        proyectiles_grupo.add(proyectil)

    def colision_asteroide(self, asteroides_grupo):
        colisiones = pygame.sprite.spritecollide(self, asteroides_grupo, False)
        return len(colisiones) > 0

# Clase para representar asteroides
class Asteroide(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = asteroide_imagen
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO_PANTALLA - ASTEROIDE_ANCHO)
        self.rect.y = random.randint(-ALTO_PANTALLA, -ASTEROIDE_ALTO)
        self.velocidad_y = random.randint(1, ASTEROIDE_VELOCIDAD)

    def update(self):
        self.rect.y += self.velocidad_y

        # Si el asteroide sale de la pantalla, lo volvemos a colocar arriba
        if self.rect.top > ALTO_PANTALLA:
            self.rect.x = random.randint(0, ANCHO_PANTALLA - ASTEROIDE_ANCHO)
            self.rect.y = random.randint(-ALTO_PANTALLA, -ASTEROIDE_ALTO)
            self.velocidad_y = random.randint(1, ASTEROIDE_VELOCIDAD)

# Clase para representar proyectiles
class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PROYECTIL_ANCHO, PROYECTIL_ALTO))
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        
        self.rect.y -= PROYECTIL_VELOCIDAD
        if self.rect.bottom < 0:
            self.kill()

# Crear la nave espacial
nave = NaveEspacial()

# Crear grupos para los asteroides y los proyectiles
asteroides_grupo = pygame.sprite.Group()
proyectiles_grupo = pygame.sprite.Group()

# Puntuación
puntuacion = 0
fuente = pygame.font.Font(None, 36)

# Bucle principal del juego
pygame.mixer.music.load("sonidos/fondo.mp3")
pygame.mixer.music.play(-1)
jugando = True
reloj = pygame.time.Clock()
while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                nave.mover_izquierda()
            elif event.key == pygame.K_RIGHT:
                nave.mover_derecha()
            elif event.key == pygame.K_SPACE:  # Tecla Espacio para disparar
                nave.disparar()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                nave.detener()

    # Generar nuevos asteroides
    if len(asteroides_grupo) < 10:
        nuevo_asteroide = Asteroide()
        asteroides_grupo.add(nuevo_asteroide)

    # Actualizar la nave y los asteroides
    nave.update()
    asteroides_grupo.update()
    proyectiles_grupo.update()

    # Verificar colisiones entre la nave y los asteroides
    if nave.colision_asteroide(asteroides_grupo):
        jugando = False

    # Verificar colisiones entre los proyectiles y los asteroides
    colisiones_proyectiles = pygame.sprite.groupcollide(proyectiles_grupo, asteroides_grupo, True, True)
    for proyectil, asteroides in colisiones_proyectiles.items():
        puntuacion += len(asteroides)

    # Dibujar en la pantalla
    fondo = pygame.image.load("imagenes/fondo.jpg")
    fondo = pygame.transform.scale(fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
    pantalla.blit(fondo, (0, 0))
    pantalla.blit(nave.image, nave.rect)
    asteroides_grupo.draw(pantalla)
    proyectiles_grupo.draw(pantalla)

    # Mostrar la puntuación en la pantalla
    texto_puntuacion = fuente.render("Puntuación: " + str(puntuacion), True, BLANCO)
    pantalla.blit(texto_puntuacion, (10, 10))

    # Actualizar la pantalla
    pygame.display.flip()

    # Limitar la velocidad de fotogramas a 60 FPS
    reloj.tick(60)

# Mostrar mensaje de "Game Over"
explosion = pygame.mixer.Sound("sonidos/explosion.mp3")
explosion.play()
muerte = pygame.mixer.Sound("sonidos/muerte.mp3")
muerte.play()
texto_game_over = fuente.render("Game Over", True, ROJO)
pantalla.blit(texto_game_over, (ANCHO_PANTALLA // 2 - 50, ALTO_PANTALLA // 2))
pygame.display.flip()

# Esperar unos segundos antes de salir
pygame.time.wait(3000)

# Salir del juego
pygame.quit()
sys.exit()

