import pygame

from .core_funcs import blit_center, itr

class DestructionParticles:
    def __init__(self, game):
        self.game = game
        self.particles = []

    def add_particle(self, surf, loc, velocity, duration=5, rotation=0, gravity=True, add=False):
        particle_data = {
            'surf': surf,
            'loc': loc,
            'vel': velocity,
            'duration': duration,
            'rotation': rotation,
            'stationary': False,
            'gravity': gravity,
            'add': add,
        }
        self.particles.append(particle_data)

    def update(self):
        dt = self.game.window.dt
        for i, particle in itr(self.particles):

            hit = False
            if not particle['stationary']:
                particle['loc'][0] += (particle['vel'][0]) * dt
                if self.game.world.tile_map.tile_collide(particle['loc']):
                    particle['vel'][0] *= -0.4
                    particle['vel'][1] *= 0.8
                    particle['vel'][2] *= 0.5
                    hit = True
                particle['loc'][1] += (particle['vel'][1]) * dt
                if self.game.world.tile_map.tile_collide(particle['loc']):
                    particle['vel'][1] *= -0.4
                    particle['vel'][0] *= 0.8
                    particle['vel'][2] *= 0.5
                    hit = True
                if hit:
                    if abs(particle['vel'][0]) + abs(particle['vel'][1]) < 1:
                        particle['stationary'] = True
                    else:
                        particle['loc'][0] += (particle['vel'][0]) * dt * 2
                        particle['loc'][1] += (particle['vel'][1]) * dt * 2

                particle['rotation'] += particle['vel'][2] * dt

                if particle['gravity']:
                    particle['vel'][1] += 100 * dt

            particle['duration'] -= dt
            if particle['duration'] < 0:
                self.particles.pop(i)

    def render(self, surf, offset=(0, 0)):
        for particle in self.particles:
            blit_center(surf, pygame.transform.rotate(particle['surf'].copy(), particle['rotation']), (particle['loc'][0] - offset[0], particle['loc'][1] - offset[1]), add=particle['add'])
