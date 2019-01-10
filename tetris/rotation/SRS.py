from copy import copy
import numpy as np
from tetris.game import Tetromino
from tetris.rotation import RotationSystem


class SRS(RotationSystem):
    def __init__(self, game):
        super().__init__(game)

        # Generate all bricks and their rotations
        i_brick = SRS.generate_brick(np.array([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]))
        o_brick = SRS.generate_brick(np.array([
            [0, 1, 1],
            [0, 1, 1],
            [0, 0, 0]
        ]))
        t_brick = SRS.generate_brick(np.array([
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0]
        ]))
        s_brick = SRS.generate_brick(np.array([
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0]
        ]))
        z_brick = SRS.generate_brick(np.array([
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0]
        ]))
        j_brick = SRS.generate_brick(np.array([
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0]
        ]))
        l_brick = SRS.generate_brick(np.array([
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0]
        ]))
        self._bricks = [i_brick, o_brick, t_brick, s_brick, z_brick, j_brick, l_brick]

        # Offset data used for calculating kick data for rotation
        jlstz_offset_data = [
            [(0, 0)] * 5,
            [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
            [(0, 0)] * 5,
            [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
        ]

        i_offset_data = [
            [(0, 0), (-1, 0), (2, 0), (-1, 0), (2, 0)],
            [(-1, 0), (0, 0), (0, 0), (0, 1), (0, -2)],
            [(-1, 1), (1, 1), (-2, 1), (1, 0), (-2, 0)],
            [(0, 1), (0, 1), (0, 1), (0, -1), (0, 2)]
        ]

        o_offset_data = [
            [(0, 0)],
            [(0, -1)],
            [(-1, -1)],
            [(-1, 0)]
        ]
        self.offset_data = [i_offset_data, o_offset_data] + [jlstz_offset_data] * 5

    def spawn(self, brick_number):
        # Bricks start centered in row 22
        start_x = 3
        start_y = 20    # self.game.state.field.height - 22
        # I-brick offset due to larger matrix size
        if brick_number == 0:
            start_x -= 1
            start_y -= 2
        # Create brick in initial rotation
        new_brick = Tetromino(brick_number, self._bricks[brick_number][0], start_x, start_y)
        if self.peek_move(new_brick):
            return None
        return new_brick

    def rotate(self, brick, direction):
        # Try rotation
        new_rotation = (brick.rotation + direction) % 4
        new_matrix = self._bricks[brick.brick_type][new_rotation]
        # Index in the offset array used for kick data calculation
        offset_index = 0
        rotation_failed = False
        while True:
            # Subtract offset data of new from old to get kick
            offset_data_new = self.offset_data[brick.brick_type][new_rotation][offset_index]
            offset_data_old = self.offset_data[brick.brick_type][brick.rotation][offset_index]
            kick = np.subtract(offset_data_old, offset_data_new)
            # Apply kick to the brick
            new_x = brick.x + kick[0]
            new_y = brick.y - kick[1]
            new_brick = Tetromino(brick.brick_type, new_matrix, new_x, new_y)
            new_brick.rotation = new_rotation
            # Check if this position is legal (no collisions)
            if not self.peek_move(new_brick):
                # Rotation successful
                break
            # Try next possible kick
            offset_index += 1
            if offset_index >= len(self.offset_data[brick.brick_type][new_rotation]):
                # Out of kick options -> Rotation has failed
                rotation_failed = True
                break

        if not rotation_failed:
            # todo: return new state instead of setting the brick directly
            self.game.state.active_brick = new_brick

    def peek_move(self, brick, x=0, y=0):
        return self.game.state.field.check_collision(brick, x, y)

    def move(self, brick, x, y):
        if self.peek_move(brick, x, y):
            return True
        else:
            new_brick = copy(brick)
            new_brick.x += x
            new_brick.y += y
            # todo: return new state instead of setting the brick directly
            self.game.state.active_brick = new_brick
            return False

    @property
    def bricks(self):
        return self._bricks

    @staticmethod
    def generate_brick(matrix):
        return [matrix, np.rot90(matrix, -1), np.rot90(matrix, 2), np.rot90(matrix, 1)]
