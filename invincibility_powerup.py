from power_up import PowerUp

class Invincibility(PowerUp):
    def __init__(self, power_box_weight, power_box_height, chance, image):
        super().__init__("Invincibility", power_box_weight, power_box_height, chance, image)

    def power_affect_player(self, player):
        """Activate invincibility for the player."""
        player.is_invincible = True
        player.power_active = True
        self.apply_invincibility_visuals(player)

    def detransform(self, player):
        """Deactivate invincibility and reset visuals."""
        self.revert_invincibility_visuals(player)
        player.is_invincible = False
        player.power_active = False

    def apply_invincibility_visuals(self, player):
        """Update the player's visuals to reflect invincibility."""
        player.active_image = player.invincible

    def revert_invincibility_visuals(self, player):
        """Revert the player's visuals to the default state."""
        if player.active_image == player.invincible:
            player.active_image = player.default
            # Set the player's current image to match the default direction (right or left)
            if player.image == player.invincible["right"]:
                player.image = player.default["right"]
            elif player.image == player.invincible["left"]:
                player.image = player.default["left"]

    def power_affect_game(self, target, target2):

        pass