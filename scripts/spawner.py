import random
from .config import config
from .entity_map import entity_map

class Spawner:
    def __init__(self, game):
        self.game = game
        self.spawn_point = None
        self.timer = 0
        self.wave = 0
        self.spawn_point = config['level_data'][self.game.state]['path'][0]
        self.max_waves = config['level_data'][self.game.state]['waves']
        self.level_clear = False
        self.wave_clear = True

        self.num_enemies = 0
        self.difficulty_rank = 1

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
            self.timer += dt * self.difficulty_rank

            if self.num_enemies == 0:
                self.wave_clear = True

            if self.wave_clear:
                self.enemy_list = self.get_enemies_by_rank(self.difficulty_rank)
                self.wave += 1
                self.new_wave()
                self.wave_clear = False

            if self.timer >= 1:
                random_entity = self.enemy_list[random.randint(0, len(self.enemy_list) - 1)]
                self.game.world.entities.entities.append(entity_map[random_entity](self.game, (self.spawn_point[0] + random.randint(1, 8), self.spawn_point[1] + random.randint(1, 16)), (14, 14), random_entity, 'enemy'))
                self.num_enemies -= 1
                self.timer = 0