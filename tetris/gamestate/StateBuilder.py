from tetris.configuration import GameConfiguration
from tetris.controller import TetrisController, TetrisJoystickController
from tetris.drawer import StandardTetrisDrawer
from tetris.gamestate import IngameState
from tetris.gamestate.menu import MenuState


class StateBuilder:
    @staticmethod
    def build_menu_state(config: GameConfiguration) -> MenuState:
        state = MenuState(config)
        return state

    @staticmethod
    def build_ingame_state(config: GameConfiguration) -> IngameState:
        state = IngameState(config)

        # Create game logic(s)
        # game_mode = StandardSinglePlayer()
        # state.game_mode = TwoPlayerCasual(GameConfiguration())
        state.game_mode = config.game_mode(config)
        # Player's controllers
        state.controllers = [TetrisController(), TetrisJoystickController()]
        # Game drawers
        state.drawers = []
        for i in range(0, len(state.game_mode.games)):
            game = state.game_mode.games[i]
            # Register player's controller to game
            state.controllers[i].game = game
            # Create a renderer for this game
            state.drawers.append(StandardTetrisDrawer(game))
            i += 1

        return state
