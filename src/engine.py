import pygame

from src.physics_entities.player import State
from . import level, settings

from .scene import Renderer
from .physics_entities import PhysicsEntities
from .ui import UIManager, UIState
from src import physics_entities

class Game:
    def __init__(self) -> None:
        pygame.init()

        self.display = pygame.display.set_mode((settings.screen_width * settings.scaling, settings.screen_height * settings.scaling))
        self.scaled_surface = pygame.Surface((settings.screen_width * settings.scaling, settings.screen_height * settings.scaling))
        self.clock = pygame.time.Clock()
        
        self.level_manager = level.LevelManager("saves/test.save")
        # self.level_info = self.level_manager.load_tilemap(0)
        # self.physics_module = PhysicsEntities(self.level_info)

        self.level_info = None
        self.physics_module = None

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
                    change_state, new_state = self.physics_module.handle_input(event)

                    if change_state: self.game_state = new_state

                elif self.game_state == UIState.PAUSE:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.game_state = UIState.GAME

                elif self.game_state == UIState.MENU or self.game_state == UIState.CREDITS:
                    change_state, new_state = self.ui_manager.handle_input(event, self.game_state)
                    if change_state: self.game_state = UIState(new_state)

                elif self.game_state == UIState.LEVEL_SELECTOR:
                    level_selected, level = self.ui_manager.handle_input(event, self.game_state)
                    if level_selected :
                        if isinstance(level, UIState):
                            self.game_state = level
                        else:
                            self.game_state = UIState.GAME
                            self.level_info = self.level_manager.load_tilemap(level)
                            self.physics_module = PhysicsEntities(self.level_info)


                elif self.game_state == UIState.GAME_END:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.game_state = UIState.GAME
                        self.physics_module.reset()


            if self.game_state == UIState.GAME:
                # probably a thing with my system, I blame auto-cpufreq
                # when the game starts with a lower fps (due to perfomance issue) the speed of player changes, which is not desirable

                last_fps = self.clock.get_fps()
                phys_update_fps = settings.physics_fps

                # checking for player state, to actually slowdown the movement for input
                if self.physics_module.player.state != State.INPUT:
                    phys_update_fps = min(settings.physics_fps, last_fps)

                change_state, new_state = self.physics_module.update(1/phys_update_fps, self.display)
                if change_state: self.game_state = UIState(new_state)

            surface = self.renderer.render(self.physics_module, self.game_state, self.level_info)
            scaled_surface = pygame.transform.scale_by(surface, settings.scaling)
            # pygame.transform.scale2x(surface, self.scaled_surface)

            self.display.blit(scaled_surface, (0, 0))

            pygame.display.update()
            self.clock.tick_busy_loop(settings.update_fps)
