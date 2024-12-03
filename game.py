import pygame
import time
from config import *
from player import Player
from enemy import Enemy
from shed import shed


from game_over import game_over_screen


def game_loop():
    # Initialize the player
    player = Player()

    # Start in the main area
    current_state = "main"

    # Endless game loop
    while True:
        if current_state == "main":
            current_state = execute_game(player)
        elif current_state == "shed":
            current_state = shed(player)

def execute_game(player):
    # SETUP:
    pygame.init()

    # Initialize the mixer for sound
    pygame.mixer.init()

    # Load the music file
    pygame.mixer.music.load("music/Undefeatable Epic Version.mp3")
    # Set volume (optional)
    pygame.mixer.music.set_volume(0.5)  # Volume ranges from 0.0 to 1.0

    # Play the music
    pygame.mixer.music.play(-1)
    # Background
    background = pygame.image.load("images/arena_background.webp")
    background = pygame.transform.scale(background, (width, height))

    # Screen setup
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Endless Wilderness Explorer")

    # Groups
    player_group = pygame.sprite.GroupSingle(player)
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # Game variables
    clock = pygame.time.Clock()
    enemy_cooldown = 0
    damage_cooldown = 1  # Cooldown in seconds
    last_damage_time = 0
    running = True

    # Fonts
    font = pygame.font.Font(None, 36)

    # MAIN GAME LOOP
    while running:
        clock.tick(fps)
        screen.blit(background, (0, 0))  # Draw background

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Shooting bullets
        player.attack(bullets)

        # Spawn enemies
        if enemy_cooldown <= 0:
            enemy = Enemy()
            enemies.add(enemy)
            enemy_cooldown = fps * 2  # 2 seconds cooldown
        enemy_cooldown -= 1

        # Update all sprites
        player_group.update()
        bullets.update()
        enemies.update(player)

        # Check if the player moved to the next area
        if player.rect.right >= width:
            return "shed"

        # Draw sprites
        player_group.draw(screen)
        enemies.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        # Check for collisions between player and enemies
        for enemy in enemies:
            if pygame.sprite.spritecollide(enemy, player_group, False):
                current_time = time.time()
                if current_time - last_damage_time > damage_cooldown:
                    player.health -= 25
                    player.image.fill(red)
                    last_damage_time = current_time
                    if player.health <= 0:
                        print("Game Over")

                        # Stop or fade out the current music
                        pygame.mixer.music.fadeout(2000)  # Fade out over 2 seconds
                        pygame.time.wait(2000)  # Wait for the fadeout to complete (non-blocking)

                        # Load and play the game over music
                        pygame.mixer.music.load("music/Sonic 1 Music_ Game Over.mp3")
                        pygame.mixer.music.set_volume(0.5)  # Adjust volume if needed
                        pygame.mixer.music.play()  # Play the new music

                        # Call the game over screen
                        game_over_screen()
                        return

        # Reset player color after taking damage
        if time.time() - last_damage_time > damage_cooldown:
            player.image.fill(blue)

        # Draw health bar
        pygame.draw.rect(screen, red, (10, 10, 200, 20))  # Red background
        pygame.draw.rect(screen, green, (10, 10, player.health*2, 20))  # Green health bar
        health_text = font.render(f'Health: {player.health}', True, white)
        screen.blit(health_text, (220, 10))

        pygame.display.flip()

    pygame.quit()



