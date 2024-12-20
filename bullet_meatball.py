from bullet import Bullet


class BulletMeatball(Bullet):
    def __init__(self, x, y, speed, direction, image_path):
        super().__init__(x, y, speed, direction, image_path, damage = 3)

    def collide(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.take_damage(self.damage)
                self.kill()
                return True
        return False