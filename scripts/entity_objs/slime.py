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
        self.spawn_point = [0, 0]
        self.current_index = 0
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

    def follow_path(self):
        self.path = tuplify(config['level_data']['tutorial']['path'])

        if self.current_index < len(self.path):
            target = (self.path[self.current_index][0], self.path[self.current_index][1])
            if target[0] < 0 or target[1] < 0:
                sign = -1
            else:
                sign = 1
            if math.floor(self.spawn_point[0]) != math.floor(target[0]):
                self.spawn_point[0] += sign * self.speed * self.game.window.dt
                self.pos[0] += sign * self.speed * self.game.window.dt
                self.flip[0] = sign < 0
                self.direction = 'side'
            elif math.floor(self.spawn_point[1]) != math.floor(target[1]):
                self.spawn_point[1] += sign * self.speed * self.game.window.dt
                self.pos[1] += sign * self.speed * self.game.window.dt
                if target[1] > 0:
                    self.direction = 'down'
                else:
                    self.direction = 'up'
            else:
                self.spawn_point = [0, 0]
                self.current_index += 1
            self.set_action('walk', self.direction)
        
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

        if self.targetable:
            self.jump()

        return self.alive