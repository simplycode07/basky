import pygame
from . import settings, colors

class Renderer:
    def __init__(self, size) -> None:
        self.surface = pygame.Surface(size)

    def render(self, display, player, tilemap):
        for y, x_positions in enumerate(tilemap):
            for x, obj in enumerate(x_positions):
                if obj == "1":
                    tilesize = settings.tilesize
                    rect = pygame.Rect(x * tilesize, y * tilesize, tilesize, tilesize)
                    pygame.draw.rect(self.surface, colors["green"], rect)


        self.surface.blit(player.img, player.pos)
        display.blit(self.surface, (0, 0))
        self.surface.fill(colors["black"])

