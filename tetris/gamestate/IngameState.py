import pygame

from tetris.configuration import GameConfiguration
from tetris.controller import TetrisJoystickController, TetrisController
from tetris.drawer import TetrisDrawer
from tetris.gamemode import GameMode
from tetris.gamestate import GameState, GameManager
from typing import List


class IngameState(GameState):
    def __init__(self, config: GameConfiguration):
        self.config = config
        self.game_mode: GameMode = None
        self.controllers: List[TetrisController] = None
        self.drawers: List[TetrisDrawer] = None

        self.background: pygame.Surface = pygame.Surface(GameManager.instance().screen.get_size())
        self.background.fill((64, 64, 64))
        self.background = self.background.convert(self.background)

        self.font = pygame.font.Font(None, 24)

    def start(self):
        self.game_mode.start()

    def update(self, milliseconds: int) -> bool:
        # Update the controllers
        for i in range(0, len(self.game_mode.games)):
            if not self.game_mode.games[i].game_over:
                self.controllers[i].update(milliseconds)

        # Get events
        for event in pygame.event.get():
            # User presses QUIT-button.
            if event.type == pygame.QUIT:
                # Application stops
                return True
            elif self.game_mode.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                from tetris.gamestate import StateBuilder
                menu_state = StateBuilder.build_menu_state(self.config)
                GameManager.instance().change_state(menu_state)
            else:
                # Update the keyboard controllers
                for i in range(0, len(self.game_mode.games)):
                    if type(self.controllers[i]) is not TetrisJoystickController:  # todo
                        if not self.game_mode.games[i].game_over:
                            self.controllers[i].process_event(event)

        # Update games
        self.game_mode.update(milliseconds)

        # Application keeps running
        return False

    def render(self, screen):
        # Render background
        screen.blit(self.background, (0, 0))

        # Render the games
        x = 20
        for i in range(0, len(self.drawers)):
            s = self.drawers[i].draw()
            screen.blit(s, (x, 20))
            x += 580

        if self.game_mode.game_over:
            txt = self.font.render("Game Over! Press [Enter] to return to the menu.", True, (255, 255, 255))
            screen.blit(txt, (100, 800))
