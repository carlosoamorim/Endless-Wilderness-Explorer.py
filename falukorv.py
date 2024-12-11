import pygame
import math
from bullet import Bullet
from weapon import Weapon

class Falukorv(Weapon):
    def __init__(self):
        super().__init__(name="Falukorv", damage=5, range=200, cooldown=0, attack_speed=80)

    def fire(self, x, y, direction):
        def falukorv_behavior(bullet):
            bullet.rect.x += int(bullet.speed * math.cos(bullet.direction))
            bullet.rect.y += int(bullet.speed * math.sin(bullet.direction))
            bullet.distance_traveled += bullet.speed
            if bullet.distance_traveled > 200:
                bullet.direction += math.pi  # Reverse direction

        return Bullet(x, y, self.bullet_speed, direction, falukorv_behavior, "images/falukorv.png")
                
