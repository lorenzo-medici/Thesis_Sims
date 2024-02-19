from threading import Thread
from time import sleep

import numpy as np
import pygame
from pygame import Surface, SurfaceType

# Pygame setup

(display_width, display_height) = (1000, 800)

origin_y = display_height / 2
origin_x = display_width / 2

AXES = (200, 200, 200)
START = (255, 255, 255)
GOAL = (255, 255, 0)
REACHED = (200, 0, 0)

unit_multiplier = 15

# simulation parameters

start = np.array([0, 0])
goal = np.array([5, 0])


def search_plane(steps: int,
                 display: Surface | SurfaceType):
    lin = np.linspace(0, 2 * np.pi, 11)[:-1]
    for action in lin:

        i_state = start
        rec_pos = start
        in_steps = steps

        while in_steps > 0:
            # compute next I-state
            i_state_delta = np.array([np.sin(action), np.cos(action)])
            i_state = i_state + i_state_delta

            # compute action that receiver takes
            goal_vector = goal - i_state
            magnitude = np.sqrt(goal_vector.dot(goal_vector))

            receiver_action = goal_vector if magnitude <= 1 else goal_vector / magnitude
            rec_pos = rec_pos + receiver_action

            # show next receiver position
            pygame.draw.circle(display, REACHED, display_pos(rec_pos.tolist()), 2)
            pygame.draw.circle(display, (0, 255, 0), display_pos(i_state.tolist()), 2)

            in_steps -= 1

        sleep(1)


def display_pos(x: tuple[float, float]) -> tuple[float, float]:
    return x[0] * unit_multiplier + origin_x, - (x[1] * unit_multiplier) + origin_y


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((display_width, display_height))

    pygame.display.set_caption('Controllability graph search')

    # draw axes
    pygame.draw.line(screen, AXES, start_pos=(0, origin_y), end_pos=(display_width, origin_y))
    pygame.draw.line(screen, AXES, start_pos=(origin_x, 0), end_pos=(origin_x, display_height))

    # draw start and goal
    pygame.draw.circle(screen, START, display_pos(start.tolist()), 8)
    pygame.draw.circle(screen, GOAL, display_pos(goal.tolist()), 8)

    t1 = Thread(target=lambda: search_plane(50, screen))
    t1.daemon = True
    t1.start()

    running = True
    check_thread = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

        if check_thread and not t1.is_alive():
            t1.join()
            print("Exploration finished!")

            check_thread = False

            # redraw start and goal
            pygame.draw.circle(screen, START, display_pos(start.tolist()), 8)
            pygame.draw.circle(screen, GOAL, display_pos(goal.tolist()), 8)

    pygame.display.update()

    t1.join()
