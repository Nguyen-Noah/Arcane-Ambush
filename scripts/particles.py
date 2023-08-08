import os, random, math

from .core_funcs import blit_center
from .vfx import glow
import pygame

global e_colorkey
e_colorkey = (0, 0, 0, 0)

class ParticleManager:
    def __init__(self, game):
        self.game = game
        self.particle_groups = {}
        self.cache = True
        self.particle_cache = {}

    def add_particle(self, group, *args, **kwargs):
        if group not in self.particle_groups:
            self.particle_groups[group] = []
        self.particle_groups[group].append(Particle(self.game, *args, **kwargs, manager=self))

    def add(self, x, y, particle_type, motion, decay_rate, start_frame, custom_color=None):
        self.particles.append(Particle(self.game, x, y, particle_type, motion, decay_rate, start_frame, custom_color=None))

    def render(self, group, surf, offset=[0,0]):
        for i, particle in sorted(enumerate(self.particle_groups[group]), reverse=True):
            particle.draw(surf, offset)

    def update(self):
        for group in self.particle_groups:
            for i, particle in sorted(enumerate(self.particle_groups[group]), reverse=True):
                alive = particle.update(self.game.window.dt)
                if not alive:
                    self.particle_groups[group].pop(i)

class Particle(object):
    def __init__(self, game, pos, particle_type, motion, decay_rate, start_frame, physics=None, custom_color=None, glow=None, glow_radius=None, manager=None):
        self.game = game
        self.pos = list(pos)
        self.type = particle_type
        self.motion = motion
        self.decay_rate = decay_rate
        self.color = custom_color
        self.frame = start_frame
        self.physics = physics
        self.orig_motion = self.motion
        self.temp_motion = [0, 0]
        self.time_left = len(self.game.assets.particles[self.type]) + 1 - self.frame
        self.render = True
        self.random_constant = random.randint(20, 30) / 30
        self.internal_offset = [0, 0]
        self.rotation = 0
        self.manager = manager
        self.glow = glow
        self.glow_radius = glow_radius

    def update(self, dt):
        self.frame += self.decay_rate * dt
        self.time_left = len(self.game.assets.particles[self.type]) + 1 - self.frame
        running = True
        self.render = True
        if self.frame >= len(self.game.assets.particles[self.type]):
            self.render = False
            if self.frame >= len(self.game.assets.particles[self.type]) + 1:
                running = False
            running = False
        if not self.physics:
            self.pos[0] += (self.temp_motion[0] + self.motion[0]) * dt
            self.pos[1] += (self.temp_motion[1] + self.motion[1]) * dt
        self.temp_motion = [0, 0]
        return running

    def draw(self, surface, scroll):
        if self.render:
            cache_id = (int(self.rotation % 360), self.type,  int(self.frame), self.color)
            if (not self.manager) or (not self.manager.cache) or (cache_id not in self.manager.particle_cache):
                img = self.game.assets.particles[self.type][str(int(self.frame))]
                if self.color:
                    img = swap_color(img, (255, 255, 255), self.color)
                if self.rotation:
                    img = pygame.transform.rotate(img, int(self.rotation))
                img.set_colorkey((0, 0, 0))
                if self.manager.cache:
                    self.manager.particle_cache[cache_id] = img
            if self.manager.cache:
                img = self.manager.particle_cache[cache_id]
            if self.glow:
                glow((self.pos[0] - scroll[0] + self.internal_offset[0], self.pos[1] - scroll[1] + self.internal_offset[1]), self.glow_radius, 0, color=self.glow)
                light_color = (self.glow[0] * 0.5, self.glow[1] * 0.5, self.glow[2] * 0.5)
                glow((self.pos[0] - scroll[0] + self.internal_offset[0], self.pos[1] - scroll[1] + self.internal_offset[1]), self.glow_radius * 2, 0, color=light_color)

            blit_center(surface, img, (self.pos[0] - scroll[0] + self.internal_offset[0], self.pos[1] - scroll[1] + self.internal_offset[1]))

def swap_color(img,old_c,new_c):
    global e_colorkey
    img.set_colorkey(old_c)
    surf = img.copy()
    surf.fill(new_c)
    surf.blit(img,(0,0))
    surf.set_colorkey(e_colorkey)
    return surf