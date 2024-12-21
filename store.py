import pygame
from config import *
from utils import *
from utils import under_construction
from store_diff_UI_ import *

class Store: 
    def __init__(self):
    
        self.restricted_areas = [
            pygame.Rect(0, 0, 190, 720),  # Left shelf
            pygame.Rect(530, 0, 190, 720),  # Right shelf
            pygame.Rect(0, 0, 720, 300),  # Back shelf
        ]
    def check_collision(self, player):
        for area in self.restricted_areas:
            if player.rect.colliderect(area):
                player.revert_position()  
                break
    
def load_store (player):
    background = pygame.image.load("images/backgrounds/store.png")
    background = pygame.transform.scale(background, (width, height))
    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()

    store = Store()

    player.rect.left = 320
    player.rect.top = height - player.rect.height - 10

    # Interactive area
    store_area = pygame.Rect(280, 300, 160, 70)

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

        store.check_collision(player)

         # CODE FOR VISUALIZING THE RESTRICTED AREAS
       # pygame.draw.rect(screen, (255, 255, 0), store_area, 3)  # Yellow border
        #for area in store.restricted_areas:
           # pygame.draw.rect(screen, (255, 0, 0), area, 3)

        # Handle special area interaction
        if store_area.colliderect(player.rect):
            #show_store_gui(player)
            player.rect.top = 420  # Reset player position to prevent instant re-trigger
            player.rect.left = 320

        # Return to main game
        if player.rect.bottom >= height:
            player.rect.bottom = 0
            return "shed"

        # Draw player
        screen.blit(player.image, player.rect)

        pygame.display.flip()
