import pygame

class Weapon:
    def __init__(self, name, damage, range, cooldown):
        self.name = name
        self.damage = damage
        self.range = range
        self.cooldown = cooldown

    def attack(self):
        pass

    