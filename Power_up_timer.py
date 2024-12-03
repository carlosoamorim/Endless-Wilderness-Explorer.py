import pygame


class Timer:
    def __init__(self):
        self.maximum = 0  # Duration of the timer in seconds
        self.start_ticks = None  # Start time in milliseconds
        self.running = False  # Timer state
        self.seconds = 0  # Elapsed time in seconds
        self.paused = False  # Pause state
        self.pause_time = 0  # Time when paused

    def start(self, maximum):
        self.maximum = int(maximum)
        self.start_ticks = pygame.time.get_ticks()
        self.running = True
        self.paused = False

    def update(self):
        if not self.running or self.paused:
            return False  # Timer is not running or paused

        self.seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
        if self.seconds >= self.maximum:
            self.stop()
            return False
        return True

    def stop(self):
        self.running = False

    def reset(self):
        self.running = False
        self.paused = False
        self.start_ticks = None
        self.seconds = 0

    def pause(self):
        if self.running and not self.paused:
            self.paused = True
            self.pause_time = pygame.time.get_ticks()

    def resume(self):
        if self.running and self.paused:
            paused_duration = pygame.time.get_ticks() - self.pause_time
            self.start_ticks += paused_duration  # Adjust the start time
            self.paused = False

    def get_remaining_time(self):
        if not self.running:
            return 0
        if self.paused:
            return max(0, self.maximum - self.seconds)
        elapsed_time = (pygame.time.get_ticks() - self.start_ticks) / 1000
        return max(0, self.maximum - elapsed_time)
