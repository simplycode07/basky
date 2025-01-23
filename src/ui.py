import pygame

from enum import Enum
from . import settings

pygame.font.init()

class UIState(Enum):
    MENU = 0
    LEVEL_SELECTOR = 1
    SETTINGS = 2
    CREDITS = 3
    GAME = 4

class UIManager:
    def __init__(self):
        self.comic_sans = pygame.font.SysFont('firacodenerdfont', 60)

    def draw(self, surface:pygame.Surface, curr_state:"UIState"):
        if curr_state == UIState.MENU:
            self.draw_text(surface, "Press Enter to Start", [settings.screen_width//2, settings.screen_height//2])
        pass


    def draw_text(self, surface, text, pos=[0, 0], align_center=True):
        text_surface = self.comic_sans.render(text, False, (255, 255, 255))

        if align_center:
            pos[0] -= text_surface.get_width()//2
            pos[1] -= text_surface.get_height()//2

        surface.blit(text_surface, pos)


class Button:
    def __init__(self, pos, size, alignment, text):
        pass
