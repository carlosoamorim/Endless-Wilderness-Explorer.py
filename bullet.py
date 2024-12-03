from config import *
import pygame
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, direction, image_path, damage):
        super().__init__()
        self.rect = pygame.Rect(x, y, 5, 5)
        self.speed = speed
        self.direction = direction
        self.image = pygame.image.load(image_path)
        self.damage = damage
        
    def update(self):
        # Move the bullet in the direction it is facing
        self.rect.x += self.speed * math.cos(math.radians(self.direction))
        self.rect.y += self.speed * math.sin(math.radians(self.direction))
        
        # Check if the bullet is off the screen
        if self.rect.x < 0 or self.rect.x > width or self.rect.y < 0 or self.rect.y > height:
            self.kill()

    def draw(self, screen):
        # drawing the bullet on the screen
        screen.blit(self.image, self.rect.topleft)
    
    def collide(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.health -= 3
                return True
        return False