from powerups.PowerUp import PowerUp
import pygame
from config import *

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
