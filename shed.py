import pygame
from config import *
from utils import *
from utils import under_construction
from store import load_store


def shed(player):
    # Basic setup
    background = pygame.image.load("images/ikea_shed.webp")
    background = pygame.transform.scale(background, (width, height))
    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    player.rect.left = 1
    
    # Music
    pygame.mixer.music.load("music/wigwalk.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # Interactive area
    ikea_entrance = pygame.Rect(450, 80, 160, 120)

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
        pygame.draw.rect(screen, (255, 255, 0), ikea_entrance, 3)  # Yellow border

        # Handle special area interaction
        if ikea_entrance.colliderect(player.rect):
            load_store(player)  # Trigger the under_construction screen
            player.rect.top = 200  # Reset player position to prevent instant re-trigger
            player.rect.left = 450

        # Return to main game
        if player.rect.left <= 0:
            player.rect.left = width - player.rect.width
            return "main"  # Transition back to the main game

        # Draw player
        screen.blit(player.image, player.rect)
        

        # Add exit hint
        exit_hint = pygame.font.Font(None, 36).render("← Exit to Main Area", True, white)
        screen.blit(exit_hint, (10, height // 2))
        # draw wallet:
        wallet_text = font.render(f"Wallet: {player.wallet}", True, white)
        screen.blit(wallet_text, (220, 50))
        pygame.display.flip()
