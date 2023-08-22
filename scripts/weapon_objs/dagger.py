import math, random
from ..weapon import Weapon

class DaggerWeapon(Weapon):
    def attack(self):
        self.invisible = 0.2

        if self.owner.weapon.combo == 2:
            self.game.world.vfs.spawn_vfx('arc', self.owner.center.copy(), 2, random.random() * 3, math.radians(self.rotation - 20), 6, random.random * 6 + 100, 0.6, start=0, end=1, duration=1.3, arc_stretch=100, motion=random.randint(300, 450), decay=['down', 50], color=(218, 36, 36), fade=0.5)
        else:
            # binary logic hack
            if self.flip - (self.owner.weapon.combo == 1):
                self.game.world.vfx.spawn_vfx('arc', self.owner.center.copy(), 2, random.random() * 3, math.radians(self.rotation - 20), 6, random.random() * 6 + 100, 0.5, start=0, end=0.5, duration=0.7, arc_stretch=300, motion=random.randint(300, 450), decay=['down', 100], color=(218, 36, 36), fade=0.5)
            else:
                self.game.world.vfx.spawn_vfx('arc', self.owner.center.copy(), 2, random.random() * 3, math.radians(self.rotation + 20), 6, random.random() * 6 + 100, 0.5, start=0.5, end=1, duration=0.7, arc_stretch=300, motion=random.randint(300, 450), decay=['up', 100], color=(218, 36, 36), fade=0.5)
        self.game.world.hitboxes.add_hitbox(self.game, 'sword', tracked=self.game.world.vfx.get_last(), owner=self.owner, angle=math.radians(self.rotation))
