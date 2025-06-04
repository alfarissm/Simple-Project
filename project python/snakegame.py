import pygame
import random
import sys
import math
from pygame import gfxdraw

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
SNAKE_SPEED = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
DARK_GREEN = (34, 139, 34)
GRID_COLOR = (40, 40, 40)
BACKGROUND_COLOR = (15, 15, 15)

# Gradients
def get_gradient_color(start_color, end_color, percent):
    return tuple(int(start + (end - start) * percent) for start, end in zip(start_color, end_color))

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0
        self.growing = False
        self.eyes_angle = 0

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)
        
        if new in self.positions[3:]:
            return False
            
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
            
        # Update eyes angle based on direction
        if self.direction == UP:
            self.eyes_angle = 0
        elif self.direction == RIGHT:
            self.eyes_angle = 90
        elif self.direction == DOWN:
            self.eyes_angle = 180
        elif self.direction == LEFT:
            self.eyes_angle = 270
            
        return True

    def reset(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.growing = False

    def render(self, surface):
        for i, p in enumerate(self.positions):
            # Calculate gradient color based on position in snake
            percent = i / max(len(self.positions), 1)
            color = get_gradient_color(GREEN, DARK_GREEN, percent)
            
            # Draw snake segment with rounded corners
            x = p[0] * GRID_SIZE + GRID_SIZE // 2
            y = p[1] * GRID_SIZE + GRID_SIZE // 2
            radius = GRID_SIZE // 2 - 2
            
            pygame.draw.circle(surface, color, (x, y), radius)
            
            # Draw eyes on head
            if i == 0:  # Head of the snake
                eye_offset = 3
                eye_radius = 2
                
                # Calculate eye positions based on direction
                left_eye = (
                    x + math.cos(math.radians(self.eyes_angle - 30)) * eye_offset,
                    y - math.sin(math.radians(self.eyes_angle - 30)) * eye_offset
                )
                right_eye = (
                    x + math.cos(math.radians(self.eyes_angle + 30)) * eye_offset,
                    y - math.sin(math.radians(self.eyes_angle + 30)) * eye_offset
                )
                
                pygame.draw.circle(surface, WHITE, (int(left_eye[0]), int(left_eye[1])), eye_radius)
                pygame.draw.circle(surface, WHITE, (int(right_eye[0]), int(right_eye[1])), eye_radius)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()
        self.glow_radius = GRID_SIZE // 2
        self.glow_direction = 1
        self.glow_speed = 0.2
        self.glow_min = GRID_SIZE // 2 - 2
        self.glow_max = GRID_SIZE // 2 + 2

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1),
                        random.randint(0, GRID_HEIGHT-1))

    def update(self):
        # Update glow effect
        self.glow_radius += self.glow_speed * self.glow_direction
        if self.glow_radius > self.glow_max:
            self.glow_direction = -1
        elif self.glow_radius < self.glow_min:
            self.glow_direction = 1

    def render(self, surface):
        x = self.position[0] * GRID_SIZE + GRID_SIZE // 2
        y = self.position[1] * GRID_SIZE + GRID_SIZE // 2
        
        # Draw glow effect
        for radius in range(int(self.glow_radius), 0, -2):
            alpha = int(255 * (radius / self.glow_radius))
            glow_color = (*self.color[:3], alpha)
            pygame.gfxdraw.filled_circle(surface, int(x), int(y), radius, glow_color)
        
        # Draw main food
        pygame.draw.circle(surface, self.color, (x, y), GRID_SIZE // 3)

def draw_grid(surface):
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, GRID_COLOR, rect, 1)

# Direction vectors
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def show_game_over(surface, score):
    font_big = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 36)
    
    game_over_text = font_big.render('Game Over!', True, WHITE)
    score_text = font_small.render(f'Final Score: {score}', True, WHITE)
    restart_text = font_small.render('Press any key to restart', True, WHITE)
    
    surface.blit(game_over_text, 
                (WINDOW_WIDTH//2 - game_over_text.get_width()//2, 
                 WINDOW_HEIGHT//2 - 60))
    surface.blit(score_text, 
                (WINDOW_WIDTH//2 - score_text.get_width()//2, 
                 WINDOW_HEIGHT//2))
    surface.blit(restart_text, 
                (WINDOW_WIDTH//2 - restart_text.get_width()//2, 
                 WINDOW_HEIGHT//2 + 40))

def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    surface = pygame.Surface(screen.get_size())
    pygame.display.set_caption('Enhanced Snake Game')
    
    font = pygame.font.Font(None, 36)
    
    snake = Snake()
    food = Food()
    game_over = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    snake.reset()
                    food.randomize_position()
                    game_over = False
                else:
                    if event.key == pygame.K_UP and snake.direction != DOWN:
                        snake.direction = UP
                    elif event.key == pygame.K_DOWN and snake.direction != UP:
                        snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                        snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                        snake.direction = RIGHT

        if not game_over:
            # Update game state
            if not snake.update():
                game_over = True
                continue

            # Check if snake has eaten the food
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                snake.growing = True
                food.randomize_position()

            # Update food animation
            food.update()

            # Draw everything
            surface.fill(BACKGROUND_COLOR)
            draw_grid(surface)
            snake.render(surface)
            food.render(surface)
            
            # Draw score with shadow effect
            score_text = font.render(f'Score: {snake.score}', True, WHITE)
            shadow_text = font.render(f'Score: {snake.score}', True, (100, 100, 100))
            surface.blit(shadow_text, (12, 12))
            surface.blit(score_text, (10, 10))
        else:
            show_game_over(surface, snake.score)

        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(SNAKE_SPEED)

if __name__ == '__main__':
    main()