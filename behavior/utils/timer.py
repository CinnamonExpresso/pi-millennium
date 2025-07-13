import pygame

# Currently calculated in milliseconds,
# 1000 millseconds == 1 second
class Timer:
    def __init__(self, duration, func=None):
        self.duration: int | float = duration
        self.func: function = func
        self.start_time: int | float = 0
        self.active: bool = False

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    # deactivate the timer
    def deactivate(self):
        self.active = False
        self.start_time = 0

    def change_duration(self, duration):
        self.duration = duration

    # is called continusly, updates timer
    def update(self):
        current_time: int | float = pygame.time.get_ticks()

        # checks if timer is run out
        if current_time - self.start_time >= self.duration:
            if self.func and self.start_time != 0:
                self.func()
            self.deactivate()