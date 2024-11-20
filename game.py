from config import *
import math
import pygame
from player import Player
from bullet import Bullet

def execute_game():
    # Clock for controlling frame rate
    clock = pygame.time.Clock()

    # Screen type
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Endless Wilderness Explorer")

    # Player setup
    player = Player()
    player_group = pygame.sprite.Group()
    player_group.add(player)

    bullets = pygame.sprite.Group()

    
    running = True
    while running:
        clock.tick(fps)

        screen.fill(green)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Shooting
        player.shoot(bullets)

        # Update positions
        player_group.update()
        bullets.update()

        # Drawing the position
        player_group.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        
        pygame.display.flip()