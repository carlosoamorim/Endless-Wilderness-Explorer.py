import pygame
import math
import time
from config import *
from utils import *
from bullet import Bullet
from weapons.meatball import Meatball
from powerups.PowerUp import *
from weapons.falukorv import Falukorv


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # VISUAL VARIABLES
        self.image = pygame.image.load("images/Characters/Kalle_Postman_Right_1.1.png")

        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)
        
        self.image = pygame.image.load("images/Characters/Kalle_Postman_Right_1.1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 100))

        

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
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < height:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < width:
            self.rect.x += self.speed

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

