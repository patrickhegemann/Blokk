from tetris.misc.NotificationType import NotificationType


class GameNotificationType(NotificationType):
    """
    Types of notifications that this observable game state sends
    """
    BRICK_SPAWN = 1
    BRICK_LOCKED = 2
    BRICK_MOVE = 3
    BRICK_DROP = 4
    BRICK_LOCK_START = 5
    BRICK_CHANGE = 6
    GAME_LOST = 7
    LINES_CLEARED = 8
    BRICK_HOLD = 9
