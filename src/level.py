import pygame
import os.path
import json
import sys
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
        # print(f"loading level {level}")
        if os.path.isfile(f"tilemaps/{level}.json"):
            with open(f"tilemaps/{level}.json", "r") as file:
                tilemap_data = json.load(file)
                tilemap = tilemap_data["layers"][0]["data"]
                # print(tilemap)

        else:
            print("tilemap not found")
            sys.exit()

        # with open(f"tilemaps/{level}.csv", "r") as file:
        #     tilemap = file.readlines()
        #     # print(tilemap)
        
        tilemap_height = tilemap_data["layers"][0]["height"]
        tilemap_width = tilemap_data["layers"][0]["width"]

        # # clean_tilemap = [[0] * tilemap_width] * tilemap_height
        # clean_tilemap = [[0 for _ in range(tilemap_width)] for _ in range(tilemap_height)]
        # for y in range(tilemap_height):
        #     for x in range(tilemap_width):
        #         clean_tilemap[y][x] = tilemap[y * tilemap_width + x]

        sep_tilemap = {}
        init_pos_player = (0, 0)
        hoop_info = [(0, 0), ""]

        # for y, x_pos in enumerate(clean_tilemap):
        #     for x, tile_type in enumerate(x_pos):

        for idx, tile_type in enumerate(tilemap):
            x = idx % tilemap_width
            y = idx // tilemap_width

            if tile_type == 1:
                sep_tilemap[f"{x};{y}"] = {"type": "wall",
                                           "rect": pygame.Rect(
                    x*settings.tilesize, y*settings.tilesize, settings.tilesize, settings.tilesize),
                                           "pixel_coor":(x*settings.tilesize, y*settings.tilesize)}
            elif tile_type == 2:
                hoop_info[0] = (x * settings.tilesize, y * settings.tilesize)
                hoop_info[1] = 1


            elif tile_type == 4:
                init_pos_player = (x * settings.tilesize, y * settings.tilesize)

            # east
            elif tile_type == 5:
                sep_tilemap[f"{x};{y}"] = {"type": "spike",
                                           "rect": pygame.Rect(x*settings.tilesize,
                                                               y*settings.tilesize,
                                                               settings.tilesize//2,
                                                               settings.tilesize),
                                           "image": pygame.image.load("assets/spike_east.png"),
                                           "pixel_coor":(x*settings.tilesize, y*settings.tilesize)}

            # west
            elif tile_type == 6:
                sep_tilemap[f"{x};{y}"] = {"type": "spike",
                                           "rect": pygame.Rect(x*settings.tilesize + settings.tilesize//2,
                                                               y*settings.tilesize,
                                                               settings.tilesize//2,
                                                               settings.tilesize),
                                           "image": pygame.image.load("assets/spike_west.png"),
                                           "pixel_coor":(x*settings.tilesize, y*settings.tilesize)}

            # north
            elif tile_type == 7:
                sep_tilemap[f"{x};{y}"] = {"type": "spike",
                                           "rect": pygame.Rect(x*settings.tilesize,
                                                               y*settings.tilesize + settings.tilesize//2,
                                                               settings.tilesize,
                                                               settings.tilesize//2),
                                           "image": pygame.image.load("assets/spike_north.png"),
                                           "pixel_coor":(x*settings.tilesize, y*settings.tilesize)}

            # south
            elif tile_type == 8:
                sep_tilemap[f"{x};{y}"] = {"type": "spike",
                                           "rect": pygame.Rect(x*settings.tilesize,
                                                               y*settings.tilesize,
                                                               settings.tilesize,
                                                               settings.tilesize//2),
                                           "image": pygame.image.load("assets/spike_south.png"),
                                           "pixel_coor":(x*settings.tilesize, y*settings.tilesize)}
            



        sep_tilemap["height"] = tilemap_height
        sep_tilemap["width"] = tilemap_width

        text_objects = []
        if len(tilemap_data["layers"]) > 1:
            text_objects = tilemap_data["layers"][1]["objects"]
    


        return sep_tilemap, init_pos_player, hoop_info, text_objects
