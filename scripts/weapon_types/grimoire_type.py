import pygame, math, random
from ..weapon import Weapon
from ..core_funcs import advance
from ..vfx import glow

class GrimoireWeapon(Weapon):
    def __init__(self, game, owner, type, amount=1, tags=[]):
        super().__init__(game, owner, type, amount, tags=tags)
        self.enable_update = True
        self.active_projectiles = []

    def attack(self):
        angle_offset = (1 - self.accuracy) * math.pi
        self.game.world.entities.projectiles.spawn_projectile(self.projectile_type + '_projectile', self.owner.center.copy(), math.radians(self.rotation) - angle_offset + random.random() * angle_offset * 2, 250, self.owner)
        self.game.world.vfx.spawn_group('bow_sparks', advance(self.owner.center.copy(), math.radians(self.rotation), 8), math.radians(self.rotation))
        self.active_projectiles.append(self.game.world.entities.projectiles.get_last())
    
    def attempt_attack(self):
        if self.owner:
            self.owner.weapon_hide = 3
            super().attempt_attack()
        
    def update(self, color=(255, 255, 255)):
        for i, projectile in enumerate(self.active_projectiles):
            #print([(random.randint(0, 10) / 10 - 0.5) * 10, (random.randint(0, 20) / 10 - 2) * 10])
            self.game.renderer.particles.add_particle('grimoire', (projectile.pos[0] - (projectile.img.get_width() // 2), projectile.pos[1] - (projectile.img.get_height() // 2) - 1), 'circle', [math.cos(projectile.rotation + (math.pi * (random.randint(1, 20) / 10))) * 20, math.sin(projectile.rotation + (math.pi * (random.randint(1, 20) / 10))) * 20], 40, random.randint(0, 20) / 10, custom_color=color)
            glow((projectile.pos[0] - self.game.world.camera.true_pos[0] - (projectile.img.get_width() // 2), projectile.pos[1] - self.game.world.camera.true_pos[1] - (projectile.img.get_height() // 2)), 10, color=(color[0] // 10, color[1] // 10, color[2] // 10))
            if not projectile.alive:
                self.active_projectiles.pop(i)

    def render(self, surf, loc, offset=(0, 0)):
        if 'grimoire' in self.game.renderer.particles.particle_groups:
            self.game.renderer.particles.render('grimoire', surf, offset)

        self.invisible = 0
        img = self.game.assets.weapons[self.type].copy()
        if not self.invisible:
            if (self.rotation % 360 < 270) and (self.rotation % 360 > 90):
                img = pygame.transform.flip(img, False, True)
                self.flip = True
            else:
                self.flip = False
            img = pygame.transform.rotate(img, -self.rotation)
            surf.blit(img, (loc[0] - (img.get_width() // 2) + (math.cos(math.radians(self.rotation)) * 8) - offset[0], loc[1] - (img.get_height() // 2) - (math.sin(math.radians(-self.rotation)) * 8) + 4 - offset[1]))