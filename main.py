import pygame
from src import level, settings
# from src.hoop import Hoop
# from src.player import Sprite
from src.scene import Renderer
from src.physics_entities import PhysicsEntities

class Game:
    def __init__(self) -> None:
        pygame.init()

        self.display = pygame.display.set_mode(settings.screen_res)
        self.clock = pygame.time.Clock()
        
        self.level_manager = level.LevelManager("saves/test.save")

        level_info = self.level_manager.load_tilemap(0)
        self.physics_module = PhysicsEntities(level_info)
        # self.player = Sprite(level_info[0], level_info[1])
        # self.hoop = Hoop(level_info[2])
        self.renderer = Renderer(settings.screen_res)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                self.physics_module.input(event)
                # self.player.handle_input(event)

            # self.player.update(1/settings.physics_fps, self.display)
            self.physics_module.update(1/settings.physics_fps, self.display)
            self.renderer.render(self.display, self.physics_module.player, self.physics_module.hoop, self.physics_module.tilemap)
            pygame.display.update()
            self.clock.tick(settings.update_fps)

Game().run()
pygame.quit()
quit()
