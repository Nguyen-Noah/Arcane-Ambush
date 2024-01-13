import pygame, math, random
from ..entity import Entity
from ..core_funcs import tuplify
from ..config import config

class Slime(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category = 'enemy'
        self.velocity = [0, 0]
        self.size = (14, 14)

    def update(self, dt):
        self.frame_motion = self.velocity.copy()
        r = super().update(dt)
        if not r:
            return r

        return self.alive