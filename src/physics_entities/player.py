import pygame

from src.ui import UIState
from . import settings, colors
from enum import Enum


class Sprite:
    def __init__(self, tilemap, init_pos) -> None:
        self.tilemap = tilemap

        self.pos = pygame.Vector2(init_pos[0], init_pos[1])
        self.init_pos = self.pos.copy()
        self.vel = pygame.Vector2(0, 0)
        self.radius = int(settings.tilesize//2)

        self.img = pygame.image.load("assets/basky_32x32.png")
        self.angle = 0

        self.health = 3

        self.input_positions = []

        self.state = State.NORMAL

    def handle_input(self, event):
        # if event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_d:
            #     self.vel.x = 300
            # if event.key == pygame.K_a:
            #     self.vel.x = -300

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_a:
                self.vel.x = 0

        mouse_state = pygame.mouse.get_pressed()
        mouse_pos = list(pygame.mouse.get_pos())

        if len(self.input_positions) == 0 and mouse_state[0]:
            settings.physics_fps /= settings.input_slow_motion
            self.state = State.INPUT

            self.input_positions.append(mouse_pos)

        if len(self.input_positions) == 1 and not mouse_state[0]:
            settings.physics_fps = settings.update_fps
            self.state = State.NORMAL

            self.input_positions.append(mouse_pos)

            self.add_impulse(settings.senstivity)
            self.input_positions = []

    def update(self, delta: float, surface):
        self.pos += self.vel * delta
        position_tilemap = [int((self.pos.x + settings.tilesize//2) // settings.tilesize),
                            int((self.pos.y + settings.tilesize//2) // settings.tilesize)]

        # pygame.draw.rect(surface, colors["red"], pygame.Rect(
        #     position_tilemap[0] * settings.tilesize, position_tilemap[1] * settings.tilesize, settings.tilesize, settings.tilesize))

        self_rect = self.get_self_rect()

        # use collision normal
        collision_data = self.get_tilemap_collision(
            surface, position_tilemap, self_rect)
        self.vel.y += settings.gravity * delta

        if collision_data.collision_with == "spike":
            self.health -= 1

        # if collided and normal and collision_point:
        self.handle_collision(delta, collision_data)

        change_state = False
        new_state = None
        if self.health <= 0:
            change_state = True
            new_state = UIState.GAME_END
        
        return (change_state, new_state)


    def handle_collision(self, delta, collision_data: "CollisionData", elasticity:float=0):
        if elasticity != 0:
            elasticity_x = elasticity
            elasticity_y = elasticity
        else: 
            elasticity_x = settings.elasticity_x
            elasticity_y = settings.elasticity_y

        if not collision_data.collision_status:
            return

        # self.pos -= self.vel * delta
        if abs(collision_data.normal.as_polar()[1]) == 90.0:
            self.vel.x *= settings.friction
            self.pos.y -= self.vel.y * delta

        elif abs(collision_data.normal.as_polar()[1]) in [0.0, 180.0]:
            self.pos.x -= self.vel.x * delta

        else:
            # print(f"normal: {collision_data.normal.as_polar()}")
            self.pos -= self.vel * delta

        self.vel.reflect_ip(collision_data.normal)

        if abs(collision_data.normal.as_polar()[1]) == 90:
            self.vel.y = self.vel.y * elasticity_y

        if abs(collision_data.normal.as_polar()[1]) in [0, 180]:
            self.vel.x = self.vel.x * elasticity_x

        # print(f"after collision {self.vel.as_polar()}")
        # center_to_pos_vec = self.pos - pygame.Vector2(self_rect.center)
        # self.pos = normal + collision_point + center_to_pos_vec

    def reset(self):
        self.state = State.NORMAL
        self.pos = self.init_pos.copy()
        self.health = 3
        self.vel = pygame.Vector2(0, 0)


    # this functions checks for collision around the player
    # and returns the collision data that has the shortest normal
    def get_tilemap_collision(self, surface, position_tilemap, self_rect: pygame.Rect) -> "CollisionData":
        position_around = [(-1, 1), (-1, -1), (0, 0), (1, 1),
                           (1, -1), (-1, 0), (1, 0), (0, 1), (0, -1)]

        old_collision_info = CollisionData(False, None, None, None)

        for pos in position_around:
            x = position_tilemap[0] + pos[0]
            y = position_tilemap[1] + pos[1]

            rect = self.tilemap.get(f"{x};{y}", {}).get("rect")
            tile_type = self.tilemap.get(f"{x};{y}", {}).get("type")
            # print(f"{x}, {y}, {rect.topleft if rect else ""}")
            if rect:
                pygame.draw.rect(surface, colors["red"], rect)
                collision_info = self.get_collision_with_rect(
                    rect, pygame.Vector2(self_rect.center), tile_type)

                if collision_info.collision_status and old_collision_info.collision_status:
                    if collision_info.normal.length() < old_collision_info.normal.length():
                        old_collision_info.update_all(collision_info)

                if old_collision_info.collision_status == False and collision_info.collision_status:
                    old_collision_info.update_all(collision_info)

        return old_collision_info

    # returns collision data between a pygame.Rect object and player
    def get_collision_with_rect(self, rect: pygame.Rect, center: pygame.Vector2, tile_type) -> "CollisionData":
        collide_point_x = self.clamp(rect.left, center.x, rect.right)
        collide_point_y = self.clamp(rect.top, center.y, rect.bottom)

        collide_point = pygame.Vector2(collide_point_x, collide_point_y)
        collision_info = CollisionData(False, None, None, None)
        collision_normal = center - collide_point

        # the length != 0 check is to avoid reflecting along a NULL vector
        if collision_normal.length() < self.radius and collision_normal.length() != 0:
            collision_info.update_collision_status(True)
            collision_info.update_normal(pygame.Vector2(
                center.x - collide_point_x, center.y - collide_point_y))
            collision_info.update_collision_point(collide_point)
            collision_info.update_collision_with(tile_type)
            # print(f"inside get_collision {collision_normal}, {center}, {collide_point}, {collision_normal.length()}")
            # print(True, collision_normal.as_polar(), collide_point)

        return collision_info

    def clamp(self, start, value, end) -> int:
        if value < start:
            return start
        if value > end:
            return end

        return value

    def get_self_rect(self) -> pygame.Rect:
        return pygame.Rect(self.pos[0], self.pos[1], settings.tilesize, settings.tilesize)

    def add_impulse(self, multiplier: int, vel: pygame.Vector2 | None = None, mos_pos: tuple[int, int] | None = None) -> pygame.Vector2 | None:
        point1 = self.input_positions[0]
        point2 = self.input_positions[1] if not mos_pos else mos_pos

        magnitude_x = (point1[0] - point2[0]) * multiplier
        magnitude_y = (point1[1] - point2[1]) * multiplier
        impulse = pygame.Vector2(magnitude_x, magnitude_y)

        if impulse.length() > settings.max_impulse:
            impulse = impulse.normalize() * settings.max_impulse

        # magnitude_x = min(magnitude_x, settings.vel_cap)
        # magnitude_y = min(magnitude_y, settings.vel_cap)

        if not vel:
            self.vel.x = impulse.x
            self.vel.y = impulse.y

        else:
            vel.x = impulse.x
            vel.y = impulse.y
            return vel

    # this function predicts where the player will move according
    # to projectile motion while ignoring collisions
    def get_path_points(self, limit: int, offset:tuple[int, int]) -> list[tuple[int, int]] | None:
        # this delta is basically the resolution of the path
        # a lower value delta will result in a smoother path
        # but of smaller length because the number of steps are same
        delta = 1/15
        mouse_pos = pygame.mouse.get_pos()
        trajectory_points = []

        vel = self.add_impulse(settings.senstivity, self.vel.copy(), mouse_pos)
        x, y = self.pos + pygame.Vector2(self.radius, self.radius)
        x -= offset[0]
        y -= offset[1]

        if not vel:
            return

        for _ in range(limit):
            trajectory_points.append((int(x), int(y)))
            x += vel.x * delta
            y += vel.y * delta
            vel.y += settings.gravity * delta

        return trajectory_points


class State(Enum):
    NORMAL = 0
    INPUT = 1


class CollisionData:
    def __init__(self, collision_detected:bool, normal:pygame.Vector2 | None, collision_point:pygame.Vector2 | None, collision_with: str | None) -> None:
        self.collision_status = collision_detected
        self.normal = normal
        self.collision_point = collision_point
        self.collision_with = collision_with

    def update_all(self, collision_info: "CollisionData"):
        self.update_collision_point(collision_info.collision_point)
        self.update_normal(collision_info.normal)
        self.update_collision_status(collision_info.collision_status)
        self.update_collision_with(collision_info.collision_with)

    def update_normal(self, new_normal):
        self.normal = new_normal

    def update_collision_point(self, new_collision_point):
        self.collision_point = new_collision_point

    def update_collision_status(self, new_collision_status):
        self.collision_status = new_collision_status

    def update_collision_with(self, new_collision_with):
        self.collision_with = new_collision_with
