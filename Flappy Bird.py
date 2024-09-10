import pygame
import sys
import random

def main():
    name = input("Enter your name: ")

    pygame.init()

    # Define the screen and game clock
    width, height = 350, 622
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Flappy Bird")

    # Load images
    back_img = pygame.image.load("img_46.png").convert()
    floor_img = pygame.image.load("img_50.png").convert()
    bird_up = pygame.image.load("img_47.png").convert_alpha()
    bird_down = pygame.image.load("img_48.png").convert_alpha()
    bird_mid = pygame.image.load("img_49.png").convert_alpha()
    pipe_img = pygame.image.load("greenpipe.png").convert()
    over_img = pygame.image.load("img_45.png").convert_alpha()

    # Bird settings
    birds = [bird_up, bird_mid, bird_down]
    bird_index = 0
    bird_img = birds[bird_index]
    bird_rect = bird_img.get_rect(center=(67, 622 // 2))
    bird_movement = 0
    gravity = 0.17
    bird_flap = pygame.USEREVENT
    pygame.time.set_timer(bird_flap, 200)

    # Pipe settings
    pipe_height = [400, 350, 533, 490]
    pipes = []
    create_pipe = pygame.USEREVENT + 1
    pygame.time.set_timer(create_pipe, 1200)

    # Floor settings
    floor_x = 0

    # Game state variables
    game_over = False
    over_rect = over_img.get_rect(center=(width // 2, height // 2))
    score = 0
    high_score = 0
    score_time = True

    # Fonts
    score_font = pygame.font.Font("freesansbold.ttf", 27)

    # Function to draw the floor
    def draw_floor():
        screen.blit(floor_img, (floor_x, 520))
        screen.blit(floor_img, (floor_x + 448, 520))

    # Function to create pipes
    def create_pipes():
        pipe_y = random.choice(pipe_height)
        top_pipe = pipe_img.get_rect(midbottom=(467, pipe_y - 300))
        bottom_pipe = pipe_img.get_rect(midtop=(467, pipe_y))
        return top_pipe, bottom_pipe

    # Function to animate pipes
    def pipe_animation():
        nonlocal game_over
        for pipe in pipes:
            if pipe.top < 0:
                flipped_pipe = pygame.transform.flip(pipe_img, False, True)
                screen.blit(flipped_pipe, pipe)
            else:
                screen.blit(pipe_img, pipe)

            pipe.centerx -= 3
            if pipe.right < 0:
                pipes.remove(pipe)

            if bird_rect.colliderect(pipe):
                game_over = True

    # Function to draw the score
    def draw_score(game_state):
        if game_state == "game_on":
            score_text = score_font.render(str(score), True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(width // 2, 66))
            screen.blit(score_text, score_rect)
        elif game_state == "game_over":
            score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(width // 2, 66))
            screen.blit(score_text, score_rect)

            high_score_text = score_font.render(f"High Score: {high_score}", True, (255, 255, 255))
            high_score_rect = high_score_text.get_rect(center=(width // 2, 506))
            screen.blit(high_score_text, high_score_rect)

    # Function to update the score
    def score_update():
        nonlocal score, score_time, high_score
        if pipes:
            for pipe in pipes:
                if 65 < pipe.centerx < 69 and score_time:
                    score += 1
                    score_time = False
                if pipe.left <= 0:
                    score_time = True

        if score > high_score:
            high_score = score

    # Main game loop
    running = True
    while running:
        clock.tick(120)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird_movement = 0
                    bird_movement = -7
                if event.key == pygame.K_SPACE and game_over:
                    game_over = False
                    pipes = []
                    bird_movement = 0
                    bird_rect = bird_img.get_rect(center=(67, 622 // 2))
                    score_time = True
                    score = 0

            if event.type == bird_flap:
                bird_index += 1
                if bird_index > 2:
                    bird_index = 0
                bird_img = birds[bird_index]
                bird_rect = bird_img.get_rect(center=bird_rect.center)

            if event.type == create_pipe:
                pipes.extend(create_pipes())

        # Draw background and floor
        screen.blit(back_img, (0, 0))
        draw_floor()

        if not game_over:
            # Bird movement and collision
            bird_movement += gravity
            bird_rect.centery += bird_movement
            rotated_bird = pygame.transform.rotozoom(bird_img, bird_movement * -6, 1)

            if bird_rect.top < 5 or bird_rect.bottom >= 550:
                game_over = True

            screen.blit(rotated_bird, bird_rect)

            # Pipe animation and score update
            pipe_animation()
            score_update()
            draw_score("game_on")

        elif game_over:
            screen.blit(over_img, over_rect)
            draw_score("game_over")

        # Move the floor
        floor_x -= 1
        if floor_x < -448:
            floor_x = 0

        # Update display
        pygame.display.update()

    pygame.quit()

def ask_to_play_again():
    user = input("Do you want to play again? (yes/no): ")

    if user == "yes":
        return True
    elif user == "no":
        print("Thank you for playing!")
        return False
    else:
        print("Invalid answer. Please enter 'yes' or 'no'.")
        return ask_to_play_again()

# Game loop
while True:
    main()  # Run the game
    if not ask_to_play_again():
        break
