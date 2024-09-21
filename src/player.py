import pygame
from . import settings, colors


class Sprite:
    def __init__(self, tilemap, init_pos) -> None:
        self.tilemap = tilemap

        # self.pos = self.get_init_pos()
        self.pos = pygame.Vector2(init_pos[0], init_pos[1])
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
       

    def get_self_rect(self) -> pygame.Rect:
        return pygame.Rect(self.pos[0], self.pos[1], settings.tilesize, settings.tilesize)

    # checks for collisions and returns kernel for collision
    def get_collision_kernel(self, position_tilemap, self_rect:pygame.Rect):
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
