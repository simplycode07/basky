import pygame
from . import level, settings

from .scene import Renderer, UIState
from .physics_entities import PhysicsEntities

class Game:
    def __init__(self) -> None:
        pygame.init()

        self.display = pygame.display.set_mode(settings.screen_res)
        self.clock = pygame.time.Clock()
        
        self.level_manager = level.LevelManager("saves/test.save")
        level_info = self.level_manager.load_tilemap(0)
        self.physics_module = PhysicsEntities(level_info)
        self.renderer = Renderer(settings.screen_res)
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.renderer.game_state == UIState.GAME:
                    self.physics_module.handle_input(event)
                elif self.renderer.game_state == UIState.MENU and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.renderer.game_state = UIState.GAME


            if self.renderer.game_state == UIState.GAME:
                self.physics_module.update(1/settings.physics_fps, self.display)

            self.renderer.render(self.display, self.physics_module.player, self.physics_module.hoop, self.physics_module.tilemap)
            pygame.display.update()
            self.clock.tick(settings.update_fps)
