import pygame
import os
import sys
import random

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)


def draw():
    screen.fill('white')
    bombs_group.draw(screen)


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


class Bomb(pygame.sprite.Sprite):
    image_bomb = load_image('bomb2.png')
    image_boom = load_image('boom.png')

    def __init__(self):
        super().__init__()
        self.image = Bomb.image_bomb
        self.rect = self.image.get_rect()
        self.random_place()
        self.add(bombs_group)

    def random_place(self):
        while pygame.sprite.spritecollideany(self, bombs_group):
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(width - self.rect.height)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(event.pos):
            self.change_image(self.image_boom)

    def change_image(self, image):
        offset_x = self.image.get_size()[0] - image.get_size()[0]
        offset_y = self.image.get_size()[1] - image.get_size()[1]

        self.rect.y += offset_y / 2
        self.rect.x += offset_x / 2

        self.image = image


running = True
clock = pygame.time.Clock()

FPS = 60

bombs_group = pygame.sprite.Group()
for i in range(10):
    Bomb()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        bombs_group.update(event)

    delta = 1 / FPS
    clock.tick(FPS)
    update(delta)

    draw()
    pygame.display.flip()
pygame.quit()
