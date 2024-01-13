import pygame, math, random, time
from .projectiles import Projectile
from .config import config
from .core_funcs import outline
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
        self.hold_type = config['weapons'][self.type]['hold_type']
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
        self.attacking = False
        self.outline_cache = {}

    @property
    def rank(self):
        rank = 0
        return rank
    
    def get_outline_surf(self, surf, rotation, cache_args=None, color=(255, 255, 255)):
        if cache_args:
            cache_id = (int(rotation % 260), *cache_args)
        else:
            cache_id = int(rotation % 360)
        print(len(self.outline_cache))
        if cache_id not in self.outline_cache:
            outline_surf = outline(surf, color=color)
            self.outline_cache[cache_id] = outline_surf
        else:
            outline_surf = self.outline_cache[cache_id]

        return outline_surf

    def attempt_attack(self):
        if self.combo == self.combo_limit:
            self.combo = 0

        if self.combo < self.combo_limit:
            if (time.time() - self.last_attack > self.attack_rate):
                self.last_attack = time.time()
                self.attack()
                self.combo += 1
                return True
        
        return False