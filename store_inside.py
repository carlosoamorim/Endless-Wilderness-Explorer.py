import sys
from player import Player
import pygame

pygame.init()

# Screen settings
WIDTH, HEIGHT = 720, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Store")

# Fonts
FONT = pygame.font.SysFont("arial", 24)
SMALL_FONT = pygame.font.SysFont("arial", 18)

# Colors
dark_bg = (30, 30, 30)        # Dark background
panel_bg = (40, 40, 40, 230)  # Semi-transparent dark panel
accent_color = (0, 150, 136)  # Teal accent color
text_color = (220, 220, 220)
button_bg = (60, 60, 60)
button_hover_bg = (80, 80, 80)
item_bg = (50, 50, 50)
item_hover_bg = (70, 70, 70)
tooltip_bg = (60, 60, 60)

# Padding for UI elements
H_PADDING = 15
V_PADDING = 8

# Initialize player
player = Player()
player_coins = player.wallet
current_weapon = None

# Weapons and sounds
weapons = [
    {"name": "Meatball", "price": 60, "description": "Launches sizzling köttbullar with pinpoint accuracy."},
    {"name": "Falukorv", "price": 80, "description": "Deliciously deadly sausage that surprisingly has a boomerang shape..."},
    {"name": "Exit", "price": 0, "description": "Click this button to get out of the store."}
]
#click_sound = pygame.mixer.Sound("music/Mouse Click Sound Effect.mp3")
#purchase_sound = pygame.mixer.Sound("music/Cash Purchase Sound Effects.mp3")

# Helper functions
def wrap_text(text, font, max_width):
    paragraphs = text.split('\n')
    lines = []
    for paragraph in paragraphs:
        words = paragraph.split(' ')
        line = ""
        for word in words:
            test_line = (line + " " + word).strip()
            if font.size(test_line)[0] <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        if paragraph.strip() == "":
            lines.append("")
    while lines and lines[-1] == "":
        lines.pop()
    return lines

def draw_rounded_rect(surface, color, rect, radius=8, border=0, border_color=(0, 0, 0)):
    x, y, w, h = rect
    pygame.draw.rect(surface, color, (x+radius, y, w-2*radius, h))
    pygame.draw.rect(surface, color, (x, y+radius, w, h-2*radius))
    pygame.draw.circle(surface, color, (x+radius, y+radius), radius)
    pygame.draw.circle(surface, color, (x+w-radius, y+radius), radius)
    pygame.draw.circle(surface, color, (x+radius, y+h-radius), radius)
    pygame.draw.circle(surface, color, (x+w-radius, y+h-radius), radius)
    if border > 0:
        pygame.draw.rect(surface, border_color, rect, border, border_radius=radius)

def draw_centered_text(surface, text_surf, rect):
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

def show_store_gui(player):
    global player_coins, current_weapon
    show_store = True
    while show_store:
        screen.fill(dark_bg)
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #click_sound.play()

                # Handle weapon buttons
                start_y = 120
                for i, w in enumerate(weapons):
                    item_rect = pygame.Rect(50, start_y + i * 70, 300, 50)
                    if item_rect.collidepoint(mx, my):
                        if w["name"] == "Exit":  # Check if the clicked weapon is the "Exit" button
                            show_store = False  # Exit the store
                            print("Exiting the store...")
                        elif player.wallet >= w["price"]:
                            player.wallet -= w["price"]
                            player.change_weapon(w["name"])

                            #purchase_sound.play()
                        else:
                            print("Not enough coins!")

        # Draw Layout
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        panel_rect = pygame.Rect(40, 40, WIDTH - 80, HEIGHT - 80)
        draw_rounded_rect(screen, panel_bg, panel_rect, radius=15)

        # Title
        title_surf = FONT.render("Weapon Store", True, text_color)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 80))
        screen.blit(title_surf, title_rect)

        # Coins
        coins_text_surf = FONT.render(f"Coins: {player.wallet}", True, text_color)
        screen.blit(coins_text_surf, (50, 50))

        # Tooltip and Items
        start_y = 120
        hovered_weapon = None
        for i, w in enumerate(weapons):
            item_rect = pygame.Rect(50, start_y + i * 70, 300, 50)
            is_hovered = item_rect.collidepoint(mx, my)
            bg_col = item_hover_bg if is_hovered else item_bg
            draw_rounded_rect(screen, bg_col, item_rect, radius=8)

            item_text_surf = FONT.render(f"{w['name']} - {w['price']} coins", True, text_color)
            screen.blit(item_text_surf, (item_rect.x + 10, item_rect.y + 10))

            if is_hovered:
                hovered_weapon = w

        if hovered_weapon:
            tooltip_lines = wrap_text(hovered_weapon["description"], SMALL_FONT, 300)
            tooltip_x, tooltip_y = mx + 10, my + 10
            tooltip_width = max(SMALL_FONT.size(line)[0] for line in tooltip_lines) + 20
            tooltip_height = len(tooltip_lines) * SMALL_FONT.get_height() + 20
            tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)
            draw_rounded_rect(screen, tooltip_bg, tooltip_rect, radius=8)
            for i, line in enumerate(tooltip_lines):
                line_surf = SMALL_FONT.render(line, True, text_color)
                screen.blit(line_surf, (tooltip_x + 10, tooltip_y + 10 + i * SMALL_FONT.get_height()))

        pygame.display.flip()


