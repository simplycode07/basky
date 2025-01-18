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
        self.comic_sans = pygame.font.SysFont('Comic Sans MS', 30)

    def draw(self, surface:pygame.Surface, curr_state:"UIState"):
        if curr_state == UIState.MENU:
            self.draw_text(surface, "Press Enter to Start")
        pass


    def draw_text(self, surface, text):
        text_surface = self.comic_sans.render(text, False, (255, 255, 255))
        surface.blit(text_surface, (0, 0))
