from math import sin, cos, sqrt
from random import gauss
from time import time
from typing import NoReturn

from pygame import Surface, SurfaceType

from simulation_engine import run_simulation
from utils import *

# pygame parameters

unit_multiplier = 35

origin_y = display_height / 2 + 100
origin_x = display_width / 2 - 100

pixel_granularity = 5

# simulation parameters

towers = [(0.0, 0.0),
          (5.0, 0.0),
          (5.0, 5.0)]

max_powers = [1.0,
              1.0,
              1.0]

dist_mu = 0.0
dist_sigma = 0.3

# save target

current_target: x_state_t = (0, 0)


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
    global current_target
    current_target = sin(time() * 5) + 2.5, cos(time() * 5) + 2.5

    return current_target


def sensor_reading(receiver_pos: tuple[float, float], target_pos: tuple[float, float]) -> reading_t:
    source_powers = [max_powers[i] * (distance(towers[i], receiver_pos) / distance(target_pos, towers[i])) ** 2 for i in
                     [0, 1, 2]]

    received_powers = [source_powers[i] / distance(towers[i], receiver_pos) ** 2 for i in [0, 1, 2]]

    disturbances = [gauss(dist_mu, dist_sigma) for _ in [0, 1, 2]]

    return [sqrt(max_powers[i] / received_powers[i]) + disturbances[i] for i in [0, 1, 2]]


def compute_iota(distances: reading_t) -> iota_t:
    probabilities = tuple(
        [mul_list([normal_pdf(distance(world_pos((p_x, p_y)), towers[i]), distances[i] + dist_mu, dist_sigma)
                   for i in [0, 1, 2]])
         for p_x in range(0, display_width, pixel_granularity)
         for p_y in range(0, display_height, pixel_granularity)]
    )

    return probabilities


def draw_iota(x: iota_t, screen: Surface | SurfaceType, color=RED) -> NoReturn:
    max_p = max(x)  # Used to normalize PDF

    for p_x in range(0, display_width, pixel_granularity):
        for p_y in range(0, display_height, pixel_granularity):

            prob = x[p_x * display_height // (pixel_granularity ** 2) + p_y // pixel_granularity] / max_p

            # "Hack" to avoid covering everything that has been drawn already
            if prob > 0.2:
                screen.fill(
                    color_alpha(color, prob),
                    ((p_x - pixel_granularity // 2, p_y - pixel_granularity // 2),
                     (pixel_granularity, pixel_granularity)))

    # pygame.draw.circle(screen, WHITE, display_pos(current_target), 5)


# specific utils
def display_pos(x: tuple[float, float]) -> tuple[float, float]:
    return x[0] * unit_multiplier + origin_x, - (x[1] * unit_multiplier) + origin_y


def world_pos(x: tuple[float, float]) -> tuple[float, float]:
    return (x[0] - origin_x) / unit_multiplier, (origin_y - x[1]) / unit_multiplier


def distance(x1: tuple[float, float], x2: tuple[float, float]) -> float:
    return sqrt((x1[0] - x2[0]) ** 2 + (x1[1] - x2[1]) ** 2)


if __name__ == '__main__':
    receiver_initial_pos = (6.0, 6.0)
    target_initial_pos = (4.0, 4.0)

    run_simulation("2D sensor illusion with probabilistic sensing disturbance",
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
