from typing import Callable, NoReturn

import pygame
from pygame import Surface, SurfaceType

from utils import x_state_t, reading_t, display_width, display_height, iota_t


def run_simulation(simulation_name: str,
                   setup_screen: Callable[[Surface | SurfaceType], NoReturn],
                   receiver_initial_pos: x_state_t,
                   transition_receiver: Callable[[x_state_t], x_state_t],
                   draw_receiver: Callable[[x_state_t, Surface | SurfaceType], NoReturn],
                   transition_target: Callable[[x_state_t], x_state_t],
                   target_initial_pos: x_state_t,
                   sensor_reading: Callable[[x_state_t, x_state_t], reading_t],
                   compute_iota: Callable[[reading_t], iota_t],
                   draw_iota: Callable[[iota_t, Surface | SurfaceType], NoReturn]
                   ):
    running = True

    pygame.init()
    screen = pygame.display.set_mode((display_width, display_height))

    # Scene setup
    pygame.display.set_caption(simulation_name)

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
