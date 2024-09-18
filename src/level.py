import pygame
from . import settings


class LevelManager:
    def __init__(self, save_file) -> None:
        self.load_save_file(save_file)

    def load_save_file(self, save_file):
        with open(save_file, "r") as file:
            data = file.read().split(",")
            self.level = data[0]

    # def load_level(self, level):
    #     self.player = Sprite(self.load_tilemap(level))

    def load_tilemap(self, level):
        print(f"loading level {level}")
        with open(f"tilemaps/{level}.csv", "r") as file:
            tilemap = file.readlines()
            # print(tilemap)
        
        clean_tilemap = []
        for i in tilemap:
            clean_tilemap.append(i.strip().split(","))

        sep_tilemap = {}
        for y, x_pos in enumerate(clean_tilemap):
            for x, tile_type in enumerate(x_pos):
                if clean_tilemap[y][x] != "0":
                    print(f"y:{y}, x:{x}, {tile_type}")
                    sep_tilemap[f"{x};{y}"] = {"type": tile_type,
                                               "rect": pygame.Rect(
                        x*settings.tilesize, y*settings.tilesize, settings.tilesize, settings.tilesize),
                                               "pixel_coor":(x*settings.tilesize, y*settings.tilesize)}

        # print(sep_tilemap)
        return sep_tilemap
