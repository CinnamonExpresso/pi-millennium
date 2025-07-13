import pygame
import time
from behavior.gui.fontEngine import render_text_with_border

#For the sake of simplicity this will not be using the "main" guiEngine file
class Toast:
    def __init__(self, title, message, duration=3):
        self.title = title
        self.message = message
        self.start_time = time.time()
        self.duration = duration  # seconds
        self.font_title = pygame.font.SysFont('Arial', 20, bold=True)
        self.font_message = pygame.font.SysFont('Arial', 16)
        self.surface = self.create_surface()
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
    
    def create_surface(self):
        padding = 10
        title_surf = render_text_with_border(self.title, self.font_title, (255, 255, 255), (48, 48, 48), 2)
        msg_surf = render_text_with_border(self.message, self.font_message, (200, 200, 200), (48, 48, 48), 2)

        width = max(title_surf.get_width(), msg_surf.get_width()) + padding * 2
        height = title_surf.get_height() + msg_surf.get_height() + padding * 3 + 6

        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        surf.fill((30, 30, 30, 220))
        surf.blit(title_surf, (padding, padding))
        surf.blit(msg_surf, (padding, padding + title_surf.get_height() + 5))
        return surf

    def is_expired(self):
        return time.time() - self.start_time > self.duration

    def draw(self, screen, index, total_toasts):
        margin = 10
        x = screen.get_width() - self.width - margin
        y = screen.get_height() - ((self.height + margin) * (index + 1))

        # Draw the toast box
        screen.blit(self.surface, (x, y))

        # Draw time progress bar
        elapsed = time.time() - self.start_time
        remaining_ratio = max(0, 1 - (elapsed / self.duration))
        bar_width = int(self.width * remaining_ratio)
        bar_height = 4

        bar_rect = pygame.Rect(x, y + self.height - bar_height - 2, bar_width, bar_height, border_radius=5)
        pygame.draw.rect(screen, (100, 200, 100), bar_rect, border_radius=2)