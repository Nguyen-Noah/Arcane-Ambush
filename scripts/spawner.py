import random
from .config import config
from .entity_map import entity_map

class Spawner:
    def __init__(self, game):
        self.game = game
        self.spawn_point = None
        self.timer = 0
        self.wave = 70
        self.spawn_point = (41, -48)
        self.max_waves = config['level_data']['level_0']['levels']
        self.level_clear = False
        self.wave_clear = True

        self.wave_data = []
        self.difficulty_rank = 1
        self.enemy_index = 0

    def get_enemies_by_rank(self, rank):
        entities = []
        entity_list = config['entities']
        for entity in entity_list:
            if entity_list[entity]['rank'] == rank:
                entities.append(entity)
        return entities

    def generate_wave(self):
        entities = self.get_enemies_by_rank(self.difficulty_rank)

        # set number of enemies per wave
        num_enemies = random.randint((self.wave + 10) * self.difficulty_rank, (self.wave + 10) * self.difficulty_rank * 2)
        while num_enemies > 0:
            choose_enemies = random.randint(0, num_enemies)
            self.wave_data.append([entities[random.randint(0, len(entities) - 1)], choose_enemies])
            num_enemies -= choose_enemies
        print(self.wave_data)

    def update(self, dt):
        if self.game.world.loaded:
            self.timer += dt * self.difficulty_rank

            if self.wave_clear:
                self.generate_wave()
                self.wave_clear = False
            
            for enemy_data in self.wave_data:
                if self.enemy_index == enemy_data[1]:
                    
                if self.timer >= 1:
                    self.enemy_index += 1
                    self.spawn_timer = 0

            '''self.timer += dt

            if self.total_enemy_count == 0:
                self.wave_clear = True

            if not self.level_clear:
                if not self.wave_clear:
                    if not self.enemy_count:
                        self.enemy_count = self.get_enemy_type()

                    for i in range(self.enemy_count):
                        if self.timer >= self.spawn_timer and self.total_enemy_count > 0:
                            self.game.world.entities.entities.append(entity_map[self.enemy_type](self.game, (self.spawn_point[0] + random.randint(1, 8), self.spawn_point[1] + random.randint(1, 16)), (14, 14), self.enemy_type, 'enemy'))
                            self.timer = 0
                            self.enemy_count -= 1
                            self.total_enemy_count -= 1
                elif self.timer > 3:
                    if self.wave == (len(self.level_waves) - 1):
                        self.level_clear = True
                        #print('level clear')
                    self.wave += 1
                    self.timer = 0
                    self.spawner_index = 0
                    if not self.level_clear:
                        self.total_enemy_count = self.get_total_count()
                    self.wave_clear = False
                    #print('new wave')'''