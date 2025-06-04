import pygame
import sys
import math
from pygame import gfxdraw

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 600
CELL_SIZE = WINDOW_SIZE // 3
LINE_WIDTH = 15
CIRCLE_WIDTH = 15
CROSS_WIDTH = 20
CIRCLE_RADIUS = CELL_SIZE // 3
CROSS_SIZE = CELL_SIZE // 2

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
HOVER_COLOR = (200, 200, 200, 50)
WIN_LINE_COLOR = (220, 20, 60)

# Game Setup
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Modern Tic Tac Toe')
screen.fill(BG_COLOR)

class Board:
    def __init__(self):
        self.squares = [['' for _ in range(3)] for _ in range(3)]
        self.empty_squares = 9
        self.marked_squares = []

    def mark_square(self, row, col, player):
        self.squares[row][col] = player
        self.marked_squares.append((row, col))
        self.empty_squares -= 1

    def is_empty_square(self, row, col):
        return self.squares[row][col] == ''

    def is_full(self):
        return self.empty_squares == 0

    def is_empty(self):
        return self.empty_squares == 9

    def get_empty_squares(self):
        empty_squares = []
        for row in range(3):
            for col in range(3):
                if self.is_empty_square(row, col):
                    empty_squares.append((row, col))
        return empty_squares

class Game:
    def __init__(self):
        self.board = Board()
        self.player = 'X'
        self.running = True
        self.game_over = False
        self.animations = []
        self.winning_line = None

    def make_move(self, row, col):
        if self.board.is_empty_square(row, col) and not self.game_over:
            self.board.mark_square(row, col, self.player)
            if self.player == 'O':
                self.animations.append(CircleAnimation(row, col))
            else:
                self.animations.append(CrossAnimation(row, col))
            
            if self.check_win(row, col):
                self.game_over = True
            elif self.board.is_full():
                self.game_over = True
            
            self.player = 'O' if self.player == 'X' else 'X'
            return True
        return False

    def check_win(self, row, col):
        # Vertical win
        if self.board.squares[0][col] == self.board.squares[1][col] == self.board.squares[2][col]:
            self.winning_line = ('V', col)
            return True

        # Horizontal win
        if self.board.squares[row][0] == self.board.squares[row][1] == self.board.squares[row][2]:
            self.winning_line = ('H', row)
            return True

        # Diagonal win
        if row == col and self.board.squares[0][0] == self.board.squares[1][1] == self.board.squares[2][2]:
            self.winning_line = ('D', 1)
            return True

        if row + col == 2 and self.board.squares[0][2] == self.board.squares[1][1] == self.board.squares[2][0]:
            self.winning_line = ('D', 2)
            return True

        return False

    def reset(self):
        self.board = Board()
        self.player = 'X'
        self.running = True
        self.game_over = False
        self.animations = []
        self.winning_line = None
        screen.fill(BG_COLOR)
        draw_lines()

class Animation:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.progress = 0
        self.speed = 0.1
        self.finished = False

    def update(self):
        if not self.finished:
            self.progress = min(1.0, self.progress + self.speed)
            if self.progress >= 1.0:
                self.finished = True

class CircleAnimation(Animation):
    def draw(self):
        center_x = self.col * CELL_SIZE + CELL_SIZE // 2
        center_y = self.row * CELL_SIZE + CELL_SIZE // 2
        current_radius = int(CIRCLE_RADIUS * self.progress)
        
        if not self.finished:
            pygame.draw.circle(screen, CIRCLE_COLOR, (center_x, center_y), current_radius, CIRCLE_WIDTH)
        else:
            pygame.draw.circle(screen, CIRCLE_COLOR, (center_x, center_y), CIRCLE_RADIUS, CIRCLE_WIDTH)

class CrossAnimation(Animation):
    def draw(self):
        center_x = self.col * CELL_SIZE + CELL_SIZE // 2
        center_y = self.row * CELL_SIZE + CELL_SIZE // 2
        current_size = int(CROSS_SIZE * self.progress)
        
        if not self.finished:
            start_desc_x = center_x - current_size
            start_desc_y = center_y - current_size
            end_desc_x = center_x + current_size
            end_desc_y = center_y + current_size
            pygame.draw.line(screen, CROSS_COLOR, (start_desc_x, start_desc_y), 
                           (end_desc_x, end_desc_y), CROSS_WIDTH)

            start_asc_x = center_x - current_size
            start_asc_y = center_y + current_size
            end_asc_x = center_x + current_size
            end_asc_y = center_y - current_size
            pygame.draw.line(screen, CROSS_COLOR, (start_asc_x, start_asc_y),
                           (end_asc_x, end_asc_y), CROSS_WIDTH)
        else:
            start_desc = (center_x - CROSS_SIZE, center_y - CROSS_SIZE)
            end_desc = (center_x + CROSS_SIZE, center_y + CROSS_SIZE)
            start_asc = (center_x - CROSS_SIZE, center_y + CROSS_SIZE)
            end_asc = (center_x + CROSS_SIZE, center_y - CROSS_SIZE)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

def draw_lines():
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, CELL_SIZE), (WINDOW_SIZE, CELL_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * CELL_SIZE), (WINDOW_SIZE, 2 * CELL_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE, 0), (CELL_SIZE, WINDOW_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * CELL_SIZE, 0), (2 * CELL_SIZE, WINDOW_SIZE), LINE_WIDTH)

def draw_win_line(type, index):
    if type == 'H':  # Horizontal
        start_pos = (10, (index * CELL_SIZE) + CELL_SIZE // 2)
        end_pos = (WINDOW_SIZE - 10, (index * CELL_SIZE) + CELL_SIZE // 2)
    elif type == 'V':  # Vertical
        start_pos = ((index * CELL_SIZE) + CELL_SIZE // 2, 10)
        end_pos = ((index * CELL_SIZE) + CELL_SIZE // 2, WINDOW_SIZE - 10)
    elif type == 'D':
        if index == 1:  # Main diagonal
            start_pos = (10, 10)
            end_pos = (WINDOW_SIZE - 10, WINDOW_SIZE - 10)
        else:  # Secondary diagonal
            start_pos = (10, WINDOW_SIZE - 10)
            end_pos = (WINDOW_SIZE - 10, 10)
    
    pygame.draw.line(screen, WIN_LINE_COLOR, start_pos, end_pos, LINE_WIDTH)

def main():
    game = Game()
    draw_lines()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row = pos[1] // CELL_SIZE
                col = pos[0] // CELL_SIZE
                
                if game.game_over:
                    game.reset()
                else:
                    game.make_move(row, col)

        # Update and draw animations
        for anim in game.animations:
            if not anim.finished:
                anim.update()
            anim.draw()

        # Draw winning line if game is over
        if game.winning_line:
            draw_win_line(game.winning_line[0], game.winning_line[1])

        pygame.display.update()

if __name__ == '__main__':
    main()