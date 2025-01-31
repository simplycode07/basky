import pygame

from enum import Enum
from src import settings, colors

from .button import fonts, Button

class UIState(Enum):
    MENU = 0
    LEVEL_SELECTOR = 1
    SETTINGS = 2
    CREDITS = 3
    GAME = 4
    PAUSE = 5
    GAME_END = 6

    @classmethod
    def from_name(cls, state):
        return cls(state)

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

        if curr_state == UIState.GAME_END:
            self.draw_text(surface, "you ded", pos=list(settings.screen_mid_point), alignment=[1, 2])
            self.draw_text(surface, "press return to start again", pos=list(settings.screen_mid_point), alignment=[1, 0])
    def draw_text(self, surface, text, pos=[0, 0], alignment=[0, 0]):
        text_surface = fonts["fira"][2].render(text, False, (255, 255, 255))

        pos[0] -= (text_surface.get_width() * alignment[0]) //2
        pos[1] -= (text_surface.get_height() * alignment[1]) //2
        surface.blit(text_surface, pos)


