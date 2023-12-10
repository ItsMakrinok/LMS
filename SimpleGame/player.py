import math
import pygame

from sprite import Sprite
from wall import Wall


class Player(Sprite):
    image = None
    left_keys = (pygame.K_LEFT, pygame.K_a)
    right_keys = (pygame.K_RIGHT, pygame.K_d)
    up_keys = (pygame.K_UP, pygame.K_w)
    down_keys = (pygame.K_DOWN, pygame.K_s)

    def __init__(self, game, x, y, *groups):
        Player.image = pygame.transform.scale(self.load_image('player.png'), (50, 50))
        super().__init__(game, Player.image, *groups)
        self.rect.center = x, y
        self.x = self.rect.x
        self.y = self.rect.y

        self.speed = 500
        self.x_direction = 0
        self.y_direction = 0

    def update(self, delta):
        self.x_direction = self.y_direction = 0
        keys = pygame.key.get_pressed()

        if keys[self.left_keys[0]] or keys[self.left_keys[1]]:
            self.x_direction -= 1
        if keys[self.right_keys[0]] or keys[self.right_keys[1]]:
            self.x_direction += 1
        if keys[self.up_keys[0]] or keys[self.up_keys[1]]:
            self.y_direction -= 1
        if keys[self.down_keys[0]] or keys[self.down_keys[1]]:
            self.y_direction += 1

        if self.x_direction and self.y_direction:
            self.x_direction /= math.sqrt(2)
            self.y_direction /= math.sqrt(2)

        self.move(self.x_direction * self.speed * delta,
                  self.y_direction * self.speed * delta)

    def move(self, x_speed, y_speed):
        if x_speed < 0:
            i = pygame.rect.Rect(self.rect.left + x_speed, self.rect.top, 1, self.rect.h).collidelist(self.game.walls)
            if i != -1:
                wall: Wall = self.game.walls[i]
                x_speed = wall.rect.right - self.rect.left
            if self.rect.left > 0:
                self.x += x_speed
            else:
                self.rect.left = 0
                self.x = self.rect.x
        if x_speed > 0:
            i = pygame.rect.Rect(self.rect.right + x_speed, self.rect.top, 1, self.rect.h).collidelist(self.game.walls)
            if i != -1:
                wall: Wall = self.game.walls[i]
                x_speed = wall.rect.left - self.rect.right
            if self.rect.right < self.game.width:
                self.x += x_speed
            else:
                self.rect.right = self.game.width
                self.x = self.rect.x
        if y_speed < 0:
            i = pygame.rect.Rect(self.rect.left, self.rect.top + y_speed, self.rect.w, 1).collidelist(self.game.walls)
            if i != -1:
                wall: Wall = self.game.walls[i]
                y_speed = wall.rect.bottom - self.rect.top
            if self.rect.top > 0:
                self.y += y_speed
            else:
                self.rect.top = 0
                self.y = self.rect.y
        if y_speed > 0:
            i = pygame.rect.Rect(self.rect.left, self.rect.bottom + y_speed, self.rect.w, 1).collidelist(self.game.walls)
            if i != -1:
                wall: Wall = self.game.walls[i]
                y_speed = wall.rect.top - self.rect.bottom
            if self.rect.bottom < self.game.height:
                self.y += y_speed
            else:
                self.rect.bottom = self.game.height
                self.y = self.rect.y

        self.rect.x = self.x
        self.rect.y = self.y

        # for i in self.rect.collidelistall(self.game.walls):
        #     wall: Wall = self.game.walls[i]
        #     if x_speed > 0 and self.rect.right > wall.rect.left:
        #         self.rect.right = wall.rect.left
        #     if x_speed < 0 and self.rect.left < wall.rect.right:
        #         self.rect.left = wall.rect.right
        #     if y_speed > 0 and self.rect.bottom > wall.rect.top:
        #         self.rect.bottom = wall.rect.top
        #     if y_speed < 0 and self.rect.top < wall.rect.bottom:
        #         self.rect.top = wall.rect.bottom
        #     self.x = self.rect.x
        #     self.y = self.rect.y




    # def get_walls_collisions(self, x_speed, y_speed):
    #     left = right = top = bottom = False
    #     for i in self.rect.collidelistall(self.game.walls):
    #         wall: Wall = self.game.walls[i]
    #         if wall.rect.right - x_speed >= self.rect.left:
    #             self.x = self.rect.left = wall.rect.right + 1
    #         if wall.rect.left - x_speed <= self.rect.right:
    #             right = True
    #         if wall.rect.bottom - y_speed >= self.rect.top:
    #             top = True
    #         if wall.rect.top - y_speed <= self.rect.bottom:
    #             bottom = True
    #     return left, right, top, bottom

    def event(self, event: pygame.event.Event):
        pass
