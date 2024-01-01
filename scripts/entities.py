import math, pygame
from .core_funcs import tuplify
from .config import config
from .entity_objs.player import Player
from .spawner import Spawner
from .entity import Entity
from .projectiles import ProjectileManager
from .tower import Tower
from .core_funcs import itr
from .weapons import create_weapon

class EntityManager:
    def __init__(self, game):
        self.game = game
        self.entities = []
        self.spawner = Spawner(self.game)
        self.render_entities = True
        self.projectiles = ProjectileManager(self.game)

    def gen_player(self):
        self.entities.append(Player(self.game, config['level_data'][self.game.state]['player_spawn_point'], (12, 12), 'player', 'player'))
        #self.entities[-1].give_item(create_weapon(self.game, self.entities[-1], 'dagger'), 'active')
        #self.entities[-1].give_item(create_weapon(self.game, self.entities[-1], 'spear'), 'active')
        #self.entities[-1].give_item(create_weapon(self.game, self.entities[-1], 'earthStaff'), 'active')
        #self.entities[-1].give_item(create_weapon(self.game, self.entities[-1], 'lightStaff'), 'active')
        self.entities[-1].give_item(create_weapon(self.game, self.entities[-1], 'fireGrimoire'), 'active')

        self.player = self.entities[-1]
        self.player.load_actives()
        return self.entities[-1]

    def y_sort(self, entity):
        if isinstance(entity, Entity):
            return entity.pos[1] + entity.size[1] - self.game.world.camera.true_pos[1]
        elif isinstance(entity, Tower):
            return entity.rect[1] + (entity.img.get_size()[1] // 1.25)
        else:
            return entity[1][1] + entity[0].get_rect().height

    def update(self, dt):
        #self.spawner.update(self.game.window.dt)
        for i, entity in enumerate(self.entities):
            alive = entity.update(dt)
            if not alive:
                self.entities.pop(i)

        self.projectiles.update(dt)

    def render(self, surf, offset=(0, 0)):
        sorted_entities = sorted(self.entities + self.game.world.render_list + self.game.world.towers.towers, key=self.y_sort)

        for entity in sorted_entities:
            if isinstance(entity, Entity):
                if self.render_entities or entity.category in ['player', 'enemy']:
                    entity.render(surf, offset)
            elif isinstance(entity, Tower):
                entity.render(surf, offset)
            else:
                surf.blit(entity[0], (math.floor(entity[1][0]), math.floor(entity[1][1])))

        self.projectiles.render(surf, offset)