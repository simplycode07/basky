import pygame
from . import settings, colors

class Renderer:
    def __init__(self, size) -> None:
        self.surface = pygame.Surface(size)

    def render(self, display, player, tilemap):
        for x in range(settings.num_tiles_x):
            for y in range(settings.num_tiles_y):
                tile = tilemap.get(f"{x};{y}")
                if tile and tile["type"] == "1":
                    pygame.draw.rect(self.surface, colors["green"], tile["rect"])


        self.surface.blit(player.img, player.pos)
        display.blit(self.surface, (0, 0))
        self.surface.fill(colors["black"])

