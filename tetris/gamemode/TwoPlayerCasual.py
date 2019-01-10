from tetris.game import TetrisGame
from tetris.gamemode import GameMode
import numpy as np
import time

from tetris.misc import GameNotificationType


class TwoPlayerCasual(GameMode):
    def __init__(self, configuration):
        # Create two games with the same random seed
        super().__init__(configuration)
        configuration.seed = int(time.time())
        self._games = [TetrisGame(configuration), TetrisGame(configuration)]

        # Amount of garbage spawned for the opponent for amount of cleared lines
        self.garbage_lines = [0, 0, 1, 2, 4]
        self._game_over = False

    @property
    def games(self):
        return self._games

    @property
    def game_over(self) -> bool:
        return self._game_over

    def start(self):
        for game in self._games:
            game.start()
            game.state.attach(self)

    def update(self, milliseconds):
        count_game_over = 0

        if not self._game_over:
            for game in self._games:
                if not game.game_over:
                    game.update(milliseconds)
                else:
                    count_game_over += 1

        if count_game_over >= len(self._games) - 1:
            self._game_over = True

    def obs_update(self, subject, notification_type, message):
        for g in self._games:
            if subject == g.state:
                if notification_type == GameNotificationType.LINES_CLEARED:
                    # Create some garbage lines for the other player
                    num_garbage_lines = self.garbage_lines[int(message)]
                    garbage = np.random.random_integers(7, size=(num_garbage_lines, 10))
                    for i in range(0, num_garbage_lines):
                        gap = np.random.randint(0, 10)
                        garbage[i][gap] = 0

                    # Spawn the garbage in the other players' game
                    for h in self._games:
                        if g != h:
                            h.state.spawn_garbage(garbage)
