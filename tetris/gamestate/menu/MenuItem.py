from tetris.configuration import GameConfiguration
from tetris.gamestate.menu import MenuItemRenderType
from tetris.misc import Observable


class MenuItem(Observable):
    def __init__(self, config: GameConfiguration):
        super().__init__()
        self.config = config
        self.render_type = MenuItemRenderType.UNDEFINED
        self.disabled = False

    def update(self, event):
        raise NotImplementedError()
