from utils import *
from config import *
import pygame
import math
import random
from player import Player

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((enemy_size, enemy_size))
        self.image.fill(red)
        self.rect = self.image.get_rect()

        #Positioning
        self.rect.x = random.randint(0, width - enemy_size)
        self.rect.y = random.randint(0, height - enemy_size)

        #Random speed
        self.speed = random.randint(2, 3)

        self.health = 10
    
    def update(self, player):
        """
        Update the enemy position according to the player

        """

        #Direction
        direction = math.atan2(player.rect.y - self.rect.y, player.rect.x - self.rect.x)

        #Move towards the player
        self.rect.x += int(self.speed * math.cos(direction))
        self.rect.y += int(self.speed * math.sin(direction))

        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)