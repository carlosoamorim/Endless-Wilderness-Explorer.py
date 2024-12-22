from power_up import PowerUp

class Heal(PowerUp):
    def __init__(self, power_box_weight, power_box_height, chance, image):
        super().__init__("Blåbärssoppa", power_box_weight, power_box_height, chance, image)

    def power_affect_player(self, player):

        if player.current_health + 25 > player.max_health:
            player.current_health = player.max_health
        self.visual_aplication(player)
        player.heal = True

    def detransform(self, player):
        player.heal = False
        self.revert_heal_visuals(player)
    def power_affect_game(self, target, target2):
        pass

    def visual_aplication(self, player):
        player.active_image = player.healing

    def revert_heal_visuals(self, player):
        """Revert the player's visuals to the default state."""
        if player.active_image == player.healing:
            player.active_image = player.default
            # Set the player's current image to match the default direction (right or left)
            if player.image == player.healing["right"]:
                player.image = player.default["right"]
            elif player.image == player.healing["left"]:
                player.image = player.default["left"]