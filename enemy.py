import pygame
import random
import math
from config import width, height, enemy_size, fps

class Enemy(pygame.sprite.Sprite):
    HURT_IMAGE_DURATION = 500  # Duration to show hurt image in milliseconds

    def __init__(self, player, current_round):
        super().__init__()
        
        self.damage = 10
        self.health = 10
        self.speed = 5
        self.hurt_time = None
        self.frozen = False

        self.default = {
            "right": pygame.transform.scale(pygame.image.load("images/Characters/Enemy/enemy_right.png").convert_alpha(), enemy_size),
            "left": pygame.transform.scale(pygame.image.load("images/Characters/Enemy/enemy_left.png").convert_alpha(), enemy_size)
        }

        self.hurt = {
            "right": pygame.transform.scale(pygame.image.load("images/Characters/Enemy/enemy_hurt_right.png").convert_alpha(), (110, 120)),
            "left": pygame.transform.scale(pygame.image.load("images/Characters/Enemy/enemy_hurt_left.png").convert_alpha(), (110, 120))
        }

        self.affected = {
            "freeze": pygame.transform.scale(pygame.image.load("images/Characters/Enemy/enemy_freeze.png").convert_alpha(), (110, 120))
        }

        self.image = self.default["right"]
        self.image = pygame.transform.scale(self.image, enemy_size)

        self.active_image = self.default
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
        
        if self.frozen:
            self.image = self.affected["freeze"]
            self.active_image = self.affected
        elif self.hurt_time and pygame.time.get_ticks() - self.hurt_time > self.HURT_IMAGE_DURATION:
            self.image = self.default["right"]
            self.active_image = self.default
            self.hurt_time = None
        

    def take_damage(self, damage):

        print("Enemy took damage")  # Debug print statement
        if self.frozen is not True:
            self.image = self.hurt["right"]
            self.active_image = self.hurt
        self.health -= damage
        self.hurt_time = pygame.time.get_ticks()

    def freeze(self):
        self.frozen = True
        self.speed = 0

    def unfreeze(self):
        self.frozen = False
        self.image = self.default["right"]
        self.active_image = self.default
        self.speed = random.randint(2, 3)