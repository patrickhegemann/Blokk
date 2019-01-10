
class Tetromino:
    def __init__(self, brick_type, matrix, x, y):
        self.brick_type = brick_type
        self.matrix = matrix
        self.rotation = 0
        self.x = x
        self.y = y
