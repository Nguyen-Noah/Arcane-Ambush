import pygame, math, random
from ..tower import Tower

class Aether(Tower):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = (205, 180, 20)

    def update(self, dt):
        super().update(dt, color=self.color)

    def render(self, surf, offset):
        super().render(surf, offset)
        print(self.rotation)
        num_shots = 12
        # add particle emitters
        if self.attack_timer >= self.attack_cd:
            for i in range(num_shots):
                speed = random.randint(60, 100)
                angle = self.rotation + random.random() * math.pi / 4 - math.pi / 8
                self.game.world.vfx.spawn_group('aether_sparks', self.center, angle + math.pi, color=self.color)
                self.game.world.entities.projectiles.spawn_projectile(self.type + '_projectile', self.center, angle, speed, self)
            self.attack_timer = 0
        pygame.draw.line(self.game.window.display, 'red', (self.center[0] - offset[0], self.center[1] - offset[1]), (self.targeted_entity.center[0] - offset[0], self.targeted_entity.center[1] - offset[1]), 1)
