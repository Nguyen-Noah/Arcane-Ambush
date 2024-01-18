import pygame, math, random
from .config import config
from .core_funcs import advance, itr, collision_list
from .vfx import glow
from .ease_functions import linear

class Projectile:
    def __init__(self, game, type, pos, rot, speed, duration, owner, ease, ease_speed):
        self.game = game
        self.owner = owner
        self.type = type
        self.pos = list(pos)
        self.rotation = rot
        self.speed = speed
        self.true_speed = speed
        self.img = self.game.assets.projectiles[self.type]
        self.config = config['projectiles'][self.type]
        self.duration = duration
        self.dist_moved = 0
        self.ease = ease
        self.ease_speed = ease_speed
        self.alive = True

        advance(self.pos, self.rotation, self.config['spawn_advance'])

    def move(self, dt):
        rect = pygame.Rect(self.pos[0], self.pos[1], self.img.get_width(), self.img.get_height())
        directions = {k: False for k in ['top', 'left', 'right', 'bottom']}  

        hit_list = collision_list(rect, self.game.world.collideables)
        cx = math.cos(self.rotation) * self.speed * dt
        self.pos[0] += cx
        if len(hit_list) > 0:
            if cx > 0:
                directions['right'] = True
            else:
                directions['left'] = True
                
        cy = math.sin(self.rotation) * self.speed * dt
        self.pos[1] += cy
        if len(hit_list) > 0:
            if cy > 0:
                directions['bottom'] = True
            else:
                directions['top'] = True
        
        return directions

    def update(self, dt):
        self.duration -= dt
        collisions = self.move(dt)

        if any(hit for hit in collisions.values()):
            self.alive = False

        for entity in self.game.world.entities.entities:
            if (entity != self.owner) and ((entity.type == 'player') or (entity.type != self.owner.type)) and (entity.type != 'item') and (entity.health > 0) and entity.targetable and (entity.i_frames == 0):
                if entity.rect.collidepoint(self.pos):
                    entity.i_frames = 0.4
                    if entity.category == 'player':
                        self.game.window.add_freeze(0.2, 0.2)
                        color = (100, 0, 0)
                    else:
                        color = (255, 255, 255)

                    self.game.world.vfx.spawn_vfx('slice', self.pos.copy(), random.random() * math.pi / 4 - math.pi / 8 + self.rotation, 20 * random.random() + 50, 2, 3, 0.4, color=color)

                    entity.velocity[0] += math.cos(self.rotation) * 100 * dt * self.config['knockback']
                    entity.velocity[1] += math.sin(self.rotation) * 100 * dt * self.config['knockback']

                    killed = entity.damage(self.config['power'])
                    if killed:
                        if self.owner.type == 'player':
                            self.owner.process_kill(entity)

                    for i in range(random.randint(10, 20)):
                        self.game.world.vfx.spawn_group('arrow_impact_sparks', self.pos.copy(), self.rotation, color=color)
                    for i in range(random.randint(8, 16)):
                        random_angle = self.rotation + (random.random() - 0.5) / 3.5
                        if random.randint(1, 4) == 1:
                            random_angle = self.rotation + (random.random() - 0.5) / 7 + math.pi

                        random_speed = random.randint(20, 200)
                        vel = [math.cos(random_angle) * random_speed, math.sin(random_angle) * random_speed]
                        self.game.world.vfx.spawn_vfx('spark', self.pos.copy(), vel, 1 + random.random(),  drag=50, color=color)
                    self.alive = False

        if self.duration <= 0:
            self.alive = False

        return self.alive

    def render(self, surf, offset=(0, 0)):
        render_pos = [self.pos[0] - offset[0], self.pos[1] - offset[1]]
        if self.config['shape']:
            if self.config['shape'][0] == 'line':
                pygame.draw.line(surf, self.config['shape'][1], render_pos, advance(render_pos.copy(), self.rotation, self.config['shape'][2]), self.config['shape'][3])
                glow(render_pos, 2, -math.degrees(self.rotation), width=self.config['shape'][2] + 4, color=(50, 50, 50), padding=-0.6)
                glow(render_pos, 4, -math.degrees(self.rotation), width=self.config['shape'][2] + 8, color=(8, 8, 8), padding=-0.6)
        else:
            img = self.game.assets.projectiles[self.type]
            render_pos[0] -= img.get_width()
            render_pos[1] -= img.get_height()
            surf.blit(img, render_pos)

class ProjectileManager:
    def __init__(self, game):
        self.game = game
        self.projectiles = []

    def spawn_projectile(self, type, pos, rot, speed, duration, owner, ease=linear, ease_speed=100):
        if not self.game.world.builder_mode:
            self.projectiles.append(Projectile(self.game, type, pos, rot, speed, duration, owner, ease, ease_speed))

    def get_last(self):
        return self.projectiles[-1]

    def update(self, dt):
        for i, projectile in itr(self.projectiles):
            alive = projectile.update(dt)
            if not alive:
                self.projectiles.pop(i)

    def render(self, surf, offset=(0, 0)):
        for projectile in self.projectiles:
            projectile.render(surf, offset)