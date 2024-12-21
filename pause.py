from config import *
import pygame

class Pause:
    @staticmethod
    def pause_game(screen, font, bg_color=black, text_color=white, active_timer=None, active_timer2=None,
                   active_timer3=None, active_timer4=None, active_timer5=None):
        """
        Displays a pause menu and waits for the player to resume or quit.
        Args:
            screen: The Pygame display surface.
            font: Font object for rendering text.
            bg_color: Background color for the pause screen.
            text_color: Text color for the pause messages.
            active_timer: The currently active power-up timer.
        """
        paused = True
        pause_text = font.render("Game Paused", True, text_color)
        resume_text = font.render("Press ESC to Resume", True, text_color)
        quit_text = font.render("Press Q to Quit", True, text_color)
        volume_up_text = font.render("Press + to Increase Volume", True, text_color)
        volume_down_text = font.render("Press - to Decrease Volume", True, text_color)
        mute_text = font.render("Press M to Mute/Unmute", True, text_color)

        # Pause music
        pygame.mixer.music.pause()

        # Pause the timers
        if active_timer and not active_timer.paused:
            active_timer.pause()
        if active_timer2 and not active_timer2.paused:
            active_timer2.pause()
        if active_timer3 and not active_timer3.paused:
            active_timer3.pause()
        if active_timer4 and not active_timer4.paused:
            active_timer4.pause()
        if active_timer5 and not active_timer5.paused:
            active_timer5.pause()

        # Track volume
        volume = pygame.mixer.music.get_volume()

        while paused:
            screen.fill(bg_color)
            screen.blit(pause_text, (width // 2 - pause_text.get_width() // 2, height // 2 - 150))
            screen.blit(resume_text, (width // 2 - resume_text.get_width() // 2, height // 2 - 50))
            screen.blit(quit_text, (width // 2 - quit_text.get_width() // 2, height // 2))
            screen.blit(volume_up_text, (width // 2 - volume_up_text.get_width() // 2, height // 2 + 50))
            screen.blit(volume_down_text, (width // 2 - volume_down_text.get_width() // 2, height // 2 + 100))
            screen.blit(mute_text, (width // 2 - mute_text.get_width() // 2, height // 2 + 150))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Resume game
                        paused = False
                        if active_timer and active_timer.paused:
                            active_timer.resume()
                        if active_timer2 and active_timer2.paused:
                            active_timer2.resume()
                        if active_timer3 and active_timer3.paused:
                            active_timer3.resume()
                        if active_timer4 and active_timer4.paused:
                            active_timer4.resume()
                        if active_timer5 and active_timer5.paused:
                            active_timer5.resume()
                    elif event.key == pygame.K_q:  # Quit game
                        pygame.quit()
                        return "quit"
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:  # Increase volume
                        volume = min(volume + 0.1, 1.0)  # Cap at 1.0
                        pygame.mixer.music.set_volume(volume)
                    elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:  # Decrease volume
                        volume = max(volume - 0.1, 0.0)  # Cap at 0.0
                        pygame.mixer.music.set_volume(volume)
                    elif event.key == pygame.K_m:  # Mute/Unmute
                        if pygame.mixer.music.get_volume() > 0:
                            volume = 0.0
                        else:
                            volume = 0.5
                        pygame.mixer.music.set_volume(volume)

        # Resume music
        pygame.mixer.music.unpause()
