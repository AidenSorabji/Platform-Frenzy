import pygame
import sys
import random
import pickle
import os
from pygame import mixer
import sound_module
import time

pygame.init()  # Initialize Pygame

def clear_screen():
    # Clear command for Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # Clear command for Mac/Linux
    else:
        _ = os.system('clear')

# Constants
WIDTH, HEIGHT = 1200, 600
FPS = 60
LIGHT_BLUE = (51, 153, 255)  # Light blue color
WHITE = (255, 255, 255)
ORANGE = (223, 162, 69)
GREY = (165, 165, 165)
BLACK = (0, 0, 0)

# Set display mode
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platform Frenzy")

# Player
player_size = 50
player_speed = 5
shift_speed_multiplier = 1.5
current_speed = player_speed
jump_velocity = -10
gravity = 0.7
knockback_speed = 2
air_acceleration_decay = 0.1

score_range = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
               110, 120, 130, 140, 150, 160, 170, 180, 190, 200]

# Stamina
max_stamina = 120
stamina_regeneration_rate = 1.0
stamina_depletion_rate = 1  # Adjusted rate

# Load player sprites
idle_sprite_right = pygame.image.load("idle_sprite_right.png").convert_alpha()
idle_sprite_left = pygame.image.load("idle_sprite_left.png").convert_alpha()
walk_sprite_right = pygame.image.load("walk_sprite_right.gif").convert_alpha()
walk_sprite_left = pygame.image.load("walk_sprite_left.gif").convert_alpha()
run_sprite_right = pygame.image.load("run_sprite_right.gif").convert_alpha()
run_sprite_left = pygame.image.load("run_sprite_left.gif").convert_alpha()
spin_sprite_right = pygame.image.load("spin_sprite_right.gif").convert_alpha()
spin_sprite_left = pygame.image.load("spin_sprite_left.gif").convert_alpha()

# Adjusted hitbox dimensions for each sprite
idle_sprite_right_rect = pygame.Rect(0, 0, 50, 50)
idle_sprite_left_rect = pygame.Rect(0, 0, 50, 50)
walk_sprite_right_rect = pygame.Rect(0, 0, 50, 50)
walk_sprite_left_rect = pygame.Rect(0, 0, 50, 50)
run_sprite_right_rect = pygame.Rect(0, 0, 50, 50)
run_sprite_left_rect = pygame.Rect(0, 0, 50, 50)
spin_sprite_right_rect = pygame.Rect(0, 0, 50, 50)
spin_sprite_left_rect = pygame.Rect(0, 0, 50, 50)

# Initialize player sprite
player_sprite = idle_sprite_right


# Platform class
class Platform:
    def __init__(self, x, y, width, height, texture):
        self.rect = pygame.Rect(x, y, width, height)
        self.texture = texture


# Platforms list
platforms = []

# Function to generate a new platform randomly


def generate_new_platform():
    if platforms:
        new_platform_x = platforms[-1].rect.right + random.randint(130, 230)
    else:
        new_platform_x = random.randint(50, 150)
    new_platform_y = random.randint(HEIGHT - 250, HEIGHT - 50)
    new_platform_width = random.randint(100, 200)
    new_platform_height = 20
    # Assign a random texture based on size
    texture_options = ["platform_texture_small.png",
                       "platform_texture_medium.png", "platform_texture_large.png"]
    texture = random.choice(texture_options)
    new_platform = Platform(new_platform_x, new_platform_y,
                            new_platform_width, new_platform_height, texture)
    platforms.append(new_platform)

# Function to clear existing platforms and generate new ones


def reset_and_generate_platforms():
    platforms.clear()
    for _ in range(5):
        generate_new_platform()


# Initialize the starting area
reset_and_generate_platforms()
player_x = platforms[0].rect.left + \
    (platforms[0].rect.width - player_size) // 4
player_y = platforms[0].rect.top - player_size - 10

# Load high score from file
high_score_file = "high_score.pkl"
if os.path.exists(high_score_file):
    with open(high_score_file, "rb") as f:
        highest_score = pickle.load(f)
else:
    # Create the high_score.pkl file with initial score 0
    highest_score = 0
    with open(high_score_file, "wb") as f:
        pickle.dump(highest_score, f)

# Load the background image
background_image = pygame.image.load("background.png").convert_alpha()
original_background_size = background_image.get_size()

# Precompute the scaled background
scaled_background = pygame.transform.smoothscale(background_image, (int(
    original_background_size[0] * 1), int(original_background_size[1] * 0.6)))

# Load the blur image #1
blur_image = pygame.image.load("blur_1.png").convert_alpha()
original_image_size = blur_image.get_size()

