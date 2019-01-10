from tetris.misc import Observer


class GameMode(Observer):
    def __init__(self, configuration):
        self.configuration = configuration

    @property
    def games(self):
        """
        :return: The games in this game mode (i.e. each player's game)
        """
        raise NotImplementedError()

    @property
    def game_over(self) -> bool:
        """
        :return: Whether the game is over
        """
        raise NotImplementedError()

    def start(self):
        raise NotImplementedError()

    def update(self, milliseconds):
        raise NotImplementedError()

    def obs_update(self, subject, notification_type, message):
        pass
