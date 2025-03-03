import pygame
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 500, 500
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)

# Font settings
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 50)

# Snake settings
snake = [(100, 100), (80, 100), (60, 100)]
snake_dir = "RIGHT"
change_to = snake_dir
speed = 10
score = 0

# Food settings
def generate_food():
    while True:
        food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
        if food not in snake:
            return food

food = generate_food()

# Game state
running = True
paused = False
wrap_mode = False
clock = pygame.time.Clock()

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.rect(screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)

def draw_snake():
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0] + 2, segment[1] + 2, CELL_SIZE - 4, CELL_SIZE - 4), border_radius=6)

def draw_food():
    pygame.draw.rect(screen, RED, (food[0] + 4, food[1] + 4, CELL_SIZE - 8, CELL_SIZE - 8), border_radius=8)

def game_over_screen():
    while True:
        screen.fill(BLACK)
        draw_text("Game Over!", WIDTH // 3.5, HEIGHT // 4, big_font, RED)
        draw_text(f"Final Score: {score}", WIDTH // 3, HEIGHT // 2.5, font, WHITE)
        draw_text("Press ENTER to Play Again", WIDTH // 4, HEIGHT // 1.8, font, WHITE)
        draw_text("Press ESC to Quit", WIDTH // 3, HEIGHT // 1.5, font, WHITE)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return main_game()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

def draw_text(text, x, y, font, color=WHITE):
    screen.blit(font.render(text, True, color), (x, y))

def main_game():
    global snake, snake_dir, change_to, food, score, speed, running, paused

    snake = [(100, 100), (80, 100), (60, 100)]
    snake_dir = "RIGHT"
    change_to = snake_dir
    food = generate_food()
    score = 0
    speed = 10
    running = True
    paused = False

    while running:
        screen.fill(BLACK)
        draw_grid()

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_dir != "DOWN":
                    change_to = "UP"
                elif event.key == pygame.K_DOWN and snake_dir != "UP":
                    change_to = "DOWN"
                elif event.key == pygame.K_LEFT and snake_dir != "RIGHT":
                    change_to = "LEFT"
                elif event.key == pygame.K_RIGHT and snake_dir != "LEFT":
                    change_to = "RIGHT"
                elif event.key == pygame.K_p:
                    paused = not paused  # Toggle pause

        if not paused:
            snake_dir = change_to

            # Move the snake
            head_x, head_y = snake[0]
            if snake_dir == "UP":
                head_y -= CELL_SIZE
            elif snake_dir == "DOWN":
                head_y += CELL_SIZE
            elif snake_dir == "LEFT":
                head_x -= CELL_SIZE
            elif snake_dir == "RIGHT":
                head_x += CELL_SIZE

            # Wrap mode
            if wrap_mode:
                head_x %= WIDTH
                head_y %= HEIGHT
            else:
                if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
                    return game_over_screen()

            new_head = (head_x, head_y)

            # Check for collisions
            if new_head in snake:
                return game_over_screen()

            snake.insert(0, new_head)

            if new_head == food:
                food = generate_food()
                score += 1
                speed += 0.3  # Speed increase over time
            else:
                snake.pop()

        draw_snake()
        draw_food()
        draw_text(f"Score: {score}", 10, 10, font)

        if paused:
            draw_text("PAUSED", WIDTH // 2 - 50, HEIGHT // 2, big_font, RED)

        pygame.display.flip()
        clock.tick(speed)

# Start the game
main_game()
