from enum import Enum
from tetris.game import TetrisField
from tetris.game.TetrisGameState import TetrisGameState
import tetris.game.ScoringSystem as ScoringSystem
from tetris.configuration import GameConfiguration
from tetris.misc import Observer, GameNotificationType


class TetrisGame(Observer):
    class DropMode(Enum):
        NORMAL = 1
        SOFT_DROP = 2
        HARD_DROP = 3
        # SONIC_DROP = 4

    def __init__(self, configuration: GameConfiguration) -> None:
        self.state = TetrisGameState(self)
        self.state.field = TetrisField()
        self.state.queue = configuration.queue(configuration.seed)
        self.state.attach(self)

        self.scoring_system = ScoringSystem.ScoringSystem(self)

        self.rotation_system = configuration.rotation_system(self)

        # todo: Put into drop handler
        self.lock_delay_time = 500
        self.current_brick_last_drop_time = 0
        self.drop_mode = TetrisGame.DropMode.NORMAL
        self.lock_delay_started = False
        self.lock_delay_start_time = 0

        self.spawn_delay = 48
        self.spawn_start_time = 0
        self.spawning_started = False

        self.game_time = 0

        self.game_over = False

    def start(self):
        self.game_time = 0
        self.start_spawning()

    def obs_update(self, subject, notification_type, message=None):
        if subject is self.state:
            if notification_type is GameNotificationType.BRICK_SPAWN:
                self.drop_mode = TetrisGame.DropMode.NORMAL
                self.lock_delay_started = False
                self.current_brick_last_drop_time = self.game_time
            elif notification_type is GameNotificationType.BRICK_DROP:
                self.current_brick_last_drop_time = self.game_time
            elif notification_type is GameNotificationType.BRICK_LOCK_START:
                self.start_lock()
            elif notification_type is GameNotificationType.BRICK_CHANGE:
                self.restart_lock()
            elif notification_type is GameNotificationType.BRICK_LOCKED:
                self.lock_delay_started = False
                self.start_spawning()
            elif notification_type is GameNotificationType.BRICK_HOLD:
                self.start_spawning()
            elif notification_type is GameNotificationType.GAME_LOST:
                self.game_over = True

    def update(self, milliseconds):
        self.game_time += milliseconds

        # Drop current brick if necessary
        # todo: put into drop handler
        if self.lock_delay_started:
            if self.game_time - self.lock_delay_start_time > self.lock_delay_time:
                self.state.lock_active_brick()
        else:
            delta_time = self.game_time - self.current_brick_last_drop_time
            if delta_time > self.get_drop_speed():  # while
                self.state.drop_step()
                # delta_time -= self.get_drop_speed()

        if self.spawning_started and self.game_time - self.spawn_start_time > self.spawn_delay:
            self.state.spawn_next_brick()
            self.spawning_started = False

    def set_soft_drop(self, value):
        if value and self.drop_mode is TetrisGame.DropMode.NORMAL:
            self.drop_mode = TetrisGame.DropMode.SOFT_DROP
        elif not value and self.drop_mode is TetrisGame.DropMode.SOFT_DROP:
            self.drop_mode = TetrisGame.DropMode.NORMAL

    def do_hard_drop(self):
        self.drop_mode = TetrisGame.DropMode.HARD_DROP
        self.do_sonic_drop()
        self.state.lock_active_brick()
        self.drop_mode = TetrisGame.DropMode.NORMAL

    def do_sonic_drop(self):
        while not self.state.drop_step():
            pass

    def start_lock(self):
        self.lock_delay_started = True
        self.lock_delay_start_time = self.game_time

    def restart_lock(self):
        if self.lock_delay_started:
            self.lock_delay_start_time = self.game_time
            if self.rotation_system.peek_move(self.state.active_brick, 0, 1) is False:
                self.lock_delay_started = False
                self.current_brick_last_drop_time = self.game_time

    def get_drop_speed(self):
        if self.drop_mode is TetrisGame.DropMode.NORMAL:
            return self.drop_by_one_time()
        elif self.drop_mode is TetrisGame.DropMode.SOFT_DROP:
            return 25

    def drop_by_one_time(self):
        """
        :return: Time that needs to pass for the falling block to drop down by one cell
        """
        return ((0.8 - (self.scoring_system.level - 1) * 0.007) ** (self.scoring_system.level - 1)) * 1000

    def start_spawning(self):
        self.spawn_start_time = self.game_time
        self.spawning_started = True
