import pygame
import random

class Chest(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, spawn_chance=0.9):
        """
        Initialize the chest.
        :param image_path: Path to the chest image.
        :param screen_width: Width of the game screen.
        :param screen_height: Height of the game screen.
        :param spawn_chance: Probability of spawning the chest (default is 5%).
        """
        super().__init__()

        # Load chest image
        self.image = pygame.image.load("images/chest.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))  # Resize to desired dimensions

        # Chest rect for positioning and collision
        self.rect = self.image.get_rect()

        # Random position for the chest
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(0, screen_height - self.rect.height)

        # Spawn logic
        self.spawned = random.random() < spawn_chance  # Rare chance to spawn

    def update(self, player_group):
        """
        Check for collision with the player.
        :param player_group: The player sprite group for collision detection.
        """
        if self.spawned and pygame.sprite.spritecollideany(self, player_group):
            print("Chest opened!")
            self.kill()