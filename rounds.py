import pygame
from config import *  # Import global configurations, such as screen dimensions and colors
from shed import shed  # Import the function or class related to the "shed" (barn/shelter)


# Rounds class: responsible for the game round logic
class Rounds:
    def display_round_message(self, message, screen, font):
        """Displays a message at the center of the screen with a shadow effect and underline."""
        # Render a shadow for the text with a dark gray color
        shadow_text = font.render(message, True, (50, 50, 50))  # Shadow color
        shadow_rect = shadow_text.get_rect(center=(width // 2 + 2, height // 2 + 2))
        screen.blit(shadow_text, shadow_rect)  # Draw the shadow on the screen

        # Render the main text in white
        text = font.render(message, True, white)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)  # Draw the text on the screen

        # Draw the underline in white
        underline_y = text_rect.bottom + 5  # Define the position just below the text
        underline_start = (text_rect.left, underline_y)  # Start point of the line
        underline_end = (text_rect.right, underline_y)  # End point of the line
        pygame.draw.line(screen, white, underline_start, underline_end, 2)  # White line with thickness 2

    def increase_difficulty(self, current_round, enemies):
        """Increases the difficulty of enemies based on the current round."""
        for enemy in enemies:  # Iterate through all enemies
            enemy.speed += current_round // 2  # Increase enemy speed
            enemy.health += int(10 + current_round * 2.5)  # Gradually increase enemy health

    def pre_round_countdown(self, screen, font, player, current_round):
        """Handles the shed exploration phase and the countdown before starting the round."""

        shed_exploration = True  # Set the player to the exploration phase of the "shed"

        # Background setup
        backgrounds = [
            pygame.transform.scale(pygame.image.load("images/rounds/loading_screen.png"), (width, height)),
        ]

        background = backgrounds[current_round - 1]

        # Render and position the second line of text (round number)
        shed_text2 = font.render(f"Press Enter to Start Round {current_round}", True, white)
        shed_text_rect2 = shed_text2.get_rect(center=(width // 2, 115))

        # Render and position the third line of text
        shed_text3 = font.render("or P to visit IKEA", True, black)
        shed_text_rect3 = shed_text3.get_rect(center=(width // 2, 150))

        # Shed exploration phase
        while shed_exploration:
            screen.blit(background, (0, 0))  # Draw the background on the screen
            screen.blit(shed_text2, shed_text_rect2)
            screen.blit(shed_text3, shed_text_rect3)
            pygame.display.flip()  # Update the screen to show elements

            # Process player events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # If the player closes the game
                    pygame.quit()
                    return  # Exit the program immediately
                elif event.type == pygame.KEYDOWN:  # If the player presses a key
                    if event.key == pygame.K_RETURN:  # Start the round
                        shed_exploration = False  # Exit the exploration phase
                    elif event.key == pygame.K_p:  # Enter the "shed"
                        shed(player)  # Execute the shed logic

        # Countdown phase
        for i in range(3, 0, -1):  # Countdown from 3 to 1
            screen.blit(background, (0, 0))  # Draw the background again
            overlay = pygame.Surface((width, height))  # Create a layer over the background
            overlay.set_alpha(180)  # Set the transparency of the layer
            overlay.fill((0, 0, 0))  # Fill the layer with black
            screen.blit(overlay, (0, 0))  # Apply the layer over the background

            # Render the countdown text
            countdown_text = font.render(f"Starting Round in {i}...", True, white)  # Text with the current number
            countdown_rect = countdown_text.get_rect(center=(width // 2, height // 2))  # Center the text
            screen.blit(countdown_text, countdown_rect)  # Display the text

            # Create a visual effect with concentric circles
            center = (width // 2, height // 2)  # Circle center
            base_radius = 100 + i * 20  # Define the initial radius that increases with the countdown
            for alpha, radius in zip(range(50, 0, -10), range(base_radius, base_radius + 50, 10)):
                # Create a transparent surface for each circle
                smooth_circle = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(
                    smooth_circle,
                    (34, 139, 34, alpha),  # Green color with transparency (RGBA)
                    (radius, radius),  # Central position of the circle
                    radius  # Radius of the circle
                )
                # Draw the smoothed circle on the screen
                screen.blit(smooth_circle, (center[0] - radius, center[1] - radius))

            pygame.display.flip()  # Update the screen to show changes
            pygame.time.wait(1000)  # Wait 1 second before continuing
