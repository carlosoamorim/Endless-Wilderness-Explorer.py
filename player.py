import pygame
import math
import time
from config import *
from utils import *
from bullet import Bullet
from meatball import Meatball
from PowerUp import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # VISUAL VARIABLES
        self.image_right = pygame.image.load(r"images\Characters\Kalle_Postman_Right_1.1.png").convert_alpha()
        self.image_left = pygame.image.load(r"images\Characters\Kalle_Postman_Left_1.1.png").convert_alpha()
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)

        # GAMEPLAY VARIABLES
        self.speed = 5
        self.health = 100
        self.weapon = Meatball()
        self.bullet_cooldown = 0
        self.power_active = False
        self.invincible = False
        self.heal = False
        self.wallet = 0
    def update(self):
        """Handle player movement with boundary checks."""
        keys = pygame.key.get_pressed()
        self.move(keys)

    def move(self, keys):
        """Move the player within screen boundaries."""
        if keys[pygame.K_a] and self.rect.left > 0:  # Moving left
            self.rect.x -= self.speed
            self.image = self.image_left
        elif keys[pygame.K_d] and self.rect.right < width:  # Moving right
            self.rect.x += self.speed
            self.image = self.image_right

        if keys[pygame.K_w] and self.rect.top > 0:  # Moving up
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < height:  # Moving down
            self.rect.y += self.speed

    def money_time(self, player):
        player.wallet += 5
    def attack(self, bullets, enemies):
        bullet = self.weapon.fire(self.rect.centerx, self.rect.centery, self.nearest_enemy_angle(enemies))
        if bullet:
            bullets.add(bullet)

    def nearest_enemy(self, enemies):
        nearest_enemy = None
        nearest_distance = float("inf")
        for enemy in enemies:
            distance = math.hypot(enemy.rect.x - self.rect.x, enemy.rect.y - self.rect.y)
            if distance < nearest_distance:
                nearest_enemy = enemy
                nearest_distance = distance
        return nearest_enemy

    def nearest_enemy_angle(self, enemies):
        nearest_enemy_angle = 0
        nearest_enemy = self.nearest_enemy(enemies)
        if nearest_enemy is not None:
            nearest_enemy_angle = math.degrees(math.atan2(nearest_enemy.rect.y - self.rect.y, nearest_enemy.rect.x - self.rect.x))
        return nearest_enemy_angle


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
