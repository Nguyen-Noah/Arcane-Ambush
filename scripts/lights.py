import pygame
from .custom_shapes import gradient_circle
from .core_funcs import itr

class Light:
    def __init__(self, radius, color, owner, manager):
        self.radius = radius
        self.color = color
        self.owner = owner
        self.manager = manager
        self.pos = self.owner.pos

    def update(self):
        self.pos = self.owner.pos
        return self.owner.alive

    def render(self, surf, offset=(0, 0)):
        cache_id = (self.radius, self.color)
        if cache_id not in self.manager.light_cache:
            img = gradient_circle(self.radius, self.color, (0, 0, 0))
            self.manager.light_cache[cache_id] = img
        else:
            img = self.manager.light_cache[cache_id]
        surf.blit(img, (((self.pos[0] - offset[0]) * 1) - (img.get_width() // 2) + (self.owner.img.get_width() // 2), ((self.pos[1] - offset[1]) * 1) - (img.get_height() // 2) + (self.owner.img.get_height() // 2)), special_flags=pygame.BLEND_RGBA_ADD)

class Lights:
    def __init__(self, game):
        self.game = game
        self.lights = []
        self.light_cache = {}

    def add_light(self, radius, color, owner):
        self.lights.append(Light(radius, color, owner, self))

    def update(self):
        for i, light in itr(self.lights):
            alive = light.update()
            if not alive:
                self.lights.pop(i)

    def render(self, surf, offset=(0, 0)):
        for light in self.lights:
            light.render(surf, offset)