from pygame import mixer

from utils import *  # Utility functions
from config import *  # Colors, resolution, width, height, etc.
from game import game_loop

optimafont = pygame.font.SysFont("Optima", 30)



def interface():
    """Main interface screen."""
    pygame.init()  # Initialize pygame
    screen = pygame.display.set_mode(resolution)  # Create the screen
    pygame.display.set_caption("Main Interface")  # Set window title

    # FONTS
    optimafont = pygame.font.SysFont("Optima", 60)
    corbelfont = pygame.font.SysFont("Corbel", 50)
    comicsansfont = pygame.font.SysFont("Comic Sans MS", 50)
    
    mixer.init()
    # Load a sound for demonstration
    mixer.music.load("music/Space Harrier Music - MAIN THEME.mp3")
    mixer.music.play(-1)  # Loop the music
    # Fonts


    # Text renderings
    wilderness_text = corbelfont.render("Slaget om Sverige", True, white)
    title_text = optimafont.render("Slaget om Sverige", True, glowing_light_red)
    

    # Button coordinates and sizes
    buttons = [
        {"label": "Start Game", "action": wilderness_explorer, "rect": (90, 240, 540, 60), "color": dark_red},
        {"label": "Instruction", "action":  rules, "rect": (90, 480, 140, 60), "color": grey},
        {"label": "Options", "action": options, "rect": (90, 600, 140, 60), "color": grey},
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
        "Rodrigo Silva, 20221926@novaims.unl.pt",
        "Lukas, 20241448@novaims.unl.pt",
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
    # Rules screen

    optimafont = pygame.font.SysFont("Optima", 60)

    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Instruction")

    # Button positions and sizes
    button_width = 250
    button_height = 60
    button_x = (resolution[0] - button_width) // 2
    controls_button_y = 200
    powerups_button_y = 300
    weapons_button_y = 400

    running = True
    while running:
        mouse = pygame.mouse.get_pos()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if is_mouse_over_button(mouse, (button_x, controls_button_y, button_width, button_height)):
                    # Display controls
                    display_controls()
                    print("Controls")
                elif is_mouse_over_button(mouse, (button_x, powerups_button_y, button_width, button_height)):
                    print("Power-ups")
                    
                elif is_mouse_over_button(mouse, (button_x, weapons_button_y, button_width, button_height)):
                    display_weapons()

                elif is_mouse_over_button(mouse, (450, 600, 140, 60)):  # Back button
                    return  

        screen.fill(ikea_blue)

        # Create buttons
        create_button(screen, "Controls", ikea_yellow, button_x, controls_button_y, button_width, button_height, optimafont)
        create_button(screen, "Power-ups", ikea_yellow, button_x, powerups_button_y, button_width, button_height, optimafont)
        create_button(screen, "Weapons", ikea_yellow, button_x, weapons_button_y, button_width, button_height, optimafont)
        create_button(screen, "Back", ikea_yellow, 450, 600, 140, 60, optimafont)

        pygame.display.update()

def display_weapons():
    optimafont = pygame.font.SysFont("Optima", 30)
    # Weapons screen
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Weapons")

    # Load weapon images
    lingonberry = pygame.image.load("images/lingon.png").convert_alpha()
    meatball = pygame.image.load("images/meatball.png").convert_alpha()
    falukorv = pygame.image.load("images/falukorv.png").convert_alpha()

    # Scale weapon images
    lingonberry = pygame.transform.scale(lingonberry, (100, 100))
    meatball = pygame.transform.scale(meatball, (100, 100))
    falukorv = pygame.transform.scale(falukorv, (100, 100))

    # Weapon descriptions
    descriptions = {
        "lingonberry": "Lingonberry: The swedes use it to everything and apparently use them in war… Does not do a lot of damage - upgrade your weapon ASAP!",
        "meatball": "Meatball: Ah, the swedish meatball. Warm, delicious and… deadly? Does more damage than the lingonberries since it contains of more protein!",
        "falukorv": "Falukorv: A Swedish sausage from the small town of “Falun”. Works as a boomerang doing double damage.. Do not try at home (it’s just in the game)"
    }

    running = True
    while running:
        mouse = pygame.mouse.get_pos()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if is_mouse_over_button(mouse, (450, 600, 140, 60)):  # Back button
                    return  # Return to the previous screen

        screen.fill(ikea_blue)

        # Display weapon images and descriptions
        display_weapon(screen, lingonberry, descriptions["lingonberry"], 20, 200)
        display_weapon(screen, meatball, descriptions["meatball"], 250, 200)
        display_weapon(screen, falukorv, descriptions["falukorv"], 480, 200)

        # Create the "Back" button
        create_button(screen, "Back", ikea_yellow, 450, 600, 140, 60, optimafont)

        pygame.display.update()


def display_weapon(screen, image, description, x, y):
    # Draw image box
    pygame.draw.rect(screen, ikea_yellow, (x, y, 100, 100), 2)
    screen.blit(image, (x, y))

    # Draw description box
    description_box_y = y + 110
    pygame.draw.rect(screen, ikea_yellow, (x, description_box_y, 200, 100), 2)

    # Render description text with wrapping
    font = pygame.font.SysFont("Optima", 18)
    wrap_text(screen, description, font, (x + 5, description_box_y + 5), 190, (255, 255, 255))


def wrap_text(surface, text, font, position, max_width, color):
    """
    Renders text within a box of width `max_width`.
    Breaks text into multiple lines if necessary.
    """
    words = text.split()
    lines = []
    current_line = words.pop(0)

    for word in words:
        test_line = f"{current_line} {word}"
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)

    y_offset = 0
    for line in lines:
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (position[0], position[1] + y_offset))
        y_offset += font.size(line)[1] + 2

def display_controls():
    # Controls screen
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Controls")

    running = True
    while running:
        mouse = pygame.mouse.get_pos()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if is_mouse_over_button(mouse, (450, 600, 140, 60)):  # Back button
                    return  # Return to the previous screen

        screen.fill(ikea_blue)

        # Draw squares representing the controls with spacing
        spacing = 20
        controls = [("W", 340, 180), ("A", 230, 300), ("S", 340, 300), ("D", 450, 300)]
        for key, x, y in controls:
            pygame.draw.rect(screen, ikea_yellow, (x, y, 100, 100))
            text = optimafont.render(key, True, ikea_blue)
            text_rect = text.get_rect(center=(x + 50, y + 50))
            screen.blit(text, text_rect)
        
        # Manually split the control description into multiple lines
        control_description_lines = [
            "Use WASD to move the player.",
            "Kalle will shoot automatically,",
            "so you can focus on dodging enemies",
            "and collecting power-ups!"
        ]

        # Render each line of the control description
        y_offset = 450
        for line in control_description_lines:
            description_text = optimafont.render(line, True, ikea_yellow)
            screen.blit(description_text, (50, y_offset))
            y_offset += optimafont.get_linesize()

        # Create the "Back" button
        create_button(screen, "Back", ikea_yellow, 450, 600, 140, 60, optimafont)

        pygame.display.update()


def is_mouse_over_button(mouse_pos, button_rect):
    x, y, width, height = button_rect
    return x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height

def create_button(screen, text, color, x, y, width, height, font):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, ikea_blue)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)