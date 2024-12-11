from config import *
from powerups.PowerUp import PowerUp

class Invincibility(PowerUp):
    def __init__(self, power_box_weight, power_box_height, chance, image):
        super().__init__("Invincibility", power_box_weight, power_box_height, chance, image)

    def power_affect_player(self, player):
        """ºinvicible activate, with this variable I deactivated the damage system."""
        player.invincible = True

        player.image.fill(gold)  # Change color to indicate invincibility

    def detransform(self, player):
        """Go back to normal."""
        player.image.fill(cute_purple)  # Reset to original color
        player.invincible = False
        player.power_active = False
    def power_affect_game(self, target, target2):
        pass