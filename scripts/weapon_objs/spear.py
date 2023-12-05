import pygame, math, random
from ..weapon import Weapon

class SpearWeapon(Weapon):
    def attack(self):
        self.invisible = 0.2

        offset = [math.cos(math.radians(self.rotation)) * 30, math.sin(math.radians(self.rotation)) * 30]

        self.game.world.weapon_anims.spawn('spear_' + str(self.owner.weapon.combo), (self.owner.center[0] + offset[0], self.owner.center[1] + offset[1]), flip=[False, False], rotation=-self.rotation, motion=100)
        self.game.world.hitboxes.add_hitbox(self.game, 'spear', tracked=self.game.world.weapon_anims.get_last(), owner=self.owner, angle=math.radians(self.rotation))