import pygame

from src.player import State, Sprite
from . import settings, colors

class Renderer:
    def __init__(self, size) -> None:
        self.surface = pygame.Surface(size)
        self.offset_x = 0
        self.offset_y = 0

    def render(self, display, player:"Sprite", tilemap):
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
            trajectory_points = player.get_path_points(15)
            if trajectory_points:
                pygame.draw.lines(self.surface, colors["white"], False, trajectory_points, width=2)

        # self.move_camera(tilemap, (0, 0))

        cam_direction = [0, 0]
        if player.pos.x > settings.screen_width//2:
            cam_direction[0] = 1

        elif player.pos.x < settings.screen_width//2:
            cam_direction[0] = -1

        if player.pos.y > settings.screen_height//2:
            cam_direction[1] = 1

        elif player.pos.x < settings.screen_height//2:
            cam_direction[1] = -1

        print(f"cam_dir: {cam_direction}")
        # self.move_camera(tilemap, cam_direction)
        self.surface.blit(player.img, player.pos)
        display.blit(self.surface, (0, 0))
        self.surface.fill(colors["black"])

    def move_camera(self, tilemap, direction:list[int]):
        offset_x_max = (tilemap["width"] - settings.num_tiles_x) * settings.tilesize
        offset_y_max = (tilemap["height"] - settings.num_tiles_y) * settings.tilesize

        # print(f"offset_max: {offset_x_max}, {offset_y_max}")

        if direction[0]:
            self.offset_x += settings.camera_speed * direction[0]

        if direction[1]:
            self.offset_y += settings.camera_speed * direction[1]

        self.offset_x = self.clamp(0, self.offset_x, offset_x_max)
        self.offset_y = self.clamp(0, self.offset_y, offset_y_max)

    def clamp(self, start, value, end) -> int:
        if value < start:
            return start
        if value > end:
            return end

        return value
