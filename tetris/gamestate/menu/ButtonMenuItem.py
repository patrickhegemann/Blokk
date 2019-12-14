import pygame

from tetris.gamestate.menu import MenuItem, MenuItemRenderType, MenuNotificationType


class ButtonMenuItem(MenuItem):
    def __init__(self, config, caption: str):
        super().__init__(config)
        self.caption = caption
        self.render_type = MenuItemRenderType.BUTTON

    def update(self, event):
        # todo: map this to some other class and take this as parameter so we can use different input methods
        if not self.disabled and event.key == pygame.K_RETURN:
            self.enter()

    def enter(self):
        raise NotImplementedError


class StartSinglePlayerMenuItem(ButtonMenuItem):
    def enter(self):
        from tetris.gamemode import StandardSinglePlayer
        self.config.game_mode = StandardSinglePlayer
        self.config.players = 1
        self._notify(MenuNotificationType.START_GAME)


class StartTwoPlayerMenuItem(ButtonMenuItem):
    def enter(self):
        from tetris.gamemode import TwoPlayerCasual
        self.config.game_mode = TwoPlayerCasual
        self.config.players = 2
        self._notify(MenuNotificationType.START_GAME)


class QuitApplicationMenuItem(ButtonMenuItem):
    def enter(self):
        self._notify(MenuNotificationType.QUIT, None)
