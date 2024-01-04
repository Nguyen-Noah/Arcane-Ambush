import  math, random
from ..tower import Tower
from ..ease_functions import easeInOutExpo

class Aether(Tower):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = (205, 180, 20)
        self.active_projectiles = []

    def update(self, dt):
        super().update(dt, color=self.color)
        num_shots = 12
        # add particle emitters
        if self.attack_timer >= self.attack_cd:
            for i in range(num_shots):
                speed = random.randint(60, 100)
                angle = self.rotation + random.random() * math.pi / 4 - math.pi / 8
                self.game.world.vfx.spawn_group('aether_sparks', self.center, angle + math.pi, color=self.color)
                self.game.world.entities.projectiles.spawn_projectile(self.type + '_projectile', self.center, angle, speed, 2, self)
                self.active_projectiles.append(self.game.world.entities.projectiles.get_last())
            self.attack_timer = 0

        for i, projectile in enumerate(self.active_projectiles):
            self.game.renderer.particles.add_particle('aether', (projectile.pos[0] - (projectile.img.get_width() // 2), projectile.pos[1] - (projectile.img.get_height() // 2) - 1), 'aether', [math.cos(projectile.rotation + (math.pi * (random.randint(1, 20) / 10))) * 30, math.sin(projectile.rotation + (math.pi * (random.randint(1, 20) / 10))) * 30], 20, random.randint(0, 20) / 10)
            if not projectile.alive:
                self.active_projectiles.pop(i)

    def render(self, surf, offset):
        super().render(surf, offset)
        if 'aether' in self.game.renderer.particles.particle_groups:
            self.game.renderer.particles.render('aether', surf, offset)