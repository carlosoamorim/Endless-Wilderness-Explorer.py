from config import *
import math
import pygame
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        # Character
        super().__init__()

        # Visuals
        self.image = pygame.Surface(player_size)
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)

        # Gameplay
        self.speed = 5
        self.health = 100
        self.bullet_cooldown = 0

    def update(self):
        # Update player position
        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < width:
            self.rect.x += self.speed
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < height:
            self.rect.y += self.speed

    def shoot(self, bullets: pygame.sprite.Group):
        """
        Shoot bullets in 4 directions depending on cd

        Args
        ---
        bullets (pygame.sprite.Group)
            the bullet group that we will add new ones to
        """
        if self.bullet_cooldown <= 0:
            for angle in [0, math.pi / 2, math.pi, 3 * math.pi / 2]:
                bullet = Bullet(
                    self.rect.center[0], self.rect.center[1], angle
                )
                bullets.add(bullet)
            self.bullet_cooldown = 60
        self.bullet_cooldown -= 1