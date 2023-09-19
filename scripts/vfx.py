import math
import random

from .core_funcs import *

def rdm(scale, offset):
    return random.random() * scale + offset

def point_surf(point_list):
    x_positions = [v[0] for v in point_list]
    y_positions = [v[1] for v in point_list]
    min_x = min(x_positions)
    min_y = min(y_positions)
    size_x = max(x_positions) - min_x + 1
    size_y = max(y_positions) - min_y + 1
    new_surf = pygame.Surface((int(size_x), int(size_y)))
    new_surf.set_colorkey((0, 0, 0))
    new_points = [[v[0] - min_x, v[1] - min_y] for v in point_list]
    return new_surf, new_points, [min_x, min_y]

# glow renders are stored for post-processing rendering
GLOW_SURFS = []
GLOW_CACHE = {}

def glow(location, radius, angle, width=0, color=(20, 20, 20), padding=0, surf=None):
    global GLOW_SURFS

    # padding the surface is used as a math hack to prevent the need to use trig for rotated placement
    if not width:
        # check if cached
        glow_id = (int(radius), color)
        if glow_id in GLOW_CACHE:
            GLOW_SURFS.append([GLOW_CACHE[glow_id], (location[0] - radius, location[1] - radius)])
            return None

        render_surf = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(render_surf, color, (radius, radius), radius)
        if not surf:
            GLOW_SURFS.append([render_surf, (location[0] - radius, location[1] - radius)])
        else:
            surf.blit(render_surf, (location[0] - radius, location[1] - radius), special_flags=pygame.BLEND_RGBA_ADD)
        GLOW_CACHE[glow_id] = render_surf
    else:
        render_surf = pygame.Surface((radius * 2 + width + abs(padding * (width + 2 * radius)), radius * 2))
        offset_x = 0
        if padding < 0:
            offset_x = (width + 2 * radius) * abs(padding)
        pygame.draw.rect(render_surf, color, pygame.Rect(radius + offset_x, 0, width, radius * 2))
        pygame.draw.circle(render_surf, color, (radius + offset_x, radius), radius)
        pygame.draw.circle(render_surf, color, (radius + width + offset_x, radius), radius)

        # a hack to get around the pygame rotation bug resulting in a segfault with surfs that have dimensions of 0 if the angle isn't 90deg
        if render_surf.get_width() * render_surf.get_height() == 0:
            angle = 0

        if angle:
            render_surf.set_colorkey((0, 0, 0))
            rotated_surf = pygame.transform.rotate(render_surf, angle)
        else:
            rotated_surf = render_surf

        if not surf:
            GLOW_SURFS.append([rotated_surf, (location[0] - rotated_surf.get_width() // 2, location[1] - rotated_surf.get_height() // 2)])
        else:
            surf.blit(rotated_surf, (location[0] - rotated_surf.get_width() // 2, location[1] - rotated_surf.get_height() // 2), special_flags=pygame.BLEND_RGBA_ADD)

def draw_glows(surf):
    global GLOW_SURFS
    for glow in GLOW_SURFS:
        surf.blit(glow[0], glow[1], special_flags=pygame.BLEND_RGBA_ADD)
    GLOW_SURFS = []

class PlainLine:
    def __init__(self, pos1, pos2, decay_rate, width=1, color=(255, 255, 255, 255)):
        self.pos1 = pos1
        self.pos2 = pos2
        self.decay_rate = decay_rate
        self.color = color
        self.width = width

    def update(self, dt):
        dt *= 60
        self.color = (self.color[0], self.color[1], self.color[2], max(0, self.color[3] - self.decay_rate * dt))
        return bool(self.color[3])

    def render(self, surf, offset=(0, 0)):
        new_surf, new_points, base_offset = point_surf([[self.pos1[0] - offset[0], self.pos1[1] - offset[1]], [self.pos2[0] - offset[0], self.pos2[1] - offset[1]]])
        pygame.draw.line(new_surf, self.color, new_points[0], new_points[1], self.width)
        new_surf.set_alpha(self.color[3])
        surf.blit(new_surf, base_offset)

class CurvedSpark:
    def __init__(self, pos, angle, curve, speed, scale, decay_rate, fatness=1, color=(255, 255, 255), glow=True):
        self.pos = list(pos)
        self.angle = angle
        self.curve = curve
        self.scale = scale
        self.color = color
        self.speed = speed
        self.fatness = fatness
        self.decay_rate = decay_rate
        self.glow = glow

    def update(self, dt):
        dt *= 60
        self.pos[0] += math.cos(self.angle) * self.speed * dt
        self.pos[1] += math.sin(self.angle) * self.speed * dt
        self.angle += self.curve * self.speed * dt
        self.speed = max(0, self.speed - self.decay_rate * dt)

        return bool(self.speed)

    def render(self, surf, offset=(0, 0)):
        if self.speed:
            iterations = 10
            position = self.pos.copy()
            temp_angle = self.angle
            points = []
            for i in range(iterations // 2):
                temp_angle -= self.curve * self.speed * self.scale / iterations
                position[0] -= math.cos(temp_angle) * self.speed * self.scale / iterations
                position[1] -= math.sin(temp_angle) * self.speed * self.scale / iterations
            for i in range(iterations + 1):
                progress = i / iterations

                dif = ((0.5 - abs(0.5 - progress)) * 2) ** (1 / 2.5)
                points.append([position[0] + math.cos(temp_angle + math.pi / 2) * self.scale * dif * 0.05 * self.fatness * self.speed, position[1] + math.sin(temp_angle + math.pi / 2) * self.scale * dif * 0.05 * self.fatness * self.speed])
                points = [[position[0] + math.cos(temp_angle - math.pi / 2) * self.scale * dif * 0.05 * self.fatness * self.speed, position[1] + math.sin(temp_angle - math.pi / 2) * self.scale * dif * 0.05 * self.fatness * self.speed]] + points

                position[0] += math.cos(temp_angle) * self.speed * self.scale / iterations
                position[1] += math.sin(temp_angle) * self.speed * self.scale / iterations
                temp_angle += self.curve * self.speed * self.scale / iterations

            for p in points:
                p[0] -= offset[0]
                p[1] -= offset[1]

            new_surf, new_points, base_offset = point_surf(points)
            pygame.draw.polygon(new_surf, self.color, new_points)
            if len(self.color) == 4:
                new_surf.set_alpha(self.color[3])
            surf.blit(new_surf, base_offset)

            if self.glow:
                glow([position[0] - offset[0], position[1] - offset[1]], self.fatness + 2, -math.degrees(self.angle), width=self.scale * self.speed + 2, color=(8, 8, 8), padding=0)
                glow([position[0] - offset[0], position[1] - offset[1]], self.fatness + 4, -math.degrees(self.angle), width=self.scale * self.speed + 8, color=(6, 6, 6), padding=0)

class Arc:
    def __init__(self, pos, radius, spacing, start_angle, speed, curve_rate, scale, start=0, end=1, duration=30, color=(255, 255, 255), fade=0.3, arc_stretch=0, width_decay=50, motion=0, decay=['up', 60], angle_width=0.2):
        self.start_angle = start_angle
        self.speed = speed
        self.curve_rate = curve_rate
        self.scale = scale
        self.time = 0
        self.spacing = spacing
        self.radius = radius
        self.angle_width = angle_width
        self.width = 0.05
        self.end = end
        self.start = start
        self.duration = duration
        self.color = color
        self.fade = fade
        self.pos = list(pos)
        self.arc_stretch = arc_stretch
        self.width_decay = width_decay
        self.motion = motion
        self.decay = decay
        self.alive = True

    def get_angle_point(self, base_point, t, curve_rate):
        p = advance(base_point.copy(), self.start_angle + (0.5 - t) * math.pi * 4 * self.angle_width, self.radius)
        advance(p, self.start_angle, (0.5 ** 2 - abs(0.5 - t) ** 2) * self.radius * curve_rate)
        if self.arc_stretch != 0:
            advance(p, self.start_angle + math.pi / 2, (0.5 - t) * self.arc_stretch * self.scale)
        return p

    def calculate_points(self, start, end, curve_rate):
        base_point = advance([0, 0], self.start_angle, self.spacing)
        point_count = 20
        arc_points = [self.get_angle_point(base_point, start + (i / point_count) * (end - start), curve_rate) for i in range(point_count + 1)]
        arc_points = [[p[0] * self.scale, p[1] * self.scale] for p in arc_points]
        return arc_points

    def update(self, dt):
        self.time += self.speed * dt
        if self.decay[0] == 'up':
            #self.end -= self.end / 10 * dt * self.decay[1]
            self.start -= self.start / 20 * dt * self.decay[1]
        elif self.decay[0] == 'down':
            self.end += (1 - self.end) / 20 * dt * self.decay[1]
            #self.start += (1 - self.start) / 10 * dt * self.decay[1]
        self.width += (1 - self.width) / 4 * dt * self.width_decay
        self.spacing += self.motion * dt
        if self.time > self.duration:
            self.alive = False
            return False
        return True

    def create_mask(self):
        start = self.start
        end = self.end
        points = self.calculate_points(start, end, self.curve_rate + self.time / 12) + self.calculate_points(start, end, (self.curve_rate + self.time / 12) * self.width)[::-1]
        points = [[p[0] + self.pos[0], p[1] + self.pos[1]] for p in points]
        points_x = [p[0] for p in points]
        points_y = [p[1] for p in points]
        min_x = min(points_x)
        min_y = min(points_y)
        mask_surf = pygame.Surface((max(points_x) - min_x + 1, max(points_y) - min_y + 1))
        points = [[p[0] - min_x, p[1] - min_y] for p in points]
        pygame.draw.polygon(mask_surf, (255, 255, 255), points)
        mask_surf.set_colorkey((0, 0, 0))
        return pygame.mask.from_surface(mask_surf), (min_x, min_y)

    def render(self, surf, offset=(0, 0)):
        if self.time > 0:
            start = self.start
            end = self.end
            points = self.calculate_points(start, end, self.curve_rate + self.time / 12) + self.calculate_points(start, end, (self.curve_rate + self.time / 12) * self.width)[::-1]
            points = [[p[0] - offset[0] + self.pos[0], p[1] - offset[1] + self.pos[1]] for p in points]
            c = [int(self.color[i] - self.color[i] * self.fade * self.time / self.duration) for i in range(3)]
            pygame.draw.polygon(surf, c, points)

SPARK_CACHE = {}

class Spark:
    def __init__(self, pos, velocity, duration, glow_color, color=(255, 255, 255), drag=0, gravity=100):
        self.pos = list(pos)
        self.velocity = list(velocity)
        self.orig_duration = duration
        self.duration = duration
        self.glow_color = glow_color
        self.color = color
        self.drag = drag
        self.gravity = gravity

    def update(self, dt):
        self.duration -= dt
        self.pos[0] += self.velocity[0] * dt
        self.pos[1] += self.velocity[1] * dt
        self.velocity[0] = normalize(self.velocity[0], self.drag * dt)
        self.velocity[1] += self.gravity * dt
        if self.duration <= 0:
            return False
        return True

    def render(self, surf, offset=(0, 0)):
        radius = int(self.duration / self.orig_duration * 6) + 1
        center = (int(self.pos[0] - offset[0]), int(self.pos[1] - offset[1]))
        glow(center, radius, 0, color=self.glow_color)
        surf.set_at(center, self.color)

class Slice:
    def __init__(self, pos, angle, length, width, decay_rate, speed=0, glow=True):
        self.angle = angle
        self.length = length
        self.orig_length = length
        self.width = width
        self.decay_rate = decay_rate
        self.time_left = 1
        self.pos = list(pos)
        self.speed = speed
        self.glow = glow

    def update(self, dt):
        self.time_left -= self.decay_rate * dt
        self.length = self.time_left * self.length
        if self.time_left < 0:
            return False
        else:
            return True

    def render(self, surf, offset=(0, 0)):
        if self.length > 1.5:
            pos = [self.pos[0] - offset[0], self.pos[1] - offset[1]]
            advance(pos, self.angle, (self.orig_length - self.length) * self.speed)
            points = [
                advance(pos.copy(), self.angle, self.length),
                advance(pos.copy(), self.angle + math.pi / 2, self.width * (self.length / self.orig_length)),
                advance(pos.copy(), self.angle + math.pi, self.length),
                advance(pos.copy(), self.angle + math.pi * 3 / 2, self.width * (self.length / self.orig_length)),
            ]
            pygame.draw.polygon(surf, (255, 255, 255), points)

            if self.glow:
                glow(pos, self.width // 2 + 1, -math.degrees(self.angle), width=self.length * 2 + 2, color=(24, 24, 24), padding=0)
                glow(pos, self.width // 2 + 2, -math.degrees(self.angle), width=self.length * 2 + 30, color=(14, 14, 14), padding=0)
                glow(pos, 1, -math.degrees(self.angle), width=self.length * 2 + 800, color=(14, 14, 14), padding=0)

VFX_TYPES = {
    'curved_spark': CurvedSpark,
    'plain_line': PlainLine,
    'arc': Arc,
    'slice': Slice,
    'spark': Spark,
}

# random is scaling for 0-1 and offset
EFFECT_GROUPS = {
    'bow_sparks': {
        'base': [
            ['curved_spark', math.pi / 8, math.pi / 120, 3, 5, 0.4, 0.6],
            ['curved_spark', -math.pi / 8, -math.pi / 120, 3, 5, 0.4, 0.6],
            ['curved_spark', 0, 0, 3, 4, 0.2, 1],
        ],
        'random': [
            [[[0, 0], [0, 0]], [math.pi / 4, -math.pi / 8], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
            [[[0, 0], [0, 0]], [math.pi / 4, -math.pi / 8], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
            [[[0, 0], [0, 0]], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
        ],
    },
    'arrow_impact_sparks': {
        'base': [
            ['curved_spark', 0, 0, 2, 6, 0.1, 0.7],
        ],
        'random': [
            [[[0, 0], [0, 0]], [math.pi * 3 / 4, math.pi * 5 / 8], [0, 0], [2, 0], [1, 0], [0.3, 0], [0, 0]],
        ],
    },
    'dash_sparks': {
        'base': [
            ['curved_spark', 0, 0, 2, 2, 0.1, 0.7],
        ],
        'random': [
            [[[0, 0], [0, 0]], [math.pi / 10, -math.pi / 20], [0, 0], [2, 0], [1, 0], [0.3, 0], [0, 0]],
        ],
    }
}

class VFX:
    def __init__(self, game):
        self.game = game
        self.effects_front = []
        self.effects_back = []

    def output_stats(self):
        print('- vfx -')
        print('front:', len(self.effects_front))
        print('back:', len(self.effects_back))

    def update(self):
        for group in [self.effects_front, self.effects_back]:
            for i, effect in itr(group):
                alive = effect.update(self.game.window.dt)
                if not alive:
                    group.pop(i)

    def render_front(self, surf, offset=(0, 0)):
        for effect in self.effects_front:
            effect.render(surf, offset)

    def render_back(self, surf, offset=(0, 0)):
        for effect in self.effects_back:
            effect.render(surf, offset)

    def spawn_vfx(self, effect_type, *args, layer='front', **kwargs):
        if layer == 'front':
            self.effects_front.append(VFX_TYPES[effect_type](*args, **kwargs))
        if layer == 'back':
            self.effects_back.append(VFX_TYPES[effect_type](*args, **kwargs))

    def get_last(self, layer='front'):
        if layer == 'front':
            return self.effects_front[-1]
        if layer == 'back':
            return self.effects_back[-1]

    def spawn_group(self, group_type, position, rotation, layer='front', color=(255, 255, 255)):
        for i, particle in itr(EFFECT_GROUPS[group_type]['base']):
            effect_type = particle[0]
            particle = particle[1:]
            particle_data = [list(position)] + particle.copy()
            particle_data[1] += rotation
            random_data = EFFECT_GROUPS[group_type]['random'][i]
            particle_data[0][0] += rdm(*random_data[0][0])
            particle_data[0][1] += rdm(*random_data[0][1])
            for j in range(len(random_data) - 1):
                particle_data[j + 1] += rdm(*random_data[j + 1])
            if layer == 'front':
                self.effects_front.append(VFX_TYPES[effect_type](*particle_data, color))
            if layer == 'back':
                self.effects_back.append(VFX_TYPES[effect_type](*particle_data, color))
