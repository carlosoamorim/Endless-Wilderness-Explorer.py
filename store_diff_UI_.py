import sys
from player import Player
import pygame

pygame.init()

# Screen settings
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Store")

# Fonts
FONT = pygame.font.SysFont("arial", 30)
SMALL_FONT = pygame.font.SysFont("arial", 24)

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

player = Player()
player_coins = player.wallet
current_weapon = None

weapons = [
    {"name": "Sword", "price": 50, "description": "A basic blade. Nothing too fancy, but it does the job."},
    {"name": "The Björn-and-Arrow™", "price": 75, "description": "Ethically-sourced birchwood bow with Runestone Arrows."},
    {"name": "Staff", "price": 100, "description": "A magical staff that channels arcane energy."},
    {"name": "Meatball Gun", "price": 60, "description": "Launches sizzling köttbullar with pinpoint accuracy."},
    {"name": "Falukorv Gun", "price": 80, "description": "Slaps foes with salami precision. Don't forget the mustard!"},
]

# Sounds
click_sound = pygame.mixer.Sound("music/Mouse Click Sound Effect.mp3")
purchase_sound = pygame.mixer.Sound("music/Cash Purchase Sound Effects.mp3")

# Padding
H_PADDING = 20
V_PADDING = 10

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

def draw_rounded_rect(surface, color, rect, radius=10, border=0, border_color=(0, 0, 0)):
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
                click_sound.play()
                # Close Store
                close_btn_text = "Close Store"
                cb_surf = FONT.render(close_btn_text, True, text_color)
                cb_w = cb_surf.get_width() + H_PADDING * 4
                cb_h = cb_surf.get_height() + V_PADDING * 4
                close_button_rect = pygame.Rect(WIDTH - cb_w - 20, 20, cb_w, cb_h)

                if close_button_rect.collidepoint(mx, my):
                    show_store = False

                # Sell Weapon
                sell_btn_text = "Sell Current Weapon"
                sell_button_rect = pygame.Rect(close_button_rect.x,
                                               close_button_rect.y + close_button_rect.height + 20,
                                               cb_w, cb_h)
                if sell_button_rect.collidepoint(mx, my) and current_weapon:
                    sell_price = current_weapon["price"] // 2
                    player_coins += sell_price
                    current_weapon = None

                # Buy Weapons
                start_y = 150
                for i, w in enumerate(weapons):
                    item_rect = pygame.Rect(100, start_y + i * 80, 400, 60)
                    if item_rect.collidepoint(mx, my):
                        if player_coins >= w["price"]:
                            player_coins -= w["price"]
                            current_weapon = w
                            purchase_sound.play()
                        else:
                            print("Not enough coins!")

        # Drawing Store Layout
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        panel_rect = pygame.Rect(50, 50, WIDTH - 100, HEIGHT - 100)
        draw_rounded_rect(screen, panel_bg, panel_rect, radius=20)

        title_surf = FONT.render("Weapon Store", True, text_color)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 90))
        screen.blit(title_surf, title_rect)

        # Display Coins
        coins_text_surf = FONT.render(f"Coins: {player_coins}", True, text_color)
        screen.blit(coins_text_surf, (60, 60))

        # Close Button
        close_btn_text = "Close Store"
        cb_surf = FONT.render(close_btn_text, True, text_color)
        cb_w = cb_surf.get_width() + H_PADDING * 4
        cb_h = cb_surf.get_height() + V_PADDING * 4
        close_button_rect = pygame.Rect(WIDTH - cb_w - 20, 20, cb_w, cb_h)
        draw_rounded_rect(screen, button_bg, close_button_rect, radius=10)
        draw_centered_text(screen, cb_surf, close_button_rect)

        # Tooltip and Buy Weapon Buttons
        start_y = 150
        hovered_weapon = None
        for i, w in enumerate(weapons):
            item_rect = pygame.Rect(100, start_y + i * 80, 400, 60)
            is_hovered = item_rect.collidepoint(mx, my)
            bg_col = item_hover_bg if is_hovered else item_bg
            draw_rounded_rect(screen, bg_col, item_rect, radius=10)

            item_text_surf = FONT.render(f"{w['name']} - {w['price']} coins", True, text_color)
            screen.blit(item_text_surf, (item_rect.x + H_PADDING, item_rect.y + V_PADDING))

            if is_hovered:
                hovered_weapon = w

        # Tooltip
        if hovered_weapon:
            tooltip_lines = wrap_text(hovered_weapon["description"], SMALL_FONT, 300)
            tooltip_x, tooltip_y = mx + 10, my + 10
            tooltip_width = max(SMALL_FONT.size(line)[0] for line in tooltip_lines) + 20
            tooltip_height = len(tooltip_lines) * SMALL_FONT.get_height() + 20
            tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)
            draw_rounded_rect(screen, tooltip_bg, tooltip_rect, radius=10)
            for i, line in enumerate(tooltip_lines):
                line_surf = SMALL_FONT.render(line, True, text_color)
                screen.blit(line_surf, (tooltip_x + 10, tooltip_y + 10 + i * SMALL_FONT.get_height()))

        pygame.display.flip()

# Main Game Loop
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
            open_btn_text = "Open Store"
            o_surf = FONT.render(open_btn_text, True, text_color)
            tw, th = o_surf.get_size()
            tw += H_PADDING * 2
            th += V_PADDING * 2
            store_button_rect = pygame.Rect((WIDTH - tw)//2, (HEIGHT - th)//2, tw, th)
            if store_button_rect.collidepoint(mx, my):
                show_store_gui(player)

    # Main Menu
    open_btn_text = "Open Store"
    o_surf = FONT.render(open_btn_text, True, text_color)
    tw, th = o_surf.get_size()
    tw += H_PADDING * 2
    th += V_PADDING * 2
    store_button_rect = pygame.Rect((WIDTH - tw)//2, (HEIGHT - th)//2, tw, th)
    is_hover = store_button_rect.collidepoint(mx, my)

    draw_rounded_rect(screen, button_hover_bg if is_hover else button_bg, store_button_rect, radius=8)
    draw_centered_text(screen, o_surf, store_button_rect)

    # Show Coins and Current Weapon
    coins_text = FONT.render(f"Coins: {player_coins}", True, text_color)
    screen.blit(coins_text, (20, 20))
    if current_weapon:
        weapon_text = FONT.render(f"Equipped: {current_weapon['name']}", True, text_color)
        screen.blit(weapon_text, (20, 60))

    pygame.display.flip()
    clock.tick(60)
