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
