import pygame
from constants import SHOT_RADIUS

class Shot(CircleShape):
    def __init__(self, x, y, velocity):
        super().__init__(x, y, SHOT_RADIUS)

        # Initialize velocity
        self.velocity = velocity
        