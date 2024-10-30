import re
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
        init_pos_player = (0, 0)
        hoop_info = [(0, 0), ""]
        tilemap_height = len(clean_tilemap)
        tilemap_width = len(clean_tilemap[0])
        for y, x_pos in enumerate(clean_tilemap):
            for x, tile_type in enumerate(x_pos):
                match = re.search(r"\(.*\)", tile_type)
                # if clean_tilemap[y][x] != "0" and clean_tilemap[y][x] not in ["-1", "-2"]:
                if clean_tilemap[y][x] == "1":
                    sep_tilemap[f"{x};{y}"] = {"type": tile_type,
                                               "rect": pygame.Rect(
                        x*settings.tilesize, y*settings.tilesize, settings.tilesize, settings.tilesize),
                                               "pixel_coor":(x*settings.tilesize, y*settings.tilesize)}

                elif tile_type == "-1":
                    init_pos_player = (x * settings.tilesize, y * settings.tilesize)

                elif match:
                    print(tile_type)
                    hoop_info[0] = (x * settings.tilesize, y * settings.tilesize)
                    hoop_info[1] = match.string

        sep_tilemap["height"] = tilemap_height
        sep_tilemap["width"] = tilemap_width
    


        return sep_tilemap, init_pos_player, hoop_info
