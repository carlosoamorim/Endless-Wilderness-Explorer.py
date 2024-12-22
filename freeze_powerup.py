from power_up import PowerUp
from config import fps

class Freeze(PowerUp):
    def __init__(self, power_box_weight, power_box_height, chance, image):
        super().__init__("Fika", power_box_weight, power_box_height, chance, image)

    def power_affect_player(self, player):
        pass

    def power_affect_game(self, current_enemy_cooldown, target):
        """
        Increases the respawn cooldown for enemies and changes their color.
        """
        # Increase the cooldown time for spawning new enemies
        current_enemy_cooldown += fps * 5  # Add 5 seconds to the cooldown

        # Change the color of all enemies in the target group
        for enemy in target:
            # Create a new surface for the enemy

            # Update the enemy's image

            enemy.freeze()

        return current_enemy_cooldown
