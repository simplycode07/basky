import pygame

from enum import Enum
from . import settings, colors

pygame.font.init()


class UIState(Enum):
    MENU = 0
    LEVEL_SELECTOR = 1
    SETTINGS = 2
    CREDITS = 3
    GAME = 4


fonts = {"fira": [
            pygame.font.SysFont('firacodenerdfont', 20),
            pygame.font.SysFont('firacodenerdfont', 30),
            pygame.font.SysFont('firacodenerdfont', 40)
        ],
        "notosans": [
            pygame.font.SysFont('notosans', 20),
            pygame.font.SysFont('notosans', 30),
            pygame.font.SysFont('notosans', 40)
        ],

}


class UIManager:
    def __init__(self):
        self.my_button = Button(pos=list(settings.screen_mid_point),
                                size=2,
                                alignment=(2, 1),
                                text="this is my button",
                                colors=[colors["white"], (20, 20, 20)],
                                on_click=lambda: print("hello world"))

    def handle_input(self, event: pygame.event.Event, curr_state: "UIState"):
        if curr_state == UIState.MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_state = pygame.mouse.get_pressed()
                self.my_button.handle_input(mouse_pos, mouse_state)

    def draw(self, surface: pygame.Surface, curr_state: "UIState"):
        if curr_state == UIState.MENU:
            self.my_button.draw(surface)
            # self.draw_text(surface, "Press Enter to Start", [
                           # settings.screen_width//2, settings.screen_height//2])
        pass

    def draw_text(self, surface, text, pos=[0, 0], align_center=True):
        text_surface = fonts["notosans"][2].render(text, False, (255, 255, 255))

        if align_center:
            pos[0] -= text_surface.get_width()//2
            pos[1] -= text_surface.get_height()//2

        surface.blit(text_surface, pos)


class Button:
    # alignment -> (x, y)
    # alignment 1 will center the button, 2 -> right align, 0 -> left align
    def __init__(self, pos:list[int], size, alignment, text, colors, on_click):
        self.text_surface = fonts["fira"][size].render(text, False, colors[0], colors[1])
        
        self.pos = pos

        self.pos[0] -= (self.text_surface.get_width() * alignment[0]) //2
        self.pos[1] -= (self.text_surface.get_height() * alignment[1]) //2

        self.rect = pygame.Rect(*pos, *self.text_surface.get_size())

        self.on_click = on_click
        
    def handle_input(self, mouse_pos, mouse_state):
        if self.rect.collidepoint(mouse_pos) and mouse_state == (1, 0, 0):
            print("button clicked")
            self.on_click()

    def draw(self, surface):
        surface.blit(self.text_surface, self.pos)
