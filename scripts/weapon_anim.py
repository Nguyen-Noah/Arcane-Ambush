import pygame, math, random
from .core_funcs import itr

class WeaponAnimation:
    def __init__(self, animation_obj, location, angle, flip=[False, False]):
        self.animation = animation_obj
        self.pos = list(location)
        self.animation.rotation = -math.degrees(angle)
        self.animation.flip = flip.copy()

class WeaponAnimations:
    def __init__(self, game):
        self.game = game
        self.animations = []

    def spawn(self, animation_id, location, angle, flip=[False, False]):
        self.animations.append(WeaponAnimation(self.game.assets.animations.new(animation_id), location, angle, flip))

    def update(self):
        dt = self.game.window.dt
        for i, animation in itr(self.animations):
            animation.pos[0] += math.cos(math.radians(animation.animation.rotation)) * (random.randint(40, 70) * 0.01)
            animation.pos[1] -= math.sin(math.radians(animation.animation.rotation)) * (random.randint(40, 70) * 0.01)
            animation.animation.play(dt)
            if animation.animation.done:
                self.animations.pop(i)

    def render(self, surf, offset=(0, 0)):
        for animation in self.animations:
            animation.animation.render(surf, animation.pos, offset)