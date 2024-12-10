import pygame

class Weapon:
    def __init__(self, name, damage, range, cooldown, attack_speed):
        self.name = name
        self.damage = damage
        self.range = range
        self.cooldown = cooldown
        self.attack_speed = attack_speed

    def fire(self, bullets):
        pass

    