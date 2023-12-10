import pygame

from sprite import Sprite


class Wall(Sprite):
    image = None

    def __init__(self, game, x, y, width, height, *groups):
        Wall.image = pygame.transform.scale(self.load_image('wall.png'), (width, height))
        super().__init__(game, Wall.image, *groups)
        self.rect.center = x, y
        self.x = self.rect.x
        self.y = self.rect.y

    def update(self, delta):
        pass

    def event(self, event: pygame.event.Event):
        pass
