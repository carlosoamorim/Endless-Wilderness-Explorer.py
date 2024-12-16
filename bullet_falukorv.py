from bullet import Bullet
import math
from config import *
import pygame

class BulletFalukorv(Bullet):
    def __init__(self, x, y, speed, direction, image_path, distance_travelled):
        self.distance_travelled = 0
        super().__init__(x, y, speed, direction, image_path, damage = 3)

    def update(self):
        # Move the bullet in the direction it is facing
        self.rect.x += self.speed * math.cos(math.radians(self.direction))
        self.rect.y -= self.speed * math.sin(math.radians(self.direction))
        self.distance_travelled += self.speed

        # Handle boomerang effect
        if self.distance_travelled == 200:
            self.direction += 180

        # If the bullet is off the screen, remove it
        if self.rect.x < 0 or self.rect.x > width or self.rect.y < 0 or self.rect.y > height or self.distance_travelled > 400:
            self.kill()



        
    def collide(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.health -= self.damage
                return True
        return False