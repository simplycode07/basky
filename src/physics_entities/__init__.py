import pygame

from src import settings, colors
from .player import Sprite
from .hoop import Hoop

class PhysicsEntities:
    def __init__(self, level_info) -> None:
        self.tilemap = level_info[0]
        player_info = level_info[1]
        hoop_info = level_info[2]

        self.player = Sprite(self.tilemap, player_info)
        self.hoop = Hoop(hoop_info)

    def input(self, event):
        self.player.handle_input(event)

    def update(self, delta, display):
        self.player.update(delta, display)
        center = self.player.get_self_rect().center
        for rect in self.hoop.collision_rects:
            collision_data = self.player.get_collision_with_rect(rect, pygame.Vector2(center))
            self.player.handle_collision(delta, collision_data)