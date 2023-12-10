import pygame

from player import Player
from wall import Wall


class Game:
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 500, 500
        self.screen = pygame.display.set_mode(self.size)

        self.all_sprites = pygame.sprite.Group()
        self.player = Player(self, self.width // 2, self.height // 2, self.all_sprites)

        self.walls = []
        self.walls.append(Wall(self, 200, 100, 200, 50, self.all_sprites))
        self.walls.append(Wall(self, 300, 400, 50, 50, self.all_sprites))

        self.running = True
        self.clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                for sprite in self.all_sprites:
                    sprite.event(event)

            self.update(self.clock.tick(60))

            self.draw()
            pygame.display.flip()
        pygame.quit()

    def draw(self):
        self.screen.fill((50, 50, 50))
        self.all_sprites.draw(self.screen)

    def update(self, frame_time):
        delta = frame_time / 1000
        self.all_sprites.update(delta)


if __name__ == "__main__":
    game = Game()
