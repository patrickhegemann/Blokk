from tetris.configuration import GameConfiguration
from tetris.game import TetrisGame
from tetris.gamemode import GameMode
from tetris.misc import GameNotificationType


class StandardSinglePlayer(GameMode):
    def __init__(self, configuration: GameConfiguration):
        super().__init__(configuration)
        self.game = TetrisGame(configuration)

    @property
    def games(self):
        return [self.game]

    @property
    def game_over(self) -> bool:
        return self.game.game_over

    def start(self):
        self.game.state.attach(self)
        self.game.start()

    def update(self, milliseconds: int):
        if not self.game.game_over:
            self.game.update(milliseconds)
