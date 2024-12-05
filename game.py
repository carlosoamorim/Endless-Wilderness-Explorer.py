import random

import pygame
import time
from config import *
from player import *
from enemy import Enemy
from shed import shed
from PowerUp import *
import math
from game_over import game_over_screen
from Power_up_timer import Timer
from pause import Pause

def circle_collision(sprite1, sprite2):
    """Calculate distance between the two sprite centers."""
    distance = math.sqrt(
        (sprite1.rect.centerx - sprite2.rect.centerx) ** 2 +
        (sprite1.rect.centery - sprite2.rect.centery) ** 2
    )
    return distance < (sprite1.rect.width / 2 + sprite2.rect.width / 2)




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
    pygame.init()
    pygame.mixer.init()

    # Load and play music
    pygame.mixer.music.load("music/Undefeatable Epic Version.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # Background setup
    background = pygame.image.load("images/arena_background.webp")
    background = pygame.transform.scale(background, (width, height))

    # Screen setup
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Endless Wilderness Explorer")

    # Groups
    player_group = pygame.sprite.GroupSingle(player)
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    powers = pygame.sprite.Group()

    # Game variables
    clock = pygame.time.Clock()
    original_enemy_cooldown = fps * 2
    enemy_cooldown = original_enemy_cooldown
    damage_cooldown = 2
    last_damage_time = 0
    power_respawn = 0



    # Timers
    active_timer = Timer()  # Invincibility timer
    desspawn_timer = Timer()  # De-spawner timer

    running = True
    pause_game = Pause()
    font = pygame.font.Font(None, 36)

    # MAIN GAME LOOP
    while running:
        clock.tick(fps)
        screen.blit(background, (0, 0))  # Draw background
        # Power-ups
        gambling_untouch = random.randint(0, 1) #20, estas são as chances originais, caso alteradas: repor
        gambling_despawn = random.randint(0, 1) # 15
        gambling_slowdown = random.randint(0, 1) # 30
        untouch = Invincibility(48, 48, gambling_untouch, image= "images/invincible.png")
        despawn = Desspawn_machine(48, 48, gambling_despawn, image="images/order66.png")
        slowdown = Slow_respawn(48, 48, gambling_slowdown, image="images/despawn.png")
        # Pause trigger
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Pause game
                    pause_game.pause_game(screen, font, active_timer=active_timer, active_timer2=desspawn_timer)


        # Shooting bullets
        player.shoot(bullets)

        # Spawn enemies
        if enemy_cooldown <= 0:
            enemy = Enemy(player)
            enemies.add(enemy)
            enemy_cooldown = fps * 2 if not desspawn_timer.running else slowdown.power_affect_game(enemy_cooldown, enemies)  # Adjust spawn rate
        enemy_cooldown -= 1



        # Spawn power-ups
        if power_respawn <= 0:
            powers.add(untouch) if untouch.chance == 1 or untouch.chance == 10 else None
            powers.add(despawn) if despawn.chance == 1 or despawn.chance == 10 else None
            powers.add(slowdown) if slowdown.chance == 1 or slowdown.chance == 15 else None

            power_respawn = fps * 5
        power_respawn -= 1


        # Update sprites
        player_group.update()
        bullets.update()
        enemies.update(player)
        powers.update()

        # Handle power-up collision
        for power in powers:
            power_collide = pygame.sprite.spritecollide(power, player_group, False, circle_collision)
            for player in power_collide:
                if not player.power_active:  # Allow only if no power-up is active
                    if isinstance(power, Invincibility):
                        active_timer.start(10)
                        powers.remove(power)
                        power.power_affect_player(player)
                        player.power_active = "Invincibility"
                    elif isinstance(power, Desspawn_machine):
                        powers.remove(power)
                        power.power_affect_game(enemies)

                    elif isinstance(power, Slow_respawn):
                        desspawn_timer.start(15)
                        powers.remove(power)
                        player.power_active = "Slow respawn"

        # Check timers
        if active_timer.running and not active_timer.update():
            untouch.detransform(player)  # Revert invincibility
            player.power_active = False
        if desspawn_timer.running and not desspawn_timer.update():
            enemy_cooldown = original_enemy_cooldown  # Restore spawn rate
            player.power_active = False

        # Check if the player moved to the next area
        if player.rect.right >= width and not player.power_active:
            return "shed"
        # Draw sprites
        player_group.draw(screen)
        enemies.draw(screen)
        powers.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        # Draw timers
        if active_timer.running:
            remaining_time = active_timer.get_remaining_time()
            bar_width = int((remaining_time / active_timer.maximum) * 200)
            pygame.draw.rect(screen, black, (10, 40, 200, 20))
            pygame.draw.rect(screen, gold, (10, 40, bar_width, 20))

        if desspawn_timer.running:
            remaining_time = desspawn_timer.get_remaining_time()
            bar_width = int((remaining_time / desspawn_timer.maximum) * 200)
            pygame.draw.rect(screen, black, (10, 70, 200, 20))
            pygame.draw.rect(screen, green, (10, 70, bar_width, 20))



        # Handle bullet and enemy collisions
        for bullet in bullets:
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False, circle_collision)
            for enemy in collided_enemies:
                enemy.health -= 5
                bullet.kill()
                if enemy.health <= 0:
                    enemy.kill()

        # Handle player and enemy collisions
        for enemy in enemies:
            if pygame.sprite.spritecollide(enemy, player_group, False):
                current_time = time.time()
                if current_time - last_damage_time > damage_cooldown and not player.invincible:
                    player.health -= 10
                    player.image.fill(red)
                    last_damage_time = current_time
                    if player.health <= 0:
                        print("Game Over")
                        pygame.mixer.music.fadeout(2000)
                        pygame.time.wait(2000)
                        pygame.mixer.music.load("music/Sonic 1 Music_ Game Over.mp3")
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play()
                        game_over_screen()
                        return

        # Reset player color after damage cooldown
        if time.time() - last_damage_time > damage_cooldown and not player.invincible:
            player.image.fill(cute_purple)

        # Draw health bar
        pygame.draw.rect(screen, red, (10, 10, 200, 20))
        pygame.draw.rect(screen, green, (10, 10, player.health * 2, 20))
        health_text = font.render(f'Health: {player.health}', True, white)
        screen.blit(health_text, (220, 10))


        #Confirms the power up activation
        if player.power_active:
            active_power_text = font.render(f"Active Power-Up: {player.power_active}", True, white)
            screen.blit(active_power_text, (10, 100))

        pygame.display.flip()

    pygame.quit()
