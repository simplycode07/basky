import pygame
from src import utils

class PhysicsEntities:
    def __init__(self, game, pos, e_type, size):
        self.game = game
        self.pos = list(pos)
        self.type = e_type
        self.size = size

        self.vel = [0, 0]
        self.image = pygame.image.load(self.game.assets[e_type]).convert()
        self.fric = 300
    
    def update(self, dt, movement=[0,0]):
        self.vel[0] = self.vel[0] - self.fric * dt * utils.signum(self.vel[0]) if self.vel[0] else 0
        self.vel[1] = self.vel[1] - self.fric * dt * utils.signum(self.vel[1]) if self.vel[1] else 0
        del_pos = (movement[0] + self.vel[0], movement[1] + self.vel[1])
        
        self.pos[0] = self.pos[0] + del_pos[0]
        self.pos[1] = self.pos[1] + del_pos[1]

    def render(self, screen):
        screen.blit(self.image, self.pos)