# Variables for image scale and position #1
image_scale = 0.5
image_position = [WIDTH // 2 - (original_image_size[0] * image_scale) // 2, HEIGHT // 2 - (
    original_image_size[1] * image_scale) // 2 + 3]  # Adjusted Y position

# Precompute the scaled image #1
scaled_image = pygame.image.load("blur_1.png").convert_alpha()
scaled_image = pygame.transform.smoothscale(scaled_image, (int(
    original_image_size[0] * image_scale), int(original_image_size[1] * image_scale)))

# Load the blur image #2
blur_image_r = pygame.image.load("blur_2.png").convert_alpha()
original_image_size_r = blur_image_r.get_size()

# Variables for image scale and position #2
image_scale_r = 0.5
image_position_r = [WIDTH // 2 - (original_image_size_r[0] * image_scale_r) // 2, HEIGHT // 2 - (
    original_image_size_r[1] * image_scale_r) // 2 + 3]  # Adjusted Y position

# Precompute the scaled image #2
scaled_image_r = pygame.image.load("blur_2.png").convert_alpha()
scaled_image_r = pygame.transform.smoothscale(scaled_image_r, (int(
    original_image_size_r[0] * image_scale_r), int(original_image_size_r[1] * image_scale_r)))

# Font
font = pygame.font.Font(None, 24)

# Initialize on_ground, knockback, falling_through_platform, acceleration, and health
on_ground = True
knockback = 0
falling_through_platform = False
acceleration = 0

# Initialize stamina
stamina = max_stamina

# Flag to indicate if the player can sprint
can_sprint = True

# Point counter
score = 0

# Parallax variables
initial_background_x = -194
background_x = -194  # Adjusted initial position
background_speed = 1  # Adjusted speed

# Flag to disable controls when touching the bottom
disable_controls = False

continue_on_ground = 0
on_death = 0
music_play_now = 0
hit_lefty = 0
stamina_hehe = False


# Game loop
clock = pygame.time.Clock()
sound_module.background_sound()
start_time = time.time()

clear_screen()
print("""------------------------------------------
|   A - Move Left       D - Move Right   |
|                                        |
|             Space - Jump               |
|                                        |
|     R - Reset            0 - Quit      |
------------------------------------------""")


