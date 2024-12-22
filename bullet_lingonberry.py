from bullet import Bullet
import pygame

class BulletLingonberry(Bullet):
    def __init__(self, x, y, direction, damage):
        speed = 10
        image_path = "images/lingon.png"
        damage = damage

        super().__init__(x, y, speed, direction, image_path, damage)
        self.rect = self.image.get_rect(center = (x, y))
        self.image = pygame.transform.scale(pygame.image.load(image_path), (20, 20))


    def collide(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.take_damage(self.damage)
                self.kill()
                return True
        return False