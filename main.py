import pygame
from src.entities import PhysicsEntities
from math import sqrt

class Game:
    def __init__(self, window_size):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.running = False
        self.window_size = window_size

        self.screen = pygame.display.set_mode(window_size)
        self.display = pygame.Surface((window_size[0]/2, window_size[1]/2))
        
        self.colors = {"white":(255, 255, 255),
                       "black":(0, 0, 0),
                       "red":(255, 0, 0),
                       "green":(0, 255, 0),
                       "blue":(0, 0, 255),
                       "cyan":(0, 255, 255)}
        
        self.assets = {"player":"assets/basky_32x32.png"}
        self.player = PhysicsEntities(self, (30, 30), "player", (0,0))

    def run(self):
        self.running = True
        pos = []
        while self.running:
            movement = (0, 0)
            self.display.fill(self.colors["black"])
            dt = self.clock.tick(60) * 0.001
            self.fps = self.clock.get_fps() 

            # print(f"fps: {self.fps}")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if (event.type == pygame.KEYDOWN and len(pos) == 0) or (event.type == pygame.KEYUP and len(pos)):
                    pos.append(pygame.mouse.get_pos())


            if len(pos) > 1:
                point1, point2 = pos[0], pos[1]
                dir = ((point2[0] - point1[0]), (point2[1] - point1[1]))
                magnitude = sqrt((point1[0]-point2[0])**2 + (point1[1] - point2[1])**2)

                self.player.vel = list(dir)
                pos = []

            self.player.update(dt, movement)
            self.player.render(self.display)

            pygame.display.update()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))


if __name__ == "__main__":
    Game((600, 500)).run()
