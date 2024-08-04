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

# Snake setup
def draw_snake(snake_list):
    for segment in snake_list:
        pygame.draw.rect(screen, GREEN, [segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE])
        pygame.draw.circle(screen, GREEN, (segment[0] + SNAKE_SIZE // 2, segment[1] + SNAKE_SIZE // 2), SNAKE_SIZE // 2)

# Game loop
def game_loop():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 35)

    def message(msg, color):
        mesg = font.render(msg, True, color)
        screen.blit(mesg, [WIDTH / 6, HEIGHT / 3])

    game_over = False
    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_change, y1_change = 0, 0
    snake_list = []
    length_of_snake = 1

    # Random apple position
    apple_x = round(random.randrange(0, WIDTH - SNAKE_SIZE) / 20.0) * 20.0
    apple_y = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / 20.0) * 20.0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -SNAKE_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = SNAKE_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -SNAKE_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = SNAKE_SIZE
                    x1_change = 0

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_over = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, [apple_x, apple_y, SNAKE_SIZE, SNAKE_SIZE])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
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
