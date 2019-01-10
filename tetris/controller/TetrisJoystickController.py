import pygame
from tetris.controller import TetrisController
import numpy as np


class TetrisJoystickController(TetrisController):
    def __init__(self, game=None):
        super().__init__(game)
        self.stick = pygame.joystick.Joystick(0)
        self.stick.init()

        self.buttons = np.zeros(self.stick.get_numbuttons())
        self.last_buttons = np.zeros(self.stick.get_numbuttons())

        self.last_x = 0

    def update(self, milliseconds):
        e = None

        x = self.stick.get_axis(0)
        if x != 0 and x < self.last_x:
            e = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})
        elif x != 0 and x > self.last_x:
            e = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})
        elif x == 0:
            if self.last_x < 0:
                e = pygame.event.Event(pygame.KEYUP, {'key': pygame.K_LEFT})
            elif self.last_x > 0:
                e = pygame.event.Event(pygame.KEYUP, {'key': pygame.K_RIGHT})
        self.last_x = x

        if e is not None:
            super().process_event(e)

        if self.stick.get_axis(1) > 0:
            self.game.set_soft_drop(1)
        else:
            self.game.set_soft_drop(0)

        self.last_buttons = np.copy(self.buttons)
        for i in range(0, len(self.buttons)):
            self.buttons[i] = self.stick.get_button(i)

        if self.buttons[6] and not self.last_buttons[6]:
            super().process_event(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_a}))

        if self.buttons[7] and not self.last_buttons[7]:
            super().process_event(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_s}))

        if self.buttons[0] and not self.last_buttons[0]:
            super().process_event(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE}))

        if self.buttons[2] and not self.last_buttons[2]:
            super().process_event(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_c}))

        super().update(milliseconds)
