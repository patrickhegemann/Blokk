from tetris.queue import SevenBagQueue
from tetris.rotation import SRS


class GameConfiguration:
    def __init__(self):
        # Default settings
        self.seed = None
        self.queue = SevenBagQueue
        self.rotation_system = SRS
        # todo
        self.players = 1
        self.game_mode = None
