from power_up import PowerUp

class Desspawn_machine(PowerUp):
    def __init__(self, power_box_weight, power_box_height, chance, image):
        super().__init__("Execute Order 66",power_box_weight, power_box_height, chance, image)

    def power_affect_player(self, player):
        pass



    def power_affect_game(self, target, target2=None):
        for enemy in target:
            if len(target) > 2:
                enemy.kill()
