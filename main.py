import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set player position to left bottom pixel
player = pygame.Rect((0, SCREEN_HEIGHT - 1, 1.5, 1.5))  # Increase the size of the player rectangle for better visibility

# Initialize enemy position (random)
enemy = pygame.Rect((random.randint(0, SCREEN_WIDTH - 1), random.randint(0, SCREEN_HEIGHT - 1), 1.5, 1.5))  # Increase the size of the enemy rectangle for better visibility

levels = [
    {"background": (0, 0, 0), "enemy": (255, 255, 255), "player": (0, 255, 0)},  
    {"background": (255, 255, 255), "enemy": (255, 0, 0), "player": (0, 0, 0)},  
    {"background": (255, 255, 0), "enemy": (0, 0, 255), "player": (0, 0, 0)},
    {"background": (0, 0, 100), "enemy": (255, 0, 0), "player": (0, 255, 0)},
    {"background": (100, 255, 100), "enemy": (255, 0, 0), "player": (0, 0, 0)},
    {"background": (255, 0, 0), "enemy": (0, 255, 0), "player": (0, 0, 0)},
]

current_level_index = 0  # Index to track the current level

def respawn_enemy():
    global current_level_index  # Access the global variable for the current level index
    enemy.x = random.randint(0, SCREEN_WIDTH - 1)
    enemy.y = random.randint(0, SCREEN_HEIGHT - 1)
    current_level_index = (current_level_index + 1) % len(levels)  # Move to the next level index

clock = pygame.time.Clock()

# Jumping related variables
y_velocity = 0
GRAVITY = 1

# Player movement speed and acceleration
movement_speed = 1
max_speed = 3
acceleration = 0.1

# Flag to control player movement
freeze_player = False
freeze_start_time = 0  # Variable to store the time when the player was frozen

# Define the font and size for the text
font = pygame.font.Font(None, 24)

# Flag to control the visibility of the info box
info_visible = False

# List to store the last positions of the player
last_positions = []

# Flag to control game state
game_intro = True
game_running = False

def game_intro_screen():
    intro = True
    while intro:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    intro = False
                    return
                elif event.key == pygame.K_i:
                    display_info()
        # Display introduction text
        intro_text = font.render("pyxel, a pygame", True, (255, 255, 255))
        intro_text2 = font.render("In this game you control a live pixel.", True, (255, 255, 255))
        intro_text3 = font.render("Your job is to replace dead pixels.", True, (255, 255, 255))
        intro_text4 = font.render("Press Enter to start. Press 'i' for information.", True, (255, 255, 255))
        screen.blit(intro_text, (SCREEN_WIDTH/2 - intro_text.get_width()/2, SCREEN_HEIGHT/2 - 50))
        screen.blit(intro_text2, (SCREEN_WIDTH/2 - intro_text2.get_width()/2, SCREEN_HEIGHT/2))
        screen.blit(intro_text3, (SCREEN_WIDTH/2 - intro_text3.get_width()/2, SCREEN_HEIGHT/2 + 50))
        screen.blit(intro_text4, (SCREEN_WIDTH/2 - intro_text4.get_width()/2, SCREEN_HEIGHT/2 + 100))

        pygame.display.update()
        clock.tick(15)

def display_info():
    global game_intro
    info = True
    while info:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    info = False
                    game_intro = False
                    return

        # Display information text
        info_text = font.render("Controls:", True, (255, 255, 255))
        info_text2 = font.render("A/D - Move left/right", True, (255, 255, 255))
        info_text3 = font.render("Up Arrow - Jump", True, (255, 255, 255))  # Change from Space to Up Arrow
        info_text4 = font.render("R - Restart", True, (255, 255, 255))
        info_text5 = font.render("Press Enter to start", True, (255, 255, 255))
        screen.blit(info_text, (SCREEN_WIDTH/2 - info_text.get_width()/2, SCREEN_HEIGHT/2 - 50))
        screen.blit(info_text2, (SCREEN_WIDTH/2 - info_text2.get_width()/2, SCREEN_HEIGHT/2))
        screen.blit(info_text3, (SCREEN_WIDTH/2 - info_text3.get_width()/2, SCREEN_HEIGHT/2 + 50))
        screen.blit(info_text4, (SCREEN_WIDTH/2 - info_text4.get_width()/2, SCREEN_HEIGHT/2 + 100))
        screen.blit(info_text5, (SCREEN_WIDTH/2 - info_text5.get_width()/2, SCREEN_HEIGHT/2 + 150))

        pygame.display.update()
        clock.tick(15)

