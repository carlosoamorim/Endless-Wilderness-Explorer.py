from upgrades.upgrade import Upgrade

class HealthUpgrade(Upgrade):
    def __init__(self, amount):
        super().__init__("Health Boost", f"Increase health by {amount}")
        self.amount = amount

    def apply(self, player):
        player.health += self.amount
        print(f"Health increased by {self.amount}. New health: {player.health}")