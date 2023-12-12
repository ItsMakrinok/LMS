import pygame
import os
import sys

pygame.init()
size = width, height = 400, 400
screen = pygame.display.set_mode(size)


def draw(screen):
    screen.fill('black')
    all_sprites.draw(screen)
    for sprite in all_sprites:
        if type(sprite) is Landing:
            pass


def update(delta):
    all_sprites.update(delta)


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


class Mountain(pygame.sprite.Sprite):
    image = load_image('mountains.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Mountain.image
        self.rect = self.image.get_rect()
        pygame.display.set_mode((self.rect.w, height))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = height


class Landing(pygame.sprite.Sprite):
    image = load_image('pt.png')

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Landing.image
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.y = pos[1]
        self.x = self.rect.x
        self.y = self.rect.y

    def update(self, delta):
        if not pygame.sprite.collide_mask(self, mountain):
            self.y += 100 * delta
            self.rect.y = self.y


running = True
clock = pygame.time.Clock()
FPS = 60

all_sprites = pygame.sprite.Group()
mountain = Mountain()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            Landing(event.pos)

    delta = 1 / FPS
    update(delta)
    clock.tick(FPS)

    draw(screen)
    pygame.display.flip()
pygame.quit()
