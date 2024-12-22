from pygame import mixer

from utils import *  # Utility functions
from config import *  # Colors, resolution, width, height, etc.
from game import game_loop



def interface():
    """Main interface screen."""
    pygame.init()  # Initialize pygame
    screen = pygame.display.set_mode(resolution)  # Create the screen
    pygame.display.set_caption("Main Interface")  # Set window title
    
    # pygame.mixer.music.set_volume(0.1)  
    # mixer.init()
    # Load a sound for demonstration
    # mixer.music.load("music/Space Harrier Music - MAIN THEME.mp3")
    #mixer.music.play(-1)  # Loop the music
    
    # Fonts
    corbelfont = pygame.font.SysFont("Corbel", 50)
    comicsansfont = pygame.font.SysFont("Comic Sans MS", 50)
    optimafont = pygame.font.SysFont("Optima", 40)
    


    # Text renderings
    wilderness_text = corbelfont.render("", True, white)
    title_text = optimafont.render("KALLE", True, ikea_yellow)
    
    

    # Button coordinates and sizes
    buttons = [
        {"label": "Start Game", "action": start_game, "rect": (90, 240, 540, 60), "color": ikea_yellow},
        {"label": "Rules", "action":  rules, "rect": (90, 480, 140, 60), "color": ikea_grey},
        {"label": "Options", "action": options, "rect": (90, 600, 140, 60), "color": ikea_grey},
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

        screen.fill(ikea_blue)  # Background

        # Draw buttons
        for button in buttons:
            create_button(screen, button["label"], button["color"], *button["rect"], optimafont)

        # Draw title
        screen.blit(title_text, (100, 150))
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

def options():
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Options")

    # Fonts
    corbelfont = pygame.font.SysFont("Corbel", 50)
    comicsansfont = pygame.font.SysFont("Comic Sans MS", 25)

    # Initial volume
    volume = 0.5
    mixer.music.set_volume(volume)

    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear screen
        mouse = pygame.mouse.get_pos()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                # Back button
                if is_mouse_over_button(mouse, (450, 600, 140, 60)):
                    return  # Return to the interface
                # Increase volume button
                elif is_mouse_over_button(mouse, (200, 300, 140, 60)):
                    volume = min(volume + 0.1, 1.0)  # Cap at 1.0
                    mixer.music.set_volume(volume)
                # Decrease volume button
                elif is_mouse_over_button(mouse, (200, 400, 140, 60)):
                    volume = max(volume - 0.1, 0.0)  # Cap at 0.0
                    mixer.music.set_volume(volume)
                # Mute/Unmute button
                elif is_mouse_over_button(mouse, (200, 500, 140, 60)):
                    if mixer.music.get_volume() > 0:
                        volume = 0.0
                    else:
                        volume = 0.5
                    mixer.music.set_volume(volume)

        # Draw buttons
        create_button(screen, "Back", dark_red, 450, 600, 140, 60, corbelfont)
        create_button(screen, "Volume +", green, 200, 300, 140, 60, corbelfont)
        create_button(screen, "Volume -", red, 200, 400, 140, 60, corbelfont)
        create_button(screen, "Mute/Unmute", dark_red, 200, 500, 140, 60, corbelfont)

        # Display current volume
        volume_text = comicsansfont.render(f"Volume: {int(volume * 100)}%", True, white)
        screen.blit(volume_text, (200, 200))

        pygame.display.update()
def credits_():
    """Credits screen."""
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Credits")

    # Fonts
    corbelfont = pygame.font.SysFont("Corbel", 50)
    comicsansfont = pygame.font.SysFont("Comic Sans MS", 25)

    # Credit Text
    credits = [
        
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


def start_game():
    game_loop()  # Call the game loop

def rules():
    #Rules screen

        # Fonts
        corbelfont = pygame.font.SysFont("Corbel", 50)
        comicsansfont = pygame.font.SysFont("Comic Sans MS", 25)

        screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption("Rules")




        rules = [
            "Hello there! Here is how the game works:",

            "-First: W- UP, S-DOWN, A-Left, D-RIGHT",

            "-Second: the bullets are automatic ",

            "-Third: There is a store after and before each round",
            "the store allows you,after collecting coins for killing enemies,",
            "buy a new weapon.",
            
            "-Fourth: This is a game with 12 rounds of enemies, if you",
            " are able to beat all of then, you win!",
            
            "And remember, FOR THE SWEDEN!"
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