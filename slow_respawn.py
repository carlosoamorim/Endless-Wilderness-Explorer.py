from power_up import PowerUp
from config import fps

class Slow_respawn(PowerUp):
    def __init__(self, power_box_weight, power_box_height, chance, image):
        super().__init__("Slow_respawn", power_box_weight, power_box_height, chance, image)

    def power_affect_player(self, player):
        # This power-up does not directly affect the player
        pass

    def power_affect_game(self, current_enemy_cooldown, target):
        """
        Increases the respawn cooldown for enemies and changes their color.
        """
        # Increase the cooldown time for spawning new enemies
        current_enemy_cooldown += fps * 5  # Add 5 seconds to the cooldown

        # Change the color of all enemies in the target group
        for enemy in target:
            enemy.slow_respawn()

        return current_enemy_cooldown
