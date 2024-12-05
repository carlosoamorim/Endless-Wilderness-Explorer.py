from utils import *  # Utility functions
from config import *  # Colors, resolution, width, height, etc.
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
        {"label": "Wilderness Explorer", "action": wilderness_explorer, "rect": (90, 240, 540, 60), "color": dark_red},
        {"label": "Rules", "action":  rules, "rect": (90, 480, 140, 60), "color": grey},
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
        "Rodrigo Silva, 20221926@novaims.unl.pt",
        "Lukas, drasteiro@novaims.unl.pt",
        "Philip, lrosenfeld@novaims.unl.pt",
        "Carlos Amorim,  ",
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

def rules():
    #Rules screen

        # Fonts
        corbelfont = pygame.font.SysFont("Corbel", 50)
        comicsansfont = pygame.font.SysFont("Comic Sans MS", 25)

        screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption("Rules")




        rules = [
            "Rodrigo Silva, 20221926@novaims.unl.pt",
            "Lukas Andersson, 20241448@novaims.unl.pt",
            "Philip Munther, 20241463@novaims.unl.pt",
            "Carlos Amorim,  20211548@novaims.unl.pt",
        ]
        rendered_rules = [comicsansfont.render(rule, True, white) for rule in rules]

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
            for i, rule in enumerate(rendered_rules):
                screen.blit(rule, (10, 50 * i + 10))

            create_button(screen, "Back", dark_red, 450, 600, 140, 60, corbelfont)

            pygame.display.update()