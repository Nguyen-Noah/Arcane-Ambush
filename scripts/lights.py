import pygame
from .custom_shapes import gradient_circle
from .core_funcs import itr

class Light:
    def __init__(self, radius, color, owner):
        self.radius = radius
        self.color = color
        self.owner = owner
        self.pos = self.owner.pos
        self.surf = gradient_circle(self.radius, self.color, (0, 0, 0))

    def update(self):
        self.pos = self.owner.pos
        return self.owner.alive

    def render(self, surf, offset=(0, 0)):
        surf.blit(self.surf, (self.pos[0] - offset[0] - (self.surf.get_width() // 2), self.pos[1] - offset[1] - (self.surf.get_height() // 2)), special_flags=pygame.BLEND_RGBA_ADD)

class Lights:
    def __init__(self, game):
        self.game = game
        self.lights = []

    def add_light(self, radius, color, owner):
        self.lights.append(Light(radius, color, owner))

    def update(self):
        for i, light in itr(self.lights):
            alive = light.update()
            if not alive:
                self.lights.pop(i)

    def render(self, surf, offset=(0, 0)):
        for light in self.lights:
            light.render(surf, offset)