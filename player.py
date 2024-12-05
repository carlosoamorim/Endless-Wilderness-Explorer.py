import pygame
import math
import time
from config import *
from utils import *
from bullet import Bullet
from PowerUp import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # VISUAL VARIABLES
        self.image = pygame.Surface(player_size)
        self.image.fill(cute_purple)
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)

        # GAMEPLAY VARIABLES
        self.speed = 5
        self.health = 100
        self.bullet_cooldown = 0
        self.power_active = False
        self.invincible = False


    def update(self):
        """Handle player movement with boundary checks."""
        keys = pygame.key.get_pressed()
        self.move(keys)

    def move(self, keys):
        """Move the player within screen boundaries."""
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < height:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < width:
            self.rect.x += self.speed

    def shoot(self, bullets):
        """Shoot bullets in all directions."""
        if self.bullet_cooldown <= 0:
            for angle in [0, math.pi, math.pi / 2, 3 * math.pi / 2]:
                bullet = Bullet(self.rect.centerx, self.rect.centery, angle)
                bullets.add(bullet)
            self.bullet_cooldown = fps  # Reset cooldown
        elif self.bullet_cooldown > 0:
            self.bullet_cooldown -= 1


class Invincibility(PowerUp):
    def __init__(self, power_box_weight, power_box_height, chance, image):
        super().__init__("Invincibility", power_box_weight, power_box_height, chance, image)

    def power_affect_player(self, player):
        """ºinvicible activate, with this variable I deactivated the damage system."""
        player.invincible = True

        player.image.fill(gold)  # Change color to indicate invincibility

    def detransform(self, player):
        """Go back to normal."""
        player.image.fill(cute_purple)  # Reset to original color
        player.invincible = False
        player.power_active = False
    def power_affect_game(self, target, target2):
        pass