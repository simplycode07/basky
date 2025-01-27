import pygame
from . import level, settings

from .scene import Renderer, UIState
from .physics_entities import PhysicsEntities
from .ui import UIManager, UIState

class Game:
    def __init__(self) -> None:
        pygame.init()

        self.display = pygame.display.set_mode(settings.screen_res)
        self.clock = pygame.time.Clock()
        
        self.level_manager = level.LevelManager("saves/test.save")
        level_info = self.level_manager.load_tilemap(0)
        self.physics_module = PhysicsEntities(level_info)

        self.game_state = UIState.MENU
        self.ui_manager = UIManager()

        self.renderer = Renderer(settings.screen_res, self.ui_manager)
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.game_state == UIState.GAME:
                    self.physics_module.handle_input(event)

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.game_state = UIState.PAUSE

                elif self.game_state == UIState.PAUSE:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.game_state = UIState.GAME
                else:
                    change_state, new_state = self.ui_manager.handle_input(event, self.game_state)
                    if change_state: self.game_state = UIState(new_state)


            if self.game_state == UIState.GAME:
                self.physics_module.update(1/settings.physics_fps, self.display)

            self.renderer.render(self.display, self.physics_module.player, self.physics_module.hoop, self.physics_module.tilemap, self.game_state)
            pygame.display.update()
            self.clock.tick(settings.update_fps)
