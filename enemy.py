from config import *
import pygame
import random
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, current_round):
        super().__init__()
        self.damage = 10
        self.health = 10
        self.speed = 5


        self.default = {
            "right": pygame.image.load("images/Characters/Enemy/enemy_right.png").convert_alpha(),
            "left": pygame.image.load("images/Characters/Enemy/enemy_left.png").convert_alpha()
        }

        self.hurt = {
            "right": pygame.image.load("images/Characters/Enemy/enemy_hurt_right.png").convert_alpha(),
            "left": pygame.image.load("images/Characters/Enemy/enemy_hurt_right.png").convert_alpha()
        }

        self.affected = {
            "freeze": pygame.image.load("images/Characters/Enemy/enemy_freeze.png").convert_alpha()
        }

        self.image = self.default["right"]
        self.image = pygame.transform.scale(self.image, (enemy_size))

        self.active_image = self.default
        self.rect = self.image.get_rect()

        # Select the image based on the current round
        #self.image = pygame.image.load(enemy_images[(current_round - 1) % len(enemy_images)]).convert_alpha()


        # Get the rectangle for positioning

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

    def take_damage(self, damage):

        self.health -= damage