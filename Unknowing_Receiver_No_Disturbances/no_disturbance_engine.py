from typing import Callable

import pygame
from pygame import Surface, SurfaceType

from utils import x_state, reading, display_width, display_height


def run_simulation(setup_screen: Callable[[Surface | SurfaceType], None],
                   receiver_initial_pos: x_state,
                   transition_receiver: Callable[[x_state], x_state],
                   draw_receiver: Callable[[x_state, Surface | SurfaceType], None],
                   transition_target: Callable[[x_state], x_state],
                   target_initial_pos: x_state,
                   sensor_reading: Callable[[x_state, x_state], reading],
                   compute_iota: Callable[[reading], x_state],
                   draw_iota: Callable[[x_state, Surface | SurfaceType], None]
                   ):
    running = True

    pygame.init()
    screen = pygame.display.set_mode((display_width, display_height))

    # Scene setup
    pygame.display.set_caption("1D example")

    receiver_pos = receiver_initial_pos
    target_pos = target_initial_pos

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        setup_screen(screen)

        receiver_pos = transition_receiver(receiver_pos)
        draw_receiver(receiver_pos, screen)

        target_pos = transition_target(target_pos)

        distances = sensor_reading(receiver_pos, target_pos)

        iota = compute_iota(distances)

        draw_iota(iota, screen)

        pygame.display.update()
