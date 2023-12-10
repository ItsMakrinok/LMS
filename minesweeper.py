import pygame
import copy
import random


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                rect = pygame.rect.Rect(self.left + i * self.cell_size, self.top + j * self.cell_size,
                        self.cell_size, self.cell_size)
                if 10 > self.board[j][i] > -1:
                    self.draw_number_in_cell(screen, rect, self.board[j][i])
                if self.board[j][i] == 10:
                    pygame.draw.rect(screen, (255, 0, 0), rect)
                pygame.draw.rect(screen, 'white', rect, 1)

    def draw_number_in_cell(self, screen, rect: pygame.rect.Rect, number):
        font = pygame.font.Font(None, 30)
        text = font.render(str(number), True, (0, 255, 0))
        text_x = rect.left + 2
        text_y = rect.top + 2
        screen.blit(text, (text_x, text_y))

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.left) // self.cell_size
        if x < 0 or y < 0:
            return None
        if x >= self.width or y >= self.height:
            return None
        return x, y

    def on_click(self, cell_coords):
        pass


class Minesweeper(Board):
    def __init__(self, width, height, mines_count):
        super().__init__(width, height)
        self.mines_count = mines_count

        cells = []
        for i in range(self.width):
            for j in range(self.height):
                self.board[j][i] = -1
                cells.append((i, j))

        for mine in random.sample(cells, mines_count):
            self.board[mine[1]][mine[0]] = 10

    def on_click(self, cell_coords):
        if cell_coords is None:
            return
        x, y = cell_coords
        self.open_cell(x, y)

    def open_cell(self, x, y):
        if x < 0 or x >= self.width:
            return
        if y < 0 or y >= self.height:
            return
        if self.board[y][x] == -1:
            self.board[y][x] = self.count_mines_around(x, y)
            if self.board[y][x] == 0:
                for i in range(x - 1, x + 2):
                    for j in range(y - 1, y + 2):
                        if i == x and j == y:
                            continue
                        self.open_cell(i, j)

    def count_mines_around(self, x, y):
        result = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i < 0 or i >= self.width:
                    continue
                if j < 0 or j >= self.height:
                    continue
                if i == x and j == y:
                    continue
                if self.board[j][i] == 10:
                    result += 1
        return result


def draw():
    screen.fill('black')
    board.render(screen)


def update(delta):
    pass


board = Minesweeper(16, 16, 32)

pygame.init()
size = (board.width * board.cell_size + board.left * 2,
        board.height * board.cell_size + board.top * 2)
screen = pygame.display.set_mode(size)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                board.get_click(event.pos)

    delta = clock.tick() / 1000
    update(delta)

    draw()
    pygame.display.flip()
