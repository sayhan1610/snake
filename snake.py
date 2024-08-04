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

# Function to draw the snake
def draw_snake(snake_list):
    for i, segment in enumerate(snake_list):
        color = GREEN if i == len(snake_list) - 1 else DARK_GREEN
        pygame.draw.rect(screen, color, [segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE])

# Function to draw the apple
def draw_apple(apple_x, apple_y, special=False):
    color = GOLD if special else RED
    pygame.draw.rect(screen, color, [apple_x, apple_y, SNAKE_SIZE, SNAKE_SIZE])

# Function to display messages on the screen
def message(msg, color, pos):
    mesg = FONT.render(msg, True, color)
    screen.blit(mesg, pos)

# Function to handle user input and events
def handle_events(direction, paused):
    global entered_code, invincibility_end_time, invincible

    cheat_code = 'iamzebest'

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'
            elif event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'
            elif event.key == pygame.K_SPACE:
                paused = not paused

            # Handle cheat code input
            entered_code += pygame.key.name(event.key)
            if entered_code.endswith(cheat_code):
                invincible = True
                invincibility_end_time = time.time() + 120  # 2 minutes
                entered_code = ''
            elif len(entered_code) > len(cheat_code):
                entered_code = entered_code[-len(cheat_code):]  # Keep only the last characters needed

    return direction, paused

# Function to detect collision with walls or the snake itself
def detect_collision(x1, y1, snake_list):
    if invincible and time.time() < invincibility_end_time:
        # Wrap around the screen edges
        if x1 >= WIDTH:
            x1 = 0
        elif x1 < 0:
            x1 = WIDTH - SNAKE_SIZE
        if y1 >= HEIGHT:
            y1 = 0
        elif y1 < 0:
            y1 = HEIGHT - SNAKE_SIZE

        # Check if the snake collides with itself
        for segment in snake_list[:-1]:
            if segment == [x1, y1]:
                return True
        return False

    # Normal collision detection when not invincible
    if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
        return True
    for segment in snake_list[:-1]:
        if segment == [x1, y1]:
            return True
    return False

# Function to spawn a new apple at a random location
def spawn_apple():
    return round(random.randrange(0, WIDTH - SNAKE_SIZE) / 20.0) * 20.0, round(random.randrange(0, HEIGHT - SNAKE_SIZE) / 20.0) * 20.0

# Main game loop
def game_loop():
    global SNAKE_SPEED, entered_code, invincible, invincibility_end_time
    entered_code = ''
    invincibility_end_time = 0
    invincible = False

    clock = pygame.time.Clock()
    SNAKE_SPEED = INITIAL_SNAKE_SPEED

    game_over = False
    paused = False
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

    start_time = time.time()

    while not game_over:
        direction, paused = handle_events(direction, paused)

        if not paused:
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

            # Wrap around the screen edges if invincible
            if invincible and time.time() < invincibility_end_time:
                if x1 >= WIDTH:
                    x1 = 0
                elif x1 < 0:
                    x1 = WIDTH - SNAKE_SIZE
                if y1 >= HEIGHT:
                    y1 = 0
                elif y1 < 0:
                    y1 = HEIGHT - SNAKE_SIZE

            if detect_collision(x1, y1, snake_list):
                if not invincible:
                    if game_over_sound:
                        game_over_sound.play()
                    game_over = True

            screen.fill(BLACK)
            draw_apple(apple_x, apple_y)

            if special_apple_active:
                draw_apple(special_apple_x, special_apple_y, special=True)
                special_apple_timer -= 1
                message(f"Special apple: {special_apple_timer // SNAKE_SPEED}s", GOLD, [0, 35])
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
                if score % 5 == 0:
                    SNAKE_SPEED += 1
                if score % 10 == 0 and not special_apple_active:
                    special_apple_x, special_apple_y = spawn_apple()
                    special_apple_active = True
                    special_apple_timer = 10 * SNAKE_SPEED

            if special_apple_active and x1 == special_apple_x and y1 == special_apple_y:
                if eat_sound:
                    eat_sound.play()
                special_apple_active = False
                length_of_snake += 3
                score += 3

            # Check invincibility status
            if invincible and time.time() > invincibility_end_time:
                invincible = False

            clock.tick(SNAKE_SPEED)
        else:
            message("Paused. Press SPACE to Resume", WHITE, [WIDTH / 6, HEIGHT / 3])
            pygame.display.update()

    total_time = time.time() - start_time

    screen.fill(BLACK)
    message(f"You Lost! Score: {score} Time: {int(total_time)}s", RED, [WIDTH / 6, HEIGHT / 3])
    message("Press Q to Quit or C to Play Again", RED, [WIDTH / 6, HEIGHT / 2])
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

def show_instructions():
    screen.fill(BLACK)
    message("Instructions:", WHITE, [WIDTH / 6, HEIGHT / 4])
    message("Use arrow keys to move the snake.", WHITE, [WIDTH / 6, HEIGHT / 3])
    message("Press SPACE to pause the game.", WHITE, [WIDTH / 6, HEIGHT / 2.7])
    message("Eat apples to grow and earn points.", WHITE, [WIDTH / 6, HEIGHT / 2.4])
    message("Avoid running into the walls or yourself.", WHITE, [WIDTH / 6, HEIGHT / 2.1])
    message("Press B to go back to main menu.", RED, [WIDTH / 6, HEIGHT / 1.8])
    pygame.display.update()
    
    instructions = True
    while instructions:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    instructions = False
                    main_menu()

def main_menu():
    screen.fill(BLACK)
    message("Welcome to Snake Game", WHITE, [WIDTH / 6, HEIGHT / 3])
    message("Press S to Start the Game", GREEN, [WIDTH / 6, HEIGHT / 2])
    message("Press I for Instructions", GREEN, [WIDTH / 6, HEIGHT / 1.8])
    pygame.display.update()
    
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    menu = False
                    game_loop()
                elif event.key == pygame.K_i:
                    menu = False
                    show_instructions()

# Start with the main menu
main_menu()
