import pygame, math, random
from ..entity import Entity
from ..core_funcs import tuplify
from ..config import config

class Slime(Entity):
    def __init__(self, *args):
        super().__init__(*args)
        self.category = 'enemy'
        self.velocity = [0, 0]
        self.size = (14, 14)
        self.direction = 'down'
        self.direction_calculated = False
        self.set_action('walk', self.direction)

    def jump(self):
        jump_timer = sum(self.active_animation.data.config['frames'])
        
        if self.active_animation.frame > (self.active_animation.data.config['frames'][0] + self.active_animation.data.config['frames'][1]):
            if self.active_animation.frame < jump_timer - self.active_animation.data.config['frames'][5]:
                self.frame_motion = self.get_target_distance(self.game.world.player)
                self.direction_calculated = True
                self.move(self.frame_motion, self.game.world.collideables)
            else:
                self.timer = 0

    def update(self, dt):
        self.frame_motion = self.velocity.copy()
        r = super().update(dt)
        if not r:
            return r
        else:
            self.jump()

        return self.alive