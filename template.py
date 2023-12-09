import pygame
import os
import sys

pygame.init()
size = width, height = 400, 400
screen = pygame.display.set_mode(size)


def draw():
    screen.fill('black')


def update(delta):
    pass


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    return image


running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    delta = clock.tick() / 1000
    update(delta)

    draw()
    pygame.display.flip()
pygame.quit()
