import pygame


class TetrisController:
    def __init__(self, game=None):
        self.game = game
        self.total_time = 0

        # todo: read from configuration
        self.auto_shift_delay = 250
        self.auto_shift_repeat = 50

        # todo: make this better
        self.holding_left_key = False
        self.holding_right_key = False

        self.hold_key_start_time = 0
        self.auto_shifting = False
        self.last_auto_shift = 0

        self.hard_drop_gap = 150
        self.last_hard_drop = -self.hard_drop_gap

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.game.state.move_active_brick(-1)
                self.holding_left_key = True
                self.holding_right_key = False
                self.auto_shifting = False
                self.hold_key_start_time = self.total_time
            elif event.key == pygame.K_RIGHT:
                self.game.state.move_active_brick(1)
                self.holding_right_key = True
                self.holding_left_key = False
                self.auto_shifting = False
                self.hold_key_start_time = self.total_time
            elif event.key == pygame.K_UP or event.key == pygame.K_s:
                self.game.state.rotate_active_brick(1)
            elif event.key == pygame.KMOD_CTRL or event.key == pygame.K_a:
                self.game.state.rotate_active_brick(-1)
            elif event.key == pygame.K_DOWN:
                self.game.set_soft_drop(1)
            elif event.key == pygame.K_SPACE:
                if self.total_time - self.last_hard_drop >= self.hard_drop_gap:
                    self.game.do_hard_drop()
                    self.last_hard_drop = self.total_time
            elif event.key == pygame.K_v:
                self.game.do_sonic_drop()
            elif event.key == pygame.K_c:
                self.game.state.hold_current_brick()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.holding_left_key = False
                self.auto_shifting = False
            elif event.key == pygame.K_RIGHT:
                self.holding_right_key = False
                self.auto_shifting = False
            elif event.key == pygame.K_DOWN:
                self.game.set_soft_drop(0)

    def update(self, milliseconds):
        self.total_time += milliseconds

        if self.holding_left_key:
            if self.total_time - self.hold_key_start_time > self.auto_shift_delay:
                self.auto_shifting = True
            if self.auto_shifting and self.total_time - self.last_auto_shift > self.auto_shift_repeat:
                self.game.state.move_active_brick(-1)
                self.last_auto_shift = self.total_time

        if self.holding_right_key:
            if self.total_time - self.hold_key_start_time > self.auto_shift_delay:
                self.auto_shifting = True
            if self.auto_shifting and self.total_time - self.last_auto_shift > self.auto_shift_repeat:
                self.game.state.move_active_brick(1)
                self.last_auto_shift = self.total_time
