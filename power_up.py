import pygame
import random
from config import *
from utils import *
from abc import abstractmethod, ABC

class Power_up(ABC, pygame.sprite.Sprite):

    def __init__(self, power_name, power_box_weight, power_box_height, chance, image):
        super().__init__()
        self.image = pygame.image.load(image)  # Load the image
        self.image = pygame.transform.scale(self.image, (power_box_weight, power_box_height))  # Scale it
        self.chance =  chance

        self.power_name = power_name
        self.power_box_weight = power_box_weight
        self.power_box_height = power_box_height

        # filling the surface with chosen enemy colour

        # getting rectangle for positioning
        self.rect = self.image.get_rect()


        # starting the power up at a random valid location on the screen
        self.rect.x = random.randint(0, width - self.power_box_weight)
        self.rect.y = random.randint(0, height - self.power_box_height)

    @abstractmethod
    def power_affect_player(self, player):
        pass

    @abstractmethod
    def power_affect_game(self, target):
        pass


class Execute_Order_66(Power_up):
    def __init__(self, power_box_weight, power_box_height, chance, image):
        super().__init__("Execute Order 66",power_box_weight, power_box_height, chance, image)

    def power_affect_player(self, player):
        pass

    def power_affect_game(self, target):
        for enemy in target:
            enemy.kill()


class Desspawn_machine(Power_up):
    def __init__(self, power_box_weight, power_box_height, chance, image):
        super().__init__("Desspawn machine", power_box_weight, power_box_height, chance, image)

    def power_affect_player(self, player):
        pass

    def power_affect_game(self, current_enemy_cooldown):

        #Increases the respawn cooldown for enemies.
        current_enemy_cooldown = fps * 5

        return current_enemy_cooldown
