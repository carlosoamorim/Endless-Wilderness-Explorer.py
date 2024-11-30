import pygame
import math
from bullet import Bullet
from weapon import Weapon

class Meatball(Weapon):
    def __init__(self):
        super().__init__("Meatball", 3, 200, 30)

    def attack(self, player, bullets):
        if player.bullet_cooldown <= 0:
            for angle in [0, math.pi, math.pi / 2, 3 * math.pi / 2]:
                bullet = Bullet(player.rect.centerx, player.rect.centery, angle)
                bullets.add(bullet)
            player.bullet_cooldown = self.cooldown
    
