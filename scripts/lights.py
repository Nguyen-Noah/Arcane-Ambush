import pygame
from .custom_shapes import gradient_circle
from .core_funcs import itr
from .config import config

class Light:
    def __init__(self, radius, color):
        self.radius = radius
        self.color = color
        self.owner = None
        self.img = gradient_circle(radius, color, (0, 0, 0))

    def set_owner(self, owner):
        self.owner = owner

    def update(self):
        self.pos = self.owner.pos
        return self.owner.alive

    def render(self, surf, offset=(0, 0)):
        surf.blit(self.img, (((self.pos[0] - offset[0]) * 1) - (self.img.get_width() // 2) + (self.owner.img.get_width() // 2), ((self.pos[1] - offset[1]) * 1) - (self.img.get_height() // 2) + (self.owner.img.get_height() // 2)), special_flags=pygame.BLEND_RGBA_ADD)

class Lights:
    def __init__(self, game):
        self.game = game
        self.lights = {}
        self.active_lights = []

    def load(self):
        lights = config['lights']
        for light in lights:
            self.lights[light] = Light(*lights[light])

    def attach_owner(self, light, owner):
        if light in self.lights:
            self.lights[light].set_owner(owner)

    def update(self):
        for light in self.lights:
            if self.lights[light].owner:
                alive = self.lights[light].update()
                if not alive:
                    self.lights.pop(light)

    def render(self, surf, offset=(0, 0)):
        for light in self.lights:
            if self.lights[light].owner:
                self.lights[light].render(surf, offset)