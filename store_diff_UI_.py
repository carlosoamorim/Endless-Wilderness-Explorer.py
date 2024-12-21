

pygame.init()

# Screen settings
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Store")

# Fonts
FONT = pygame.font.SysFont("arial", 30)
SMALL_FONT = pygame.font.SysFont("arial", 24)

# colors
dark_bg = (30, 30, 30)        # dark background
panel_bg = (40, 40, 40, 230)  # semi-transparent dark panel
accent_color = (0, 150, 136)  # teal accent color
text_color = (220, 220, 220)
button_bg = (60, 60, 60)
button_hover_bg = (80, 80, 80)
item_bg = (50, 50, 50)
item_hover_bg = (70, 70, 70)
tooltip_bg = (60, 60, 60)

player_coins = 100
current_weapon = None

weapons = [
    {
        "name": "Sword",
        "price": 50,
        "description": "A basic blade. Nothing too fancy, but it does the job. Much like the creators of this game."
    },
    {
        "name": "The Björn-and-Arrow™",
        "price": 75,
        "description": (
            "The Björn-and-Arrow™ — Serving Katniss Everdeen but make it Scandi-core."
            "This sleek, ethically-sourced birchwood baddie lets you snipe monsters "
            "from 500 meters while looking like you just walked off a Viking runway. "
            "Oh, and it shoots glowing Runestone Arrows that scream ‘SKOL’ as they fly. Slay (literally)!"
        )
    },
    {
        "name": "Staff",
        "price": 100,
        "description": "A magical staff that channels arcane energy."
    },
    {
        "name": "Meatball Gun",
        "price": 60,
        "description": (
            "Introducing the culinary cannon of chaos:\n\n"
            "The Meatball Gun! This bad boy launches sizzling, gravy-drenched köttbullar "
            "with pinpoint accuracy, faster than you can say IKEA assembly instructions. "
            "Watch your enemies get absolutely smörgåsboarded into submission. "
            "Side effects may include hunger pangs and a sudden desire to furniture shop!"
        )
    },
    {
        "name": "Falukorv Gun",
        "price": 80,
        "description": (
            "Say hello to the tubular terror:\n\n"
            "The Falukorv Gun! Armed with Sweden’s favorite sausage, this weapon "
            "slaps foes with salami precision. Perfect for sizzling action "
            "and leaving a meaty impression. Just don’t forget the mustard!"
        )
    },
]

show_store = False

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

def draw_rounded_rect(surface, color, rect, radius=10, border=0, border_color=(0,0,0)):
    """
    Draw a rectangle with rounded corners.
    """
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
    """
    Helper to draw text_surf centered in rect.
    """
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

clock = pygame.time.Clock()

