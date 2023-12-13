import pygame, math, random
from ..weapon_types.spear_type import SpearWeapon
from ..core_funcs import normalize, normalize_vector

class SpearWeapon(SpearWeapon):
    def attack(self):
        self.invisible = 0.2

        offset = [math.cos(math.radians(self.rotation)) * 30, math.sin(math.radians(self.rotation)) * 30]

        self.game.world.weapon_anims.spawn('spear_' + str(self.owner.weapon.combo), (self.owner.center[0] + offset[0], self.owner.center[1] + offset[1]), flip=[False, False], rotation=-self.rotation, motion=100)
        self.game.world.hitboxes.add_hitbox(self.game, 'spear', tracked=self.game.world.weapon_anims.get_last(), owner=self.owner, angle=math.radians(self.rotation))

        if self.combo == 3:
            self.enable_update = True
            if (math.degrees(self.owner.aim_angle) % 360 < 270) and (math.degrees(self.owner.aim_angle) % 360 > 90):
                self.owner.flip[0] = True
            else:
                self.owner.flip[0] = False

            self.dash_distance = 2

            self.owner.velocity[0] = math.cos(self.owner.aim_angle) * self.dash_distance
            self.owner.velocity[1] = math.sin(self.owner.aim_angle) * self.dash_distance

    def update(self):
        if self.dash_distance:
            normalize_vector(self.owner.velocity, 0.1)
            self.dash_distance = normalize(self.dash_distance, 0.1)
        else:
            self.enable_update = False