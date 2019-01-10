import pygame


class GameState:
    def start(self):
        """
        Starts this game state
        :return: nothing
        """
        raise NotImplementedError()

    def update(self, milliseconds: int) -> bool:
        """
        Updates the game in this state
        :param milliseconds: The amount of milliseconds that have passed since the last update
        :return: True, if the application should terminate
        """
        raise NotImplementedError()

    def render(self, screen):
        """
        Renders the game in this state
        :param screen: The screen the game should be rendered onto
        :return: Nothing
        """
        raise NotImplementedError()
