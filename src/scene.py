import pygame

from math import floor

from . import settings, colors
from .ui import UIState, fonts
from .physics_entities.player import State


text_fonts = {}


class Renderer:
    def __init__(self, size, ui_manager) -> None:
        self.surface = pygame.Surface(size)
        self.ui_manager = ui_manager
        self.offset_x = 0
        self.offset_y = 0

    def render(self, display, physics_module, game_state, level_info):
        if game_state == UIState.GAME:
            for x in range(settings.num_tiles_x + 1):
                for y in range(settings.num_tiles_y + 1):
                    tile = level_info[0].get(f"{x + self.offset_x//settings.tilesize};{y + self.offset_y//settings.tilesize}")
                    if tile and tile["type"] == "wall":
                        tile_rect:pygame.Rect = tile["rect"].copy()
                        tile_rect.left -= self.offset_x
                        tile_rect.top -= self.offset_y
                        pygame.draw.rect(self.surface, colors["green"], tile_rect)
                        pygame.draw.rect(self.surface, colors["black"], tile_rect, width=1)

                    if tile and tile["type"] == "spike":
                        tile_rect:pygame.Rect = tile["rect"].copy()
                        tile_rect.left -= self.offset_x
                        tile_rect.top -= self.offset_y

                        # tile["pixel_coor"][0] -= self.offset_x
                        # tile["pixel_coor"][1] -= self.offset_y


                        # self.surface.blit(tile["image"], tile["pixel_coor"])
                        self.surface.blit(tile["image"], [tile["pixel_coor"][0] - self.offset_x, tile["pixel_coor"][1] - self.offset_y])

                        # draw hitboxes
                        # pygame.draw.rect(self.surface, colors["red"], tile_rect, width=1)
            for text_object in level_info[3]:
                font_family = text_object["text"]["fontfamily"]
                font_size = text_object["text"]["pixelsize"]
                text_font = text_fonts.get(f"{font_family};{font_size}")

                if text_font == None:
                    text_fonts[f"{font_family};{font_size}"] = pygame.font.SysFont(font_family, font_size)
                    text_font = text_fonts[f"{font_family};{font_size}"]

                text_surface = text_font.render(text_object["text"]["text"], True, (255, 255, 255))
                text_position_x = text_object["x"] - self.offset_x
                text_position_y = text_object["y"] - self.offset_y
                self.surface.blit(text_surface, (text_position_x, text_position_y))


            if physics_module.player.state == State.INPUT:
                trajectory_points = physics_module.player.get_path_points(15, (self.offset_x, self.offset_y))
                if trajectory_points:
                    pygame.draw.lines(self.surface, colors["white"], False, trajectory_points, width=2)

            adjusted_player_pos = physics_module.player.pos - (self.offset_x, self.offset_y)
            self.move_camera(level_info[0], adjusted_player_pos)

            self.surface.blit(physics_module.player.img, adjusted_player_pos)
            physics_module.hoop.draw(self.surface, (self.offset_x, self.offset_y))
            
            if physics_module.player.damage_timeout:
                self.show_damage()

            self.draw_text(self.surface, f" health: {physics_module.player.health} ", pos=[10, 10], alignment=[0, 0])

        else:
            self.ui_manager.draw(self.surface, game_state)
        
        display.blit(self.surface, (0, 0))
        self.surface.fill(colors["background"])
    
    
    def show_damage(self):
        pygame.draw.rect(self.surface, colors["red"], pygame.Rect(100, 100, 20, 20))


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
