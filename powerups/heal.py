from powerups.PowerUp import PowerUp
from config import *

class Heal(PowerUp):
    def __init__(self, power_box_weight, power_box_height, chance, image):
        super().__init__("Heal", power_box_weight, power_box_height, chance, image)

    def power_affect_player(self, player):

        player.health += 25
        player.image.fill(blue)
        player.heal = True

    def detransform(self, player):
        player.heal = False

    def power_affect_game(self, target, target2):
        pass
