import math, pygame
from .entity_objs.player import Player
from .spawner import Spawner
from .entity import Entity
from .core_funcs import itr
from .weapons import create_weapon

class EntityManager:
    def __init__(self, game):
        self.game = game
        self.entities = []
        self.spawner = Spawner(self.game)
        self.render_entities = True

    def gen_player(self):
        self.entities.append(Player(self.game, (474, 138), (12, 12), 'player', 'player'))
        self.entities[-1].give_item(create_weapon(self.game, self.entities[-1], 'dagger'), 'active')

        self.player = self.entities[-1]
        self.player.load_actives()
        return self.entities[-1]

    def spawn_entities(self):
        self.spawner.update(self.game.window.dt)

    def y_sort(self, entity):
        if isinstance(entity, Entity):
            return entity.pos[1] + entity.size[1] - self.game.world.camera.true_pos[1]
        else:
            return entity[1][1] + entity[0].get_rect().height

    def render(self, surf):
        sorted_entities = sorted(self.entities + self.game.world.render_list, key=self.y_sort)
        entities = self.entities.copy()

        for entity in sorted_entities:
            if isinstance(entity, Entity):
                if self.render_entities or entity.type == 'player':
                    alive = entity.update(self.game.window.dt)
                    if not alive:
                        entities.remove(entity)
                    entity.render(surf, self.game.world.camera.true_pos)
            else:
                    surf.blit(entity[0], (math.floor(entity[1][0]), math.floor(entity[1][1])))
        self.entities = entities

#TODO: combine entity, tower, and obstacle sorting to accomodate for Y-sorting