import pygame

from enum import Enum
from math import floor

from . import settings, colors
from .ui import UIState, fonts
from .physics_entities.hoop import Hoop
from .physics_entities.player import State, Sprite



class Renderer:
    def __init__(self, size, ui_manager) -> None:
        self.surface = pygame.Surface(size)
        self.ui_manager = ui_manager
        self.offset_x = 0
        self.offset_y = 0

    def render(self, display, player:"Sprite", hoop:"Hoop", tilemap, game_state):
        if game_state == UIState.GAME:
            for x in range(settings.num_tiles_x + 1):
                for y in range(settings.num_tiles_y + 1):
                    tile = tilemap.get(f"{x + self.offset_x//settings.tilesize};{y + self.offset_y//settings.tilesize}")
                    if tile and tile["type"] == "1":
                        tile_rect:pygame.Rect = tile["rect"].copy()
                        tile_rect.left -= self.offset_x
                        tile_rect.top -= self.offset_y
                        pygame.draw.rect(self.surface, colors["green"], tile_rect)
                        pygame.draw.rect(self.surface, colors["black"], tile_rect, width=1)

                    if tile and tile["type"] == "2":
                        tile_rect:pygame.Rect = tile["rect"].copy()
                        tile_rect.left -= self.offset_x
                        tile_rect.top -= self.offset_y
                        pygame.draw.rect(self.surface, colors["red"], tile_rect)
                        # pygame.draw.rect(self.surface, colors["black"], tile_rect, width=1)

            if player.state == State.INPUT:
                trajectory_points = player.get_path_points(15, (self.offset_x, self.offset_y))
                if trajectory_points:
                    pygame.draw.lines(self.surface, colors["white"], False, trajectory_points, width=2)


            adjusted_player_pos = player.pos - (self.offset_x, self.offset_y)
            self.move_camera(tilemap, adjusted_player_pos)

            self.surface.blit(player.img, adjusted_player_pos)
            hoop.draw(self.surface, (self.offset_x, self.offset_y))

            self.draw_text(self.surface, f" health: {player.health} ", pos=[10, 10], alignment=[0, 0])

        else:
            self.ui_manager.draw(self.surface, game_state)
        
        display.blit(self.surface, (0, 0))
        self.surface.fill(colors["background"])


    def draw_text(self, surface, text, pos=[0, 0], alignment=[0, 0]):
        text_surface = fonts["notosans"][1].render(text, False, colors["white"], colors["background"])

        pos[0] -= (text_surface.get_width() * alignment[0]) //2
        pos[1] -= (text_surface.get_height() * alignment[1]) //2

        surface.blit(text_surface, pos)
        pygame.draw.rect(surface, colors["white"], text_surface.get_rect(topleft=pos), width=2)

    # when adding to offset, subtract from player pos 
    def move_camera(self, tilemap, adjusted_player_pos):
        offset_x_max = (tilemap["width"] - settings.num_tiles_x) * settings.tilesize
        offset_y_max = (tilemap["height"] - settings.num_tiles_y) * settings.tilesize

        # old_offsets = (self.offset_x, self.offset_y)

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
