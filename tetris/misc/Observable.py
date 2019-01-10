from tetris.misc import NotificationType, Observer


class Observable:
    def __init__(self):
        self._observers = set()

    def attach(self, observer: Observer):
        self._observers.add(observer)

    def detach(self, observer: Observer):
        self._observers.discard(observer)

    def _notify(self, notification_type: NotificationType, data=None):
        for observer in self._observers:
            observer.obs_update(self, notification_type, data)
