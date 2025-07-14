import pygame
import time

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

class StopWatchTimer:
    def __init__(self):
        self.start_time = time.time()
        self.total_paused_duration = 0
        self.paused_at = None
        self.elapsed_time = {
            "sec": 0,
            "min": 0,
            "hour": 0
        }

    def pause(self):
        if self.paused_at is None:
            self.paused_at = time.time()

    def resume(self):
        if self.paused_at is not None:
            self.total_paused_duration += time.time() - self.paused_at
            self.paused_at = None

    def update(self):
        if self.paused_at is not None:
            # While paused, do not update the time
            return self.format_elapsed()

        current_time = time.time()
        active_time = int(current_time - self.start_time - self.total_paused_duration)

        self.elapsed_time["hour"] = active_time // 3600
        self.elapsed_time["min"] = (active_time % 3600) // 60
        self.elapsed_time["sec"] = active_time % 60

        return self.format_elapsed()

    def format_elapsed(self):
        return f"{self.elapsed_time['hour']:02}:{self.elapsed_time['min']:02}:{self.elapsed_time['sec']:02}"