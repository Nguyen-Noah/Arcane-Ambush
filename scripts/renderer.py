import pygame, random
from .particles import ParticleManager
from .interface import Interface
import cProfile

class Renderer:
    def __init__(self, game):
        self.game = game
        self.interface = Interface(self.game)
        self.particles = ParticleManager(self.game)
        #self.overlay_particles()
        self.profiler = cProfile.Profile()

    def overlay_particles(self):
        for i in range(25):
            loc = [random.random() * self.game.window.display.get_width(), random.random() * self.game.window.display.get_height()]
            r = random.randint(1, 4)
            if r == 4:
                self.particles.add_particle('overlay', loc, 'p', [random.random() * -25 - 15, random.random() * 25 + 25], 0, random.choice([5, 5, 4]), custom_color=(200, 200, 200), glow=(10, 10, 10), glow_radius=4) #(201, 255, 229)
            else:
                self.particles.add_particle('overlay', loc, 'p', [random.random() * -25 - 15, random.random() * 25 + 25], 0, random.choice([5, 5, 4]), custom_color=(50, 50, 50))

    def update_overlay_particles(self, surf):
        self.particles.update()

        offset = [self.game.world.camera.pos[0] // 3, self.game.world.camera.pos[1] // 4]

        for particle in self.particles.particle_groups['overlay']:
            if particle.pos[0] + particle.internal_offset[0] < offset[0] - 1:
                particle.pos[0] += self.game.window.display.get_width()
            if particle.pos[0] + particle.internal_offset[0] > offset[0] + self.game.window.display.get_width() + 1:
                particle.pos[0] -= self.game.window.display.get_width()
            if particle.pos[1] + particle.internal_offset[1] < offset[1] - 1:
                particle.pos[1] += self.game.window.display.get_height()
            if particle.pos[1] + particle.internal_offset[1] > offset[1] + self.game.window.display.get_height() + 1:
                particle.pos[1] -= self.game.window.display.get_height()

        self.particles.render('overlay', surf, offset)

    def render(self):
        surf = self.game.window.display

        self.game.world.render(surf)
        self.game.world.entities.render(surf)

        #self.update_overlay_particles(surf)

        # ui
        self.interface.render(surf)
        self.interface.update()

        # display the player money
        self.game.assets.text.render(surf, '$' + str(self.game.world.entities.player.money), (300, 20))
