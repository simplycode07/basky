import pygame
from src import level, settings
from src.player import Sprite
from src.scene import Renderer

class Game:
    def __init__(self) -> None:
        pygame.init()

        self.display = pygame.display.set_mode(settings.screen_res)
        self.clock = pygame.time.Clock()
        
        self.level_manager = level.LevelManager("saves/test.save")
        self.player = Sprite(*self.level_manager.load_tilemap(0))
        self.renderer = Renderer(settings.screen_res)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                self.player.handle_input(event)

            self.player.update(1/settings.physics_fps, self.display, (self.renderer.offset_x, self.renderer.offset_y))
            self.renderer.render(self.display, self.player, self.player.tilemap)
            pygame.display.update()
            self.clock.tick(settings.update_fps)

Game().run()
pygame.quit()
quit()
