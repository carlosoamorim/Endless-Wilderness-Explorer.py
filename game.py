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
from rounds import Rounds
from chest import Chest
from store import *
from save_files import *


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
            next_state = execute_game(player)
            if next_state is None:
                break
            current_state = next_state
        elif current_state == "shed":
            current_state = shed(player)
        elif current_state == "store":
            current_state = load_store(player)


def execute_game(player):
    pygame.init()
    pygame.mixer.init()

    # Load and play music
    pygame.mixer.music.load("music/Space Harrier Music - MAIN THEME.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    # Background setup
    background = pygame.transform.scale(pygame.image.load("images/backgrounds/ikea_arena.webp"), (width, height))

    # Screen setup
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Endless Wilderness Explorer")

    # Groups
    player_group = pygame.sprite.GroupSingle(player)
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    powers = pygame.sprite.Group()
    chests = pygame.sprite.Group()

    # Game variables
    clock = pygame.time.Clock()
    original_enemy_cooldown = fps * 2
    enemy_cooldown = original_enemy_cooldown
    damage_cooldown = 2
    last_damage_time = 0
    power_respawn = 0


    chest = Chest(width, height, spawn_chance=0.9)
    if chest.spawned:
        chests.add(chest)

    #round system:
    # Initialize round variables
    current_round = 1
    enemies_per_round = 5  # Number of enemies to spawn each round
    enemies_spawned = 0  # Number of enemies spawned in the current round
    round_active = True  # Indicates if the current round is active
    rounds = Rounds()
    current_round, enemies_per_round = load_game(player)


    # Timers
    active_timer = Timer()  # Invincibility timer
    slowdown_timer = Timer()  # De-spawner timer
    kboom_timer = Timer()
    heal_timer = Timer()
    freeze_timer = Timer()
    running = True
    pause_game = Pause()
    font = pygame.font.Font(None, 36)

    # Pre-round countdown and shed exploration
    rounds.pre_round_countdown(screen, font, player,current_round)

    # MAIN GAME LOOP
    while running:
        clock.tick(fps)
        screen.blit(background, (0, 0))  # Draw the current background
        #rounds systems:

        # Power-ups
        gambling_untouch = random.randint(0, 20) #20, estas são as chances originais, caso alteradas: repor
        gambling_despawn = random.randint(0, 15) # 15
        gambling_slowdown = random.randint(0, 30) # 30
        gambling_heal = random.randint(0, 5) # 5
        gambling_freeze = random.randint(0, 45)

        untouch = Invincibility(48, 48, gambling_untouch, image= "images/powerups/snus-powerup.png")
        despawn = Desspawn_machine(48, 48, gambling_despawn, image="images/powerups/mjolnir.png")
        slowdown = Slow_respawn(48, 48, gambling_slowdown, image="images/powerups/surstromming.png")
        healup = Heal(48, 48, gambling_heal, image="images/powerups/blabarssoppa.png")
        chaos_control = Freeze(48,48, gambling_freeze, image="images/powerups/fika-powerup.png")

        # Pause trigger
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Pause game
                    pause_game.pause_game(screen, font, active_timer=active_timer, active_timer2=slowdown_timer,
                                          active_timer3=kboom_timer,
                                          active_timer4=heal_timer, active_timer5= freeze_timer)

        # Shooting bullets
        if player.nearest_enemy(enemies) is not None:
            player.attack(bullets, enemies)

        # Spawn enemies if the round is active
        if round_active:
            if enemy_cooldown <= 0 and enemies_spawned < enemies_per_round:

                enemy = Enemy(player,current_round)
                enemies.add(enemy)
                enemy_cooldown = fps * 2 if not slowdown_timer.update() else slowdown.power_affect_game(enemy_cooldown, enemies)
                if freeze_timer.update():
                    enemy_cooldown = chaos_control.power_affect_game(enemy_cooldown, enemies)
                enemies_spawned += 1
            enemy_cooldown -= 1

            # Check if all enemies are defeated to end the round
            if enemies_spawned == enemies_per_round and len(enemies) == 0:
                player.current_health = player.max_health  # Restore player health
                round_active = False  # End the current round
        # Transition to the next round if round is not active
        if not round_active:

            # Check if the player has reached the final round
            if current_round == 12:
                # Display the win message and exit the game

                # Change music to victory theme
                pygame.mixer.music.stop()
                pygame.mixer.music.load("music/victory_theme.mp3")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)

                # Load and display the victory image
                victory_image = pygame.image.load("images/WIN.png").convert_alpha()
                victory_image = pygame.transform.scale(victory_image, resolution)
                screen.blit(victory_image, (0, 0))

                # Display the victory message
                font = pygame.font.Font(None, 72)
                rounds.display_round_message("Congratulations! You Won!", screen, font)
                pygame.display.flip()

                pygame.time.wait(5000) # Wait for 5 seconds before quitting
                reset_save()
                pygame.quit()
                return

            rounds.display_round_message(f"Round {current_round} Complete!", screen, font)
            pygame.display.flip()
            # Return to the shed
            current_round += 1
            enemies_per_round += 2
            rounds.increase_difficulty(enemies)
            save_game(player, current_round, enemies_per_round)
            pygame.time.wait(2000)
            rounds.pre_round_countdown(screen, font, player, current_round)

            enemies_spawned = 0  # Reset enemy spawn counter
            round_active = True  # Activate the next round

        # Spawn power-ups
        if power_respawn <= 0:
            powers.add(untouch) if untouch.chance == 20 else None
            powers.add(despawn) if despawn.chance == 15 else None
            powers.add(slowdown) if  slowdown.chance == 30 else None
            powers.add(healup) if  healup.chance == 5 else None
            powers.add(chaos_control) if chaos_control.chance == 45 else None
            power_respawn = fps * 5
        power_respawn -= 1

        # Update sprites
        player_group.update()
        bullets.update()
        enemies.update(player)
        chests.update(player_group, 720, 720)

        # Set nearest enemy as target
        for bullet in bullets:
            if bullet.direction == 0:
                bullet.direction = player.nearest_enemy_angle(enemies)

        # Check for bullet-enemy collisions
        for bullet in bullets:
            if bullet.collide(enemies):
                for enemy in enemies:
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                        player.wallet_time(player)
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
                        kboom_timer.start(3)
                        power.power_affect_game(enemies)
                        player.power_active = "Kboom"
                    elif isinstance(power, Slow_respawn):
                        slowdown_timer.start(15)
                        powers.remove(power)
                        player.power_active = "Slow respawn"

                    elif isinstance(power, Heal):
                        heal_timer.start(5)
                        powers.remove(power)
                        power.power_affect_player(player)
                        player.power_active = "Healing"


                    elif isinstance(power, Freeze):
                        freeze_timer.start(10)
                        powers.remove(power)
                        player.power_active ="Coffee Break"

        # Check timers
        if active_timer.running and not active_timer.update():
            untouch.detransform(player)  # Revert invincibility
            player.power_active = False
        if slowdown_timer.running and not slowdown_timer.update():
            enemy_cooldown = original_enemy_cooldown  # Restore spawn rate
            player.power_active = False

        if kboom_timer.running and not kboom_timer.update():
            player.power_active = False

        if heal_timer.running and not heal_timer.update():
            player.power_active = False
            healup.detransform(player)

        if freeze_timer.running and not freeze_timer.update():
            player.power_active = False
            enemy_cooldown = original_enemy_cooldown


        # Draw sprites
        player_group.draw(screen)
        enemies.draw(screen)
        chests.draw(screen)
        powers.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)


        # Draw timers
        if freeze_timer.running:
            remaining_time = freeze_timer.get_remaining_time()
            bar_width = int((remaining_time/freeze_timer.maximum)*200)
            pygame.draw.rect(screen, black, (10, 40, 200, 20))
            pygame.draw.rect(screen, white, (10,40, bar_width, 20))
            if freeze_timer.get_remaining_time() == 0:
                for enemy in enemies:
                    enemy.unfreeze()

        if active_timer.running:
            remaining_time = active_timer.get_remaining_time()
            bar_width = int((remaining_time / active_timer.maximum) * 200)
            pygame.draw.rect(screen, black, (10, 40, 200, 20))
            pygame.draw.rect(screen, gold, (10, 40, bar_width, 20))

        if slowdown_timer.running:
            remaining_time = slowdown_timer.get_remaining_time()
            bar_width = int((remaining_time / slowdown_timer.maximum) * 200)
            pygame.draw.rect(screen, black, (10, 70, 200, 20))
            pygame.draw.rect(screen, green, (10, 70, bar_width, 20))

        if kboom_timer.running:
            remaining_time = kboom_timer.get_remaining_time()
            bar_width = int((remaining_time/kboom_timer.maximum) * 200)
            pygame.draw.rect(screen, black, (10, 40, 200, 20))
            pygame.draw.rect(screen, ikea_blue, (10, 40, bar_width, 20))

        if heal_timer.running:
            remaining_time = heal_timer.get_remaining_time()
            bar_width = int((remaining_time / heal_timer.maximum) * 200)
            pygame.draw.rect(screen, black, (10, 70, 200, 20))
            pygame.draw.rect(screen, cute_purple, (10, 70, bar_width, 20))

        # Handle bullet and enemy collisions
        for bullet in bullets:
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False, circle_collision)
            for enemy in collided_enemies:
                bullet.collide(collided_enemies)
                if enemy.health <= 0:
                    enemy.kill()

        # Handle player and enemy collisions
        # Handle player and enemy collisions
        for enemy in enemies:
            if pygame.sprite.spritecollide(enemy, player_group, False):
                current_time = time.time()

                # Check if enough time has passed since the last damage and player is not invincible
                if (current_time - last_damage_time > damage_cooldown) and not player.is_invincible:
                    player.take_damage(enemy.damage)
                    last_damage_time = current_time

                    # Debugging logs
                    print(f"Player health: {player.current_health}")
                    print(f"Enemy damage: {enemy.damage}")


                    if player.current_health <= 0:
                        print("Game Over")
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("music/Space Harrier Music - MAIN THEME.mp3")
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play()
                        pygame.time.wait(5000)  # Wait for music to play
                        reset_save()
                        game_over_screen()
                        save_game(player, current_round, enemies_per_round)
                        return

        # Draw health bar
        pygame.draw.rect(screen, red, (10, 10, 200, 20))
        pygame.draw.rect(screen, green, (10, 10, player.current_health*2, 20))
        health_text = font.render(f'Health: {player.current_health}', True, white)
        screen.blit(health_text, (220, 10))

        #draw wallet:
        wallet_text = font.render(f"Wallet: {player.wallet}", True, white)
        screen.blit(wallet_text, (220, 50))
        # Draw round number
        round_text = font.render(f"Round: {current_round}", True, white)
        screen.blit(round_text, (10, 40))

        #Confirms the power up activation
        if player.power_active:
            active_power_text = font.render(f"Active Power-Up: {player.power_active}", True, white)
            screen.blit(active_power_text, (10, 100))
        ##print(f"Round: {current_round}, Enemies Left: {len(enemies)}, Spawned: {enemies_spawned}/{enemies_per_round}, Round Active: {round_active}")

        pygame.display.flip()

    pygame.quit()