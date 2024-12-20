import pygame
from config import *
from utils import *
from utils import under_construction


def load_store (player):
    # Basic setup
    background = pygame.image.load("images/backgrounds/store.png")
    background = pygame.transform.scale(background, (width, height))
    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()

    player.rect.left = 320
    player.rect.top = height - player.rect.height - 10

    # Interactive area
    store_area = pygame.Rect(280, 300, 160, 70)
    
    store_shelf_left = pygame.Rect(0, 0, 190, 720)
    store_shelf_right = pygame.Rect(530, 0, 190, 720)
    store_shelf_back = pygame.Rect(0, 0, 720, 300)

    running = True
    while running:
        clock.tick(fps)
        screen.blit(background, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Update the player's position
        player.update()

         # Highlight special area
        pygame.draw.rect(screen, (255, 255, 0), store_area, 3)  # Yellow border
        pygame.draw.rect(screen, (255, 255, 0), store_shelf_left, 3)  
        pygame.draw.rect(screen, (255, 255, 0), store_shelf_right, 3)  
        pygame.draw.rect(screen, (255, 255, 0), store_shelf_back, 3)

        # Handle special area interaction
        if store_area.colliderect(player.rect):
            under_construction()  # Trigger the under_construction screen
            player.rect.top = 420  # Reset player position to prevent instant re-trigger
            player.rect.left = 320

        # Return to main game
        if player.rect.bottom >= height:
            player.rect.bottom = 0
            return "shed"  

        # Draw player
        screen.blit(player.image, player.rect)

        pygame.display.flip()









#def under_construction():

    # creating the screen at 720x720 pixels
    background = pygame.image.load("images/ikea_shed.webp")
    background = pygame.transform.scale(background, (width, height))
    screen = pygame.display.set_mode(resolution)

    # setting my texts:
    back_text = corbelfont.render("back", True, white)
    construction_text = corbelfont.render("UNDER CONSTRUCTION", True, white)
    first_speech = conversation_font.render("Can we fix it?", True, white)
    bob_speech = conversation_font.render("Probably not...", True, white)

    # setting up the "images" positions
    bob_x_position = 460
    bob_y_position = 450

    normal_x_position = 260
    normal_y_position = 450

    # same old, same old while True loop

    while True:
        # getting the mouse position
        mouse = pygame.mouse.get_pos()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                # checking if the back button was clicked
                if 450 <= mouse[0] <= 590 and 600 <= mouse[1] <= 660:
                    return

        # displaying the screen:
        screen.fill(deep_black)

        # displaying the main UNDER CONSTRUCTION text
        construction_rect = construction_text.get_rect(center=(720 // 2, 300))
        screen.blit(construction_text, construction_rect)

        # drawing the back button
        pygame.draw.rect(screen, dark_red, [450, 600, 140, 60])
        back_rect = back_text.get_rect(center=(450 + 140 // 2, 600 + 60 // 2))
        screen.blit(back_text, back_rect)

        # stick figures text and "images"
        draw_normal_stick_figure(screen, normal_x_position, normal_y_position)
        draw_stick_figure_with_hat(screen, bob_x_position, bob_y_position)

        screen.blit(first_speech, (normal_x_position - 60, normal_y_position -80))
        screen.blit(bob_speech, (bob_x_position - 60, bob_y_position - 80))

        # finally, as always, updating our screen
        pygame.display.update()