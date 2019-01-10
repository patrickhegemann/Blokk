from tetris.misc import Observable, GameNotificationType
import numpy as np


class TetrisGameState(Observable):
    def __init__(self, game):
        super().__init__()
        self._game = game
        self._field = None
        self._active_brick = None
        self._queue = None
        self._hold_brick = None
        self._can_hold = True
        self._last_brick_was_hold = False
        self.garbage = None

    @property
    def field(self):
        return self._field

    @property
    def active_brick(self):
        return self._active_brick

    @property
    def hold_brick(self):
        return self._hold_brick

    @property
    def can_hold(self):
        return self._can_hold

    @property
    def queue(self):
        return self._queue

    @field.setter
    def field(self, field):
        self._field = field

    @active_brick.setter
    def active_brick(self, brick):
        self._active_brick = brick
        self._notify(GameNotificationType.BRICK_CHANGE)

    @queue.setter
    def queue(self, queue):
        self._queue = queue

    def move_active_brick(self, x):
        """
        Moves the currently active brick in x-direction
        :param x:
        :return:
        """
        if self._active_brick is not None:
            self._game.rotation_system.move(self.active_brick, x, 0)

    def rotate_active_brick(self, direction):
        """
        Rotates the currently active brick
        :param direction: 1 for clockwise, -1 for counter-clockwise
        :return:
        """
        if self._active_brick is not None:
            self._game.rotation_system.rotate(self.active_brick, direction)

    def drop_step(self):
        """
        Drops the active brick by 1 in y-direction
        :return:
        """
        if self._game.rotation_system.move(self.active_brick, 0, 1):
            self._notify(GameNotificationType.BRICK_LOCK_START)
            return True

        self._notify(GameNotificationType.BRICK_DROP)
        return False

    def lock_active_brick(self):
        """
        Locks the active brick onto the playing field
        :return:
        """
        if self.active_brick is not None:
            self.field.add_brick(self.active_brick)
            self._notify(GameNotificationType.BRICK_LOCKED)
            self._check_for_lines()
            self._active_brick = None
            # self.spawn_next_brick()

    def spawn_next_brick(self):
        # If there is garbage, spawn that first
        if self.garbage is not None and self.garbage != []:
            self.field.field = np.vstack((self.field.field[len(self.garbage):], self.garbage))
            self.garbage = None

        next_brick = self._queue.pop()
        self._active_brick = self._game.rotation_system.spawn(next_brick)
        if self._active_brick is None:
            # Brick can't be spawned -> Game lost
            self._notify(GameNotificationType.GAME_LOST)
        else:
            # We got a new active brick
            self._notify(GameNotificationType.BRICK_SPAWN)

        # Can hold the next brick again if this was not the last hold brick
        if not self._last_brick_was_hold:
            self._can_hold = True
        self._last_brick_was_hold = False

    def hold_current_brick(self):
        if not self._can_hold:
            return False

        # Put currently held brick to beginning of queue
        if self._hold_brick is not None:
            self.queue.insert(self._hold_brick.brick_type)
        # Put active brick in holding space
        self._hold_brick = self.active_brick

        self._notify(GameNotificationType.BRICK_HOLD)

        # Can't swap twice in a row
        self._can_hold = False
        self._last_brick_was_hold = True

        return True

    def _check_for_lines(self):
        full_rows = []
        y = 0
        for row in self.field.field:
            row_full = True
            for cell in row:
                if cell == 0:
                    row_full = False
                    break
            if row_full:
                full_rows.append(y)
            y += 1
        full_rows.sort(reverse=True)

        y_offset = 0
        for y in full_rows:
            real_y = y + y_offset
            for other_y in range(real_y, 0, -1):
                self.field.field[other_y] = self.field.field[other_y-1]
            self.field.field[0] = np.zeros(self.field.width)
            y_offset += 1

        if len(full_rows) > 0:
            self._notify(GameNotificationType.LINES_CLEARED, len(full_rows))
            # self.clear_sound.play()
            pass

    def spawn_garbage(self, garbage):
        if self.garbage is not None:
            self.garbage = np.vstack((self.garbage, garbage))
        else:
            self.garbage = garbage
