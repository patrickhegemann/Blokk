from tetris import configuration
from tetris.gamestate.menu import Menu, ButtonMenuItem, StartSinglePlayerMenuItem, QuitApplicationMenuItem, \
    StartTwoPlayerMenuItem


class MenuBuilder:
    @staticmethod
    def build_main_menu(config: configuration.GameConfiguration) -> Menu:
        items = [
            StartSinglePlayerMenuItem(config, "Single Player"),
            StartTwoPlayerMenuItem(config, "Multi Player"),
            ButtonMenuItem(config, "Settings"),
            QuitApplicationMenuItem(config, "Quit")
        ]
        items[2].disabled = True
        return Menu(items)
