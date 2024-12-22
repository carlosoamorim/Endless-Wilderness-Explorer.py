import pygame
import random
from config import *
from utils import *
from abc import abstractmethod, ABC

class PowerUp(ABC, pygame.sprite.Sprite):

    def __init__(self, power_name, power_box_weight, power_box_height, chance, image):
        super().__init__()
        self.image = pygame.image.load(image)  # Load the image
        self.image = pygame.transform.scale(self.image, (power_box_weight, power_box_height))  # Scale it
        self.chance = chance

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
    def power_affect_game(self, target, target2):
        pass


class Desspawn_machine(PowerUp):
    def __init__(self, power_box_weight, power_box_height, chance, image):
        super().__init__("Execute Order 66",power_box_weight, power_box_height, chance, image)

    def power_affect_player(self, player):
        pass



    def power_affect_game(self, target, target2=None):
        for enemy in target:
            if len(target) > 2:
                enemy.kill()


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


class Heal(PowerUp):
    def __init__(self, power_box_weight, power_box_height, chance, image):
        super().__init__("Heal", power_box_weight, power_box_height, chance, image)

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
        player.active_image = player.heald

    def revert_heal_visuals(self, player):
        """Revert the player's visuals to the default state."""
        if player.active_image == player.heald:
            player.active_image = player.default
            # Set the player's current image to match the default direction (right or left)
            if player.image == player.heald["right"]:
                player.image = player.default["right"]
            elif player.image == player.heald["left"]:
                player.image = player.default["left"]

class Freeze(PowerUp):
    def __init__(self, power_box_weight, power_box_height, chance, image):
        super().__init__("Chaos Control", power_box_weight, power_box_height, chance, image)

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
