import pygame

from tetris.configuration import GameConfiguration
from tetris.gamestate import GameState


class GameManager:
    # Put this into config files later
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 900
    WANTED_FPS = 60

    _instance = None

    @staticmethod
    def instance():
        if GameManager._instance is None:
            GameManager._instance = GameManager()
        return GameManager._instance

    def __init__(self):
        # Initialize window
        pygame.init()
        self.screen = pygame.display.set_mode((GameManager.SCREEN_WIDTH, GameManager.SCREEN_HEIGHT))
        pygame.display.set_caption("Blokk")

        # Game time
        self.mainloop = True
        self.playtime = 0.0
        self.clock = pygame.time.Clock()

        self.current_state = None

        self.config = GameConfiguration()

    def start(self):
        # Start in the menu
        from tetris.gamestate import StateBuilder
        self.current_state = StateBuilder.build_menu_state(self.config)
        self.current_state.start()

        # Game mainloop
        while self.mainloop:
            milliseconds = self.clock.tick(GameManager.WANTED_FPS)
            self.playtime += milliseconds

            if self.current_state.update(milliseconds):
                self.mainloop = False

            self.current_state.render(self.screen)
            # Flip everything to the front buffer
            pygame.display.flip()

        # End
        pygame.quit()

    def change_state(self, new_state: GameState):
        del self.current_state
        self.current_state = new_state
        new_state.start()

    def end_game(self):
        self.mainloop = False
