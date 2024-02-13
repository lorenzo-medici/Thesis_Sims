from math import sin, isclose, sqrt
from time import time
from typing import NoReturn

from pygame import Surface, SurfaceType

from simulation_engine import run_simulation
from utils import *

# pygame parameters

unit_multiplier = 45

origin_y = display_height / 2
origin_x = display_width / 2 - 100

# simulation parameters

towers = [0.0,
          1.0]

max_powers = [1.0,
              1.0]


def setup_screen(screen: Surface | SurfaceType) -> NoReturn:
    screen.fill(BACKGROUND)

    pygame.draw.line(screen, AXES, start_pos=(0, origin_y), end_pos=(display_width, origin_y))
    pygame.draw.line(screen, AXES, start_pos=(origin_x, origin_y + 20), end_pos=(origin_x, origin_y - 20))
    pygame.draw.circle(screen, PURPLE, number_line_pos(towers[0]), 8)
    pygame.draw.circle(screen, CYAN, number_line_pos(towers[1]), 8)

    text(screen, 10, 10, content="Tower 1", colour=PURPLE)
    text(screen, 10, 40, content="Tower 2", colour=CYAN)
    text(screen, 10, 70, content="Receiver true position", colour=YELLOW)
    text(screen, 10, 100, content="Receiver measured position", colour=RED)


def transition_receiver(old_state: tuple[float]) -> tuple[float]:
    return (sin(time() * 3) + 6,)


def draw_receiver(x: tuple[float], screen: Surface | SurfaceType, color=YELLOW) -> NoReturn:
    pygame.draw.circle(screen, color, number_line_pos(x[0]), 5)


def transition_target(old_target: tuple[float]) -> tuple[float]:
    return (sin(time() * 5) + 3.5,)


def sensor_reading(receiver_pos: tuple[float], target_pos: tuple[float]) -> reading_t:
    source_powers = [max_powers[i] * ((towers[i] - receiver_pos[0]) / (target_pos[0] - towers[i])) ** 2 for i in [0, 1]]

    received_powers = [source_powers[i] / (towers[i] - receiver_pos[0]) ** 2 for i in [0, 1]]

    return [sqrt(max_powers[i] / received_powers[i]) for i in [0, 1]]


def compute_iota(distances: reading_t) -> tuple[float]:
    d1, d2 = distances

    if isclose(towers[0] + d1, towers[1] + d2) or isclose(towers[0] + d1, towers[1] - d2):
        return (towers[0] + d1,)

    if isclose(towers[0] - d1, towers[1] + d2) or isclose(towers[0] - d1, towers[1] - d2):
        return (towers[0] - d1,)


def draw_iota(x: tuple[float], screen: Surface | SurfaceType, color=RED) -> NoReturn:
    pygame.draw.circle(screen, color, number_line_pos(x[0]), 5)


# specific util
def number_line_pos(x: float) -> tuple[float, float]:
    return x * unit_multiplier + origin_x, origin_y


if __name__ == '__main__':
    receiver_initial_pos: tuple[float] = (5.0,)
    target_initial_pos: tuple[float] = (4.0,)

    run_simulation("1D sensor illusion",
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
