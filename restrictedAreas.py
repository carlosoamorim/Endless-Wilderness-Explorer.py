import pygame
from config import *

class RestrictedArea:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def on_enter(self, player):
        """Default behavior: do nothing."""
        pass

    def check_collision(self, player):
        if self.rect.colliderect(player.rect):
            self.on_enter(player)