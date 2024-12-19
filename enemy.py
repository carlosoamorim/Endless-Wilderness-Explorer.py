from config import *
import pygame
import random
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, current_round):
        super().__init__()
        self.damage = 10
        
        enemy_images = [
            "images/characters/enemies/dinossauro.png",  # Round 1
            "images/characters/enemies/flor.png",    # Round 2
            "images/characters/enemies/ave.png",    # Round 3
            "images/characters/enemies/borboleta.png",   # Round 4
            "images/characters/enemies/peixe.png",   # Round 5
            "images/characters/enemies/tubarao.png",   # Round 6
            "images/characters/enemies/dragao.png",   # Round 7
            "images/characters/enemies/robo.png",   # Round 8
            "images/characters/enemies/alien.png",   # Round 9
            "images/characters/enemies/neve.png",   # Round 10
            "images/characters/enemies/grinch.png",   # Round 11
            "images/characters/enemies/elfo.png",   # Round 12

        ]

        # Select the image based on the current round
        self.image = pygame.image.load(enemy_images[(current_round - 1) % len(enemy_images)]).convert_alpha()

        # Scale the image to the desired size
        self.image = pygame.transform.scale(self.image, (60, 60))

        # Get the rectangle for positioning
        self.rect = self.image.get_rect()
        # Ensure the enemy does not spawn at the same position as the player
        valid_position = False
        while not valid_position:
            # Start the enemy at a random valid location on the screen
            self.rect.x = random.randint(0, width - self.rect.width)
            self.rect.y = random.randint(0, height - self.rect.height)
            # Check if the enemy overlaps with the player's position
            if not self.rect.colliderect(player.rect):
                valid_position = True
        # Set a random initial speed for the enemy
        self.speed = random.randint(2, 3)

        # Set the health of the enemy
        self.health = 10

    def update(self, player):
        """
        Update the enemy's position to move towards the player.
        """
        # Calculate the direction towards the player
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y

        # Calculate the direction in radians
        direction = math.atan2(dy, dx)

        # Move the enemy towards the player
        self.rect.x += int(self.speed * math.cos(direction))
        self.rect.y += int(self.speed * math.sin(direction))
