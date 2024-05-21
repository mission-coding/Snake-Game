import pygame
import random
import sys

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
screen_width = 288
screen_height = 512
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake game by Vivek")

# Define colors
white = (225, 225, 225)
black = (0, 0, 0)
red = (225, 0, 0)
green = (0, 225, 0)
grey = (70, 70, 70)

# Functions
fps = 30
clock = pygame.time.Clock()

# Function to display text on screen
def display_text(text, colour, size, x, y):
    font = pygame.font.SysFont(None, size)
    screen_text = font.render(text, True, colour)
    screen.blit(screen_text, [x, y])

# Music and sound
pygame.mixer.music.load("game files\\bg.mp3")
# pygame.mixer.music.play(-1)

food_sound = pygame.mixer.Sound("game files\\food.mp3")
over_sound = pygame.mixer.Sound("game files\\gameover.mp3")

# Load images
bgimg = pygame.image.load("game files\\bg.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()
home_screen = pygame.image.load("game files\\homescreen.jpg")
home_screen = pygame.transform.scale(home_screen, (screen_width, screen_height)).convert_alpha()
gameover = pygame.image.load("game files\\gameover.jpg")
gameover = pygame.transform.scale(gameover, (screen_width, screen_height)).convert_alpha()

# Welcome screen
def welcome():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_play()
        
        # Check for mouse click to start the game
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 110 < mouse[0] < 180 and 330 < mouse[1] < 400:
            if click == (1, 0, 0):
                game_play()

        screen.blit(home_screen, [0, 0])
        display_text("Tap to start!", green, 25, 100, 410)
        pygame.display.update()

# Main game loop
def game_play():
    run = True
    over = False
    snake_x = 100
    snake_y = 200
    food_x = random.randint(25, screen_width - 25)
    food_y = random.randint(25, 360 - 25)
    snake_size = 15
    velocity_x = 0
    velocity_y = 0
    velocity = 8
    score = 0
    snake_list = []
    snake_length = 1
    
    while run:
        if over:
            # Save the high score to a file
            with open('game files\\hiscore.txt', 'w') as f:
                f.write(str(hiscore))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_play()
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if 110 < mouse[0] < 180 and 145 < mouse[1] < 395:
                if click == (1, 0, 0):
                    game_play()
            
            screen.blit(gameover, [0, 0])

            if score < int(hiscore):
                display_text("Score : " + str(score), black, 30, 100, 290)
            if score == int(hiscore):
                display_text("Highscore : " + str(score), black, 30, 100, 290)

            display_text("Tap to play again!", green, 25, 75, 410)
            clock.tick(fps)
            pygame.display.update()

        if not over:
            # Load high score from file
            with open('game files\\hiscore.txt', 'r') as f:
                hiscore = f.read()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_v:
                        snake_length += 5
                        score += 10
                    if event.key == pygame.K_LEFT:
                        velocity_x = -velocity
                        velocity_y = 0
                    if event.key == pygame.K_RIGHT:
                        velocity_x = velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = velocity
                        velocity_x = 0

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            snake_x += velocity_x
            snake_y += velocity_y

            # Eating food and increasing score
            if abs(snake_x - food_x) < 9 and abs(snake_y - food_y) < 9:
                score += 10
                snake_length += 2
                pygame.mixer.Channel(0).play(food_sound)
                food_x = random.randint(25, screen_width - 25)
                food_y = random.randint(25, screen_height - 25)

            if score >= int(hiscore):
                hiscore = score

            # If snake goes out of wall
            if snake_x <= 0 or snake_x >= screen_width - snake_size or snake_y <= 0 or snake_y >= screen_height - snake_size:
                pygame.mixer.Channel(1).play(over_sound)
                over = True

            # Increasing snake length
            head = [snake_x, snake_y]
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                over = True
                pygame.mixer.Channel(1).play(over_sound)

            screen.blit(bgimg, [0, 0])
            # Draw food
            pygame.draw.rect(screen, red, [food_x, food_y, snake_size, snake_size])
            # Draw snake
            for x, y in snake_list:
                pygame.draw.rect(screen, black, [x, y, snake_size, snake_size])

            # Display score
            display_text("Score : " + str(score) + "  Highscore : " + str(hiscore), green, 30, 15, 10)

            clock.tick(fps)
            pygame.display.update()

# Start the game
welcome()
