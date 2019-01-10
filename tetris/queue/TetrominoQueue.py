
class TetrominoQueue:
    def pop(self):
        """
        :return: The next brick in the queue
        """
        raise NotImplementedError()

    def peek(self, index):
        """
        :param index: The index of the brick in the queue, index 0 for the next brick
        :return: The brick at the specified index
        """
        raise NotImplementedError()

    def insert(self, brick):
        """
        Re-inserts a brick at the beginning of the queue
        :param brick: Number of the brick to put back into the queue
        :return:
        """
        raise NotImplementedError()
