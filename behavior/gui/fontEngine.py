import pygame

def render_text_with_border(text, font, text_color, border_color, border_width=2):
    base = font.render(text, True, text_color)
    size = (base.get_width() + border_width * 2, base.get_height() + border_width * 2)
    surface = pygame.Surface(size, pygame.SRCALPHA)

    # Draw border by rendering text around the center in 8 directions
    for dx in range(-border_width, border_width + 1):
        for dy in range(-border_width, border_width + 1):
            if dx != 0 or dy != 0:
                offset_text = font.render(text, True, border_color)
                surface.blit(offset_text, (dx + border_width, dy + border_width))

    # Draw main text in center
    surface.blit(base, (border_width, border_width))
    return surface
