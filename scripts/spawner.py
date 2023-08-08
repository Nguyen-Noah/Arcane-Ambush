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
        self.spawner_index = 0
        self.level_waves = config['level_data']['level_0']['waves']
        self.spawn_timer = self.level_waves[self.wave]['timer']
        self.enemy_count = 0
        self.level_clear = False
        self.wave_clear = False

        self.total_enemy_count = self.get_total_count()

    def get_total_count(self):
        count = 0
        for spawner in self.level_waves[self.wave]['spawners']:
            count += spawner['count']
        return count

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

            if self.total_enemy_count == 0:
                self.wave_clear = True

            if not self.level_clear:
                if not self.wave_clear:
                    if not self.enemy_count:
                        self.enemy_count = self.get_enemy_type()

                    for i in range(self.enemy_count):
                        if self.timer >= self.spawn_timer and self.total_enemy_count > 0:
                            self.game.world.entities.entities.append(entity_map[self.enemy_type](self.game, (self.spawn_point[0] + random.randint(1, 8), self.spawn_point[1] + random.randint(1, 16)), (14, 14), self.enemy_type))
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