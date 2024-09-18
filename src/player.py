import pygame
from . import settings

class Sprite:
    def __init__(self, tilemap) -> None:
        self.tilemap = tilemap

        self.pos = self.get_init_pos()
        print(self.pos)
        self.vel = pygame.Vector2(0, 0)

        self.img = pygame.image.load("assets/basky_32x32.png")
        self.angle = 0

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("jumping")
                self.vel.y += -settings.jump_vel
            if event.key == pygame.K_d:
                self.vel.x = 50 
            if event.key == pygame.K_a:
                self.vel.x = -50
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_a:
                self.vel.x = 0

    def update(self, delta:float):
        self.pos += self.vel * delta
        position_tilemap = (int(self.pos.x // settings.tilesize), int(self.pos.y // settings.tilesize) + 1)

        
        # if position_tilemap[1] > 0:
        #     if self.tilemap[position_tilemap[1]][position_tilemap[0]] == "1" and position_tilemap[1] * settings.tilesize >= self.pos.y:
        #         self.pos.y = (position_tilemap[1] - 1) * settings.tilesize
        #         self.vel.y *= settings.elasticity * -1
        #         return

        self.vel.y += settings.gravity * delta

    def get_init_pos(self) -> pygame.Vector2:
        for i in range(settings.num_tiles_x):
            for j in range(settings.num_tiles_y):
                if self.tilemap.get(f"{i};{j}", {}).get("type") == "-1":
                    return pygame.Vector2(i*settings.tilesize, j*settings.tilesize)



        return pygame.Vector2(0, 0)

    
    def get_rects_around(self, position_tilemap):
        rects_around = []

        position_around = [(-1,1), (-1,0), (-1,-1), (0,1), (0,-1), (1,1), (1,0), (1,-1)]




