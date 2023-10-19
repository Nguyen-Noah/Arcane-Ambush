import random
import math

from .config import config
from .core_funcs import itr

class Hitbox:
    def __init__(self, game, hitbox_type, duration=-1, rect=None, tracked=None, owner=None, angle=None):
        self.game = game
        if tracked:
            self.mode = 'tracked'
            self.tracked = tracked
        else:
            self.mode = 'rect'
            self.rect = rect
        self.duration = duration
        self.hitbox_type = hitbox_type
        self.config = config['hitboxes'][hitbox_type]
        self.owner = owner
        self.angle = angle
        self.ignore = [owner]

    def update(self, dt):
        if self.mode == 'tracked':
            tracked_mask, offset = self.tracked.create_mask()

            for entity in self.game.world.entities.entities:
                if (entity not in self.ignore) and (entity.type != 'item'):
                    entity_offset = entity.calculate_render_offset()
                    collision = tracked_mask.overlap(entity.mask, (int((entity.pos[0] - entity_offset[0]) - offset[0] - self.game.world.camera.true_pos[0]), int((entity.pos[1] - entity_offset[1]) - offset[1] - self.game.world.camera.true_pos[1])))
                    #collision_point = (entity.pos[0] - entity_offset[0] + collision[0], entity.pos[1] - entity_offset[1] + collision[1])
                    if collision:
                        collision_point = [offset[0] + collision[0], offset[1] + collision[1]]
                        if self.angle:
                            #self.game.window.add_freeze(0.2, 0.4)
                            self.game.world.vfx.spawn_vfx('slice', collision_point.copy(), random.random() * math.pi / 4 - math.pi / 8 + self.angle, 20 * random.random() + 60, 2, 1, 0.8)
                            entity.velocity[0] += math.cos(self.angle) * 300 * self.config['knockback']
                            entity.velocity[1] += math.sin(self.angle) * 300 * self.config['knockback']
                            killed = entity.damage(self.config['power'], self.angle)
                            #if killed:
                                #if self.owner.type == 'player':
                                    #self.owner.process_kill(entity)
                            for i in range(random.randint(10, 15)):
                                self.game.world.vfx.spawn_group('arrow_impact_sparks', collision_point.copy(), self.angle)
                            '''for i in range(random.randint(14, 20)):
                                random_angle = self.angle + (random.random() - 0.5) / 3.5
                                if random.randint(1, 4) == 1:
                                    random_angle = self.angle + (random.random() - 0.5) / 7 + math.pi

                                random_speed = random.randint(20, 200)
                                vel = [math.cos(random_angle) * random_speed, math.sin(random_angle) * random_speed]
                                self.game.world.vfx.spawn_vfx('spark', collision_point.copy(), vel, 1 + random.random() * 3, (15, 15, 8), drag=50)'''
                        self.ignore.append(entity)
            return self.tracked.alive

class Hitboxes:
    def __init__(self, game):
        self.game = game
        self.hitboxes = []

    def update(self):
        for i, hitbox in itr(self.hitboxes):
            alive = hitbox.update(self.game.window.dt)
            if not alive:
                self.hitboxes.pop(i)

    def add_hitbox(self, *args, **kwargs):
        self.hitboxes.append(Hitbox(*args, **kwargs))
