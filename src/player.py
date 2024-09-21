import pygame
from . import settings, colors


class Sprite:
    def __init__(self, tilemap, init_pos) -> None:
        self.tilemap = tilemap

        # self.pos = self.get_init_pos()
        self.pos = init_pos
        self.vel = pygame.Vector2(0, 0)

        self.img = pygame.image.load("assets/basky_32x32.png")
        self.angle = 0

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.vel.y += -settings.jump_vel
            if event.key == pygame.K_d:
                self.vel.x = 300
            if event.key == pygame.K_a:
                self.vel.x = -300

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_a:
                self.vel.x = 0

    def update(self, delta: float, surface):
        self.pos += self.vel * delta
        position_tilemap = (int((self.pos.x + settings.tilesize//2) // settings.tilesize),
                            int((self.pos.y + settings.tilesize//2) // settings.tilesize))

        self_rect = self.get_self_rect()
        collided, kernel = self.get_collision_kernel(position_tilemap, self_rect)

        # pygame.draw.rect(surface, colors["red"], pygame.Rect(
        #     position_tilemap[0] * settings.tilesize, position_tilemap[1] * settings.tilesize, settings.tilesize, settings.tilesize))

        if collided:
            # [0, 1, 0]
            # [0, 0, 0]
            # [0, 1, 0]
            # a kernel like this means collision in the vertical plane
            if kernel[1][0] or kernel[1][2]:
                self.pos.x -= self.vel.x * delta
                self.vel.x = -self.vel.x * settings.elasticity

                # for i in kernel:
                #     print(i)
                #
                # print("-----------------")

                # self.vel.y += settings.gravity * delta

            elif any(kernel[0]) or any(kernel[2]):
                self.pos.y -= self.vel.y * delta
                self.vel.y = -self.vel.y * settings.elasticity

            # elif any([kernel[i][0] for i in range(3)]) or any([kernel[i][2] for i in range(3)]) :
            
            # return
                
        self.vel.y += settings.gravity * delta
            # for rect in rects_around:
        #     if self_rect.colliderect(rect):
        #         pygame.draw.rect(surface, colors["yellow"], rect)
        #         # if collision_plane == 0:
        #         #     self.pos -= self.vel * delta
        #         #     self.vel = -self.vel * settings.elasticity
        #         #
        #         # elif collision_plane == 1:
        #         #     self.pos.x -= self.vel.x * delta
        #         #     self.vel.x = -self.vel.x * settings.elasticity
        #         #     self.vel.y += settings.gravity * delta
        #         #
        #         #     if self.vel.x > 0:
        #         #         self.pos.x = rect.left - settings.tilesize
        #         #
        #         #
        #         # elif collision_plane == 2:
        #         #     self.pos.y -= self.vel.y * delta
        #         #     self.vel.y = -self.vel.y * settings.elasticity
        #
        #         # return
        #         # this will move the sprite to its previous position
        #         self.pos -= self.vel * delta
        #
        #         # debug statement
        #         pygame.draw.rect(surface, colors["red"], rect)
        #
        #         # if the collion is in the vertical plane, i dont want to add the gravity in that instant
        #         # hence the return statements
        #         if self.vel.y > 0:
        #             self.vel.y *= -settings.elasticity
        #             # self.pos.y -= self.vel.y * delta
        #
        #         elif self.vel.y < 0:
        #             self.vel.y *= -settings.elasticity
        #             # self.pos.y -= self.vel.y * delta
        #
        #         elif self.vel.x > 0:
        #             self.vel.x *= -settings.elasticity
        #             self.pos.x -= self.vel.x * delta
        #             self.vel.y += settings.gravity * delta
        #
        #         elif self.vel.x  < 0:
        #             self.vel.x *= -settings.elasticity
        #             self.pos.x -= self.vel.x * delta
        #             self.vel.y += settings.gravity * delta
        #
        #         # this made the sprite oscillate
        #         self.pos = self_rect.topleft
        #         # self.pos[0] = self_rect.center[0] - settings.tilesize//2
        #         # self.pos[1] = self_rect.center[1] - settings.tilesize//2 + 1
        #
        #         return


    def get_self_rect(self) -> pygame.Rect:
        return pygame.Rect(self.pos[0], self.pos[1], settings.tilesize, settings.tilesize)

    def get_init_pos(self) -> pygame.Vector2:
        for i in range(settings.num_tiles_x):
            for j in range(settings.num_tiles_y):
                if self.tilemap.get(f"{i};{j}", {}).get("type") == "-1":
                    return pygame.Vector2(i*settings.tilesize, j*settings.tilesize)

        return pygame.Vector2(0, 0)

    # get collision plane based on distance
    # probably the best soln
    # def get_collision_plane(self, rect):
    #     x_distance = self.pos[0] - rect.x
    #     y_distance = self.pos[1] - rect.y
    #
    #     print(f"xdist: {x_distance} ydist: {y_distance}")
    #
    #     if abs(x_distance) >= settings.tilesize:
    #         return 1
    #
    #     if abs(y_distance) >= settings.tilesize:
    #         return 2
    #
    #     return 0
        
    # remove the collision plane shit
    # get collision plane based on collision not tiles around
    def get_collision_kernel(self, position_tilemap, self_rect:pygame.Rect):
        # collision_plane is 1 for collision in horizontal plane
        # collision_plane is 2 for collision in vertical plane
        # collision_plane is 0 for collision in both planes, i dunno if this is possible or not
        rects_around = []

        kernel = [[0, 0, 0],
                  [0, 0, 0],
                  [0, 0, 0]]

        position_around = [(-1, 1), (-1, -1), (0, 0), (1, 1), (1, -1), (-1, 0), (1, 0), (0, 1), (0, -1)]

        collided = False

        for pos in position_around:
            x = position_tilemap[0] + pos[0]
            y = position_tilemap[1] + pos[1]
            rect = self.tilemap.get(f"{x};{y}", {}).get("rect")
            if rect:
                if self_rect.colliderect(rect):
                    collided = True
                    kernel[pos[1] + 1][pos[0] + 1] = 1
                rects_around.append(rect)

        if collided:
            for i in kernel:
                print(i)

            print("-----------------")

        # return rects_around, collision_plane
        return collided, kernel
