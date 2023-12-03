import pygame
from .core_funcs import itr

class StandaloneAnimation:
    def __init__(self, animation_obj, location, flip=[False, False], rotation=0):
        self.pos = list(location)
        self.animation = animation_obj
        self.animation.flip = flip.copy()
        self.rotation = rotation
        self.alive = not self.animation.done

    def create_mask(self):
        offset = self.animation.data.image_list[0].get_size()
        return pygame.mask.from_surface(self.animation.img), (self.pos[0] - offset[0] // 2, self.pos[1] - offset[1] // 2)

class StandaloneAnimations:
    def __init__(self, game):
        self.game = game
        self.animations = []

    def spawn(self, animation_id, location, flip=[False, False], rotation=0):
        self.animations.append(StandaloneAnimation(self.game.assets.animations.new(animation_id, rotation=rotation), location, flip, rotation))

    def get_last(self):
        return self.animations[-1]

    def update(self):
        dt = self.game.window.dt
        for i, animation in itr(self.animations):
            animation.animation.play(dt)
            if animation.animation.done:
                animation.alive = False
                self.animations.pop(i)

    def render(self, surf, offset=(0, 0)):
        for animation in self.animations:
            #pygame.draw.circle(surf, 'black', (animation.pos[0] - offset[0], animation.pos[1] - offset[1]), 10)
            animation.animation.render(surf, animation.pos, offset)