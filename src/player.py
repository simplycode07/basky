import pygame
from . import settings

class Sprite:
    def __init__(self, tilemap) -> None:
        self.tilemap = tilemap

        self.pos = self.get_init_pos()
        self.vel = pygame.Vector2(0, 0)

        self.img = pygame.image.load("assets/basky_32x32.png")
        self.angle = 0

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            print("jumping")
            self.vel.y += -settings.jump_vel
            
    def update(self, delta:float):
        self.pos += self.vel * delta
        print(self.pos)
        position_tilemap = (round(self.pos.x // settings.tilesize), round(self.pos.y // settings.tilesize) + 1)


        if position_tilemap[1] > 0:
            if self.tilemap[position_tilemap[1]][position_tilemap[0]] == "1" and position_tilemap[1] * settings.tilesize >= self.pos.y:
                self.pos.y = (position_tilemap[1] - 1) * settings.tilesize
                self.vel.y *= settings.elasticity * -1
                return

        self.vel.y += settings.gravity * delta

    def get_init_pos(self) -> pygame.Vector2:
        for y, x_positions in enumerate(self.tilemap):
            for x, obj in enumerate(x_positions):
                print(obj)
                if obj == "-1":
                    print("obj found")
                    return pygame.Vector2(x*settings.tilesize, y*settings.tilesize)


        return pygame.Vector2(0, 0)






