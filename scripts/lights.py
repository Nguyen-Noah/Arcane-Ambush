import pygame
from .custom_shapes import gradient_circle
from .core_funcs import itr
from .config import config

class Light:
    def __init__(self, img, owner):
        self.owner = owner
        self.img = img
        self.pos = self.owner.pos.copy()

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
            self.lights[light] = gradient_circle(*lights[light])

    def add_light(self, light, owner):
        self.active_lights.append(Light(self.lights[light], owner))

    def update(self):
        for i, light in itr(self.active_lights):
            alive = light.update()
            if not alive:
                self.active_lights.pop(i)

    def render(self, surf, offset=(0, 0)):
        for light in self.active_lights:
            light.render(surf, offset)