
class RotationSystem:
    """
    Abstract class for systems that specify how Tetris bricks spawn and rotate
    """
    def __init__(self, game):
        self.game = game

    def spawn(self, brick_number):
        """
        Spawn the specified brick out of the system's brick set.
        :param brick_number:
        """
        raise NotImplementedError()

    def peek_move(self, brick, x, y):
        """
        Checks what would happen if the piece was moved in the specified way
        :param brick: The brick to move
        :param x: Translation in x direction
        :param y: Translation in y direction
        :return: True, if a collision would happen
        """
        raise NotImplementedError()

    def move(self, brick, x, y):
        """
        Move the active brick.
        :param brick: The brick to move
        :param x: Translation in x direction
        :param y: Translation in y direction
        :return:
        """
        raise NotImplementedError()

    def rotate(self, brick, direction):
        """
        Rotate the brick.
        :param brick: The brick to rotate
        :param direction: 1 for clockwise rotation, -1 for counter-clockwise rotation
        :return:
        """
        raise NotImplementedError()

    @property
    def bricks(self):
        """
        The set of bricks this system supports
        :return:
        """
        raise NotImplementedError()
