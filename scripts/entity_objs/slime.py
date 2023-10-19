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
        self.set_action('walk', self.direction)

    def randomize_color(self):
        random_color = (random.randint(197, 255), random.randint(233, 255), random.randint(225, 255))
        
        # (90, 197, 79) main color
        # (153, 230, 96) secondary color
        # (211 252 126) highlight color
        # 1: -58, -63
        # 2: -22, -33
        # 3: -30, -17

    def shadow(self):
        pygame.draw.circle(self.game.window.display, 'grey', (self.pos[0] - self.game.world.camera.true_pos[0], self.pos[1] - self.game.world.camera.true_pos[1] + self.size[1]), 5)

    def jump(self):
        jump_timer = 0
        for time in self.active_animation.data.config['frames']:
            jump_timer += time
        
        if self.active_animation.frame > (self.active_animation.data.config['frames'][0] + self.active_animation.data.config['frames'][1]): 
            if self.active_animation.frame < jump_timer - self.active_animation.data.config['frames'][5]:
                self.follow_path()
            else:
                self.timer = 0

    def update(self, dt):
        r = super().update(dt)
        if not r:
            return r
        else:
            self.jump()

        return self.alive