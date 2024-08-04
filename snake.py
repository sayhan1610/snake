import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Game settings
SNAKE_SIZE = 20
SNAKE_SPEED = 15

# Fonts
FONT = pygame.font.SysFont(None, 35)

def draw_snake(snake_list):
    for segment in snake_list:
        pygame.draw.rect(screen, GREEN, [segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE])

def draw_apple(apple_x, apple_y):
    pygame.draw.rect(screen, RED, [apple_x, apple_y, SNAKE_SIZE, SNAKE_SIZE])

def message(msg, color):
    mesg = FONT.render(msg, True, color)
    screen.blit(mesg, [WIDTH / 6, HEIGHT / 3])

def handle_events(direction):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                return 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                return 'RIGHT'
            elif event.key == pygame.K_UP and direction != 'DOWN':
                return 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                return 'DOWN'
    return direction

def detect_collision(x1, y1, snake_list):
    if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
        return True
    for segment in snake_list[:-1]:
        if segment == [x1, y1]:
            return True
    return False

def game_loop():
    clock = pygame.time.Clock()

    game_over = False
    direction = 'STOP'
    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_change, y1_change = 0, 0
    snake_list = []
    length_of_snake = 1

    apple_x = round(random.randrange(0, WIDTH - SNAKE_SIZE) / 20.0) * 20.0
    apple_y = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / 20.0) * 20.0

    while not game_over:
        direction = handle_events(direction)
        
        if direction == 'LEFT':
            x1_change = -SNAKE_SIZE
            y1_change = 0
        elif direction == 'RIGHT':
            x1_change = SNAKE_SIZE
            y1_change = 0
        elif direction == 'UP':
            x1_change = 0
            y1_change = -SNAKE_SIZE
        elif direction == 'DOWN':
            x1_change = 0
            y1_change = SNAKE_SIZE

        x1 += x1_change
        y1 += y1_change

        if detect_collision(x1, y1, snake_list):
            game_over = True

        screen.fill(BLACK)
        draw_apple(apple_x, apple_y)
        
        snake_Head = [x1, y1]
        snake_list.append(snake_Head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        draw_snake(snake_list)
        pygame.display.update()

        if x1 == apple_x and y1 == apple_y:
            apple_x = round(random.randrange(0, WIDTH - SNAKE_SIZE) / 20.0) * 20.0
            apple_y = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / 20.0) * 20.0
            length_of_snake += 1

        clock.tick(SNAKE_SPEED)

    message("You Lost! Press Q-Quit or C-Play Again", RED)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_c:
                    game_loop()

game_loop()
