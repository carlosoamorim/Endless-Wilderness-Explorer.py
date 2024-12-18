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
            # Create a new surface for the enemy
            new_image = pygame.Surface(enemy.image.get_size(), pygame.SRCALPHA)

            # Draw the enemy with a new color (e.g., red for slowed enemies)
            pygame.draw.rect(new_image, (255, 0, 0), (20, 20, 30, 20))  # Red body
            pygame.draw.rect(new_image, (255, 0, 0), (10, 10, 15, 15))  # Red head
            pygame.draw.polygon(new_image, (255, 0, 0), [(50, 25), (70, 30), (50, 35)])  # Red tail
            pygame.draw.rect(new_image, (128, 0, 0), (25, 40, 8, 12))  # Dark red left leg
            pygame.draw.rect(new_image, (128, 0, 0), (37, 40, 8, 12))  # Dark red right leg
            pygame.draw.line(new_image, (128, 0, 0), (15, 30), (10, 35), 3)  # Dark red left arm
            pygame.draw.line(new_image, (128, 0, 0), (25, 30), (30, 35), 3)  # Dark red right arm
            pygame.draw.circle(new_image, (0, 0, 0), (15, 15), 2)  # Black eye
            pygame.draw.line(new_image, (0, 0, 0), (12, 20), (18, 20), 2)  # Mouth
            pygame.draw.polygon(new_image, (128, 0, 0), [(22, 20), (26, 10), (30, 20)])  # Spike 1
            pygame.draw.polygon(new_image, (128, 0, 0), [(30, 20), (34, 10), (38, 20)])  # Spike 2

            # Update the enemy's image
            enemy.image = new_image

        return current_enemy_cooldown


class Heal(PowerUp):
    def __init__(self, power_box_weight, power_box_height, chance, image):
        super().__init__("Heal", power_box_weight, power_box_height, chance, image)

    def power_affect_player(self, player):

        player.health += 25
        player.image = player.load_image("images/Characters/Kalle_Postman_Left_1.1.png") 
        player.heal = True

    def detransform(self, player):
        player.heal = False

    def power_affect_game(self, target, target2):
        pass

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
            new_image = pygame.Surface(enemy.image.get_size(), pygame.SRCALPHA)

            # Draw the enemy with a new color (e.g., red for slowed enemies)
            pygame.draw.rect(new_image, (255, 255, 255), (20, 20, 30, 20))  # white body
            pygame.draw.rect(new_image, (255, 255, 255), (10, 10, 15, 15))  # Red head
            pygame.draw.polygon(new_image, (255, 255, 255), [(50, 25), (70, 30), (50, 35)])  # white tail
            pygame.draw.rect(new_image, (128, 0, 0), (25, 40, 8, 12))  # Dark red left leg
            pygame.draw.rect(new_image, (128, 0, 0), (37, 40, 8, 12))  # Dark red right leg
            pygame.draw.line(new_image, (128, 0, 0), (15, 30), (10, 35), 3)  # Dark red left arm
            pygame.draw.line(new_image, (128, 0, 0), (25, 30), (30, 35), 3)  # Dark red right arm
            pygame.draw.circle(new_image, (0, 0, 0), (15, 15), 2)  # Black eye
            pygame.draw.line(new_image, (0, 0, 0), (12, 20), (18, 20), 2)  # Mouth
            pygame.draw.polygon(new_image, (128, 0, 0), [(22, 20), (26, 10), (30, 20)])  # Spike 1
            pygame.draw.polygon(new_image, (128, 0, 0), [(30, 20), (34, 10), (38, 20)])  # Spike 2

            # Update the enemy's image
            enemy.image = new_image
            enemy.speed = 0
        return current_enemy_cooldown
