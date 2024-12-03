from config import *
import pygame


class Pause:
    @staticmethod
    def pause_game(screen, font, bg_color=black, text_color=white, active_timer=None, active_timer2 = None):
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

        # Pause music
        pygame.mixer.music.pause()

        # Pause the timer once
        if active_timer and not active_timer.paused:
            active_timer.pause()

        if active_timer2 and not active_timer2.paused:
            active_timer2.pause()
        while paused:
            screen.fill(bg_color)
            screen.blit(pause_text, (width // 2 - pause_text.get_width() // 2, height // 2 - 100))
            screen.blit(resume_text, (width // 2 - resume_text.get_width() // 2, height // 2))
            screen.blit(quit_text, (width // 2 - quit_text.get_width() // 2, height // 2 + 50))
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
                    elif event.key == pygame.K_q:  # Quit game
                        pygame.quit()
                        return "quit"

        # Resume music
        pygame.mixer.music.unpause()