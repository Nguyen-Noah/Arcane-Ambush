import random, pygame, math
from .config import config
from .entity_map import entity_map
from .ai.slime_ai import SlimeAI

class Spawner:
    def __init__(self, game):
        self.game = game
        self.spawn_point = None
        self.timer = 0
        self.wave_timer = 0
        self.wave = 0
        #self.spawn_point = config['level_data'][self.game.state]['path'][0]
        self.max_waves = config['level_data'][self.game.state]['waves']
        self.level_clear = False
        self.wave_clear = True

        self.num_enemies = 0
        self.difficulty_rank = 1
        self.enemy_list = self.get_enemies_by_rank(self.difficulty_rank)

        self.loaded = False

    def get_enemies_by_rank(self, rank):
        entities = []
        entity_list = config['entities']
        for entity in entity_list:
            if entity_list[entity]['rank'] == rank:
                entities.append(entity)
        return entities

    def new_wave(self):
        self.num_enemies = random.randint((self.wave) * self.difficulty_rank, (self.wave) * self.difficulty_rank * 2)

    def update(self, dt):
        if self.game.world.loaded:
            if not self.loaded:
                self.loaded = True
                self.game.world.entities.entities.append(entity_map['slime'](self.game, (300, 300), (14, 14), 'slime', 'enemy', controller=SlimeAI))
            """ if len(self.game.world.entities.entities) < 50:
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(100, 200)
                self.spawn_point = (self.game.world.player.pos[0] + distance * math.cos(angle), self.game.world.player.pos[1] + distance * math.sin(angle))
                self.timer += dt * self.difficulty_rank * 10

                if self.timer >= 1:
                    random_entity = self.enemy_list[random.randint(0, len(self.enemy_list) - 1)]
                    entity = entity_map[random_entity](self.game, (self.spawn_point[0] + random.randint(1, 8), self.spawn_point[1] + random.randint(1, 16)), (14, 14), random_entity, 'enemy')
                    self.game.world.entities.entities.append(entity)
                    #insert_entity(self.game.world.entities.quadtree, entity)
                    self.timer = 0 """