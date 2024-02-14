import math

import pygame

# TYPES

type x_state_t = tuple[float] | tuple[float, float]
type iota_interval_t = tuple[float, float]
type iota_t = iota_interval_t | tuple[iota_interval_t, iota_interval_t, iota_interval_t] | tuple[float, ...]
type reading_t = list[float]

# COLORS

AXES = (200, 200, 200)
BACKGROUND = (30, 30, 30)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

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


# Gaussian/Normal pdf
def normal_pdf(x: float, mean: float, sd: float) -> float:
    var = float(sd) ** 2
    num = math.exp(-(float(x) - float(mean)) ** 2 / (2 * var))
    denom = (2 * math.pi * var) ** .5
    return num / denom
