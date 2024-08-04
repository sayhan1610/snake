import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)

# Game settings
SNAKE_SIZE = 20
INITIAL_SNAKE_SPEED = 15

# Fonts
FONT = pygame.font.SysFont(None, 35)

# Sound Effects (Make sure to have these files in your directory)
try:
    eat_sound = pygame.mixer.Sound('eat.wav')
    game_over_sound = pygame.mixer.Sound('game_over.wav')
except pygame.error as e:
    print(f"Error loading sound: {e}")
    eat_sound = None
    game_over_sound = None

def draw_snake(snake_list):
    for i, segment in enumerate(snake_list):
        if i == len(snake_list) - 1:
            color = GREEN  # Snake head
        else:
            color = DARK_GREEN  # Snake body
        pygame.draw.rect(screen, color, [segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE])

def draw_apple(apple_x, apple_y, special=False):
    color = GOLD if special else RED
    pygame.draw.rect(screen, color, [apple_x, apple_y, SNAKE_SIZE, SNAKE_SIZE])

def message(msg, color, pos):
    mesg = FONT.render(msg, True, color)
    screen.blit(mesg, pos)

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
            elif event.key == pygame.K_p:
                return 'PAUSE'
    return direction

def detect_collision(x1, y1, snake_list):
    if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
        return True
    for segment in snake_list[:-1]:
        if segment == [x1, y1]:
            return True
    return False

def spawn_apple():
    return round(random.randrange(0, WIDTH - SNAKE_SIZE) / 20.0) * 20.0, round(random.randrange(0, HEIGHT - SNAKE_SIZE) / 20.0) * 20.0

def game_loop():
    clock = pygame.time.Clock()
    global SNAKE_SPEED
    SNAKE_SPEED = INITIAL_SNAKE_SPEED

    game_over = False
    direction = 'STOP'
    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_change, y1_change = 0, 0
    snake_list = []
    length_of_snake = 1
    score = 0

    apple_x, apple_y = spawn_apple()
    special_apple_active = False
    special_apple_x, special_apple_y = None, None
    special_apple_timer = 0

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
        elif direction == 'PAUSE':
            paused = True
            while paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            paused = False

        x1 += x1_change
        y1 += y1_change

        if detect_collision(x1, y1, snake_list):
            if game_over_sound:
                game_over_sound.play()
            game_over = True

        screen.fill(BLACK)
        draw_apple(apple_x, apple_y)

        if special_apple_active:
            draw_apple(special_apple_x, special_apple_y, special=True)
            special_apple_timer -= 1
            if special_apple_timer <= 0:
                special_apple_active = False

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        draw_snake(snake_list)
        message(f"Score: {score}", WHITE, [0, 0])
        pygame.display.update()

        if x1 == apple_x and y1 == apple_y:
            if eat_sound:
                eat_sound.play()
            apple_x, apple_y = spawn_apple()
            length_of_snake += 1
            score += 1
            if score % 5 == 0:  # Increase speed every 5 apples eaten
                SNAKE_SPEED += 1
            if score % 10 == 0 and not special_apple_active:
                special_apple_x, special_apple_y = spawn_apple()
                special_apple_active = True
                special_apple_timer = 10 * SNAKE_SPEED  # 10 seconds

        if special_apple_active and x1 == special_apple_x and y1 == special_apple_y:
            if eat_sound:
                eat_sound.play()
            special_apple_active = False
            length_of_snake += 3
            score += 3

        clock.tick(SNAKE_SPEED)

    screen.fill(BLACK)
    message("You Lost! Press Q-Quit or C-Play Again", RED, [WIDTH / 6, HEIGHT / 3])
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
