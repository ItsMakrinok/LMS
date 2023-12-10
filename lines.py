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
                if self.board[j][i] == -1:
                    pygame.draw.rect(screen, (0, 255, 0), rect)
                if self.board[j][i] == 1:
                    pygame.draw.circle(screen, (0, 0, 255), rect.center, self.cell_size // 2)
                if self.board[j][i] == 2:
                    pygame.draw.circle(screen, (255, 0, 0), rect.center, self.cell_size // 2)
                pygame.draw.rect(screen, 'white', rect, 1)

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


class Lines(Board):
    def __init__(self, width, height):
        super().__init__(width, height)

    def on_click(self, cell_coords):
        if cell_coords is None:
            return
        x, y = cell_coords

        if self.board[y][x] == 0:
            red_circle_coords = self.get_red_circle_coords()
            if red_circle_coords is None:
                self.board[y][x] = 1
            else:
                self.move_red_circle(*red_circle_coords, x, y)
        elif self.board[y][x] == 1:
            self.board[y][x] = 2
        elif self.board[y][x] == 2:
            self.board[y][x] = 1

    def get_red_circle_coords(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.board[j][i] == 2:
                    return i, j
        return None

    def move_red_circle(self, x1, y1, x2, y2):
        if self.has_path(x1, y1, x2, y2):
            self.board[y1][x1] = 0
            self.board[y2][x2] = 2

    def has_path(self, x1, y1, x2, y2):
        board = copy.deepcopy(self.board)
        for i in range(self.width):
            for j in range(self.height):
                if board[j][i] == 1:
                    board[j][i] = -1
                else:
                    board[j][i] = 0
        board = self.wave(board, x1, y1, 1, x2, y2)
        return board[y2][x2] > 0

    def wave(self, board, x1, y1, current, x2, y2):
        board[y1][x1] = current
        if board[y2][x2] > 0:
            return board
        if x1 - 1 >= 0:
            if board[y1][x1 - 1] == 0:
                self.wave(board, x1 - 1, y1, current + 1, x2, y2)
        if x1 + 1 < self.width:
            if board[y1][x1 + 1] == 0:
                self.wave(board, x1 + 1, y1, current + 1, x2, y2)
        if y1 - 1 >= 0:
            if board[y1 - 1][x1] == 0:
                self.wave(board, x1, y1 - 1, current + 1, x2, y2)
        if y1 + 1 < self.height:
            if board[y1 + 1][x1] == 0:
                self.wave(board, x1, y1 + 1, current + 1, x2, y2)
        return board


def draw():
    screen.fill('black')
    board.render(screen)


def update(delta):
    pass


board = Lines(16, 16)

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
