import pygame, math
from ..weapon import Weapon
from ..core_funcs import lerp

class ShortswordWeapon(Weapon):
    def __init__(self, game, owner, type, amount=1, tags=[]):
        super().__init__(game, owner, type, amount, tags=tags)
        self.angle = 0

        self.offset = pygame.math.Vector2(0, 0)
        self.swing_speed = 20

        self.swing = -1
        self.swing_angle = 0
        self.target = 0
        self.weapon_angle = -134
        self.swinging = False

    def process_swing(self, dt):
        self.swing_angle = lerp(self.swing_angle, self.swing * 135, dt * self.swing_speed)

        t = 255 if self.swing == 1 else -45
        self.target = lerp(self.target, t, dt * self.swing_speed)

        if abs(t - self.target) < 5:
            self.swinging = False
            
        self.weapon_angle = self.swing_angle

    def attempt_attack(self):
        if self.owner:
            if super().attempt_attack():
                self.swing *= -1

    def update(self, dt):
        if self.attacking:
            self.process_swing(dt)

    def render(self, surf, loc, offset=(0, 0)):
        self.invisible = 0
        img = self.game.assets.weapons[self.type].copy()
        if not self.invisible:
            img = self.game.assets.weapons[self.type].copy()
            if (self.rotation % 360 < 270) and (self.rotation % 360 > 90):
                # FACING LEFT
                if self.swing == -1:
                    img = pygame.transform.flip(img, False, False)
                else:
                    img = pygame.transform.flip(img, False, True)
                self.flip = True
                angle_offset = -20
            else:
                # FACING RIGHT
                if self.swing == -1:
                    img = pygame.transform.flip(img, False, False)
                else:
                    img = pygame.transform.flip(img, False, True)
                self.flip = False
                angle_offset = 20
            img = pygame.transform.rotate(img, -self.rotation + angle_offset - self.weapon_angle)
            surf.blit(img, (loc[0] - (img.get_width() // 2) + (math.cos(math.radians(self.rotation + self.weapon_angle)) * 10) - offset[0], loc[1] - (img.get_height() // 2) - (math.sin(math.radians(-self.rotation - self.weapon_angle)) * 10) - offset[1]))