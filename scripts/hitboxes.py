import pygame, math, random

from .config import config
from .core_funcs import itr

class Hitbox:
    def __init__(self, game, hitbox_type, duration=-1, rect=None, tracked=None, owner=None, angle=None, offset=None):
        self.game = game
        if tracked:
            self.mode = 'tracked'
            self.tracked = tracked
            self.offset = offset
        if rect:
            self.mode = 'rotated_rect'
            self.rect = rect
        self.duration = duration
        self.hitbox_type = hitbox_type
        self.config = config['hitboxes'][hitbox_type]
        self.owner = owner
        self.angle = angle
        self.ignore = [owner]

    def update(self):
        if self.mode == 'tracked':
            tracked_mask, offset = self.tracked.create_mask()

            for entity in self.game.world.entities.entities:
                if (entity not in self.ignore) and (entity.type != 'item'):
                    entity_offset = entity.calculate_render_offset()
                    collision = tracked_mask.overlap(entity.mask, (int((entity.pos[0] - entity_offset[0]) - offset[0]), int((entity.pos[1] - entity_offset[1]) - offset[1])))
                    if collision:
                        entity.i_frames = 0.4
                        collision_point = [offset[0] + collision[0], offset[1] + collision[1]]
                        if self.angle:
                            self.game.world.vfx.spawn_vfx('slice', collision_point.copy(), random.random() * math.pi / 4 - math.pi / 8 + self.angle, 20 * random.random() + 60, 2, 1, 0.8)
                            entity.velocity[0] += math.cos(self.angle) * 300 * self.config['knockback']
                            entity.velocity[1] += math.sin(self.angle) * 300 * self.config['knockback']
                            killed = entity.damage(self.config['power'], self.angle)
                            #if killed:
                                #if self.owner.type == 'player':
                                    #self.owner.process_kill(entity)
                            for i in range(random.randint(10, 15)):
                                self.game.world.vfx.spawn_group('arrow_impact_sparks', collision_point.copy(), self.angle)
                        self.ignore.append(entity)
            return self.tracked.alive
        
        if self.mode == 'rotated_rect':
            tracked_mask = pygame.mask.from_surface(self.rect)

            for entity in self.game.world.entities.entities:
                if (entity not in self.ignore) and (entity.type != 'item'):
                    degrees = math.degrees(-self.angle)
                    offset = [int(entity.center[0] - self.owner.center[0]), int(entity.center[1] - self.owner.center[1])]
                    if degrees > 0 and degrees < 180:                                               # Q1 or Q2
                        offset[1] += self.rect.get_height()
                    if (degrees < 180 and degrees > 90) or (degrees > -180 and degrees < -90):      # Q3 or Q4
                        offset[0] += self.rect.get_width()
                    collision = tracked_mask.overlap(entity.mask, offset)
                    if collision:
                        # fix collision point and add more particles
                        collision_point = [offset[0] + collision[0], offset[1] + collision[1]]

            self.duration -= self.game.window.dt
            return self.duration > 0
                    
class Hitboxes:
    def __init__(self, game):
        self.game = game
        self.hitboxes = []

    def update(self):
        for i, hitbox in itr(self.hitboxes):
            alive = hitbox.update()
            if not alive:
                self.hitboxes.pop(i)

    def add_hitbox(self, *args, **kwargs):
        self.hitboxes.append(Hitbox(*args, **kwargs))
