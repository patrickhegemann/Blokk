import pygame

from tetris.configuration import GameConfiguration
from tetris.gamestate import GameState
from tetris.gamestate.menu import MenuNotificationType, Menu
from tetris.misc import Observer, Observable


class MenuState(GameState, Observer):
    def __init__(self, config: GameConfiguration):
        self.current_menu: Menu = None
        self.config = config

        from tetris.gamestate.menu import MenuRenderer
        self.renderer: MenuRenderer = MenuRenderer()

        self.quit = False

    def obs_update(self, subject: Observable, notification_type: MenuNotificationType, message):
        if notification_type == MenuNotificationType.CHANGE_MENU:
            assert type(message) == Menu
            self.change_menu(message)
        elif notification_type == MenuNotificationType.QUIT:
            self.quit = True
        elif notification_type == MenuNotificationType.START_GAME:
            from tetris.gamestate import StateBuilder
            state = StateBuilder.build_ingame_state(self.config)
            from tetris.gamestate import GameManager
            GameManager.instance().change_state(state)

    def start(self):
        from tetris.gamestate.menu import MenuBuilder
        self.current_menu = MenuBuilder.build_main_menu(self.config)
        self.current_menu.attach(self)

    def update(self, milliseconds: int) -> bool:
        # Get events
        for event in pygame.event.get():
            # User presses QUIT-button.
            if event.type == pygame.QUIT:
                # Application stops
                return True
            else:
                self.current_menu.update(event)

        return self.quit

    def render(self, screen):
        self.renderer.render(screen, self.current_menu)

    def change_menu(self, menu: Menu):
        self.current_menu = menu
