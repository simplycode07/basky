import pygame

from . import settings, colors
from .player import Sprite

ring_size = settings.tilesize + 20
ring_cross_section_size = 5

class Hoop:
    def __init__(self, hoop_info):
        # self.pos = list(init_pos)
        print(f"hoop_info: {hoop_info[0]}, {hoop_info[1]}")
        self.pos = self.get_pos(hoop_info)

        self.win_rect = pygame.Rect(5, self.pos[1] + 3, ring_size, 5)
        self.win_rect.left += self.pos[0]

        self.collision_rects = [pygame.Rect(0, 0, 5, 5), pygame.Rect(ring_size, 0, ring_cross_section_size, ring_cross_section_size)]
        for rect in self.collision_rects:
            rect.left += self.pos[0]
            rect.top += self.pos[1]
        self.detection_rect = []

        self.color = colors["red"]
        self.elasticity = 0.3

        # this is to store whether the player is colliding with the "win" rect or not 
        self.win_stat = False
        
        # this is for the area in which player checks for collision
        # this is just approximated so make sure the value is atleast more than 32
        self.collision_range = 100

    def draw(self, surface: pygame.Surface, offset: tuple[int, int]):
        converted_rects = self.convert_coords(offset)

        for rect in converted_rects:
            pygame.draw.rect(surface, self.color, rect)


    
    def convert_coords(self, offset: tuple[int, int]) -> list[pygame.Rect]:
        converted_rects = []
        for i, rect in enumerate(self.collision_rects):
            converted_rects.append(rect.copy())

            converted_rects[i].left -= offset[0]
            converted_rects[i].top -= offset[1]

        return converted_rects

    def get_pos(self, hoop_info:tuple[tuple[int, int], str]) -> tuple[int, int]:
        pos = list(hoop_info[0])

        if hoop_info[1] == "(-1)":
            pos[0] += -ring_size + settings.tilesize - ring_cross_section_size

        if hoop_info[1] == "(1)":
            pos[0] -= -ring_size + settings.tilesize - ring_cross_section_size

        return (pos[0], pos[1])


    # checks for win by checking if the player leaves the rect
    # and also the y velocity of the player should be +ive
    def check_for_win(self, player:"Sprite", center:pygame.Vector2):
        old_win_stat = self.win_stat
        self.win_stat = player.get_collision_with_rect(self.win_rect, center, "(-1)").collision_status

        if old_win_stat and not self.win_stat:
            if player.vel.y > 0:
                return True
        
            print("moved through area")
        return False