game_intro_screen()

# Set game_running to True after intro screen
game_running = True

while game_running:
    screen.fill(levels[current_level_index]["background"])  # Fill the screen with the background color

    pygame.draw.rect(screen, levels[current_level_index]["enemy"], enemy)  # Draw enemy with updated color

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not freeze_player:  # K_UP for jumping
                y_velocity = -15  # Initial velocity for jumping
            elif event.key == pygame.K_r:  # Respawn enemy when 'R' key is pressed
                respawn_enemy()
            elif event.key == pygame.K_i:  # Toggle info box visibility when 'I' key is pressed
                info_visible = not info_visible

    key = pygame.key.get_pressed()
    if key[pygame.K_a] and player.left > 0 and not freeze_player:
        movement_speed += acceleration
        if movement_speed > max_speed:
            movement_speed = max_speed
        player.move_ip(-movement_speed, 0)
    elif key[pygame.K_d] and player.right < SCREEN_WIDTH and not freeze_player:
        movement_speed += acceleration
        if movement_speed > max_speed:
            movement_speed = max_speed
        player.move_ip(movement_speed, 0)
    else:
        movement_speed = 1  # Reset movement speed when keys are released

    # Handle jumping and gravity if player is not frozen
    if not freeze_player:
        # Store the current player position in the list
        last_positions.append(player.copy())
        # Keep only the last two positions
        if len(last_positions) > 5:
            del last_positions[0]

        player.y += y_velocity
        y_velocity += GRAVITY

        # Ensure the player stays within the screen bounds
        if player.y >= SCREEN_HEIGHT - 1:
            player.y = SCREEN_HEIGHT - 1
            y_velocity = 0

    # Check if the player is within range of 1 pixel from the enemy
    if not freeze_player and abs(player.x - enemy.x) <= 1 and abs(player.y - enemy.y) <= 1:
        player.x, player.y = enemy.x, enemy.y  # Set player position to enemy's position
        freeze_player = True  # Freeze the player's movement
        freeze_start_time = pygame.time.get_ticks()  # Record the time when the player was frozen

        
    pygame.draw.rect(screen, levels[current_level_index]["player"], player)  # Draw player after enemy

    # Check if 0.5 seconds has passed since the player was frozen, but less than 1 second
    if freeze_player and 500 <= pygame.time.get_ticks() - freeze_start_time < 1000:
        player_color = levels[current_level_index]["background"]  # Change player color to background color
        pygame.draw.rect(screen, player_color, player)  # Draw player with the new color


    # Check if one second has passed since the player was frozen
    if freeze_player and pygame.time.get_ticks() - freeze_start_time >= 1000:
        freeze_player = False  # Unfreeze the player
        respawn_enemy()  # Respawn the enemy


    # Draw the last two positions of the player only if player is not frozen
    if not freeze_player:
        for position in last_positions:
            pygame.draw.rect(screen, levels[current_level_index]["player"], position)

    # Draw info box if it is visible
    if info_visible:
        # Define info box dimensions and position
        info_box_width = 120
        info_box_height = 100
        info_box_x = SCREEN_WIDTH - info_box_width - 10  # 10 pixels from the right edge
        info_box_y = 10  # 10 pixels from the top edge

        # Draw the info box background
        pygame.draw.rect(screen, (255, 255, 255), (info_box_x, info_box_y, info_box_width, info_box_height))
        pygame.draw.rect(screen, (0, 0, 0), (info_box_x, info_box_y, info_box_width, info_box_height), 2)  # Black border

        # Render and draw the text
        text_surface1 = font.render("i - info", True, (0, 0, 0))  # Black text color
        text_surface2 = font.render("r - restart", True, (0, 0, 0))  # Black text color
        text_surface3 = font.render("<-a   d->", True, (0, 0, 0))  # Black text color
        text_surface4 = font.render("Up Arrow - jump", True, (0, 0, 0))  # Black text color
        screen.blit(text_surface1, (info_box_x + 10, info_box_y + 10))  # 10 pixels padding from left and top edges for the first line of text
        screen.blit(text_surface2, (info_box_x + 10, info_box_y + 30))  # 10 pixels padding from left and top edges for the second line of text
        screen.blit(text_surface3, (info_box_x + 10, info_box_y + 50))  # 10 pixels padding from left and top edges for the third line of text
        screen.blit(text_surface4, (info_box_x + 10, info_box_y + 70))  # 10 pixels padding from left and top edges for the fourth line of text

    pygame.display.update()

    clock.tick(60)

pygame.quit()
