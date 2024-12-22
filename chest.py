import pygame
import random

class Chest(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, spawn_chance=0.9):
        """
        Initialize the chest.
        :param screen_width: Width of the game screen.
        :param screen_height: Height of the game screen.
        :param spawn_chance: Probability of spawning the chest.
        """
        super().__init__()
        # Load chest image
        self.image = pygame.image.load("images/chest_IKEA.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))  # Resize to desired dimensions

        # Chest rect for positioning and collision
        self.rect = self.image.get_rect()

        # Random position for the chest
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(0, screen_height - self.rect.height)

        # Spawn logic
        self.spawned = random.random() < spawn_chance  # Rare chance to spawn

        self.upgrades = {
            1: "Health",
            2: "Speed",
            3: "Damage",
            4: "Attack speed"
        }

    def update(self, player_group, screen_width, screen_height):
        """
        Check for collision with the player.
        :param player_group: The player sprite group for collision detection.
        :param screen_width: Width of the game screen.
        :param screen_height: Height of the game screen.
        """
        amount = 0
        if self.spawned and pygame.sprite.spritecollideany(self, player_group):
            self.offered_upgrades = {}

            selected_upgrades = set()
            while len(selected_upgrades) < 3:
                random_upgrade = random.choice(list(self.upgrades.values()))
                if random_upgrade not in selected_upgrades:
                    selected_upgrades.add(random_upgrade)
                    if random_upgrade == "Health":
                        amount = random.randint(5, 10)
                    elif random_upgrade == "Speed":
                        amount = random.randint(1, 3)
                    elif random_upgrade == "Damage":
                        amount = random.randint(1, 5)
                    elif random_upgrade == "Attack speed":
                        amount = random.randint(1, 5)

                    # Add the upgrade to the dictionary
                    self.offered_upgrades[random_upgrade] = amount

            self.open(self.offered_upgrades, screen_width, screen_height)

            self.kill()

    def open(self, offered_upgrades, screen_width, screen_height):
        """
        Open the chest and offer the player upgrades.
        :param offered_upgrades: Dictionary of offered upgrades.
        :param screen_width: Width of the game screen.
        :param screen_height: Height of the game screen.
        """
        print("Chest opened!")
        print("You found the following upgrades:")
        for upgrade, amount in offered_upgrades.items():
            print(f"{upgrade}: +{amount}")
        print()

        # Create a pop-up surface
        popup_width, popup_height = 300, 200
        popup_surface = pygame.Surface((popup_width, popup_height))
        popup_surface.fill((0, 0, 0))  # Fill with black color

        # Draw the pop-up message
        font = pygame.font.Font(None, 36)
        y_offset = 20
        for upgrade, amount in offered_upgrades.items():
            text = font.render(f"{upgrade}: +{amount}", True, (255, 255, 255))
            popup_surface.blit(text, (20, y_offset))
            y_offset += 40

        # Center the popup on the screen
        popup_x = (screen_width // 2) - (popup_width // 2)
        popup_y = (screen_height // 2) - (popup_height // 2)

        # Blit the pop-up surface onto the main screen
        screen = pygame.display.get_surface()  # Get the current screen
        screen.blit(popup_surface, (popup_x, popup_y))
        pygame.display.flip()

        # Wait for a few seconds to show the popup
        pygame.time.wait(3000)
