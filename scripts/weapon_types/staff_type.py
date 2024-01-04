import pygame, math, random
from ..weapon import Weapon
from ..core_funcs import advance

class StaffWeapon(Weapon):
    def __init__(self, game, owner, type, amount=1, tags=[]):
        super().__init__(game, owner, type, amount, tags=tags)

    def attack(self):
        angle_offset = (1 - self.accuracy) * math.pi
        self.game.world.entities.projectiles.spawn_projectile(self.projectile_type + '_projectile', self.owner.center.copy(), math.radians(self.rotation) - angle_offset + random.random() * angle_offset * 2, 300, 1, self.owner)
        self.game.world.vfx.spawn_group('bow_sparks', advance(self.owner.center.copy(), math.radians(self.rotation), 8), math.radians(self.rotation))
    
    def attempt_attack(self):
        if self.owner:
            self.owner.weapon_hide = 3
            super().attempt_attack()

    def render(self, surf, loc, offset=(0, 0)):
        self.invisible = 0
        img = self.game.assets.weapons[self.type].copy()
        if not self.invisible:
            if (self.rotation % 360 < 270) and (self.rotation % 360 > 90):
                img = pygame.transform.flip(img, False, True)
                self.flip = True
            else:
                self.flip = False
            img = pygame.transform.rotate(img, -self.rotation)
            blit_loc = (loc[0] - (img.get_width() // 2) + (math.cos(math.radians(self.rotation)) * 8) - offset[0], loc[1] - (img.get_height() // 2) - (math.sin(math.radians(-self.rotation)) * 8) - 2 - offset[1])
            surf.blit(img, blit_loc)