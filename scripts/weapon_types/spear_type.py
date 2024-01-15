import pygame, math
from ..weapon import Weapon

class SpearWeapon(Weapon):
    def __init__(self, game, owner, type, amount=1, tags=[]):
        super().__init__(game, owner, type, amount, tags=tags)
    
    def attack(self):
        return super().attack()
    
    def attempt_attack(self):
        if self.owner:
            self.owner.weapon_hide = 3
            super().attempt_attack()
            
    def render(self, surf, loc, offset):
        self.invisible = max(0, self.invisible - self.game.window.dt)
        img = self.game.assets.weapons[self.type].copy()
        if not self.invisible:
            if (self.rotation % 360 < 270) and (self.rotation % 360 > 90):
                img = pygame.transform.flip(img, False, True)
                self.flip = True
            else:
                self.flip = False
            img = pygame.transform.rotate(img, -self.rotation)
            surf.blit(img, (loc[0] - offset[0] - (img.get_width() // 2) + (math.cos(math.radians(self.rotation)) * 8), loc[1] - offset[1] - (img.get_height() // 2) - (math.sin(math.radians(-self.rotation)) * 8) + 7))