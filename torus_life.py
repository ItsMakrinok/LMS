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
                rect = (self.left + i * self.cell_size, self.top + j * self.cell_size,
                        self.cell_size, self.cell_size)
                if self.board[j][i] == 1:
                    pygame.draw.rect(screen, (0, 255, 0), rect)
                if self.board[j][i] == 2:
                    pygame.draw.rect(screen, (0, 50, 0), rect)
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


class TorusLife(Board):
    def on_click(self, cell_coords):
        if cell_coords is None:
            return
        x, y = cell_coords
        if self.board[y][x] == 1:
            self.board[y][x] = 0
        elif self.board[y][x] in (0, 2):
            self.board[y][x] = 1

    def next_move(self):
        previous_board = copy.deepcopy(self.board)
        for i in range(self.width):
            for j in range(self.height):
                cells_around = self.count_cells_around(previous_board, i, j)
                if previous_board[j][i] == 2:
                    self.board[j][i] = 0
                if previous_board[j][i] in (0, 2):
                    if cells_around == 3:
                        self.board[j][i] = 1
                if previous_board[j][i] == 1:
                    if cells_around not in (2, 3):
                        self.board[j][i] = 2

    def count_cells_around(self, board, x, y):
        result = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i == x and j == y:
                    continue
                if self.get_cell_by_coords(board, i, j) == 1:
                    result += 1
        return result

    def get_cell_by_coords(self, board, x, y):
        if x < 0:
            x += self.width
        if x >= self.width:
            x -= self.width
        if y < 0:
            y += self.height
        if y >= self.height:
            y -= self.height
        return board[y][x]

    def generate(self):
        for i in range(self.width):
            for j in range(self.height):
                self.board[j][i] = random.randint(0, 1)

    def clear(self):
        for i in range(self.width):
            for j in range(self.height):
                self.board[j][i] = 0


def draw():
    screen.fill('black')
    board.render(screen)


def update(delta):
    global time_before_generation
    if processing:
        time_before_generation -= game_speed * delta

        if time_before_generation <= 0:
            board.next_move()
            time_before_generation = 1


board = TorusLife(20, 20)
processing = False
game_speed = 20
time_before_generation = 1

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
            if event.button == pygame.BUTTON_RIGHT:
                processing = not processing
        if event.type == pygame.MOUSEWHEEL:
            game_speed = min(max(game_speed + event.y, 1), 100)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                processing = not processing
            if event.key == pygame.K_r:
                board.generate()
            if event.key == pygame.K_c:
                board.clear()

    delta = clock.tick() / 1000
    update(delta)

    draw()
    pygame.display.flip()
