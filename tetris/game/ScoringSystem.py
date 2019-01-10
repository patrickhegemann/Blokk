from tetris.misc import Observer, GameNotificationType
import tetris.game.TetrisGame as TetrisGame


class ScoringSystem(Observer):
    score_for_lines = [0, 100, 300, 500, 800]

    def __init__(self, game):
        self.game = game
        self.level = 1
        self.score = 0
        self.total_lines = 0
        self.game.state.attach(self)

    def obs_update(self, subject, notification_type, message):
        if subject == self.game.state:
            if notification_type == GameNotificationType.LINES_CLEARED:
                cleared_lines = int(message)
                self.total_lines += cleared_lines
                self.score += ScoringSystem.score_for_lines[cleared_lines] * self.level
                self.update_level()
            if notification_type == GameNotificationType.BRICK_DROP:
                if self.game.drop_mode == TetrisGame.TetrisGame.DropMode.SOFT_DROP:
                    self.score += 1
                elif self.game.drop_mode == TetrisGame.TetrisGame.DropMode.HARD_DROP:
                    self.score += 2

    def update_level(self):
        self.level = int(self.total_lines / 10) + 1
