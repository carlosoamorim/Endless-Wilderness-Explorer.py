from config import *
import math
import pygame
from player import Player
from bullet import Bullet
from enemy import Enemy
from shed import shed

def game_loop():
    player = Player()
    current_state = "main"
    
    while True:
        if current_state == "main":
            current_state = execute_game(player)
        elif current_state == "shed":
            current_state = shed(player)
    """ Used for different levels etc """

def execute_game(player: Player):
    # Clock for controlling frame rate
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((resolution))
    background = pygame.image.load("images/arena_background.webp")
    background = pygame.transform.scale(background, (width, height))

    # Screen type
    pygame.display.set_caption("Endless Wilderness Explorer")

    # Player setup
    player = Player()
    player_group = pygame.sprite.Group()
    player_group.add(player)

    bullets = pygame.sprite.Group()

    # Initialize enemies
    enemies = pygame.sprite.Group()
    enemy_spawn_timer = 0
    
    running = True
    while running:
        clock.tick(fps)

        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Shooting
        player.shoot(bullets)

        # Enemy spawning
        if enemy_spawn_timer <= 0:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            enemy_spawn_timer = 2 * fps

         # Collision detection
        for bullet in bullets:
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in collided_enemies:
                enemy.image.fill(glowing_light_red)
                enemy.health -= 5
                bullet.kill()
                if enemy.health <= 0:
                    enemy.kill()
        
        enemy_spawn_timer -= 1

        # Update positions
        player_group.update()
        bullets.update()
        enemies.update(player)

        # Checking if the user goes into the shed area
        if player.rect.right >= width:
            return "shed"

        # Drawing the objects
        player_group.draw(screen)
        enemies.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        
        pygame.display.flip()