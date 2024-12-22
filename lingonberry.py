from weapon import Weapon
from bullet_lingonberry import BulletLingonberry

class Lingonberry(Weapon):
    def __init__(self):
        super().__init__(name="Lingonberry", damage=3, range=200, cooldown=0, attack_speed=50)

    def fire(self, x, y, direction):
        if self.cooldown <= 0:
            self.cooldown = self.attack_speed
            return BulletLingonberry(x, y, direction, self.damage)
        else:
            self.cooldown -= 1
            return None
