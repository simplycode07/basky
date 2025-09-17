import pygame
import sys

from enum import Enum
from src import settings, colors

from .button import fonts, Button, ButtonList

class UIState(Enum):
    MENU = 0
    LEVEL_SELECTOR = 1
    SETTINGS = 2
    CREDITS = 3
    GAME = 4
    PAUSE = 5
    GAME_END = 6


class UIManager:
    def __init__(self):
        self.start_menu = StartMenu()
        self.level_selector = LevelSelector()
        self.level_selector.add_level_buttons((5, 9), (50, 50), (100, 100), 20)
        self.github_qr = pygame.image.load("assets/github.png")
        self.linkedin_qr = pygame.image.load("assets/linkedin.png")

    def handle_input(self, event: pygame.event.Event, curr_state: "UIState"):
        change_state, new_state = False, None

        if curr_state == UIState.MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pos_new = (mouse_pos[0]//settings.scaling, mouse_pos[1]//settings.scaling)
                mouse_state = pygame.mouse.get_pressed()
                print(mouse_pos)
                change_state, new_state = self.start_menu.handle_input(mouse_pos_new, mouse_state)

        if curr_state == UIState.LEVEL_SELECTOR:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pos_new = (mouse_pos[0]//settings.scaling, mouse_pos[1]//settings.scaling)
                mouse_state = pygame.mouse.get_pressed()
                change_state, new_state = self.level_selector.handle_input(mouse_pos_new, mouse_state)

        if curr_state == UIState.CREDITS:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                change_state = True
                new_state = UIState.MENU

        
        return (change_state, new_state)

    def draw(self, surface: pygame.Surface, curr_state: "UIState"):
        if curr_state == UIState.MENU:
            self.start_menu.draw(surface)

        if curr_state == UIState.PAUSE:
            self.draw_text(surface, "Game Paused", pos=list(settings.screen_mid_point), alignment=[1, 1])

        if curr_state == UIState.LEVEL_SELECTOR:
            self.level_selector.draw(surface)
            # self.draw_text(surface, "This is level selector", pos=list(settings.screen_mid_point), alignment=[1, 0])

        if curr_state == UIState.GAME_END:
            self.draw_text(surface, "you ded", pos=list(settings.screen_mid_point), alignment=[1, 2])
            self.draw_text(surface, "press return to start again", pos=list(settings.screen_mid_point), alignment=[1, 0])
        
        if curr_state == UIState.CREDITS:
            github_qr_x = settings.screen_width // 4 - self.github_qr.get_width() // 2
            linkedin_qr_x = settings.screen_width * 3 // 4 - self.linkedin_qr.get_width() // 2

            github_qr_y = settings.screen_height // 6
            linkedin_qr_y = settings.screen_height // 6

            surface.blit(self.github_qr, (github_qr_x, github_qr_y))
            surface.blit(self.linkedin_qr, (linkedin_qr_x, linkedin_qr_y))
            self.draw_text(surface, "Github", size=1, pos=[github_qr_x, github_qr_y + self.github_qr.get_height()])
            self.draw_text(surface, "LinkedIn", size=1, pos=[linkedin_qr_x, linkedin_qr_y + self.linkedin_qr.get_height()])

            self.draw_text(surface, "Thanks for bearing with me!", size=1, pos=list(settings.screen_mid_point), alignment=[1, 2])
            self.draw_text(surface, "Hope to see you in one of the Game Jam", size=1, pos=list(settings.screen_mid_point), alignment=[1, 0])

    def draw_text(self, surface, text, size=2, pos=[0, 0], alignment=[0, 0]):
        text_surface = fonts["fira"][size].render(text, True, (255, 255, 255))

        pos[0] -= (text_surface.get_width() * alignment[0]) //2
        pos[1] -= (text_surface.get_height() * alignment[1]) //2
        surface.blit(text_surface, pos)


class LevelSelector(ButtonList):
    def __init__(self) -> None:
        self.buttons = [Button(pos=[10, 10],
                               size=2,
                               alignment=(0, 0),
                               text="Back",
                               colors=[colors["white"], colors["background"]],
                               next_state=UIState.MENU,

                        ),
                        ]

    def add_level_buttons(self, matrix, gaps, start_pos, total_levels):
        for i in range(1, total_levels):
            x = gaps[0] * ((i - 1) % matrix[1]) + start_pos[0]
            y = gaps[1] * (((i - 1) // matrix[1])) + start_pos[1]
            self.buttons.append(Button(pos=[x, y],
                                       size=1,
                                       alignment=(0,0),
                                       text=f"{i:2}",
                                       colors=[colors["white"], (50, 50, 50)],
                                       next_state=f"{i-1}"
                                       )
                                )

class StartMenu(ButtonList):
    def __init__(self) -> None:
        self.buttons = [
                Button(pos=list(settings.screen_mid_point),
                       size=2,
                       alignment=(1, 3),
                       text="Start Game",
                       colors=[colors["white"], colors["background"]],
                       next_state=UIState.LEVEL_SELECTOR,
                       # on_click=lambda: print("Button Pressed"),
                      ),
            

                Button(pos=list(settings.screen_mid_point),
                       size=2,
                       alignment=(1, 1),
                       text="Settings",
                       colors=[colors["white"], colors["background"]],
                       next_state=UIState.SETTINGS,
                       # on_click=lambda: print("Button Pressed"),
                     ),

                Button(pos=list(settings.screen_mid_point),
                       size=2,
                       alignment=(1, -1),
                       text="Quit",
                       colors=[colors["white"], colors["background"]],
                       next_state=UIState.SETTINGS,
                       on_click=sys.exit
                       # on_click=lambda: print("Button Pressed"),
                     ),
                
                ]
