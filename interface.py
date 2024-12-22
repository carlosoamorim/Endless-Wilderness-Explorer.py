from pygame import mixer

from utils import *  # Utility functions
from config import *  # Colors, resolution, width, height, etc.
from game import game_loop




def interface():
    """Main interface screen."""
    pygame.init()  # Initialize pygame
    screen = pygame.display.set_mode(resolution)  # Create the screen
    pygame.display.set_caption("Main Interface")  # Set window title


    # FONTS
    optimafont = pygame.font.SysFont("Optima", 40)
    optimafont_BOLD = pygame.font.SysFont("Optima", 60, bold=True)
    corbelfont = pygame.font.SysFont("Corbel", 50)
    comicsansfont = pygame.font.SysFont("Comic Sans MS", 50)

    
    # pygame.mixer.music.set_volume(0.1)  
    # mixer.init()

    # Load a sound for demonstration
    # mixer.music.load("music/Space Harrier Music - MAIN THEME.mp3")
    #mixer.music.play(-1)  # Loop the music


    # Text renderings
    wilderness_text = corbelfont.render("", True, white)
    title_text = optimafont_BOLD.render("KALLE STRIKES BACK", True, ikea_yellow)
    
    

    # Button coordinates and sizes
    buttons = [

        {"label": "Start Game", "action": start_game, "rect": (90, 240, 540, 60), "color": ikea_yellow},
        {"label": "Rules", "action":  rules, "rect": (90, 480, 140, 60), "color": ikea_yellow},
        {"label": "Options", "action": options, "rect": (90, 600, 140, 60), "color": ikea_yellow},
        {"label": "Credits", "action": credits_, "rect": (450, 480, 140, 60), "color": ikea_yellow},
        {"label": "Quit", "action": pygame.quit, "rect": (450, 600, 140, 60), "color": ikea_yellow},

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
    
    optimafont = pygame.font.SysFont("Optima", 40)
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Options")

    # Button positions and sizes
    button_width = 250
    button_height = 60
    button_x = (resolution[0] - button_width) // 2
    back_button_y = 600
    volume_increase_button_y = 300
    volume_decrease_button_y = 400
    volume_mute_button_y = 500
    # Initial volume
    volume = 0.5
    mixer.music.set_volume(volume)

    running = True
    while running:
        mouse = pygame.mouse.get_pos()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:                    
                
                if is_mouse_over_button(mouse, (button_x, volume_increase_button_y, button_width, button_height)):
                    volume = min(volume + 0.1, 1.0)  # Cap at 1.0
                    mixer.music.set_volume(volume)
                    # Increase volume
                
                elif is_mouse_over_button(mouse, (button_x, volume_decrease_button_y, button_width, button_height)):
                    volume = max(volume - 0.1, 0.0)  # Cap at 0.0
                    mixer.music.set_volume(volume)
                # Decrease volume
                
                elif is_mouse_over_button(mouse, (button_x, volume_mute_button_y, button_width, button_height)):
                    if mixer.music.get_volume() > 0:
                        volume = 0.0
                    else:
                        volume = 0.5
                    mixer.music.set_volume(volume)
                    # Mute/Unmute
                    
                elif is_mouse_over_button(mouse, (button_x, back_button_y, button_width, button_height)):
                    return  # Back button - Return to the interface 
                
        screen.fill(ikea_blue)

        # Draw buttons
        create_button(screen, "Back", ikea_yellow, button_x, back_button_y, button_width, button_height, optimafont)
        create_button(screen, "Volume +", ikea_yellow,button_x, volume_increase_button_y, button_width, button_height, optimafont)
        create_button(screen, "Volume -", ikea_yellow, button_x, volume_decrease_button_y, button_width, button_height, optimafont)
        create_button(screen, "Mute/Unmute", ikea_yellow, button_x, volume_mute_button_y, button_width, button_height, optimafont)
        
        
        # Display current volume
        volume_text = optimafont.render(f"Volume: {int(volume * 100)}%", True, white)
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
    # Rules screen

    optimafont = pygame.font.SysFont("Optima", 40)

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

                    print("Controls")
                elif is_mouse_over_button(mouse, (button_x, powerups_button_y, button_width, button_height)):
                    # Display power-ups

                    print("Power-ups")
                    
                elif is_mouse_over_button(mouse, (button_x, weapons_button_y, button_width, button_height)):
                    # Display weapons
                    display_weapons()
                    print("Weapons")
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
    # Weapons screen
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Weapons")
    
    optimafont = pygame.font.SysFont("Optima", 40)

    # Load weapon image
    weapon_image = pygame.image.load("images/weapon_rules.png").convert_alpha()
    weapon_image = pygame.transform.scale(weapon_image, resolution)  # Scale image to fit the screen

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

        screen.blit(weapon_image, (0, 0))  # Draw the weapon image

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