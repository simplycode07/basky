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
    PAUSE = 5

    @classmethod
    def from_name(cls, state):
        return cls(state)


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
                                alignment=(1, 1),
                                text="Start Game",
                                colors=[colors["white"], (20, 20, 20)],
                                on_click=lambda: print("Button Pressed"),
                                next_state=UIState.GAME)

    def handle_input(self, event: pygame.event.Event, curr_state: "UIState"):
        change_state, new_state = False, None

        if curr_state == UIState.MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_state = pygame.mouse.get_pressed()
                change_state, new_state = self.my_button.handle_input(mouse_pos, mouse_state)

        
        return (change_state, new_state)

    def draw(self, surface: pygame.Surface, curr_state: "UIState"):
        if curr_state == UIState.MENU:
            self.my_button.draw(surface)

        if curr_state == UIState.PAUSE:
            self.draw_text(surface, "Game Paused", pos=list(settings.screen_mid_point), alignment=[1, 1])

    def draw_text(self, surface, text, pos=[0, 0], alignment=[0, 0]):
        text_surface = fonts["fira"][2].render(text, False, (255, 255, 255))

        pos[0] -= (text_surface.get_width() * alignment[0]) //2
        pos[1] -= (text_surface.get_height() * alignment[1]) //2
        surface.blit(text_surface, pos)


class Button:
    # alignment -> (x, y)
    # alignment 1 will center the button, 2 -> right align, 0 -> left align
    def __init__(self, pos:list[int], size, alignment, text, colors, on_click, next_state):
        self.text_surface = fonts["fira"][size].render(text, False, colors[0], colors[1])
        
        self.pos = pos

        self.pos[0] -= (self.text_surface.get_width() * alignment[0]) //2
        self.pos[1] -= (self.text_surface.get_height() * alignment[1]) //2

        self.rect = pygame.Rect(*pos, *self.text_surface.get_size())

        self.on_click = on_click

        self.next_state = next_state
        
    def handle_input(self, mouse_pos, mouse_state):
        if self.rect.collidepoint(mouse_pos) and mouse_state == (1, 0, 0):
            print("button clicked")
            self.on_click()
            return (True, self.next_state)

        return (False, None)

    def draw(self, surface):
        surface.blit(self.text_surface, self.pos)
