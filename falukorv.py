import pygame
import math
from bullet import Bullet
from weapon import Weapon
from bullet_falukorv import BulletFalukorv

class Falukorv(Weapon):
    def __init__(self):
        name = "Falukorv"
        damage = 5
        range = 200
        cooldown = 0
        attack_speed = 80

        super().__init__(name, damage, range, cooldown, attack_speed)

    def fire(self, x, y, direction):
        if self.cooldown <= 0:
            self.cooldown = self.attack_speed
            return BulletFalukorv(x, y, direction)
        else:
            self.cooldown -= 1
            return None                

        bullet.rect.x += int(bullet.speed * math.cos(bullet.direction))
        bullet.rect.y += int(bullet.speed * math.sin(bullet.direction))
        bullet.distance_traveled += bullet.speed
        if bullet.distance_traveled > 200:
            bullet.direction += math.pi  # Reverse direction
