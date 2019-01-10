import numpy as np


class TetrisField:
    def __init__(self, width=10, height=40):
        self.width = width
        self.height = height
        self.field = np.zeros((self.height, self.width), int)

    def check_collision(self, brick, offset_x=0, offset_y=0):
        if brick is None:
            return True

        """
        Checks if the brick collides with the blocks in the game or is out of bounds
        :param brick: The Tetris brick to check
        :param offset_x: Offset to the brick in x-direction
        :param offset_y: Offset to the brick in y-direction
        :return: True if it collides or is out of bounds. False otherwise.
        """
        for y in range(0, brick.matrix.shape[0]):
            for x in range(0, brick.matrix.shape[1]):
                if brick.matrix[y][x]:
                    cx = brick.x + x + offset_x
                    cy = brick.y + y + offset_y
                    if cy >= self.height or cx >= self.width or cy < 0 or cx < 0:
                        return True
                    if self.field[cy][cx]:
                        return True
        return False

    def add_brick(self, brick):
        for y in range(0, brick.matrix.shape[0]):
            for x in range(0, brick.matrix.shape[1]):
                if brick.matrix[y][x] and 0 <= brick.x + x < self.width and 0 <= brick.y + y < self.height:
                    self.field[brick.y + y][brick.x + x] = brick.brick_type + 1
