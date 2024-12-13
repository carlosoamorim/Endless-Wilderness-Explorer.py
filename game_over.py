import pygame
from config import * # width, height
from main import main  # Import the interface function
from interface import *

def game_over_screen():
    pygame.init()

    # Initialize the mixer for sound
    pygame.mixer.init()

    # Screen setup
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Game Over")

    # Fonts
    font = pygame.font.Font(None, 72)
    button_font = pygame.font.Font(None, 48)

    # Button setup
    button_rect = pygame.Rect((width // 2 - 100, height // 2 + 50), (200, 50))

    # Game Over loop
    running = True
    while running:
        screen.fill(black)

        # Game Over text
        game_over_text = font.render("Game Over", True, white)
        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - 100))

        # Back button
        pygame.draw.rect(screen, red, button_rect)
        button_text = button_font.render("Back", True, white)
        screen.blit(button_text, (button_rect.x + 50, button_rect.y + 10))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    # Return to the main interface
                    return interface()

        from game import game_loop

        def interface():
            """Main interface screen."""
            pygame.init()  # Initialize pygame
            screen = pygame.display.set_mode(resolution)  # Create the screen
            pygame.display.set_caption("Main Interface")  # Set window title

            # Fonts
            corbelfont = pygame.font.SysFont("Corbel", 50)
            comicsansfont = pygame.font.SysFont("Comic Sans MS", 50)

            # Text renderings
            wilderness_text = corbelfont.render("Wilderness Explorer", True, white)
            title_text = comicsansfont.render("Computation III - Project", True, glowing_light_red)

            # Button coordinates and sizes
            buttons = [
                {"label": "Wilderness Explorer", "action": wilderness_explorer, "rect": (90, 240, 540, 60),
                 "color": dark_red},
                {"label": "Rules", "action": under_construction, "rect": (90, 480, 140, 60), "color": grey},
                {"label": "Options", "action": under_construction, "rect": (90, 600, 140, 60), "color": grey},
                {"label": "Credits", "action": credits_, "rect": (450, 480, 140, 60), "color": grey},
                {"label": "Quit", "action": pygame.quit, "rect": (450, 600, 140, 60), "color": grey},
            ]

            running = True
            while running:
                mouse = pygame.mouse.get_pos()

                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif ev.type == pygame.MOUSEBUTTONDOWN:
                        # Handle button clicks
                        for button in buttons:
                            if is_mouse_over_button(mouse, button["rect"]):
                                button["action"]()  # Execute the associated action

                screen.fill(deep_black)  # Background

                # Draw buttons
                for button in buttons:
                    create_button(screen, button["label"], button["color"], *button["rect"], corbelfont)

                # Draw title
                screen.blit(title_text, (55, 0))

                pygame.display.update()

        def create_button(screen, text, color, x, y, width, height, font):
            """Helper function to draw a button with text."""
            pygame.draw.rect(screen, color, [x, y, width, height])
            text_rendered = font.render(text, True, white)
            text_rect = text_rendered.get_rect(center=(x + width // 2, y + height // 2))
            screen.blit(text_rendered, text_rect)

        def is_mouse_over_button(mouse_pos, rect):
            """Check if the mouse is over a button."""
            x, y, width, height = rect
            return x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height

        def credits_():
            """Credits screen."""
            screen = pygame.display.set_mode(resolution)
            pygame.display.set_caption("Credits")

            # Fonts
            corbelfont = pygame.font.SysFont("Corbel", 50)
            comicsansfont = pygame.font.SysFont("Comic Sans MS", 25)

            # Credit Text
            credits = [
                "Augusto Santos, ajrsantos@novaims.unl.pt",
                "Diogo Rastreio, drasteiro@novaims.unl.pt",
                "Liah Rosenfeld, lrosenfeld@novaims.unl.pt",
            ]
            rendered_credits = [comicsansfont.render(credit, True, white) for credit in credits]

            running = True
            while running:
                mouse = pygame.mouse.get_pos()

                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif ev.type == pygame.MOUSEBUTTONDOWN:
                        if is_mouse_over_button(mouse, (450, 600, 140, 60)):  # Back button
                            return  # Return to the interface

                screen.fill(deep_black)

                # Display credits
                for i, credit in enumerate(rendered_credits):
                    screen.blit(credit, (10, 50 * i + 10))

                create_button(screen, "Back", dark_red, 450, 600, 140, 60, corbelfont)

                pygame.display.update()

        def wilderness_explorer():
            """Start the game."""
            game_loop()  # Call the game loop

        pygame.display.flip()
