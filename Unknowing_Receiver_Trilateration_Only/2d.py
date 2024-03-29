from math import sin, cos, sqrt
from time import time
from typing import NoReturn

from pygame import Surface, SurfaceType

from simulation_engine import run_simulation
from utils import *

# pygame parameters

unit_multiplier = 35

origin_y = display_height / 2 + 100
origin_x = display_width / 2 - 100

# simulation parameters

towers = [(0.0, 0.0),
          (1.0, 0.0),
          (1.0, 1.0)]

max_powers = [1.0,
              1.0,
              1.0]


def setup_screen(screen: Surface | SurfaceType) -> NoReturn:
    screen.fill(BACKGROUND)

    pygame.draw.line(screen, AXES, start_pos=(0, origin_y), end_pos=(display_width, origin_y))
    pygame.draw.line(screen, AXES, start_pos=(origin_x, 0), end_pos=(origin_x, display_height))
    pygame.draw.circle(screen, PURPLE, display_pos(towers[0]), 8)
    pygame.draw.circle(screen, CYAN, display_pos(towers[1]), 8)
    pygame.draw.circle(screen, BLUE, display_pos(towers[2]), 8)

    text(screen, 10, 10, content="Tower 1", colour=PURPLE)
    text(screen, 10, 40, content="Tower 2", colour=CYAN)
    text(screen, 10, 70, content="Tower 3", colour=BLUE)
    text(screen, 10, 100, content="Receiver true position", colour=YELLOW)
    text(screen, 10, 130, content="Receiver measured position", colour=RED)


def transition_receiver(old_state: tuple[float, float]) -> tuple[float, float]:
    return sin(time() * 3) + 5, cos(time() * 3) + 5


def draw_receiver(x: tuple[float, float], screen: Surface | SurfaceType, color=YELLOW) -> NoReturn:
    pygame.draw.circle(screen, color, display_pos(x), 5)


def transition_target(old_target: tuple[float, float]) -> tuple[float, float]:
    return sin(time() * 5) + 3.5, cos(time() * 5) + 3.5


def sensor_reading(receiver_pos: tuple[float, float], target_pos: tuple[float, float]) -> reading_t:
    source_powers = [max_powers[i] * (distance(towers[i], receiver_pos) / distance(target_pos, towers[i])) ** 2 for i in
                     [0, 1, 2]]

    received_powers = [source_powers[i] / distance(towers[i], receiver_pos) ** 2 for i in [0, 1, 2]]

    return [sqrt(max_powers[i] / received_powers[i]) for i in [0, 1, 2]]


def compute_iota(distances: reading_t) -> tuple[float, float]:
    d1, d2, d3 = distances

    A = - 2 * towers[0][0] + 2 * towers[1][0]
    B = -2 * towers[0][1] + 2 * towers[1][1]
    C = d1 ** 2 - d2 ** 2 - towers[0][0] ** 2 + towers[1][0] - towers[0][1] ** 2 + towers[1][1] ** 2
    D = -2 * towers[1][0] + 2 * towers[2][0]
    E = -2 * towers[1][1] + 2 * towers[2][1]
    F = d2 ** 2 - d3 ** 2 - towers[1][0] ** 2 + towers[2][0] - towers[1][1] ** 2 + towers[2][1] ** 2

    den = A * E - B * D

    return (C * E - B * F) / den, (A * F - C * D) / den


def draw_iota(x: tuple[float, float], screen: Surface | SurfaceType, color=RED) -> NoReturn:
    pygame.draw.circle(screen, color, display_pos(x), 5)


# specific utils
def display_pos(x: tuple[float, float]) -> tuple[float, float]:
    return x[0] * unit_multiplier + origin_x, - (x[1] * unit_multiplier) + origin_y


def distance(x1: tuple[float, float], x2: tuple[float, float]) -> float:
    return sqrt((x1[0] - x2[0]) ** 2 + (x1[1] - x2[1]) ** 2)


if __name__ == '__main__':
    receiver_initial_pos = (6.0, 6.0)
    target_initial_pos = (4.0, 4.0)

    run_simulation("2D sensor illusion",
                   setup_screen,
                   receiver_initial_pos,
                   transition_receiver,
                   draw_receiver,
                   transition_target,
                   target_initial_pos,
                   sensor_reading,
                   compute_iota,
                   draw_iota)
    # run_simulation(setup_screen: Callable[[Surface | SurfaceType], NoReturn],
    # receiver_initial_pos: x_state,
    # transition_receiver: Callable[[x_state], x_state],
    # draw_receiver: Callable[[x_state, Surface | SurfaceType], NoReturn],
    # transition_target: Callable[[x_state], x_state],
    # target_initial_pos: x_state,
    # sensor_reading: Callable[[x_state, x_state], reading],
    # compute_iota: Callable[[reading], x_state],
    # draw_iota: Callable[[x_state], NoReturn]
    # )