while True:
    screen.fill(dark_bg)
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if show_store:
                # 1) Close Store Button
                close_btn_text = "Close Store"
                cb_surf = FONT.render(close_btn_text, True, text_color)
                cb_w = cb_surf.get_width() + H_PADDING * 4
                cb_h = cb_surf.get_height() + V_PADDING * 4
                close_button_rect = pygame.Rect(WIDTH - cb_w - 20, 20, cb_w, cb_h)

                if close_button_rect.collidepoint(mx, my):
                    show_store = False

                # 2) Sell Current Weapon Button (always visible below close store)
                sell_btn_text = "Sell Current Weapon"
                sb_surf = FONT.render(sell_btn_text, True, text_color)
                sb_w = sb_surf.get_width() + H_PADDING * 2
                sb_h = sb_surf.get_height() + V_PADDING * 2
                sell_button_rect = pygame.Rect(close_button_rect.x,
                                               close_button_rect.y + close_button_rect.height + 20,
                                               sb_w, sb_h)

                if sell_button_rect.collidepoint(mx, my):
                    # If the player has a weapon, sell it. Otherwise, do nothing.
                    if current_weapon is not None:
                        sell_price = current_weapon["price"] // 2
                        player_coins += sell_price
                        current_weapon = None

                # 3) Buy Weapons
                start_y = 150
                for i, w in enumerate(weapons):
                    item_text_str = f"{w['name']} - {w['price']} coins"
                    item_text_surf = FONT.render(item_text_str, True, text_color)
                    item_tw, item_th = item_text_surf.get_size()

                    # Extra width for comfort
                    item_width = item_tw + H_PADDING * 2 + 100
                    item_height = item_th + V_PADDING * 2
                    item_rect = pygame.Rect(100, start_y + i * 80, item_width, item_height)

                    if item_rect.collidepoint(mx, my):
                        if player_coins >= w["price"]:
                            player_coins -= w["price"]
                            current_weapon = w
                        else:
                            print("Not enough coins!")
            else:
                # Main Screen: Open Store Button
                open_btn_text = "Open Store"
                o_surf = FONT.render(open_btn_text, True, text_color)
                tw, th = o_surf.get_size()
                tw += H_PADDING * 2
                th += V_PADDING * 2
                store_button_rect = pygame.Rect((WIDTH - tw)//2, (HEIGHT - th)//2, tw, th)
                if store_button_rect.collidepoint(mx, my):
                    show_store = True

    # Drawing
    if show_store:
        # Dark overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Store panel
        panel_rect = pygame.Rect(50, 50, WIDTH - 100, HEIGHT - 100)
        draw_rounded_rect(screen, panel_bg, panel_rect, radius=20)

        # Title
        title_surf = FONT.render("Weapon Store", True, text_color)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 90))
        screen.blit(title_surf, title_rect)

        # Close Store Button
        close_btn_text = "Close Store"
        cb_surf = FONT.render(close_btn_text, True, text_color)
        cb_w = cb_surf.get_width() + H_PADDING * 4
        cb_h = cb_surf.get_height() + V_PADDING * 4
        close_button_rect = pygame.Rect(WIDTH - cb_w - 20, 20, cb_w, cb_h)
        hovered_close = close_button_rect.collidepoint(mx, my)
        draw_rounded_rect(screen, button_hover_bg if hovered_close else button_bg, close_button_rect, 8)
        draw_centered_text(screen, cb_surf, close_button_rect)

        # Sell Current Weapon Button (always drawn, below close store)
        sell_btn_text = "Sell Current Weapon"
        sb_surf = FONT.render(sell_btn_text, True, text_color)
        sb_w = sb_surf.get_width() + H_PADDING * 2
        sb_h = sb_surf.get_height() + V_PADDING * 2
        sell_button_rect = pygame.Rect(close_button_rect.x,
                                       close_button_rect.y + close_button_rect.height + 20,
                                       sb_w, sb_h)
        hovered_sell = sell_button_rect.collidepoint(mx, my)
        draw_rounded_rect(screen, button_hover_bg if hovered_sell else button_bg, sell_button_rect, 8)
        draw_centered_text(screen, sb_surf, sell_button_rect)

        # Display coins
        coins_text_surf = FONT.render(f"Coins: {player_coins}", True, text_color)
        screen.blit(coins_text_surf, (60, 60))

        # If weapon is owned, show some info under the Sell button
        if current_weapon:
            sell_price = current_weapon["price"] // 2
            sell_info_text = SMALL_FONT.render(f"Sell for {sell_price} coins", True, text_color)
            screen.blit(sell_info_text, (sell_button_rect.x + 10,
                                         sell_button_rect.y + sell_button_rect.height + 5))

        # List weapons
        hovered_weapon = None
        start_y = 150
        for i, w in enumerate(weapons):
            item_text_str = f"{w['name']} - {w['price']} coins"
            item_text_surf = FONT.render(item_text_str, True, text_color)
            item_tw, item_th = item_text_surf.get_size()

            # Make item buttons wider
            item_width = item_tw + H_PADDING * 2 + 100
            item_height = item_th + V_PADDING * 2
            item_rect = pygame.Rect(100, start_y + i * 80, item_width, item_height)

            is_hovered = item_rect.collidepoint(mx, my)
            bg_col = item_hover_bg if is_hovered else item_bg
            draw_rounded_rect(screen, bg_col, item_rect, radius=10)
            screen.blit(item_text_surf, (item_rect.x + H_PADDING, item_rect.y + V_PADDING))

            if is_hovered:
                hovered_weapon = w

        # Tooltip
        if hovered_weapon:
            max_tooltip_width = 400
            lines = wrap_text(hovered_weapon["description"], SMALL_FONT, max_tooltip_width)
            line_height = SMALL_FONT.get_height()
            tooltip_width = max(SMALL_FONT.size(line)[0] for line in lines) + 40
            tooltip_height = line_height * len(lines) + 40

            tooltip_x = mx + 20
            tooltip_y = my + 20

            if tooltip_x + tooltip_width > WIDTH:
                tooltip_x = WIDTH - tooltip_width - 20
            if tooltip_y + tooltip_height > HEIGHT:
                tooltip_y = HEIGHT - tooltip_height - 20

            tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)
            draw_rounded_rect(screen, tooltip_bg, tooltip_rect, radius=10)

            y_offset = tooltip_y + 20
            for line in lines:
                desc_surf = SMALL_FONT.render(line, True, text_color)
                screen.blit(desc_surf, (tooltip_x + 20, y_offset))
                y_offset += line_height

    else:
        # Main screen
        # Display coins
        coins_text = FONT.render(f"Coins: {player_coins}", True, text_color)
        screen.blit(coins_text, (20, 20))

        # "Open Store" button
        open_btn_text = "Open Store"
        o_surf = FONT.render(open_btn_text, True, text_color)
        tw, th = o_surf.get_size()
        tw += H_PADDING * 2
        th += V_PADDING * 2
        store_button_rect = pygame.Rect((WIDTH - tw)//2, (HEIGHT - th)//2, tw, th)
        is_hover = store_button_rect.collidepoint(mx, my)

        draw_rounded_rect(screen, button_hover_bg if is_hover else button_bg, store_button_rect, radius=8)
        draw_centered_text(screen, o_surf, store_button_rect)

        # Current weapon display
        if current_weapon:
            owned_text = FONT.render(f"Current Weapon: {current_weapon['name']}", True, text_color)
            screen.blit(owned_text, (20, 60))

    pygame.display.flip()
    clock.tick(60)
