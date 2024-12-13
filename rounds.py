import pygame
from config import *
from shed import shed
class Rounds:
    def display_round_message(self, message, screen, font):
        text = font.render(message, True, white)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)

    def increase_difficulty(self, current_round, enemies):
        for enemy in enemies:
            if len(enemies) > 0:
                enemy.speed += current_round // 2
                enemy.health += int(current_round * 2.5)  # Slower scaling

    def pre_round_countdown(self, screen, font, player):
        # Move player to the shed location
        shed_exploration = True
        shed_text = font.render(
            "Explore the Shed! Press Enter to Start a new Round or P to go to the Shed",
            True, white
        )
        shed_text_rect = shed_text.get_rect(center=(width // 2, height // 2 - 50))

        # Exploration phase
        while shed_exploration:
            screen.fill(black)
            screen.blit(shed_text, shed_text_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Exit shed and prepare for countdown
                        shed_exploration = False
                    elif event.key == pygame.K_p:  # Go to shed
                        shed(player)


        # Countdown before the next round starts
        for i in range(3, 0, -1):
            screen.fill(black)
            countdown_text = font.render(f"Next Round in {i}...", True, white)
            countdown_rect = countdown_text.get_rect(center=(width // 2, height // 2))
            screen.blit(countdown_text, countdown_rect)
            pygame.display.flip()
            pygame.time.wait(1000)  # Wait for 1 second



