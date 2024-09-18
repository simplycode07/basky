import pygame
from . import settings, colors

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

    def update(self, delta:float, surface):
        self.pos += self.vel * delta
        position_tilemap = (int(self.pos.x // settings.tilesize), int(self.pos.y // settings.tilesize) + 1)
        
        rects_around = self.get_rects_around(position_tilemap)

        self_rect = self.get_self_rect()
        for rect in rects_around:
            if self_rect.colliderect(rect):
                pygame.draw.rect(surface, colors["red"], rect)
                print(f"{rect.topleft}")
                if self.vel.y > 0:
                    self.vel.y *= -settings.elasticity
                    self_rect.bottom = rect.top

                elif self.vel.y < 0:
                    self.vel.y *= -settings.elasticity
                    self_rect.top = rect.bottom

                elif self.vel.x > 0:
                    self.vel.x *= -settings.elasticity
                    self_rect.right = rect.left

                elif self.vel.x  < 0:
                    self.vel.x *= -settings.elasticity
                    self_rect.left = rect.right

                self.pos = self_rect.topleft

                return

        # if position_tilemap[1] > 0:
        #     if self.tilemap[position_tilemap[1]][position_tilemap[0]] == "1" and position_tilemap[1] * settings.tilesize >= self.pos.y:
        #         self.pos.y = (position_tilemap[1] - 1) * settings.tilesize
        #         self.vel.y *= settings.elasticity * -1
        #         return

        self.vel.y += settings.gravity * delta

    def get_self_rect(self) -> pygame.Rect:
        return pygame.Rect(self.pos[0], self.pos[1], settings.tilesize, settings.tilesize)

    def get_init_pos(self) -> pygame.Vector2:
        for i in range(settings.num_tiles_x):
            for j in range(settings.num_tiles_y):
                if self.tilemap.get(f"{i};{j}", {}).get("type") == "-1":
                    return pygame.Vector2(i*settings.tilesize, j*settings.tilesize)



        return pygame.Vector2(0, 0)

    
    def get_rects_around(self, position_tilemap):
        rects_around = []

        position_around = [(-1,1), (-1,0), (-1,-1), (0,1), (0,-1), (1,1), (1,0), (1,-1)]

        for pos in position_around:
            x = position_tilemap[0] + pos[0]
            y = position_tilemap[1] + pos[1]
            if rect := self.tilemap.get(f"{x};{y}", {}).get("rect"):
                rects_around.append(rect)

        return rects_around