while True:
    sound_module.background_sound()

    keys = pygame.key.get_pressed()

    # Disable controls when touching the bottom
    if player_y + player_size >= HEIGHT:
        disable_controls = True
        if on_death == 0:
            sound_module.death_sound()
            sound_module.music_pause()
            music_play_now += 1
            on_death += 1
        if on_death == 1:
            pass

    # Disable controls when touching the bottom
    if player_y + player_size >= HEIGHT:
        disable_controls = True
        if on_death == 0:
            sound_module.death_sound()
            sound_module.music_pause()
            music_play_now += 1
            on_death += 1
        if on_death == 1:
            pass

    # Move left and right
    if keys[pygame.K_a] and player_x > 0 and not disable_controls:
        if on_ground:
            acceleration = -current_speed
        else:
            acceleration -= air_acceleration_decay
        player_x += acceleration
        background_x += background_speed  # Shift background right when moving left

    if keys[pygame.K_d] and not disable_controls:
        if on_ground:
            acceleration = current_speed
        else:
            acceleration += air_acceleration_decay
        player_x += acceleration
        background_x -= background_speed  # Shift background left when moving right

    if keys[pygame.K_0]:
        with open(high_score_file, "wb") as f:
            pickle.dump(highest_score, f)
        pygame.quit()
        sys.exit()

    # Hold down the shift key to increase speed temporarily
    if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and not disable_controls:
        if can_sprint and stamina > 0:
            current_speed = player_speed * shift_speed_multiplier
            stamina -= stamina_depletion_rate
        else:
            if stamina_hehe == False:
                sound_module.stamina_zero_sound()
                stamina_hehe = True
            if stamina_hehe == True:
                pass
            current_speed = player_speed

    else:
        current_speed = player_speed
        if stamina < max_stamina:
            if stamina_hehe == False:
                pass
            if stamina_hehe == True:
                stamina_hehe = False
            stamina += stamina_regeneration_rate
            can_sprint = True  # Enable sprinting when stamina is fully replenished

    # Jump
    if on_ground and keys[pygame.K_SPACE] and not disable_controls:
        continue_on_ground == 0
        sound_module.jump_sound()
        on_ground = False
        jump_velocity = -12
        continue_on_ground -= 1

    # Respawn (R key)
    if keys[pygame.K_r]:
        end_time = time.time()
        if music_play_now == 1:
            sound_module.music_play()
            music_play_now -= 1
        if music_play_now == 0:
            pass
        if hit_lefty == 1:
            hit_lefty -= 1
        if hit_lefty == 0:
            pass
        sound_module.restart_sound()
        disable_controls = False
        reset_and_generate_platforms()
        player_x = platforms[0].rect.left + \
            (platforms[0].rect.width - player_size) // 4
        player_y = platforms[0].rect.top - player_size - 10
        jump_velocity = 0
        stamina = max_stamina
        can_sprint = True
        if on_death == 1:
            on_death -= 1
        if on_death == 0:
            pass
        score = 0  # Reset score when respawning
        background_x = initial_background_x  # Reset background position
        time.sleep(0.1)

    # Apply gravity and update velocity
    player_y += jump_velocity
    jump_velocity += gravity

    # Check for collision with platforms
    on_ground = False
    falling_through_platform = False
    for platform in platforms:
        if player_x < platform.rect.right and player_x + player_size > platform.rect.left and \
                player_y + player_size >= platform.rect.top and player_y <= platform.rect.bottom:
            if jump_velocity > 0:
                if continue_on_ground == 0:
                    sound_module.land_sound()
                    continue_on_ground += 1
                if continue_on_ground == 1:
                    pass
                on_ground = True
                player_y = platform.rect.top - player_size
                jump_velocity = 0
            else:
                if player_y + player_size > platform.rect.bottom:
                    player_y = platform.rect.bottom
                    jump_velocity = 0
                    falling_through_platform = True
                else:
                    if player_y + player_size <= platform.rect.bottom:
                        player_y += knockback_speed
                    else:
                        player_x -= knockback_speed
                        knockback = knockback_speed

    # Apply knockback effect
    if knockback > 0:
        player_x += knockback
        knockback -= 1

    # Check if the player is at the right edge of the window
    if player_x > WIDTH - player_size:
        score += 1
        if score in score_range:
            sound_module.win_sound10()
        elif score not in score_range:
            sound_module.win_sound()
        highest_score = max(highest_score, score)
        saved_velocity = jump_velocity
        saved_acceleration = acceleration
        reset_and_generate_platforms()
        player_x = platforms[0].rect.left + \
            (platforms[0].rect.width - player_size) // 4
        player_y = platforms[0].rect.top - player_size
        jump_velocity = saved_velocity
        acceleration = saved_acceleration
        background_x = initial_background_x  # Reset background position

    # Check if the player touches the left part of the window
    if player_x <= 0:
        if hit_lefty == 0:
            sound_module.hit_left_wall()
            hit_lefty += 1
        if hit_lefty == 1:
            pass

    # Clear the screen
    screen.fill(WHITE)

    # Draw the background with blur
    screen.blit(scaled_background, (background_x, -17))

    # Draw the platforms with textures
    for platform in platforms:
        platform_texture = pygame.image.load(platform.texture).convert_alpha()
        # Stretch the texture if the platform is not of standard size
        platform_texture = pygame.transform.smoothscale(
            platform_texture, (platform.rect.width, platform.rect.height))
        screen.blit(platform_texture, platform.rect)
    # Reset acceleration when player is on the ground and not pressing movement keys
    if on_ground and not (keys[pygame.K_a] or keys[pygame.K_d]):
        acceleration = 0

    # Draw the player based on direction and action
    if on_ground:
        if acceleration > 5.2:
            player_sprite = run_sprite_right
        elif acceleration < -5.2:
            player_sprite = walk_sprite_left
        elif -5.2 <= acceleration <= 5.2:  # No horizontal movement
            if acceleration > 0:
                player_sprite = run_sprite_right
            elif acceleration < 0:
                player_sprite = run_sprite_left
            else:
                player_sprite = idle_sprite_right  # Default to right idle sprite
    else:  # Player is in the air
        if acceleration > 0:
            player_sprite = spin_sprite_right
        elif acceleration < 0:
            player_sprite = spin_sprite_left
        else:
            player_sprite = spin_sprite_right

    screen.blit(player_sprite, (player_x, player_y))

    # Draw the scaled image
    screen.blit(scaled_image, image_position)

    # Draw the scaled image
    screen.blit(scaled_image_r, image_position_r)

    # Draw the stamina bar
    pygame.draw.rect(screen, GREY, (WIDTH - 10 -
                     max_stamina, 13.5, max_stamina, 13.5))
    pygame.draw.rect(screen, "#206ca4", (WIDTH - 10 -
                     max_stamina, 13.5, stamina, 13.5))

    # Draw the "Stamina:" text
    stamina_text = font.render("Stamina:", True, BLACK)
    screen.blit(stamina_text, (WIDTH - 205, 11.65))

    # Draw the point counter
    score_text = font.render(f"Points: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Draw the highest score
    highest_score_text = font.render(
        f"Highest Score: {highest_score}", True, BLACK)
    screen.blit(highest_score_text, (10, 40))

    pygame.display.flip()
    clock.tick(FPS)
