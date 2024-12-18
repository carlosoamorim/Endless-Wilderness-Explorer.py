from upgrades.upgrade import Upgrade

class SpeedUpgrade(Upgrade):
    def __init__(self, amount):
        super().__init__("Speed Boost", f"Increase speed by {amount}")
        self.amount = amount

    def apply(self, player):
        player.speed += self.amount
        print(f"Speed increased by {self.amount}. New speed: {player.speed}")