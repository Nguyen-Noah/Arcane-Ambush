import math, pygame
from .core_funcs import tuplify
from .config import config
from .entity_objs.player import Player
from .spawner import Spawner
from .entity import Entity
from .tower import Tower
from .core_funcs import itr
from .weapons import create_weapon
from .quadtree import QuadTreeNode

class EntityManager:
    def __init__(self, game):
        self.game = game
        self.entities = []
        self.spawner = Spawner(self.game)
        self.render_entities = True
        self.projectiles = []
        self.quadtree = QuadTreeNode(0, 0, self.game.world.floor.get_size()[0], self.game.world.floor.get_size()[1])

    def gen_player(self):
        self.entities.append(Player(self.game, config['level_data'][self.game.state]['player_spawn_point'], (12, 12), 'player', 'player'))
        self.entities[-1].give_item(create_weapon(self.game, self.entities[-1], 'dagger'), 'active')

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

    def update(self):
        self.spawner.update(self.game.window.dt)

        for i, projectile in itr(self.projectiles):
            alive = projectile.update(self.game.window.dt)
            if not alive:
                self.projectiles.pop(i)

    def render(self, surf):
        sorted_entities = sorted(self.entities + self.game.world.render_list + self.game.world.towers.towers, key=self.y_sort)

        for entity in sorted_entities:
            if isinstance(entity, Entity):
                if self.render_entities or entity.category in ['player', 'enemy']:
                    alive = entity.update(self.game.window.dt)
                    if not alive:
                        self.entities.remove(entity)
                    entity.render(surf, self.game.world.camera.true_pos)
            elif isinstance(entity, Tower):
                entity.render(surf)
            else:
                surf.blit(entity[0], (math.floor(entity[1][0]), math.floor(entity[1][1])))

        for projectile in self.projectiles:
            projectile.render(surf, self.game.world.camera.true_pos)