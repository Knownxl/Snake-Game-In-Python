import pygame
import random

# Initialize pygame
pygame.init()

# Screen size
WIDTH, HEIGHT = 500, 500
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Snake settings
snake = [(100, 100), (90, 100), (80, 100)]
snake_dir = "RIGHT"
change_to = snake_dir
speed = 10

# Food settings
food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))

# Font settings
font = pygame.font.Font(None, 36)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir != "DOWN":
                change_to = "UP"
            elif event.key == pygame.K_DOWN and snake_dir != "UP":
                change_to = "DOWN"
            elif event.key == pygame.K_LEFT and snake_dir != "RIGHT":
                change_to = "LEFT"
            elif event.key == pygame.K_RIGHT and snake_dir != "LEFT":
                change_to = "RIGHT"

    # Update snake direction
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

    new_head = (head_x, head_y)
    
    # Check for collisions
    if new_head in snake or head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        running = False  # Game over

    # Move snake
    snake.insert(0, new_head)
    if new_head == food:
        food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))  # Generate new food
    else:
        snake.pop()  # Remove last part

    # Draw snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

    # Draw food
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

    # Update display
    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
