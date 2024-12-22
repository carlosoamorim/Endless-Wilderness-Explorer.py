from bullet import Bullet
import math
from config import *
import pygame

class BulletFalukorv(Bullet):
    def __init__(self, x, y, direction, damage):
        self.distance_travelled = 0
        damage = damage
        speed = 10
        image_path = "images/falukorv.png"
        super().__init__(x, y, speed, direction, image_path, damage)
        self.hit = False

    def update(self):
        # Move the bullet in the direction it is facing
        self.rect.x += self.speed * math.cos(math.radians(self.direction))
        self.rect.y += self.speed * math.sin(math.radians(self.direction))
        self.distance_travelled += self.speed

        # Handle boomerang effect
        if self.distance_travelled == 200:
            self.hit = False
            self.direction += 180

        # If the bullet is off the screen, remove it
        if self.rect.x < 0 or self.rect.x > width or self.rect.y < 0 or self.rect.y > height or self.distance_travelled > 400:
            self.kill()


        
    def collide(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect) and not self.hit:
                enemy.take_damage(self.damage)
                self.hit = True
                return True
        return False