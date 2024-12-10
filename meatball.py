import pygame
import math
from bullet import Bullet
from bullet_meatball import BulletMeatball
from weapon import Weapon
from config import *

class Meatball(Weapon):
    def __init__(self):
        super().__init__(name="Meatball Cannon", damage=3, range=200, cooldown=0, attack_speed=30)

    def fire(self, x, y, direction):
        if self.cooldown <= 0:
            self.cooldown = self.attack_speed
            return BulletMeatball(x, y, 10, direction, "images/meatball.png")
        else:
            self.cooldown -= 1
            return None

        
