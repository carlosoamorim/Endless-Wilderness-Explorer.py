import pygame
import math
from config import *
from utils import *
from bullet import Bullet
from meatball import Meatball
from PowerUp import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Preload all images for efficiency
        self.image = pygame.Surface(player_size)
        self.image_R = pygame.image.load("images/Characters/Kalle_R.png").convert_alpha()

        self.image_R = pygame.transform.scale(self.image_R, (57, 141))
        self.image_L = pygame.transform.flip(self.image_R, True, False)
        self.active_skin = None
        self.image_right_invincible = pygame.image.load(r"images\Characters\Kalle_Postman_Right_invincible1.1.png").convert_alpha()
        self.image
        self.image_right_damage = pygame.image.load(r"images\Characters\player_oof_right.png").convert_alpha()

        # Default settings
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)

        # Gameplay variables
        self.speed = 5
        self.health = 100
        self.weapon = Meatball()
        self.bullet_cooldown = 0
        self.power_active = False
        self.invincible = False
        self.heal = False

    def set_image(self, image):
        """Set the player's image and update the rect."""
        self.image = image
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        """Handle player movement and image updates."""
        keys = pygame.key.get_pressed()
        self.move(keys)

    def move(self, keys):
        """Move the player within screen boundaries and update the image."""
        if keys[pygame.K_a] and self.rect.left > 0:  # Move left
            self.rect.x -= self.speed
            self.active_skin = self.image_right if not
        elif keys[pygame.K_d] and self.rect.right < width:  # Move right
            self.rect.x += self.speed


        if keys[pygame.K_w] and self.rect.top > 0:  # Move up
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < height:  # Move down
            self.rect.y += self.speed

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


class Invincibility(PowerUp):
    def __init__(self, power_box_weight, power_box_height, chance, image):
        super().__init__("Invincibility", power_box_weight, power_box_height, chance, image)

    def power_affect_player(self, player):
        """Activate invincibility for the player."""
        player.invincible = True
        player.power_active = True
        self.apply_invincibility_visuals(player)

    def detransform(self, player):
        """Deactivate invincibility and reset visuals."""
        self.revert_invincibility_visuals(player)
        player.invincible = False
        player.power_active = False

    def apply_invincibility_visuals(self, player):
        """Update the player's visuals to reflect invincibility."""
        if player.image == player.image_right:
            player.set_image(player.image_right_invincible)
        elif player.image == player.image_left:
            player.set_image(player.image_left_invincible)

    def revert_invincibility_visuals(self, player):
        """Revert the player's visuals to the default state."""
        if player.image == player.image_right_invincible:
            player.set_image(player.image_right)
        elif player.image == player.image_left_invincible:
            player.set_image(player.image_left)

    def power_affect_game(self, target, target2):

        pass
