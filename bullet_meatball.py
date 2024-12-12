from bullet import Bullet

class BulletMeatball(Bullet):
    def __init__(self, x, y, speed, direction, image_path):
        super().__init__(x, y, speed, direction, image_path, damage = 4)
