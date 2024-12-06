import pygame
from config import *
class Rounds:
    def display_round_message(self, message, screen, font):
        text = font.render(message, True, white)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)

    def increase_difficulty(self, current_round, enemies):
        for enemy in enemies:
            enemy.speed += current_round // 2
            enemy.health += int(10 + current_round * 2.5)  # Slower scaling

    def pre_round_countdown(self, screen, font):
        for i in range(3, 0, -1):
            screen.fill(black)  # Clear the screen
            countdown_text = font.render(f"Next Round in {i}...", True, white)
            countdown_rect = countdown_text.get_rect(center=(width // 2, height // 2))
            screen.blit(countdown_text, countdown_rect)
            pygame.display.flip()
            pygame.time.wait(1000)  # Wait for 1 second

