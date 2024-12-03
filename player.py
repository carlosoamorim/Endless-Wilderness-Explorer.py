from utils import *
from config import *
import pygame
import math
from bullet import Bullet
from meatball import Meatball
from falukorv import Falukorv


# making Player a child of the Sprite class
class Player(pygame.sprite.Sprite):

    def __init__(self):
        # calling the mother class' init
        super().__init__()

        # VISUAL VARIABLES
        # we call surface to represent the player image
        self.image = pygame.Surface(player_size)
        # drawing the image of the player
        self.image.fill(cute_purple)
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)

        # GAMEPLAY VARIABLES
        self.speed = 5
        self.health = 100
        self.weapon = Meatball()

    def update(self):

        # getting the keys input:
        keys = pygame.key.get_pressed()

        # checking which keys were pressed and moving the player accordingly
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < height:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < width:
            self.rect.x += self.speed

    def attack(self, bullets):
        direction = 0  # Example direction, you might want to calculate this based on player orientation
        bullet = self.weapon.fire(self.rect.centerx, self.rect.centery, direction)
        if bullet:
            bullets.add(bullet)
            print(f"Bullet added at ({bullet.rect.x}, {bullet.rect.y})")

