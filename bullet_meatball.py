from bullet import Bullet
import pygame

class BulletMeatball(Bullet):
    def __init__(self, x, y, direction):
        speed = 10
        image_path = "images/meatball.png"
        damage = 3

        super().__init__(x, y, speed, direction, image_path, damage)
        self.rect = self.image.get_rect(center = (x, y))

        self.image = pygame.image.load(image_path)


    def collide(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.take_damage(self.damage)
                self.kill()
                return True
        return False