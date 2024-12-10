from config import *
import pygame
import random
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()

        # Create a surface for the dinosaur with transparency
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA, 32)

        # Draw a detailed dinosaur using shapes

        # Body
        pygame.draw.rect(self.image, (34, 139, 34), (20, 20, 30, 20))  # Green rectangular body
        # Head
        pygame.draw.rect(self.image, (34, 139, 34), (10, 10, 15, 15))  # Smaller rectangle for the head
        # Tail
        pygame.draw.polygon(self.image, (34, 139, 34), [(50, 25), (70, 30), (50, 35)])  # Triangle tail
        # Legs
        pygame.draw.rect(self.image, (34, 139, 34), (25, 40, 8, 12))  # Left leg
        pygame.draw.rect(self.image, (34, 139, 34), (37, 40, 8, 12))  # Right leg
        # Arms
        pygame.draw.line(self.image, (34, 139, 34), (15, 30), (10, 35), 3)  # Left arm
        pygame.draw.line(self.image, (34, 139, 34), (25, 30), (30, 35), 3)  # Right arm
        # Eye
        pygame.draw.circle(self.image, (0, 0, 0), (15, 15), 2)  # Black eye
        # Mouth
        pygame.draw.line(self.image, (0, 0, 0), (12, 20), (18, 20), 2)  # Horizontal line for mouth
        # Spikes
        pygame.draw.polygon(self.image, (0, 100, 0), [(22, 20), (26, 10), (30, 20)])  # Middle spike
        pygame.draw.polygon(self.image, (0, 100, 0), [(30, 20), (34, 10), (38, 20)])  # Right spike

        # Get the rectangle for positioning
        self.rect = self.image.get_rect()
        # Ensure the enemy does not spawn at the same position as the player
        valid_position = False
        while not valid_position:
            # Start the enemy at a random valid location on the screen
            self.rect.x = random.randint(0, width - self.rect.width)
            self.rect.y = random.randint(0, height - self.rect.height)
            # Check if the enemy overlaps with the player's position
            if not self.rect.colliderect(player.rect):
                valid_position = True
        # Set a random initial speed for the enemy
        self.speed = random.randint(2, 3)

        # Set the health of the enemy
        self.health = 10

    def update(self, player):
        """
        Update the enemy's position to move towards the player.
        """
        # Calculate the direction towards the player
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y

        # Calculate the direction in radians
        direction = math.atan2(dy, dx)

        # Move the enemy towards the player
        self.rect.x += int(self.speed * math.cos(direction))
        self.rect.y += int(self.speed * math.sin(direction))
