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

        self.wave_data = []
        self.difficulty_rank = 1
        self.spawner_index = 0
        self.enemy_index = 0

    def get_enemies_by_rank(self, rank):
        entities = []
        entity_list = config['entities']
        for entity in entity_list:
            if entity_list[entity]['rank'] == rank:
                entities.append(entity)
        return entities

    def generate_wave(self):
        if self.wave_data:
            self.wave_data = []
        
        entities = self.get_enemies_by_rank(self.difficulty_rank)

        # set number of enemies per wave
        num_enemies = random.randint((self.wave) * self.difficulty_rank, (self.wave) * self.difficulty_rank * 2)
        while num_enemies > 0:
            choose_enemies = random.randint(1, num_enemies)
            self.wave_data.append([entities[random.randint(0, len(entities) - 1)], choose_enemies])
            num_enemies -= choose_enemies
        print(self.wave_data)

    def update(self, dt):
        if self.game.world.loaded:
            self.timer += dt * self.difficulty_rank

            if self.spawner_index == len(self.wave_data):
                self.wave_clear = True
                self.spawner_index = 0

            if self.wave_clear:
                self.wave += 1
                self.generate_wave()
                self.wave_clear = False

            # if the number of enemies spawned is equal to the random number, change enemies
            if self.enemy_index == self.wave_data[self.spawner_index][1]:
                self.enemy_index = 0
                self.spawner_index += 1

            if self.timer >= 1:
                self.game.world.entities.entities.append(entity_map[self.wave_data[self.spawner_index][0]](self.game, (self.spawn_point[0] + random.randint(1, 8), self.spawn_point[1] + random.randint(1, 16)), (14, 14), self.wave_data[self.spawner_index][0], 'enemy'))
                self.enemy_index += 1
                self.timer = 0