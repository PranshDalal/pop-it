import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Pop It Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

# Bubble variables
bubble_radius = 30
bubble_speed = 2
bubble_timer = 2000  # Time interval for bubble generation in milliseconds

# Game variables
score = 0
# Sound effect for popping bubbles
pop_sound = pygame.mixer.Sound("pop.mp3")

# Timer for bubble generation
pygame.time.set_timer(pygame.USEREVENT, bubble_timer)

# Create a new bubble


def create_bubble():
    x = random.randint(bubble_radius, window_width - bubble_radius)
    y = random.randint(bubble_radius, window_height - bubble_radius)
    bubble_color = random.choice([green, red])
    bubble = pygame.Rect(x, y, bubble_radius, bubble_radius)
    return bubble, bubble_color

# Game loop


def game_loop():
    score = 0
    running = True
    clock = pygame.time.Clock()
    pygame.mixer.music.load("game.mp3")
    pygame.mixer.music.play(-1)
    bubbles = []  # List to store the bubbles
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT:
                bubble, bubble_color = create_bubble()
                bubbles.append((bubble, bubble_color))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Check if any bubble is clicked
                    for bubble, bubble_color in bubbles:
                        if bubble.collidepoint(event.pos):
                            if bubble_color == green:
                                bubbles.remove((bubble, bubble_color))
                                score += 1
                                pop_sound.play()
                            elif bubble_color == red:
                                bubbles.remove((bubble, bubble_color))
                                score -= 1
                                pop_sound.play()

        # Update game logic
        t = pygame.time.get_ticks()/3 % 1000
        x = t
        y = math.sin(t/50)*100 + 200
        for bubble, _ in bubbles:
            bubble.y -= bubble_speed

            # Remove bubbles that are off the screen
        bubbles = [(bubble, bubble_color)
                   for bubble, bubble_color in bubbles if bubble.y > -bubble_radius]

        # Clear the window
        window.fill(black)

        # Draw the bubbles
        for bubble, bubble_color in bubbles:
            pygame.draw.circle(window, bubble_color,
                               bubble.center, bubble_radius)
            if score > 10:
                pygame.draw.circle(window, bubble_color, (x, y), bubble_radius)

        # Draw the score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, white)
        window.blit(text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(60)

        # Check if score is below 0
        if score < 0:
            running = False
            end_screen(score)

    # Game over
    pygame.mixer.music.stop()
    pygame.quit()

# End screen


def end_screen(score):
    # Set up end screen window
    end_window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Pop It Game - Game Over")

    # Clear the end screen window
    end_window.fill(black)

    # Draw the game over message
    font = pygame.font.Font(None, 48)
    game_over_text = font.render("Game Over!", True, white)
    game_over_text_rect = game_over_text.get_rect(
        center=(window_width // 2, window_height // 2 - 50))
    end_window.blit(game_over_text, game_over_text_rect)

    background_img = pygame.image.load("background.jpg")
    background_img = pygame.transform.scale(
        background_img, (window_width, window_height))

    # Draw the final text
    score_text = font.render(
        "Try not to hit the red ones next time", True, white)
    score_text_rect = score_text.get_rect(
        center=(window_width // 2, window_height // 2))
    end_window.blit(score_text, score_text_rect)

    # Draw the play button
    play_button_rect = pygame.Rect(
        button_x, play_button_y, button_width, button_height)
    pygame.draw.rect(window, black, play_button_rect)
    play_font = pygame.font.Font(None, 36)
    play_text = play_font.render("Play Again", True, white)
    play_text_rect = play_text.get_rect(center=play_button_rect.center)
    window.blit(play_text, play_text_rect)

    # Draw the quit button
    quit_button_rect = pygame.Rect(
        button_x, quit_button_y, button_width, button_height)
    pygame.draw.rect(window, black, quit_button_rect)
    quit_font = pygame.font.Font(None, 36)
    quit_text = quit_font.render("Quit", True, white)
    quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
    window.blit(quit_text, quit_text_rect)

    # Update the display
    pygame.display.flip()

    # Wait for a key press to exit the end screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Check if play button is clicked
                    if play_button_rect.collidepoint(event.pos):
                        pygame.mixer.music.stop()
                        game_loop()
                    # Check if quit button is clicked
                    if quit_button_rect.collidepoint(event.pos):
                        pygame.mixer.music.stop()
                        pygame.quit()
                        sys.exit()


# Button variables
button_width = 200
button_height = 50
button_x = window_width // 2 - button_width // 2
play_button_y = window_height // 2 + 50
quit_button_y = window_height // 2 + 120
instruction_button_y = window_height // 2 + 190

# Main menu screen


def instruction_menu():
    # Set up instruction screen window
    instruction_window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Pop It Game -  Instructions")

    # Clear the instruction screen window
    instruction_window.fill(black)

    # Draw the game over message
    font = pygame.font.Font(None, 16)
    instruction_text = font.render(
        "Bubbles will appear on the screen.  Tap the green ones to increase you score but dont tap the red ones!", True, white)
    instruction_text_rect = instruction_text.get_rect(
        center=(window_width // 2, window_height // 2 - 50))
    instruction_window.blit(instruction_text, instruction_text_rect)

    # Draw the back button

    back_button_rect = pygame.Rect(
        button_x, play_button_y, button_width, button_height)
    pygame.draw.rect(window, black, back_button_rect)
    back_font = pygame.font.Font(None, 36)
    back_text = back_font.render("Back", True, white)
    back_text_rect = back_text.get_rect(center=back_button_rect.center)
    window.blit(back_text, back_text_rect)

    # Draw the quit button
    quit_button_rect = pygame.Rect(
        button_x, quit_button_y, button_width, button_height)
    pygame.draw.rect(window, black, quit_button_rect)
    quit_font = pygame.font.Font(None, 36)
    quit_text = quit_font.render("Quit", True, white)
    quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
    window.blit(quit_text, quit_text_rect)

    # updating
    pygame.display.flip()

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Check if play button is clicked
                    if back_button_rect.collidepoint(event.pos):
                        pygame.mixer.music.stop()
                        main_menu()
                    # Check if quit button is clicked
                    if quit_button_rect.collidepoint(event.pos):
                        pygame.mixer.music.stop()
                        pygame.quit()
                        sys.exit()


def main_menu():
    # Load background image
    pygame.mixer.music.load("arcade.mp3")
    pygame.mixer.music.play(-1)
    background_img = pygame.image.load("background.jpg")
    background_img = pygame.transform.scale(
        background_img, (window_width, window_height))

    # Load game title image
    title_img = pygame.image.load("text.png")
    title_img = pygame.transform.scale(title_img, (500, 200))
    title_rect = title_img.get_rect(
        center=(window_width // 2, window_height // 2 - 100))

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Check if play button is clicked
                    if play_button_rect.collidepoint(event.pos):
                        pygame.mixer.music.stop()
                        game_loop()
                    # Check if quit button is clicked
                    if quit_button_rect.collidepoint(event.pos):
                        pygame.mixer.music.stop()
                        pygame.quit()
                        sys.exit()
                    # check if instruction button is clicked
                    if instruction_button_rect.collidepoint(event.pos):
                        pygame.mixer.music.stop()
                        instruction_menu()

        # Clear the window
        window.fill(white)

        # Draw the background image
        window.blit(background_img, (0, 0))

        # Draw the game title
        window.blit(title_img, title_rect)

        # Draw the play button
        play_button_rect = pygame.Rect(
            button_x, play_button_y, button_width, button_height)
        pygame.draw.rect(window, black, play_button_rect)
        play_font = pygame.font.Font(None, 36)
        play_text = play_font.render("Play", True, white)
        play_text_rect = play_text.get_rect(center=play_button_rect.center)
        window.blit(play_text, play_text_rect)

        # Draw the quit button
        quit_button_rect = pygame.Rect(
            button_x, quit_button_y, button_width, button_height)
        pygame.draw.rect(window, black, quit_button_rect)
        quit_font = pygame.font.Font(None, 36)
        quit_text = quit_font.render("Quit", True, white)
        quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
        window.blit(quit_text, quit_text_rect)

        # Draw the instruction button
        instruction_button_rect = pygame.Rect(
            button_x, instruction_button_y, button_width, button_height)
        pygame.draw.rect(window, black, instruction_button_rect)
        instruction_font = pygame.font.Font(None, 36)
        instruction_text = instruction_font.render("Instructions", True, white)
        instruction_text_rect = instruction_text.get_rect(
            center=instruction_button_rect.center)
        window.blit(instruction_text, instruction_text_rect)

        # Update the display
        pygame.display.flip()


# Run the main menu
main_menu()
