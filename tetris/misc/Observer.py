from tetris.misc import Observable, NotificationType


class Observer:
    def obs_update(self, subject: Observable, notification_type: NotificationType, message):
        raise NotImplementedError()
