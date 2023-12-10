import pygame
import os
import sys


class Sprite(pygame.sprite.Sprite):
    @staticmethod
    def load_image(name, colorkey=None):
        fullname = os.path.join('SimpleGame/data/images', name)
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

    def __init__(self, game, image: pygame.Surface, *groups):
        super().__init__(*groups)
        self.game = game
        self.image = image
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0

    def update(self, delta):
        pass

    def event(self, event: pygame.event.Event):
        pass

    def rotate(self, image: pygame.Surface, angle):
        self.image = pygame.transform.rotate(image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
