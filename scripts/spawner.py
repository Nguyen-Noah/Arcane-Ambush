import random
from .config import config
from .entity_map import entity_map

class Spawner:
    def __init__(self, game):
        self.game = game
        self.spawn_point = None
        self.timer = 0
        self.wave = 0
        self.spawn_point = (41, -48)
<<<<<<< HEAD
        self.max_waves = config['level_data']['level_0']['waves']
=======
        self.spawner_index = 0
        self.level_waves = config['level_data']['level_0']['waves']
        self.spawn_timer = self.level_waves[self.wave]['timer']
        self.enemy_count = 0
>>>>>>> dd66f4a1204550f902eef134d5e08600cb6aa5c0
        self.level_clear = False
        self.wave_clear = False

<<<<<<< HEAD
        self.wave_data = []
        self.difficulty_rank = 1
        self.spawner_index = 0
        self.enemy_index = 0
=======
        self.total_enemy_count = self.get_total_count()
>>>>>>> dd66f4a1204550f902eef134d5e08600cb6aa5c0

    def get_total_count(self):
        count = 0
        for spawner in self.level_waves[self.wave]['spawners']:
            count += spawner['count']
        return count

<<<<<<< HEAD
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

            '''self.timer += dt
=======
    def get_enemy_type(self):
        self.enemy_type = self.level_waves[self.wave]['spawners'][self.spawner_index]['enemy']
        enemy_count = self.level_waves[self.wave]['spawners'][self.spawner_index]['count']
        print(self.enemy_type, enemy_count)
        if self.spawner_index < (len(self.level_waves[self.wave]['spawners']) - 1):
            self.spawner_index += 1
        return enemy_count

    def update(self, dt):
        if self.game.world.loaded:
            self.timer += dt
>>>>>>> dd66f4a1204550f902eef134d5e08600cb6aa5c0

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
                    #print('new wave')