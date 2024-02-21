import os
from threading import Thread

import numpy as np
import numpy.typing as npt
import pygame
from pygame import Surface, SurfaceType

# Pygame setup

(display_width, display_height) = (1000, 800)

origin_y = display_height / 2
origin_x = display_width / 2 - 200

AXES = (200, 200, 200)
START = (255, 255, 255)
GOAL = (255, 255, 0)
REACHED = (200, 0, 0)

unit_multiplier = 15

# simulation parameters

start = np.array([0, 0])
goal = np.array([10, 0])

unitary_steps_only = False

# storage options

dest_folder = "data_experiment_unitary_steps_only/"


def save_result(final_pos: npt.NDArray[np.float64], history: list[float]):
    pos = final_pos.tolist()
    x_string = str(round(pos[0], 1)).replace('.', '_').replace('-', 'm')
    y_string = str(round(pos[1], 1)).replace('.', '_').replace('-', 'm')

    filename = f'{dest_folder}{x_string}p{y_string}.txt'

    if os.path.isfile(filename):
        return

    with open(filename, 'w+') as f:
        f.write(f'{final_pos[0]:.4f} {final_pos[1]:.4f}\n')

        for a in history:
            f.write(f'{a:.4f}\n')


def search_plane(real_pos: npt.NDArray[np.float64],
                 i_state: npt.NDArray[np.float64],
                 step: int,
                 history: list[float],
                 display: Surface | SurfaceType):
    pos = real_pos.tolist()
    x_string = str(round(pos[0], 1)).replace('.', '_').replace('-', 'm')
    y_string = str(round(pos[1], 1)).replace('.', '_').replace('-', 'm')

    filename = f'{dest_folder}{x_string}p{y_string}.txt'

    if step == 0 or \
            np.sqrt((i_state - goal).dot(i_state - goal)) < 0.05 or \
            os.path.isfile(filename):
        # final actions (print, etc.)
        save_result(real_pos, history)
        return

    # for each possible action
    action_space = np.linspace(0, 2 * np.pi, 7)[:-1]

    for action in action_space:
        # compute action that receiver takes
        goal_vector = goal - i_state
        magnitude = np.sqrt(goal_vector.dot(goal_vector))

        if unitary_steps_only or magnitude > 1:
            receiver_action = goal_vector / magnitude
        else:
            receiver_action = goal_vector

        next_receiver_state = real_pos + receiver_action

        # compute next I-state
        if unitary_steps_only or magnitude > 1:
            i_state_delta = np.array([np.cos(action), np.sin(action)])
        else:
            i_state_delta = np.array([np.cos(action), np.sin(action)]) * magnitude
        next_istate = i_state + i_state_delta

        # show next receiver position
        pygame.draw.circle(display, REACHED, display_pos(next_receiver_state.tolist()), 2)

        # append action to history
        history.append(action)

        # recursion
        search_plane(next_receiver_state, next_istate, step - 1, history, display)

        # remove action from history
        history.pop()


def display_pos(x: tuple[float, float]) -> tuple[float, float]:
    return x[0] * unit_multiplier + origin_x, - (x[1] * unit_multiplier) + origin_y


if __name__ == '__main__':

    os.makedirs(dest_folder, exist_ok=True)

    pygame.init()
    screen = pygame.display.set_mode((display_width, display_height))

    pygame.display.set_caption('Controllability graph search')

    # draw axes
    pygame.draw.line(screen, AXES, start_pos=(0, origin_y), end_pos=(display_width, origin_y))
    pygame.draw.line(screen, AXES, start_pos=(origin_x, 0), end_pos=(origin_x, display_height))

    # draw start and goal
    pygame.draw.circle(screen, START, display_pos(start.tolist()), 8)
    pygame.draw.circle(screen, GOAL, display_pos(goal.tolist()), 8)

    t1 = Thread(target=lambda: search_plane(start, start, 15, [], screen))
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
