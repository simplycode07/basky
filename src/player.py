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
                self.vel.x = 300 
            if event.key == pygame.K_a:
                self.vel.x = -300
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_a:
                self.vel.x = 0

    def update(self, delta:float, surface):
        self.pos += self.vel * delta
        position_tilemap = (int(self.pos.x // settings.tilesize), int(self.pos.y // settings.tilesize) + 1)
        
        rects_around, collision_plane = self.get_rects_around(position_tilemap)

        self_rect = self.get_self_rect()
        for rect in rects_around:
            if self_rect.colliderect(rect):

                # this will move the sprite to its previous position
                self.pos -= self.vel * delta

                # debug statement
                # pygame.draw.rect(surface, colors["red"], rect)
                print(f"{rect.topleft}")
                # if the collion is in the vertical plane, i dont want to add the gravity in that instant
                # hence the return statements
                if self.vel.y > 0:
                    self.vel.y *= -settings.elasticity
                    # self.pos.y -= self.vel.y * delta
                    return

                elif self.vel.y < 0:
                    self.vel.y *= -settings.elasticity
                    # self.pos.y -= self.vel.y * delta
                    return

                elif self.vel.x > 0:
                    self.vel.x *= -settings.elasticity
                    # self.pos.x -= self.vel.y * delta

                elif self.vel.x  < 0:
                    self.vel.x *= -settings.elasticity
                    # self.pos.x -= self.vel.x * delta

                # this made the sprite oscillate
                # self.pos = self_rect.topleft
                # self.pos[0] = self_rect.center[0] - settings.tilesize//2
                # self.pos[1] = self_rect.center[1] - settings.tilesize//2 + 1

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
        # collision_plane is 1 for collision in horizontal plane
        # collision_plane is 2 for collision in vertical plane
        # collision_plane is 0 for collision in both planes, i dunno if this is possible or not
        rects_around = []

        position_around_x = [(-1,0), (1,0)]
        position_around_y = [(0,1), (0,-1)]
        position_around_xy = [(-1,1), (-1,-1), (0, 0), (1,1), (1,-1)]

        collision_plane = 0
        for pos in position_around_x:
            x = position_tilemap[0] + pos[0]
            y = position_tilemap[1] + pos[1]
            if rect := self.tilemap.get(f"{x};{y}", {}).get("rect"):
                rects_around.append(rect)
            
            collision_plane = 1

        for pos in position_around_y:
            x = position_tilemap[0] + pos[0]
            y = position_tilemap[1] + pos[1]
            if rect := self.tilemap.get(f"{x};{y}", {}).get("rect"):
                rects_around.append(rect)
            
            collision_plane = 1

        for pos in position_around_xy:
            x = position_tilemap[0] + pos[0]
            y = position_tilemap[1] + pos[1]
            if rect := self.tilemap.get(f"{x};{y}", {}).get("rect"):
                rects_around.append(rect)
            
            collision_plane = 0

        return rects_around, collision_plane


