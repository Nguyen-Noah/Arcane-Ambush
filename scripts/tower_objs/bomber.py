import math, random
from ..tower import Tower
from ..projectiles import Projectile

class Bomber(Tower):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self):
        if self.hoverable:
            self.attack_timer += self.game.window.dt

            if self.attack_timer >= self.attack_cd:
                offset = random.random() * math.pi * 2
                for i in range(12):
                    speed = 50
                    angle = math.pi * 2 * i / 12 + offset
                    vel = [math.cos(angle) * speed, math.sin(angle) * speed]
                    self.game.world.entities.projectiles.append(Projectile(self.type + '_projectile', self.center, angle, speed, self.game, self))
                self.attack_timer = 0

    def render(self, surf, offset):
        super().render(surf, offset)