from utils import *
from config import *
import pygame
import math
from bullet import Bullet
from meatball import Meatball


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
        self.bullet_cooldown = 0
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

    def attack(self,  bullets):
        
        if self.bullet_cooldown <=0:
                if self.weapon.name == "Meatball":
                    self.weapon.attack(self, bullets)
                    # resetting the cooldown
                    self.bullet_cooldown = fps        # cooldown ==> how many frames I need to wait until I can shoot again
                    
        self.bullet_cooldown -= 1
