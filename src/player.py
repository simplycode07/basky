import pygame
from . import settings, colors

from time import sleep


class Sprite:
    def __init__(self, tilemap, init_pos) -> None:
        self.tilemap = tilemap

        # self.pos = self.get_init_pos()
        self.pos = pygame.Vector2(init_pos[0], init_pos[1])
        self.vel = pygame.Vector2(0, 0)
        self.radius = int(settings.tilesize//2)

        self.img = pygame.image.load("assets/basky_32x32.png")
        self.angle = 0

        self.input_positions = []

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

        mouse_state = pygame.mouse.get_pressed()
        mouse_pos = list(pygame.mouse.get_pos())

        if len(self.input_positions) == 0 and mouse_state[0]:
            self.input_positions.append(mouse_pos)

        if len(self.input_positions) == 1 and not mouse_state[0]:
            self.input_positions.append(mouse_pos)

            self.add_impulse(3)
            self.input_positions = []

    def update(self, delta: float, surface):
        self.pos += self.vel * delta
        position_tilemap = (int((self.pos.x + settings.tilesize//2) // settings.tilesize),
                            int((self.pos.y + settings.tilesize//2) // settings.tilesize))

        # pygame.draw.rect(surface, colors["red"], pygame.Rect(
            # position_tilemap[0] * settings.tilesize, position_tilemap[1] * settings.tilesize, settings.tilesize, settings.tilesize))

        self_rect = self.get_self_rect()

        # collided, kernel = self.get_collision_kernel(
        #     position_tilemap, self_rect)
        # # this is still buggy
        # # try solving the "step bro im stuck problem" by storing the old kernel
        # # and using it to check change in collision
        # # ig it should work otherwise fuck me
        # if collided:
        #     # [0, 1, 0]
        #     # [0, 0, 0]
        #     # [1, 1, 0]
        #     # a kernel like this means collision in the vertical plane
        #     if kernel[1][0] or kernel[1][2]:
        #         self.pos.x -= self.vel.x * delta
        #         self.vel.x = -self.vel.x * settings.elasticity
        #         # self.vel.y += settings.gravity * delta
        #
        #     elif any(kernel[0]) or any(kernel[2]):
        #         self.pos.y -= self.vel.y * delta
        #         self.vel.y = -self.vel.y * settings.elasticity

        # use collision normal
        collided, normal, collision_point = self.get_collision_normal(surface, position_tilemap, self_rect)
        self.vel.y += settings.gravity * delta

        if collided and normal and collision_point:
            self.pos -= self.vel * delta
            print(f"before collision {self.vel.as_polar()}")
            self.vel.reflect_ip(normal)
            self.vel.y = self.vel.y * settings.elasticity
            # self.vel.rotate_ip(90)
            print(f"after collision {self.vel.as_polar()}")
            # center_to_pos_vec = self.pos - pygame.Vector2(self_rect.center)
            # self.pos = normal + collision_point + center_to_pos_vec

        # if collision_point:
    # checks for collisions and returns kernel for collision
    def get_collision_kernel(self, position_tilemap, self_rect: pygame.Rect):
        rects_around = []

        kernel = [[0, 0, 0],
                  [0, 0, 0],
                  [0, 0, 0]]

        position_around = [(-1, 1), (-1, -1), (0, 0), (1, 1),
                           (1, -1), (-1, 0), (1, 0), (0, 1), (0, -1)]

        collided = False

        for pos in position_around:
            x = position_tilemap[0] + pos[0]
            y = position_tilemap[1] + pos[1]
            rect = self.tilemap.get(f"{x};{y}", {}).get("rect")
            if rect:
                collision_info = self.get_collision(
                    rect, pygame.Vector2(self_rect.center))
                if collision_info[0]:
                    collided = True
                    kernel[pos[1] + 1][pos[0] + 1] = 1
                rects_around.append(rect)

        if collided:
            for i in kernel:
                print(i)

            print("-----------------")

        # return rects_around, collision_plane
        return collided, kernel

    def get_collision_normal(self, surface, position_tilemap, self_rect: pygame.Rect):
        position_around = [(-1, 1), (-1, -1), (0, 0), (1, 1),
                           (1, -1), (-1, 0), (1, 0), (0, 1), (0, -1)]

        for pos in position_around:
            x = position_tilemap[0] + pos[0]
            y = position_tilemap[1] + pos[1]
            rect = self.tilemap.get(f"{x};{y}", {}).get("rect")
            if rect:
                collision_info = self.get_collision(
                    rect, pygame.Vector2(self_rect.center))
                if collision_info[0]:
                    pygame.draw.circle(surface, colors["red"], (collision_info[2].x, collision_info[2].y), 5)
                    # sleep(3)
                    return collision_info

        # return rects_around, collision_plane
        return False, None, None

    def get_collision(self, rect: pygame.Rect, center: pygame.Vector2) -> tuple[bool, pygame.Vector2 | None, pygame.Vector2 | None]:
        collide_point_x = self.clamp(rect.left, center.x, rect.right)
        collide_point_y = self.clamp(rect.top, center.y, rect.bottom)

        collide_point = pygame.Vector2(collide_point_x, collide_point_y)

        # collision_normal = pygame.Vector2(center.x - collide_point_x, center.y - collide_point_y)
        collision_normal = center - collide_point
        if collision_normal.length() < self.radius:
            print(f"inside get_collision {collision_normal}, {center}, {collide_point}, {collision_normal.length()}")
            print(True, collision_normal.as_polar(), collide_point)
            return True, collision_normal, collide_point

        return False, None, None

    def clamp(self, start, value, end) -> int:
        if value < start:
            return start
        if value > end:
            return end

        return value

    def get_self_rect(self) -> pygame.Rect:
        return pygame.Rect(self.pos[0], self.pos[1], settings.tilesize, settings.tilesize)

    def add_impulse(self, multiplier: int) -> None:
        point1 = self.input_positions[0]
        point2 = self.input_positions[1]

        magnitude_x = (point1[0] - point2[0]) * multiplier
        magnitude_y = (point1[1] - point2[1]) * multiplier

        self.vel.x = magnitude_x
        self.vel.y = magnitude_y