def main():
    clock = pygame.time.Clock()
    while True:
        screen.fill(dark_bg)
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()

                # Check for "Exit" button
                exit_btn_text = "Exit"
                eb_surf = FONT.render(exit_btn_text, True, text_color)
                eb_w = eb_surf.get_width() + H_PADDING * 2
                eb_h = eb_surf.get_height() + V_PADDING * 2
                exit_button_rect = pygame.Rect((WIDTH - eb_w) // 2, (HEIGHT - eb_h) // 2, eb_w, eb_h)

                if exit_button_rect.collidepoint(mx, my):
                    print("Returning to store.py")
                    pygame.quit()
                    sys.exit()

                # Open Store
                open_btn_text = "Open Store"
                o_surf = FONT.render(open_btn_text, True, text_color)
                tw, th = o_surf.get_size()
                tw += H_PADDING * 2
                th += V_PADDING * 2
                store_button_rect = pygame.Rect((WIDTH - tw) // 2, (HEIGHT - th) // 2 - 100, tw, th)
                if store_button_rect.collidepoint(mx, my):
                    show_store_gui(player)

        # Draw main screen
        open_btn_text = "Open Store"
        o_surf = FONT.render(open_btn_text, True, text_color)
        tw, th = o_surf.get_size()
        tw += H_PADDING * 2
        th += V_PADDING * 2
        store_button_rect = pygame.Rect((WIDTH - tw) // 2, (HEIGHT - th) // 2 - 100, tw, th)
        is_hover_store = store_button_rect.collidepoint(mx, my)

        draw_rounded_rect(screen, button_hover_bg if is_hover_store else button_bg, store_button_rect, radius=10)
        draw_centered_text(screen, o_surf, store_button_rect)

        # Draw Exit button
        exit_btn_text = "Exit"
        eb_surf = FONT.render(exit_btn_text, True, text_color)  # Render the text
        eb_w = eb_surf.get_width() + H_PADDING * 2
        eb_h = eb_surf.get_height() + V_PADDING * 2

        # Center the button
        exit_button_rect = pygame.Rect((WIDTH - eb_w) // 2, (HEIGHT - eb_h) // 2, eb_w, eb_h)
        is_hover_exit = exit_button_rect.collidepoint(mx, my)  # Check if the mouse is hovering

        # Draw a temporary debug rectangle for the button
        pygame.draw.rect(screen, (255, 0, 0), exit_button_rect)  # Debug: Draw a red rectangle for visibility

        # Draw the button background with rounded corners
        draw_rounded_rect(screen, button_hover_bg if is_hover_exit else button_bg, exit_button_rect, radius=10)

        # Draw the button text
        draw_centered_text(screen, eb_surf, exit_button_rect)

        # Coins and Weapon Info
        coins_text = FONT.render(f"Coins: {player.wallet}", True, text_color)
        screen.blit(coins_text, (20, 20))
        if current_weapon:
            weapon_text = FONT.render(f"Equipped: {current_weapon['name']}", True, text_color)
            screen.blit(weapon_text, (20, 60))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
