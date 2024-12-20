import pygame
import math
from config import *
from utils import *
from bullet import Bullet
from meatball import Meatball
from falukorv import Falukorv
from PowerUp import *


class Player(pygame.sprite.Sprite):
    HURT_IMAGE_DURATION = fps * 10
    def __init__(self):
        super().__init__()
        self.speed = 5
        self.max_health = 100
        self.current_health = self.max_health

        self.weapon = Meatball()
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

        # Default settings
        self.image = self.default["right"]
        self.active_image = self.default
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)

        self.prev_position = self.rect.topleft 
        

    def update(self):
        """Handle player movement and image updates."""
        keys = pygame.key.get_pressed()
        self.move(keys)

        if self.hurt_time and pygame.time.get_ticks() - self.hurt_time > self.HURT_IMAGE_DURATION:
            self.image = self.default["right"]
            self.active_image = self.default
            self.hurt_time = None

    def move(self, keys):
        """Move the player within screen boundaries and update the image."""
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
            
    def apply_upgrade(self, upgrade_type, amount):
        """Apply an upgrade to the player's attributes."""
        if upgrade_type == "health":
            self.max_health += amount
            self.current_health += amount
        elif upgrade_type == "speed":
            self.speed += amount
            
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


class Invincibility(PowerUp):
    def __init__(self, power_box_weight, power_box_height, chance, image):
        super().__init__("Invincibility", power_box_weight, power_box_height, chance, image)

    def power_affect_player(self, player):
        """Activate invincibility for the player."""
        player.is_invincible = True
        player.power_active = True
        self.apply_invincibility_visuals(player)

    def detransform(self, player):
        """Deactivate invincibility and reset visuals."""
        self.revert_invincibility_visuals(player)
        player.is_invincible = False
        player.power_active = False

    def apply_invincibility_visuals(self, player):
        """Update the player's visuals to reflect invincibility."""
        player.active_image = player.is_invincible

    def revert_invincibility_visuals(self, player):
        """Revert the player's visuals to the default state."""
        if player.image == player.image_right_invincible:
            player.set_image(player.image_R)
        elif player.image == player.image_left_invincible:
            player.set_image(player.image_L)

    def power_affect_game(self, target, target2):

        pass
