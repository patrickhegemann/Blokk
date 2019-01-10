import numpy as np
from tetris.queue import TetrominoQueue


class UniformRandomQueue(TetrominoQueue):
    def __init__(self, seed=None):
        self.queue = []
        self.random_generator = np.random.RandomState(seed)

    def pop(self):
        self.peek(0)
        return self.queue.pop(0)

    def peek(self, index):
        while len(self.queue) <= index:
            self.generate_new()
        return self.queue[index]

    def generate_new(self):
        self.queue += [self.random_generator.randint(0, 7)]

    def insert(self, brick):
        self.queue.insert(0, brick)
