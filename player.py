import pygame
import math
from config import *
from utils import *
from power_up import *

from lingonberry import Lingonberry
from meatball import Meatball
from falukorv import Falukorv


class Player(pygame.sprite.Sprite):
    HURT_IMAGE_DURATION = fps * 10
    def __init__(self):
        super().__init__()
        self.speed = 5
        self.max_health = 100
        self.current_health = self.max_health

        self.weapon = Lingonberry()
        self.bullet_cooldown = 0
        self.power_active = False
        self.is_invincible = False
        self.heal = False
        self.hurt_time = None
        # Preload all images for efficiency
        self.image = pygame.Surface(player_size)
        self.wallet = 0

        self.default = {
            "right": pygame.image.load("images/Characters/Kalle/Kalle_Postman_Right_1.1.png"),
            "left": pygame.image.load("images/Characters/Kalle/Kalle_Left.png")
            }       

        self.invincible = {
            "right": pygame.image.load("images/characters/player/Kalle_Postman_Right_invincible1.1.png"),
            "left": pygame.image.load("images/characters/player/Kalle_Postman_Left_invincible1.1.png")
            }
        
        self.hurt = {
            "left":pygame.image.load("images/characters/player/Kalle_Hurt_Left.png"),
            "right":pygame.image.load("images/characters/player/Kalle_Hurt_Right.png")

            }

        self.healing = {
            "left": pygame.image.load("images/characters/player/Kalle_Right_heal_left.png"),
            "right": pygame.image.load("images/characters/player/Kalle_Right_heal_right.png")
        }

        # Default settings
        self.image = self.default["right"]
        self.active_image = self.default
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)

        self.prev_position = self.rect.topleft 
        

    def update(self):
        keys = pygame.key.get_pressed()
        self.move(keys)

        if self.is_invincible:
            self.image = self.invincible["right"]
            self.active_image = self.invincible
        if self.hurt_time and pygame.time.get_ticks() - self.hurt_time > self.HURT_IMAGE_DURATION:
            self.image = self.default["right"]
            self.active_image = self.default
            self.hurt_time = None

    def move(self, keys):
        self.prev_position = self.rect.topleft  # Save position before moving
        
        if keys[pygame.K_a] and self.rect.left > 0:  # Move left
            self.rect.x -= self.speed
            self.image = self.active_image["left"]
            
        elif keys[pygame.K_d] and self.rect.right < width:  # Move right
            self.rect.x += self.speed
            self.image = self.active_image["right"]

        if keys[pygame.K_w] and self.rect.top > 0:  # Move up
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < height:  # Move down
            self.rect.y += self.speed
            
    def revert_position(self):
        self.rect.topleft = self.prev_position
            
    def wallet_time(self, player):
        player.wallet += 5
    def take_damage(self, damage):
        """Reduce the player's health by the given amount."""
        if not self.is_invincible:
            self.active_image = self.hurt
            self.current_health -= damage
            self.hurt_time = pygame.time.get_ticks()  # Record the time when hurt
            print("Player health:", self.current_health)


    def attack(self, bullets, enemies):
        """Fire a bullet towards the nearest enemy."""
        bullet = self.weapon.fire(self.rect.centerx, self.rect.centery, self.nearest_enemy_angle(enemies))
        if bullet:
            bullets.add(bullet)

    def nearest_enemy(self, enemies):
        """Find the nearest enemy to the player."""
        nearest_enemy = None
        nearest_distance = float("inf")
        for enemy in enemies:
            distance = math.hypot(enemy.rect.x - self.rect.x, enemy.rect.y - self.rect.y)
            if distance < nearest_distance:
                nearest_enemy = enemy
                nearest_distance = distance
        return nearest_enemy

    def nearest_enemy_angle(self, enemies):
        """Calculate the angle to the nearest enemy."""
        nearest_enemy_angle = 0
        nearest_enemy = self.nearest_enemy(enemies)
        if nearest_enemy is not None:
            nearest_enemy_angle = math.degrees(
                math.atan2(nearest_enemy.rect.y - self.rect.y, nearest_enemy.rect.x - self.rect.x))
        return nearest_enemy_angle

    def change_weapon(self, weapon):
        # Convert weapon (string) to weapon object
        if weapon == "Falukorv":
            self.weapon = Falukorv()
        elif weapon == "Meatball":
            self.weapon = Meatball()
        else:
            self.weapon = Lingonberry()
