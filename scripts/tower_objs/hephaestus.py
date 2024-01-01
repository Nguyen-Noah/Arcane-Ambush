import pygame, math
from ..tower import Tower

class Hephaestus(Tower):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self, dt):
        super().update(dt)
        if self.hoverable:
            if self.attack_timer >= self.attack_cd:
                num_projectiles = 16
                for i in range(num_projectiles):
                    speed = 50
                    angle = math.pi * 2 * i / num_projectiles
                    self.game.world.entities.projectiles.spawn_projectile(self.type + '_projectile', self.center, angle, speed, self)
                self.attack_timer = 0

            self.game.world.add_light_source(self.center[0], self.center[1], 0.8, 0.4, (255, 50, 50))

    def render(self, surf, offset):
        super().render(surf, offset)