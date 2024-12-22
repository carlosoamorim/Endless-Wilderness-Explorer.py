import sys

import pygame
import random


class Chest(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, spawn_chance=0.9):
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
        self.spawned = random.random() < spawn_chance

        self.upgrades = {
            1: "Health",
            2: "Speed",
            3: "Damage",
            4: "Attack speed"
        }

    def update(self, player, screen_width, screen_height):
        if self.spawned and pygame.sprite.spritecollideany(self, player):
            self.offered_upgrades = {}

            selected_upgrades = set()
            while len(selected_upgrades) < 3:
                random_upgrade = random.choice(list(self.upgrades.values()))
                if random_upgrade not in selected_upgrades:
                    selected_upgrades.add(random_upgrade)
                    amount = {
                        "Health": random.randint(5, 10),
                        "Speed": random.randint(1, 3),
                        "Damage": random.randint(1, 5),
                        "Attack speed": random.randint(1, 5),
                    }[random_upgrade]

                    self.offered_upgrades[random_upgrade] = amount

            self.open(self.offered_upgrades, player, screen_width, screen_height)
            self.kill()

    def open(self, offered_upgrades, player, screen_width, screen_height):
        print("Chest opened!")
        print("Choose one of the following upgrades:")

        popup_width, popup_height = 300, 200
        popup_surface = pygame.Surface((popup_width, popup_height))
        popup_surface.fill((30, 30, 30))  # Dark background for the popup

        button_height = 50
        button_margin = 10
        font = pygame.font.Font(None, 36)
        buttons = []

        y_offset = 20
        for upgrade, amount in offered_upgrades.items():
            button_rect = pygame.Rect(
                20, y_offset, popup_width - 40, button_height
            )
            buttons.append((button_rect, upgrade, amount))
            y_offset += button_height + button_margin

        popup_x = (screen_width // 2) - (popup_width // 2)
        popup_y = (screen_height // 2) - (popup_height // 2)

        running = True
        while running:
            screen = pygame.display.get_surface()  # Get the current screen
            screen.blit(popup_surface, (popup_x, popup_y))

            for button_rect, upgrade, amount in buttons:
                color = (80, 80, 80)  # Default button color
                if button_rect.move(popup_x, popup_y).collidepoint(pygame.mouse.get_pos()):  # Adjust for popup position
                    color = (100, 100, 100)  # Highlighted button color
                pygame.draw.rect(popup_surface, color, button_rect, border_radius=5)
                text = font.render(f"{upgrade}: +{amount}", True, (255, 255, 255))
                popup_surface.blit(
                    text,
                    (
                        button_rect.x + 10,
                        button_rect.y + (button_height - text.get_height()) // 2,
                    ),
                )

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button_rect, upgrade, amount in buttons:
                        if button_rect.move(popup_x, popup_y).collidepoint(event.pos):  # Adjust for popup position
                            print(f"Player chose: {upgrade} (+{amount})")
                            self.apply_upgrade(player, upgrade, amount)
                            running = False  # Exit the interaction loop
                            break

    def apply_upgrade(self, player_group, upgrade, amount):
        """
        Apply the chosen upgrade to the player.
        """
        for player in player_group:
            if upgrade == "Health":
                player.max_health += amount
                player.current_health = min(player.current_health + amount, player.max_health)
            elif upgrade == "Speed":
                player.speed += amount
         # Other upgrades can be added here if needed
            print(f"{upgrade} applied to player: +{amount}")
