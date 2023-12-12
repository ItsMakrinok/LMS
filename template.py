import pygame
import os
import sys

pygame.init()
size = width, height = 400, 400
screen = pygame.display.set_mode(size)


def draw(screen):
    screen.fill('black')


def update(delta):
    pass


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


running = True
clock = pygame.time.Clock()
FPS = 60

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    delta = FPS / 1000
    update(delta)
    clock.tick(FPS)

    draw(screen)
    pygame.display.flip()
pygame.quit()
