import pygame

from . import settings, colors

class Spikes:
    def __init__(self, spike_positions):
        self.spikes = [Spike(pos) for pos in spike_positions]

class Spike:
    def __init__(self, pos):
        ...
