import pygame
import math
from bullet import Bullet
from weapon import Weapon
from config import *
from bullet_falukorv import BulletFalukorv

class Falukorv(Weapon):
    def __init__(self):
        super().__init__(name="Falukorv", damage=5, range=200, cooldown=0, attack_speed=80)

    def fire(self, x, y, direction):
        if self.cooldown <=0:
            self.cooldown = self.attack_speed
            return BulletFalukorv(x, y, 10, direction, "images/falukorv.png", distance_travelled = 0)
        else:
            self.cooldown -= 1
            return None                
