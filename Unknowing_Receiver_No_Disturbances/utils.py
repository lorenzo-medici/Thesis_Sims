import pygame

# TYPES

type x_state_t = tuple[float] | tuple[float, float]
type iota_t = x_state_t
type reading_t = list[float]

# COLORS

AXES = (200, 200, 200)
BACKGROUND = (30, 30, 30)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# CONSTANTS

(display_width, display_height) = (500, 400)

# TEXT

fonts = {}


def text(surface, x, y, content, size=20, colour=AXES):
    if size in fonts:
        font = fonts[size]
    else:
        font = pygame.font.SysFont("arial", size)
        fonts[size] = font
    rendered = font.render(content, 1, colour)
    surface.blit(rendered, (x, y))
