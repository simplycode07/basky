import pygame

from src.physics_entities.hoop import Hoop
from src.physics_entities.player import State, Sprite
from . import settings, colors

from math import floor

class Renderer:
    def __init__(self, size) -> None:
        self.surface = pygame.Surface(size)
        self.offset_x = 0
        self.offset_y = 0

    def render(self, display, player:"Sprite", hoop:"Hoop", tilemap):
        # this renders all the tiles inside the camera
        for x in range(settings.num_tiles_x + 1):
            for y in range(settings.num_tiles_y + 1):
                tile = tilemap.get(f"{x + self.offset_x//settings.tilesize};{y + self.offset_y//settings.tilesize}")
                if tile and tile["type"] == "1":
                    tile_rect:pygame.Rect = tile["rect"].copy()
                    tile_rect.left -= self.offset_x
                    tile_rect.top -= self.offset_y
                    pygame.draw.rect(self.surface, colors["green"], tile_rect)
                    pygame.draw.rect(self.surface, colors["black"], tile_rect, width=1)

        if player.state == State.INPUT:
            trajectory_points = player.get_path_points(15, (self.offset_x, self.offset_y))
            if trajectory_points:
                pygame.draw.lines(self.surface, colors["white"], False, trajectory_points, width=2)


        adjusted_player_pos = player.pos - (self.offset_x, self.offset_y)
        self.move_camera(tilemap, adjusted_player_pos)

        self.surface.blit(player.img, adjusted_player_pos)
        hoop.draw(self.surface, (self.offset_x, self.offset_y))
        
        display.blit(self.surface, (0, 0))

        self.surface.fill(colors["black"])

    # when adding to offset, subtract from player pos 
    def move_camera(self, tilemap, adjusted_player_pos):
        offset_x_max = (tilemap["width"] - settings.num_tiles_x) * settings.tilesize
        offset_y_max = (tilemap["height"] - settings.num_tiles_y) * settings.tilesize

        old_offsets = (self.offset_x, self.offset_y)

        self.offset_x += floor((adjusted_player_pos.x - settings.screen_width//2) / settings.camera_speed)
        self.offset_y += floor((adjusted_player_pos.y - settings.screen_height//2) / settings.camera_speed)

        self.offset_x = self.clamp(0, self.offset_x, offset_x_max)
        self.offset_y = self.clamp(0, self.offset_y, offset_y_max)
        
        # print(f"{self.offset_x - old_offsets[0]}, {self.offset_y - old_offsets[1]}")

    def clamp(self, start, value, end) -> int:
        if value < start:
            return start
        if value > end:
            return end

        return value
