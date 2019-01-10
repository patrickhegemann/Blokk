import pygame

from tetris.gamestate import GameManager
from tetris.gamestate.menu import Menu, MenuItemRenderType


class MenuRenderer:
    def __init__(self):
        self.surface = pygame.Surface(GameManager.instance().screen.get_size())
        self.surface = self.surface.convert(self.surface)

        self.font = pygame.font.Font(None, 24)

    def render(self, screen, menu: Menu):
        self.surface.fill((64, 64, 64))

        y = 200
        for item in menu.items:
            if item.render_type == MenuItemRenderType.BUTTON:
                color = (255, 255, 255)
                if item.disabled:
                    color = (128, 128, 128)
                txt = self.font.render(item.caption, True, color)
                self.surface.blit(txt, (350, y))
                y += 40
            else:
                raise Exception("no rendering for this kind of menu item is implemented")

        pygame.draw.rect(self.surface, (255, 255, 255), (310, 200 + menu.selected_menu_item * 40, 16, 16))

        screen.blit(self.surface, (0, 0))
