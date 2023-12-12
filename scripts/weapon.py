import pygame, math, random, time
from .projectiles import Projectile
from .config import config
from .core_funcs import advance
from .item import Item

class Weapon(Item):
    def __init__(self, game, owner, type, amount=1, tags=[]):
        super().__init__(game, owner, type, amount, tags=tags)
        self.game = game
        self.owner = owner
        self.type = type
        self.rotation = 0
        self.is_weapon = True
        self.projectile_type = config['weapons'][self.type]['projectile_type']
        self.capacity = config['weapons'][self.type]['capacity']
        self.attack_rate = config['weapons'][self.type]['attack_rate']
        self.combo = 0
        self.combo_limit = config['weapons'][self.type]['combo']
        self.combo_cooldown = config['weapons'][self.type]['combo_cooldown']
        self.range = config['weapons'][self.type]['range']
        self.max_rank = config['weapons'][self.type]['max_rank']
        self.last_attack = 0
        self.flip = False
        self.invisible = 0
        self.accuracy = 1
        self.enable_update = False

    @property
    def rank(self):
        rank = 0
        return rank

    def attempt_attack(self):
        # cant attack without an owner
        if self.owner:
            self.owner.weapon_hide = 3
        
            if self.combo == self.combo_limit:
                self.combo = 0

            if self.combo < self.combo_limit:
                if (time.time() - self.last_attack > self.attack_rate):
                    self.last_attack = time.time()
                    self.attack()
                    self.combo += 1

    def attack(self):
        angle_offset = (1 - self.accuracy) * math.pi
        self.game.world.entities.particles.append(Projectile(self.projectile_type, self.owner.center.copy(), math.radians(self.rotation) - angle_offset + random.random() * angle_offset * 2, 300, self.game, self.owner))
        self.game.world.vfx.spawn_group('bow_sparks', advance(self.owner.center.copy(), math.radians(self.rotation), 8), math.radians(self.rotation))

    def render(self, surf, loc):
        self.invisible = max(0, self.invisible - self.game.window.dt)
        if not self.invisible:
            img = self.game.assets.weapons[self.type].copy()
            if (self.rotation % 360 < 270) and (self.rotation % 360 > 90):
                img = pygame.transform.flip(img, False, True)
                self.flip = True
            else:
                self.flip = False
            img = pygame.transform.rotate(img, -self.rotation)
            surf.blit(img, (loc[0] - (img.get_width() // 2) + (math.cos(math.radians(self.rotation)) * 8), loc[1] - (img.get_height() // 2) - (math.sin(math.radians(-self.rotation)) * 8) + 3))