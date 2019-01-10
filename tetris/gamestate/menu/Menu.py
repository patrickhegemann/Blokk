import pygame

from tetris.gamestate.menu import MenuItem
from tetris.misc import Observable, Observer, NotificationType
from typing import List


class Menu(Observable, Observer):
    def __init__(self, items: List[MenuItem]):
        super().__init__()
        self.items = items
        self.selected_menu_item: int = 0

        for i in self.items:
            i.attach(self)

    def obs_update(self, subject: Observable, notification_type: NotificationType, message):
        self._notify(notification_type, message)

    def update(self, event: pygame.event.EventType):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_menu_item = (self.selected_menu_item + 1) % len(self.items)
            elif event.key == pygame.K_UP:
                self.selected_menu_item = (self.selected_menu_item - 1) % len(self.items)
            else:
                self.items[self.selected_menu_item].update(event)

    def render(self):
        pass
